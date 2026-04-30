pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python & Install Dependencies') {
            steps {
                bat '''
                py -m pip install --upgrade pip
                py -m pip install -r backend/requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                py -m pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                docker build -t expense-tracker .
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                bat '''
                docker stop expense-tracker-container || exit 0
                docker rm expense-tracker-container || exit 0
                docker run -d -p 5000:5000 --name expense-tracker-container expense-tracker
                '''
            }
        }
    }
}