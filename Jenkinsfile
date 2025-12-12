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
            sh "docker run --rm -v ${env.WORKSPACE}:/ws -w /ws python:3.11 sh -c 'pip install pytest >/dev/null 2>&1 || true; python -m unittest discover -v'"
            sh "docker run --rm -v ${env.WORKSPACE}:/ws -w /ws python:3.11 sh -c 'echo test-run: ${env.BUILD_TS} > test-log.txt; cp test-log.txt /ws/test-log-${env.BUILD_ID}-${env.BUILD_TS}.txt'"
          } else {
            sh "python -m unittest discover -v"
            sh "echo test-run: ${env.BUILD_TS} > test-log.txt"
            sh "cp test-log.txt ${env.WORKSPACE}/test-log-${env.BUILD_ID}-${env.BUILD_TS}.txt"
          }
        }
      }
    }
    stage('analyse-routes') {
      steps {
        script {
          if (env.USE_DOCKER) {
            sh "docker run --rm -v ${env.WORKSPACE}:/ws -w /ws python:3.11 sh -c 'python analyse_routes.py > route-report.txt || true; cp route-report.txt /ws/route-report-${env.BUILD_ID}-${env.BUILD_TS}.txt'"
          } else {
            sh "python analyse_routes.py > route-report.txt || true"
            sh "cp route-report.txt ${env.WORKSPACE}/route-report-${env.BUILD_ID}-${env.BUILD_TS}.txt"
          }
        }
      }
    }
    stage('archive') {
      steps {
        sh "mkdir -p ${env.WORKSPACE}/yatritransit-artifacts-${env.BUILD_TS}"
        sh "cp ${env.WORKSPACE}/test-log-${env.BUILD_ID}-${env.BUILD_TS}.txt ${env.WORKSPACE}/yatritransit-artifacts-${env.BUILD_TS}/ || true"
        sh "cp ${env.WORKSPACE}/route-report-${env.BUILD_ID}-${env.BUILD_TS}.txt ${env.WORKSPACE}/yatritransit-artifacts-${env.BUILD_TS}/ || true"
        sh "echo build finished at ${env.BUILD_TS} > ${env.WORKSPACE}/yatritransit-artifacts-${env.BUILD_TS}/build-summary-${env.BUILD_ID}-${env.BUILD_TS}.txt"
        archiveArtifacts artifacts: "yatritransit-artifacts-${env.BUILD_TS}/**", fingerprint: true
      }
    }
  }
  post {
    failure {
      echo "Build failed. Check console output."
    }
  }
}
