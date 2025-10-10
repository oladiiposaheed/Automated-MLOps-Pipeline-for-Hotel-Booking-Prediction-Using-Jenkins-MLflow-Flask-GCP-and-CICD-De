
pipeline{
    agent any

    stages{
        stage('Cloning Github Repository to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github Repository to Jenkins....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/oladiiposaheed/Automated-MLOps-Pipeline-for-Hotel-Booking-Prediction-Using-Jenkins-MLflow-Flask-GCP-and-CICD-De.git']])
                }
            }
        }
    }
}