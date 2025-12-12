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
          env.BUILD_TS = sh(script: "date +%Y%m%d%H%M%S", returnStdout: true).trim()
        }
      }
    }
    stage('test') {
      steps {
        script {
          if (env.USE_DOCKER) {
            sh "docker run --rm -v ${WORKSPACE}:/ws -w /ws python:3.11 sh -c \"pip install pytest >/dev/null 2>&1 || true; python -m unittest discover -v\""
            sh "docker run --rm -v ${WORKSPACE}:/ws -w /ws python:3.11 sh -c \"echo test-run: \\$(date) > test-log.txt; cp test-log.txt /ws/test-log-${BUILD_ID}-${BUILD_TS}.txt\""
          } else {
            sh "python -m unittest discover -v"
            sh "echo test-run: \\$(date) > test-log.txt"
            sh "cp test-log.txt ${WORKSPACE}/test-log-${BUILD_ID}-${BUILD_TS}.txt"
          }
        }
      }
    }
    stage('analyse-routes') {
      steps {
        script {
          if (env.USE_DOCKER) {
            sh "docker run --rm -v ${WORKSPACE}:/ws -w /ws python:3.11 sh -c \"python analyse_routes.py > route-report.txt || true; cp route-report.txt /ws/route-report-${BUILD_ID}-${BUILD_TS}.txt\""
          } else {
            sh "python analyse_routes.py > route-report.txt || true"
            sh "cp route-report.txt ${WORKSPACE}/route-report-${BUILD_ID}-${BUILD_TS}.txt"
          }
        }
      }
    }
    stage('archive') {
      steps {
        sh "mkdir -p ${WORKSPACE}/yatritransit-artifacts-${BUILD_TS}"
        sh "cp ${WORKSPACE}/test-log-${BUILD_ID}-${BUILD_TS}.txt ${WORKSPACE}/yatritransit-artifacts-${BUILD_TS}/ || true"
        sh "cp ${WORKSPACE}/route-report-${BUILD_ID}-${BUILD_TS}.txt ${WORKSPACE}/yatritransit-artifacts-${BUILD_TS}/ || true"
        sh "echo build finished at \\$(date) > ${WORKSPACE}/yatritransit-artifacts-${BUILD_TS}/build-summary-${BUILD_ID}-${BUILD_TS}.txt"
        archiveArtifacts artifacts: "yatritransit-artifacts-${BUILD_TS}/**", fingerprint: true
      }
    }
  }
  post {
    failure {
      echo "Build failed. Check console output."
    }
  }
}
