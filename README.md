# CI/CD Journey: Setting up a Jenkins Pipeline for a Flask Application

<img width="398" height="128" alt="image" src="https://github.com/user-attachments/assets/e2858177-6415-4d68-8d92-105fdc02bdf8" />


This document chronicles the process of setting up a Continuous Integration and Continuous Delivery (CI/CD) pipeline for a simple Flask application using Jenkins and Docker.

## 1. Initial Setup

We started with a `Jenkinsfile` that defined a four-stage pipeline: Checkout, Build, Test, and Push.

```groovy
// Initial Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/lucasjotap/jenkinsforpresident.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    dockerImage = docker.build("your-org/your-app:${env.BUILD_NUMBER}")
                }
            }
        }
        stage('Test') {
            steps {
                sh 'docker run --rm your-org/your-app:${env.BUILD_NUMBER} ./run-tests.sh'
            }
        }
        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        dockerImage.push()
                    }
                }
            }
        }
    }
}
```

## 2. Creating the Flask Application

The initial repository was empty, so we created a simple Flask application to test the pipeline.

**Commands:**

```bash
# Clone the empty repository
git clone https://github.com/lucasjotap/jenkinsforpresident.git ./temp_repo

# Create the application files
touch ./temp_repo/app.py
touch ./temp_repo/requirements.txt
touch ./temp_repo/Dockerfile
touch ./temp_repo/run-tests.sh
chmod +x ./temp_repo/run-tests.sh
```

**File Contents:**

*   `app.py`:
    ```python
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')
    ```
*   `requirements.txt`:
    ```
    Flask==2.0.1
    ```
*   `Dockerfile`:
    ```dockerfile
    FROM python:3.8-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install -r requirements.txt

    COPY . .

    CMD ["python", "app.py"]
    ```
*   `run-tests.sh`:
    ```bash
    #!/bin/sh
    echo "Running tests..."
    exit 0
    ```

## 3. Pushing to GitHub

To get the code into the repository, we needed to authenticate with GitHub. We used a Personal Access Token (PAT).

**Commands:**

```bash
# Configure git
git config --global user.name "Gemini"
git config --global user.email "gemini@google.com"

# Add the files and commit
cd ./temp_repo
git add .
git commit -m "Add simple Flask application"

# Set the remote URL with the PAT and push
git remote set-url origin https://<YOUR_PAT>@github.com/lucasjotap/jenkinsforpresident.git
git push origin main
```

## 4. Reverting the Jenkinsfile

For a short period, we modified the `Jenkinsfile` to use the local directory for testing, but we reverted it to use the GitHub repository.

## 5. Setting up the Webhook

To automatically trigger the pipeline, we set up a webhook. This required exposing the local Jenkins instance to the internet using `ngrok`.

**Commands:**

```bash
# Download and install ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -O ngrok.tgz
tar -xvzf ngrok.tgz

# Add your authtoken
./ngrok config add-authtoken <YOUR_NGROK_AUTHTOKEN>

# Start ngrok
./ngrok http 8080
```

This provided a public URL (e.g., `https://xxxxxxxx.ngrok-free.app`).

**GitHub Webhook Configuration:**

*   **Payload URL:** The `ngrok` URL with `/github-webhook/` appended.
*   **Content type:** `application/json`
*   **Events:** "Just the push event"

## 6. Testing the Pipeline

We tested the pipeline by making changes to the code and pushing them to the repository.

*   Changed "Hello, World!" to "Hello, Jenkins!".
*   Added a timestamp to the message.
*   Created new branches (`feature/add-timestamp`, `docs/add-readme`).
