pipeline {
    agent any

    environment {
        APP_IMAGE   = "cicd-site"
        TEST_IMAGE  = "cicd-tests"
        NETWORK     = "cicd-net"
        STAGING     = "cicd-staging"
        LIVE        = "cicd-live"
        LIVE_PORT   = "8080"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Checked out commit ${env.GIT_COMMIT}"
            }
        }

        stage('Package') {
            steps {
                sh "docker build -t ${APP_IMAGE}:${BUILD_NUMBER} -t ${APP_IMAGE}:latest ."
            }
        }

        stage('Start Staging') {
            steps {
                sh """
                    docker network create ${NETWORK} || true
                    docker rm -f ${STAGING} || true
                    docker run -d --name ${STAGING} --network ${NETWORK} ${APP_IMAGE}:${BUILD_NUMBER}
                    sleep 3
                """
            }
        }

        stage('Test') {
            steps {
                sh """
                    docker build -t ${TEST_IMAGE} tests/
                    docker run --rm --network ${NETWORK} \
                        -e SITE_URL=http://${STAGING}:80 \
                        -v ${WORKSPACE}:/work \
                        ${TEST_IMAGE} pytest -v --junitxml=/work/results.xml /work/tests/test_site.py
                """
            }
            post {
                always {
                    junit 'results.xml'
                }
            }
        }

        stage('Deploy') {
            steps {
                sh """
                    docker rm -f ${LIVE} || true
                    docker run -d --name ${LIVE} -p ${LIVE_PORT}:80 ${APP_IMAGE}:${BUILD_NUMBER}
                    echo "Deployed build ${BUILD_NUMBER} on port ${LIVE_PORT}"
                """
            }
        }
    }

    post {
        always {
            sh "docker rm -f ${STAGING} || true"
        }
        success {
            echo "Pipeline SUCCESS - build ${BUILD_NUMBER} is live."
        }
        failure {
            echo "Pipeline FAILED - deploy skipped, live site unchanged."
        }
    }
}
