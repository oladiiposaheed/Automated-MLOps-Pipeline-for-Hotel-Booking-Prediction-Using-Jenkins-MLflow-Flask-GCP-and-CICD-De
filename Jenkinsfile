pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'prime-formula-xxxxxx-u9'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        retry(2)
    }

    stages{
        stage('Cloning Github Repository to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github Repository to Jenkins....'
                    retry(3) {
                        checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/oladiiposaheed/Automated-MLOps-Pipeline-for-Hotel-Booking-Prediction-Using-Jenkins-MLflow-Flask-GCP-and-CICD-De.git']])
                    }
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

        stage('Building and Pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId: 'gcp_key', variable:'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing Docker Image to GCR.......'
                        retry(3) {
                            sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet
                           
                            # Remove existing image quietly
                            docker rmi gcr.io/${GCP_PROJECT}/mlop-project-1:latest 2>/dev/null || true

                            # Build with cache and no network timeouts
                            docker build --network=host -t gcr.io/${GCP_PROJECT}/mlop-project-1:latest .

                            # Push with retry logic
                            docker push gcr.io/${GCP_PROJECT}/mlop-project-1:latest
                            '''
                        }
                    }
                }
            }
        }

        stage('Deploy Docker Image from GCR to Google Cloud Run'){
            steps{
                withCredentials([file(credentialsId: 'gcp_key', variable:'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploy Docker Image from GCR to Google Cloud Run.......'
                        retry(3) {
                            sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            
                            # Deploy with increased timeout and better error handling
                            gcloud run deploy mlop-project-1 \
                                --image=gcr.io/${GCP_PROJECT}/mlop-project-1:latest \
                                --platform=managed \
                                --region=us-central1 \
                                --allow-unauthenticated \
                                --timeout=600s \
                                --cpu=2 \
                                --memory=2Gi \
                                --max-instances=1
                            '''
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
        failure {
            echo 'Pipeline failed! Check network connectivity and Docker daemon.'
            sh 'docker system prune -f || true'
        }
        success {
            echo 'Pipeline completed successfully!'
            script {
                def url = sh(script: 'gcloud run services describe mlop-project-1 --region=us-central1 --format="value(status.url)"', returnStdout: true).trim()
                echo "Application deployed successfully: ${url}"
            }
        }
    }
}