pipeline {
    agent { 
      docker { 
        image 'python:3.6.2' 
      } 
    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}
