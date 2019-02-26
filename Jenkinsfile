pipeline {
    agent { 
        label 'node_agent' 
    }
    stages {
        stage('presettings') {
          steps {
            sh 'python3 --version'
          }
        }

        stage('build') {
          steps {
            cd ./src/docker
            sh 'docker-compose up -d'
            cd -
          }
        }

        stage('clean up') {
          steps {
            cd ./src/docker
            docker-compose stop
            cd -
          }
        }
    }
}
