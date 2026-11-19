
pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                "C:\\Users\\Kanishka\\AppData\\Local\\Programs\\Python\\Python310\\python.exe" -m pip install -r backend\\requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                "C:\\Users\\Kanishka\\AppData\\Local\\Programs\\Python\\Python310\\python.exe" -m pytest tests\\test.py -v
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

        stage('Deploy Container') {
            steps {
                bat '''
                docker rm -f expense-tracker-container 2>NUL || echo No previous container
                docker run -d -p 5000:5000 --name expense-tracker-container expense-tracker
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                bat '''
                docker ps
                '''
            }
        }
    }

    post {
        success {
            echo 'Expense Tracker CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'Expense Tracker CI/CD Pipeline failed. Check the console output.'
        }
    }
}
