pipeline {
  agent any
  environment {
    BUILD_TS = ""
  }
  stages {
    stage('prepare') {
      steps {
        script {
          def checkPy = sh(script: "command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1 || echo MISSING", returnStdout: true).trim()
          if (checkPy == 'MISSING') {
            error('Python (python3 or python) not found on agent')
          }
          env.BUILD_TS = sh(script: "date +%Y%m%d%H%M%S", returnStdout: true).trim()
          sh 'mkdir -p /tmp/yatritransit-builds'
        }
      }
    }
    stage('test') {
      steps {
        sh 'python -m unittest discover -v || python3 -m unittest discover -v || { echo "unit tests failed"; exit 1; }'
        sh 'echo "test-run: $(date)" > test-log.txt'
        sh 'cp test-log.txt /tmp/yatritransit-builds/test-log-${BUILD_ID}-${BUILD_TS}.txt'
      }
    }
    stage('analyse-routes') {
      steps {
        sh 'python analyse_routes.py > route-report.txt || python3 analyse_routes.py > route-report.txt || true'
        sh 'cp route-report.txt /tmp/yatritransit-builds/route-report-${BUILD_ID}-${BUILD_TS}.txt'
      }
    }
    stage('archive') {
      steps {
        sh 'cp -r /tmp/yatritransit-builds ${WORKSPACE}/yatritransit-artifacts-${BUILD_TS}'
        archiveArtifacts artifacts: "yatritransit-artifacts-${BUILD_TS}/**", fingerprint: true
      }
    }
  }
  post {
    always {
      sh 'echo build finished at $(date) > /tmp/yatritransit-builds/build-summary-${BUILD_ID}-${BUILD_TS}.txt'
    }
  }
}
