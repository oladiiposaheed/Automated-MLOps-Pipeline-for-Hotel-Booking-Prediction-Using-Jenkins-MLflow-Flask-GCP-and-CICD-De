
pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'

    stages{
        stage('Cloning Github Repository to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github Repository to Jenkins....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/oladiiposaheed/Automated-MLOps-Pipeline-for-Hotel-Booking-Prediction-Using-Jenkins-MLflow-Flask-GCP-and-CICD-De.git']])
                }
            }
        }

        stage('Setting up our Virtual Environment and Installing Dependencies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing Dependencies....'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install -e .
                    '''
                }
            }
        }
    }
}