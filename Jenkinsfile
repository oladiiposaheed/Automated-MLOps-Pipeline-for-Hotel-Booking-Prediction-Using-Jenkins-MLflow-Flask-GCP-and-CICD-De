// Clone code from github to jenkins
pipeline {
    agent any 

    stages {
        stage('Clone Github repo to Jenkins') {
            steps {
                echo 'Clone Github repo to Jenkins...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/oladiiposaheed/Automated-MLOps-Pipeline-for-Hotel-Booking-Prediction-Using-Jenkins-MLflow-Flask-GCP-and-CICD-De.git']])
            }
        }
    }
}