pipeline {
  agent any
  environment {
    BUILD_TS = ""
  }
  stages {
    stage('prepare') {
      steps {
        script {
          def pyCheck = sh(script: "command -v python || command -v python3 || echo NONE", returnStdout: true).trim()
          if (pyCheck == 'NONE') {
            def dockerCheck = sh(script: "command -v docker || echo NONE", returnStdout: true).trim()
            if (dockerCheck == 'NONE') {
              error('Neither python nor docker CLI found on agent')
            }
            env.USE_DOCKER = "true"
          } else {
            env.USE_DOCKER = ""
          }
          env.BUILD_TS = new Date().format('yyyyMMddHHmmss')
          sh "mkdir -p /tmp/yatritransit-builds || true"
          echo "DEBUG: BUILD_TS=${env.BUILD_TS}, BUILD_ID=${env.BUILD_ID}, USE_DOCKER=${env.USE_DOCKER}"
        }
      }
    }

    stage('test') {
      steps {
        script {
          def ws = env.WORKSPACE
          def bid = env.BUILD_ID
          def bts = env.BUILD_TS
          def script =
            '''cd "''' + ws + '''"
if [ -d "devops/tests" ]; then
  TEST_DIR="devops/tests"
elif [ -d "tests" ]; then
  TEST_DIR="tests"
else
  echo "ERROR: no tests directory found" >&2
  exit 1
fi
python -m unittest discover -v -s "$TEST_DIR" -p "test_*.py" > unittest_output.txt 2>&1 || true
if grep -q "Ran 0 tests" unittest_output.txt; then
  cat unittest_output.txt
  echo "ERROR: No unit tests found (Ran 0 tests)" >&2
  exit 1
fi
cat unittest_output.txt
echo "test-run: $(date)" > test-log.txt
cp test-log.txt /tmp/yatritransit-builds/test-log-''' + bid + '-' + bts + '''.txt
cp test-log.txt "''' + ws + '''/test-log-''' + bid + '-' + bts + '''.txt"
'''
          sh script
        }
      }
    }

    stage('analyse-routes') {
      steps {
        script {
          def ws = env.WORKSPACE
          def bid = env.BUILD_ID
          def bts = env.BUILD_TS
          if (env.USE_DOCKER) {
            sh "docker run --rm -v ${ws}:/ws -w /ws python:3.11 sh -c 'python analyse_routes.py > route-report.txt || true; cp route-report.txt /ws/route-report-${bid}-${bts}.txt'"
          } else {
            def script =
              '''cd "''' + ws + '''"
python analyse_routes.py > route-report.txt || true
cp route-report.txt /tmp/yatritransit-builds/route-report-''' + bid + '-' + bts + '''.txt
cp route-report.txt "''' + ws + '''/route-report-''' + bid + '-' + bts + '''.txt"
'''
            sh script
          }
        }
      }
    }

    stage('archive') {
      steps {
        script {
          def ws = env.WORKSPACE
          def bts = env.BUILD_TS
          sh "mkdir -p '${ws}/yatritransit-artifacts-${bts}'"
          sh "cp '${ws}/test-log-${env.BUILD_ID}-${bts}.txt' '${ws}/yatritransit-artifacts-${bts}/' || true"
          sh "cp '${ws}/route-report-${env.BUILD_ID}-${bts}.txt' '${ws}/yatritransit-artifacts-${bts}/' || true"
          sh "echo build finished at ${bts} > '${ws}/yatritransit-artifacts-${bts}/build-summary-${env.BUILD_ID}-${bts}.txt'"
          archiveArtifacts artifacts: "yatritransit-artifacts-${bts}/**", fingerprint: true
        }
      }
    }
  }

  post {
    always {
      echo "POST DEBUG: BUILD_TS=${env.BUILD_TS}, BUILD_ID=${env.BUILD_ID}"
    }
    failure {
      echo "Build failed. Check console output."
    }
  }
}
