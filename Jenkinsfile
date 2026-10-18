pipeline {
    agent any

    environment {
        IMAGE_NAME = "ravindudilhan/stock-portfolio-tracker"
        GITOPS_REPO = "https://github.com/WGRavinduDilhan/stock-portfolio-tracker-gitops.git"
        GITOPS_DIR = "gitops"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python Tests') {
            steps {
                sh '''
                    set -e
                    docker info >/dev/null
                    docker run --rm \
                        -v "$WORKSPACE:/workspace" \
                        -w /workspace \
                        python:3.11-slim \
                        sh -c 'python -m pip install --upgrade pip && pip install -r requirements.txt && pytest -v'
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    env.IMAGE_TAG = "${env.BUILD_NUMBER}"
                    sh '''
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Docker Login & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${IMAGE_NAME}:latest
                        docker logout
                    '''
                }
            }
        }

        stage('Update GitOps') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-token',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    sh '''
                        rm -rf ${GITOPS_DIR}
                        git clone https://${GIT_USER}:${GIT_TOKEN}@github.com/WGRavinduDilhan/stock-portfolio-tracker-gitops.git ${GITOPS_DIR}

                        sed -i "s#image: .*#image: ${IMAGE_NAME}:${IMAGE_TAG}#" ${GITOPS_DIR}/base/deployment.yaml

                        cd ${GITOPS_DIR}
                        git config user.name "Jenkins CI"
                        git config user.email "jenkins@localhost"
                        git add base/deployment.yaml

                        if git diff --cached --quiet; then
                            echo "No GitOps change required."
                        else
                            git commit -m "Deploy stock-portfolio-tracker ${IMAGE_TAG}"
                            git push origin main
                        fi
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "CI/CD pipeline completed successfully."
            echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo "Pipeline failed. Deployment was not updated."
        }
    }
}