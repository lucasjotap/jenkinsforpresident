pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/lucasjotap/jenkinsforpresident.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    dockerImage = docker.build("your-org/your-app:${env.BUILD_NUMBER}")
                }
            }
        }
        stage('Test') {
            steps {
                sh 'docker run --rm your-org/your-app:${env.BUILD_NUMBER} ./run-tests.sh'
            }
        }
        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        dockerImage.push()
                    }
                }
            }
        }
    }
}
