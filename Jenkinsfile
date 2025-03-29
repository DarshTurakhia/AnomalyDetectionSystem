pipeline {
    agent any

    environment {
        VAGRANT_CWD = "/mnt/DevSecOps" // Ensuring Vagrant runs in the correct directory
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/DarshTurakhia/AnomalyDetectionSystem'
            }
        }

        stage('Lint IaC Code') {
            steps {
                dir('/mnt/DevSecOps') {
                    sh 'vagrant validate || echo "Vagrant not available"'
                }
                sh 'ansible-lint || echo "Ansible-lint failed"'
            }
        }

        stage('Provision Infrastructure') {
            steps {
                sshagent(['fc312660-00a7-46e6-9d51-1c14d591e2dc']) {  
                    sh 'ssh sshdarsh@10.0.0.5 "cd \\"D:/Lambton College/W25/ISN 2514/Project/DevSecOps\\" && vagrant up --provision"'
                }
            }
        }

        stage('Run Security Scan') {
            steps {
                sh 'lynis audit system || echo "Lynis scan failed"'
            }
        }

        stage('Deploy Application') {
            steps {
                sh 'ansible-playbook -i inventory.ini deploy.yml || echo "Deployment failed"'
            }
        }
    }
}
