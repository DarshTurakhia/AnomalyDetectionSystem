pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/DarshTurakhia/AnomalyDetectionSystem'
            }
        }

        stage('Lint IaC Code') {
            steps {
                sh 'terraform validate'
                sh 'vagrant validate'
                sh 'ansible-lint'
            }
        }

        stage('Provision Infrastructure') {
            steps {
                sh 'vagrant up --provision'
            }
        }

        stage('Run Security Scan') {
            steps {
                sh 'lynis audit system'
            }
        }

        stage('Deploy Application') {
            steps {
                sh 'ansible-playbook -i inventory.ini deploy.yml'
            }
        }
    }
}
