
pipeline {
    agent any
    // Create venv in a Jenkins
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'prime-formula-472213-u9'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
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
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

     stage('Building and Pushing Docker Image to GCR'){
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and Pushing Docker Image to GCR...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}
                        
                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/mlop-project:latest .

                        docker push gcr.io/${GCP_PROJECT}/mlop-project:latest 

                        '''
                    }
                }
            }
        }
    }
}

