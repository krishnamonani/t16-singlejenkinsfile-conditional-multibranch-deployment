pipeline {
    agent none

    environment {
        GITHUB_CREDENTIALS = credentials('github-pat')
        REPO_URL = 'https://github.com/krishnamonani/t15-app.git'
    }

    stages {
        stage('Checkout code') {
            agent { label getAgent() }
            steps {
                echo "Checking out code from branch: ${env.BRANCH_NAME}"
                git url: "${REPO_URL}", branch: "${env.BRANCH_NAME}", credentialsId: 'github-pat'
                echo 'Code Checkout completed.'
            }
        }

        stage('Stop previous build') {
            when { anyOf { branch 'stage'; branch 'main' } }
            agent { label getAgent() }
            steps {
                echo "Stopping previous build on: ${env.BRANCH_NAME}"
                sh 'docker compose down || true'
            }
        }

        stage('Build and Deploy') {
            agent { label getAgent() }
            steps {
                script {
                    if (env.BRANCH_NAME == 'dev') {
                        echo 'Running unit tests inside docker'
                        sh 'docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from app || exit 1'
                    } else {
                        echo "Building and starting containers for ${env.BRANCH_NAME}"
                        sh 'docker compose build --no-cache || true'
                        sh 'docker compose up -d'
                    }
                }
            }
        }

        stage('Post-Deploy Checks') {
            when { anyOf { branch 'stage'; branch 'main' } }
            agent { label getAgent() }
            steps {
                echo "Running smoke test for ${env.BRANCH_NAME}..."
                sh 'curl -f http://localhost:5000 || exit 1'
                echo 'Smoke tests passed.'
            }
        }

        stage('Cleanup Docker') {
            agent { label getAgent() }
            steps {
                echo "Cleaning up unused Docker resources for ${env.BRANCH_NAME}..."
                sh 'docker system prune -af || true'
            }
        }
    }
}

def getAgent() {
    if (env.BRANCH_NAME == 'dev') {
        return 'sample-agent'
    } else if (env.BRANCH_NAME == 'stage') {
        return 'stage-agent'
    } else if (env.BRANCH_NAME == 'main') {
        return 'prod-agent'
    } else {
        return 'default-agent'
    }
}
