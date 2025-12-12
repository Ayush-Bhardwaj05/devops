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
          sh """
          cd "${env.WORKSPACE}"
          if [ -d "devops/tests" ]; then
            TEST_DIR="devops/tests"
          elif [ -d "tests" ]; then
            TEST_DIR="tests"
          else
            echo "ERROR: no tests directory found" >&2
            exit 1
          fi
          python -m unittest discover -v -s "\$TEST_DIR" -p "test_*.py" > unittest_output.txt 2>&1 || true
          if grep -q "Ran 0 tests" unittest_output.txt; then
            cat unittest_output.txt
            echo "ERROR: No unit tests found (Ran 0 tests)" >&2
            exit 1
          fi
          cat unittest_output.txt
          echo "test-run: $(date)" > test-log.txt
          cp test-log.txt /tmp/yatritransit-builds/test-log-${env.BUILD_ID}-${env.BUILD_TS}.txt
          cp test-log.txt ${env.WORKSPACE}/test-log-${env.BUILD_ID}-${env.BUILD_TS}.txt
          """
        }
      }
    }

    stage('analyse-routes') {
      steps {
        script {
          if (env.USE_DOCKER) {
            sh "docker run --rm -v ${env.WORKSPACE}:/ws -w /ws python:3.11 sh -c 'python analyse_routes.py > route-report.txt || true; cp route-report.txt /ws/route-report-${env.BUILD_ID}-${env.BUILD_TS}.txt'"
          } else {
            sh """
            cd "${env.WORKSPACE}"
            python analyse_routes.py > route-report.txt || true
            cp route-report.txt /tmp/yatritransit-builds/route-report-${env.BUILD_ID}-${env.BUILD_TS}.txt
            cp route-report.txt ${env.WORKSPACE}/route-report-${env.BUILD_ID}-${env.BUILD_TS}.txt
            """
          }
        }
      }
    }

    stage('archive') {
      steps {
        script {
          sh "mkdir -p ${env.WORKSPACE}/yatritransit-artifacts-${env.BUILD_TS}"
          sh "cp ${env.WORKSPACE}/test-log-${env.BUILD_ID}-${env.BUILD_TS}.txt ${env.WORKSPACE}/yatritransit-artifacts-${env.BUILD_TS}/ || true"
          sh "cp ${env.WORKSPACE}/route-report-${env.BUILD_ID}-${env.BUILD_TS}.txt ${env.WORKSPACE}/yatritransit-artifacts-${env.BUILD_TS}/ || true"
          sh "echo build finished at ${env.BUILD_TS} > ${env.WORKSPACE}/yatritransit-artifacts-${env.BUILD_TS}/build-summary-${env.BUILD_ID}-${env.BUILD_TS}.txt"
          archiveArtifacts artifacts: "yatritransit-artifacts-${env.BUILD_TS}/**", fingerprint: true
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
