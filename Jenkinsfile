pipeline {
  agent {
    docker {
      image 'python:3.11'
    }
  }
  environment {
    BUILD_TS = ""
  }
  stages {
    stage('prepare') {
      steps {
        script {
          env.BUILD_TS = sh(script: "date +%Y%m%d%H%M%S", returnStdout: true).trim()
          sh 'mkdir -p /tmp/yatritransit-builds'
        }
      }
    }
    stage('test') {
      steps {
        sh 'pip install pytest'
        sh 'python -m unittest discover -v'
        sh 'echo "test-run: $(date)" > test-log.txt'
        sh 'cp test-log.txt /tmp/yatritransit-builds/test-log-${BUILD_ID}-${BUILD_TS}.txt'
      }
    }
    stage('analyse-routes') {
      steps {
        sh 'python analyse_routes.py > route-report.txt'
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
