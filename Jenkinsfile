// Clone code from github to jenkins
pipeline {
    agent any
    // Create venv in a Jenkins
    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Clone Github repo to Jenkins') {
            steps{
                script {
                    echo 'Clone Github repo to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/oladiiposaheed/Automated-MLOps-Pipeline-for-Hotel-Booking-Prediction-Using-Jenkins-MLflow-Flask-GCP-and-CICD-De.git']])
                }
            }
        }
        // Stage for creating venv in a Jenkins
        stage('Setting up our Virtual Environment and Installing Dependencies') {
            steps {
                script {
                    echo 'Setting up our Virtual Environment and Installing Dependencies...'
                    sh '''
                    python -m venv ${VENV_DIR}
                    // Activate the environment
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}