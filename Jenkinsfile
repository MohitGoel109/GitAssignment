pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building the application...'
                sh 'echo "Compiling source code"'
                sh 'mkdir -p build && echo "build artifact" > build/app.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'echo "Running unit tests"'
                sh 'test -f build/app.txt && echo "Test passed: build artifact exists"'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
                sh 'mkdir -p deploy && cp build/app.txt deploy/'
                sh 'echo "Deployed at $(date)" >> deploy/deployment.log'
                sh 'echo "Deployment complete. Files in deploy/:"'
                sh 'ls -la deploy/'
                sh 'echo "---- deployment.log ----"'
                sh 'cat deploy/deployment.log'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! Application deployed.'
        }
        failure {
            echo 'Pipeline failed. Deployment aborted.'
        }
        always {
            echo "Build #${env.BUILD_NUMBER} finished with status: ${currentBuild.currentResult}"
        }
    }
}
