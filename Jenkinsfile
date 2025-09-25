pipeline {
    agent none   // we will assign agents per stage

    environment {
        GITHUB_CREDENTIALS = credentials('github-pat')
        REPO_URL           = 'https://github.com/krishnamonani/t15-app.git'
    }

    stages {
        // ---------------- DEV ----------------
        stage('Checkout Code (Dev)') {
            when { branch 'dev' }
            agent { label 'sample-agent' }
            steps {
                echo 'Checking out code for DEV...'
                git url: "${REPO_URL}", branch: 'dev', credentialsId: 'github-pat'
                echo 'Code checkout completed.'
            }
        }

        stage('Run Unit Test (Dev)') {
            when { branch 'dev' }
            agent { label 'sample-agent' }
            steps {
                echo 'Running unit tests inside a Docker container...'
                sh 'docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from app'
                echo 'Unit tests completed.'
            }
            post {
                always {
                    sh 'docker system prune -af || true'
                    echo 'Cleaned up Docker resources.'
                }
            }
        }

        // ---------------- STAGE ----------------
        stage('Down Previous Build (Stage)') {
            when { branch 'stage' }
            agent { label 'stage-agent' }
            steps {
                echo '!!!THIS IS STAGING BRANCH!!!'
                echo 'Stopping previous build...'
                sh 'docker compose down || true'
                echo 'Previous build stopped.'
            }
        }

        stage('Checkout Code (Stage)') {
            when { branch 'stage' }
            agent { label 'stage-agent' }
            steps {
                echo 'Checking out code for STAGE...'
                git url: "${REPO_URL}", branch: 'stage', credentialsId: 'github-pat'
                echo 'Code checkout completed.'
            }
        }

        stage('Build (Stage)') {
            when { branch 'stage' }
            agent { label 'stage-agent' }
            steps {
                echo 'Building the application...'
                sh 'whoami'
                // echo 'Build new image...'
                // sh 'docker compose build --no-cache'
                // echo 'Starting new containers...'
                sh 'docker compose up -d'
                echo 'Application started.'
            }
        }

        stage('Cleanup (Stage)') {
            when { branch 'stage' }
            agent { label 'stage-agent' }
            steps {
                echo 'Cleaning up unused Docker resources...'
                sh 'docker system prune -af'
                echo 'Cleanup completed.'
            }
        }

        stage('Smoke Test (Stage)') {
            when { branch 'stage' }
            agent { label 'stage-agent' }
            steps {
                echo 'Running smoke tests...'
                sh 'curl -f http://localhost:5000 || exit 1'
                echo 'Smoke tests passed.'
            }
        }

        // ---------------- PROD ----------------
        stage('Down Previous Build (Prod)') {
            when { branch 'main' }
            agent { label 'prod-agent' }
            steps {
                echo 'Stopping previous build...'
                sh 'docker compose down || true'
                echo 'Previous build stopped.'
            }
        }

        stage('Checkout Code (Prod)') {
            when { branch 'main' }
            agent { label 'prod-agent' }
            steps {
                echo 'Checking out code for PROD...'
                git url: "${REPO_URL}", branch: 'main', credentialsId: 'github-pat'
                echo 'Code checkout completed.'
            }
        }

        stage('Build (Prod)') {
            when { branch 'main' }
            agent { label 'prod-agent' }
            steps {
                echo 'Building the application...'
                sh 'whoami'
                echo 'Build new image...'
                sh 'docker compose build --no-cache'
                echo 'Starting new containers...'
                sh 'docker compose up -d'
                echo 'Application started.'
            }
        }

        stage('Cleanup (Prod)') {
            when { branch 'main' }
            agent { label 'prod-agent' }
            steps {
                echo 'Cleaning up unused Docker resources...'
                sh 'docker system prune -af'
                echo 'Cleanup completed.'
            }
        }

        stage('Smoke Test (Prod)') {
            when { branch 'main' }
            agent { label 'prod-agent' }
            steps {
                echo 'Running smoke tests...'
                sh 'curl -f http://localhost:5000 || exit 1'
                echo 'Smoke tests passed.'
            }
        }
    }
}
