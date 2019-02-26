pipeline {
    stages {
        stage('presettings') {
          steps {
            sh 'python3 --version'
          }
        }

        stage('build') {
          steps {
            dir ('./src/docker') {
              sh 'docker-compose up -d'
            }
          }
        }

        stage('clean up') {
          steps {
            dir ('./src/docker') {
              sh 'docker-compose stop'
            }
          }
        }
    }
}
