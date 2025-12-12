pipeline {
  agent any
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
          sh "mkdir -p ${env.WORKSPACE} || true"
          sh "date +%Y%m%d%H%M%S > ${env.WORKSPACE}/build_ts.txt"
          def bts = sh(script: "cat ${env.WORKSPACE}/build_ts.txt", returnStdout: true).trim()
          echo "DEBUG: bts=${bts}, BUILD_ID=${env.BUILD_ID}, USE_DOCKER=${env.USE_DOCKER}"
          sh "mkdir -p /tmp/yatritransit-builds || true"
        }
      }
    }

    stage('test') {
      steps {
        script {
          def ws = env.WORKSPACE
          def script =
            'cd "' + ws + '"\n' +
            'bts=$(cat "' + ws + '/build_ts.txt" 2>/dev/null || date +%Y%m%d%H%M%S)\n' +
            'if [ -d "devops/tests" ]; then\n  TEST_DIR="devops/tests"\n' +
            'elif [ -d "tests" ]; then\n  TEST_DIR="tests"\n' +
            'else\n  echo "ERROR: no tests directory found" >&2\n  exit 1\nfi\n' +
            'python -m unittest discover -v -s "$TEST_DIR" -p "test_*.py" > unittest_output.txt 2>&1 || true\n' +
            'if grep -q "Ran 0 tests" unittest_output.txt; then\n  cat unittest_output.txt\n  echo "ERROR: No unit tests found (Ran 0 tests)" >&2\n  exit 1\nfi\n' +
            'cat unittest_output.txt\n' +
            'echo "test-run: $(date)" > test-log.txt\n' +
            'cp test-log.txt /tmp/yatritransit-builds/test-log-${BUILD_ID}-$bts.txt\n' +
            'cp test-log.txt "' + ws + '/test-log-${BUILD_ID}-$bts.txt"\n'
          sh script
        }
      }
    }

    stage('analyse-routes') {
      steps {
        script {
          def ws = env.WORKSPACE
          if (env.USE_DOCKER) {
            sh "docker run --rm -v ${ws}:/ws -w /ws python:3.11 sh -c 'bts=\\$(cat /ws/build_ts.txt 2>/dev/null || date +%Y%m%d%H%M%S); python analyse_routes.py > route-report.txt || true; cp route-report.txt /ws/route-report-${BUILD_ID}-\\$bts.txt'"
          } else {
            def s =
              'cd "' + ws + '"\n' +
              'bts=$(cat "' + ws + '/build_ts.txt" 2>/dev/null || date +%Y%m%d%H%M%S)\n' +
              'python analyse_routes.py > route-report.txt || true\n' +
              'cp route-report.txt /tmp/yatritransit-builds/route-report-${BUILD_ID}-$bts.txt\n' +
              'cp route-report.txt "' + ws + '/route-report-${BUILD_ID}-$bts.txt"\n'
            sh s
          }
        }
      }
    }

    stage('archive') {
      steps {
        script {
          def ws = env.WORKSPACE
          sh 'bts=$(cat "' + ws + '/build_ts.txt" 2>/dev/null || date +%Y%m%d%H%M%S) && mkdir -p "' + ws + '/yatritransit-artifacts-$bts"'
          sh 'bts=$(cat "' + ws + '/build_ts.txt" 2>/dev/null || date +%Y%m%d%H%M%S) && cp "' + ws + '/test-log-${BUILD_ID}-$bts.txt" "' + ws + '/yatritransit-artifacts-$bts/" || true'
          sh 'bts=$(cat "' + ws + '/build_ts.txt" 2>/dev/null || date +%Y%m%d%H%M%S) && cp "' + ws + '/route-report-${BUILD_ID}-$bts.txt" "' + ws + '/yatritransit-artifacts-$bts/" || true'
          sh 'bts=$(cat "' + ws + '/build_ts.txt" 2>/dev/null || date +%Y%m%d%H%M%S) && echo build finished at $bts > "' + ws + '/yatritransit-artifacts-$bts/build-summary-${BUILD_ID}-$bts.txt"'
          sh 'bts=$(cat "' + ws + '/build_ts.txt" 2>/dev/null || date +%Y%m%d%H%M%S) && ls -la "' + ws + '/yatritransit-artifacts-$bts" || true'
          sh 'bts=$(cat "' + ws + '/build_ts.txt" 2>/dev/null || date +%Y%m%d%H%M%S) && echo "Archiving artifacts for build ${BUILD_ID} with ts=$bts"'
          archiveArtifacts artifacts: "${ws}/yatritransit-artifacts-*/**", fingerprint: true
        }
      }
    }
  }

  post {
    always {
      script {
        def ws = env.WORKSPACE
        def bts = sh(script: "cat ${ws}/build_ts.txt 2>/dev/null || echo none", returnStdout: true).trim()
        echo "POST DEBUG: build_ts_file=${ws}/build_ts.txt, bts=${bts}, BUILD_ID=${env.BUILD_ID}"
      }
    }
  }
}
