# Deploying a Dockerized Apache Web Server on AWS ECS with ECR: A Step-by-Step Guide

Creating a Docker image for an Apache web server on local machine, pushing it to Amazon Elastic Container Registry (ECR), and then launching an Amazon ECS (Elastic Container Service) task using the ECR image involves several steps. Below are the steps you can follow:

## Step 1: Install Docker:

  * Make sure Docker is installed on your local machine. You can download and install Docker from the official website: [Install Docker](https://docs.docker.com/engine/install/)


## Step 2: Create a Folder Structure

  * Create a directory for your project. Inside this directory, create two files: Dockerfile and index.html.

## Step 3: Write Dockerfile

  * Open the Dockerfile using a text editor. Add the following content:

        # Use the official Apache image as the base image
        FROM httpd:latest

        # Copy the local index.html file to the Apache server directory
        COPY ./index.html /usr/local/apache2/htdocs/

        # Expose port 80
        EXPOSE 80

## Step 4: Create index.html

  * In the same directory, create an index.html file and add your HTML content:
    
        <!DOCTYPE html>
        <html>
          <head>
          <title>Welcome to My Docker Apache Server</title>
          </head>
          <body>
            <h1>Hello from Docker Apache Server!</h1>
            <p>This is a sample HTML file served by Apache inside a Docker container.</p>
          </body>
        </html>
    
## Step 5: Build the Docker Image

  * Open Terminal or your preferred command-line interface. Navigate to the project directory containing your Dockerfile and 
    index.html.

  * Run the following command to build the Docker image:

        docker build -t my-apache-server .
    
    This command builds an image named my-apache-server based on the Dockerfile in the current directory (.).

## Step 6: Run the Docker Container

  * Once the image is built, run the Docker container using the following command:

        docker run -d -p 8080:80 my-apache-server
    
    This command starts a container from the my-apache-server image, mapping port 8080 on your host machine to port 80 on the      Docker container.

## Step 7: Access the Apache Server

  * Open a web browser and enter http://localhost:8080 in the address bar. You should see the content of your index.html file served by Apache running inside the Docker container.

  * Notes:
    To stop the container, use docker stop <container_id> where <container_id> is the ID of the running container. You can         find the container ID by running docker ps.
    If you make changes to your index.html or Dockerfile, you'll need to rebuild the image (docker build -t my-apache-server       .) and then rerun the container (docker run -d -p 8080:80 my-apache-server).
    These steps should get you up and running with an Apache web server inside a Docker container on your Mac!

## Step 8: Create an ECR Repository

 * Open the AWS Management Console.
 * Navigate to the Amazon ECR service.
 * In the ECR dashboard, choose "Create repository."
 * Enter a meaningful repository name, e.g., "my-project-repo".
 * Choose "Create repository."

<img src=" ">

Docker Image:
Build and Tag Your Docker Image:
Open a terminal.

Navigate to the directory containing your Dockerfile.

Build your Docker image:

bash
Copy code
docker build -t your-image-name .
Tag your Docker image:

bash
Copy code
docker tag your-image-name:latest your-account-id.dkr.ecr.your-region.amazonaws.com/your-repo-name:latest
Replace your-account-id, your-region, and your-repo-name with your AWS account ID, AWS region, and the name of the ECR repository created earlier.

3. Push Docker Image to ECR:
Authenticate Docker to your ECR registry:

bash
Copy code
aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com
Push your Docker image to ECR:

bash
Copy code
docker push your-account-id.dkr.ecr.your-region.amazonaws.com/your-repo-name:latest
4. ECS (Elastic Container Service):
Create an ECS Task Definition:
Open the Amazon ECS Console.
In the navigation pane, choose "Task Definitions" under "Amazon ECS."
Choose "Create new Task Definition."
Configure your task definition, including the container definition. Specify the ECR image URI.
Run an ECS Task:
In the ECS Console, choose "Clusters" in the navigation pane.
Choose "Create Cluster."
Configure your ECS cluster settings and choose "Create."
Run a Task in the ECS Cluster:
In the cluster details page, choose "Tasks" tab.
Choose "Run new task."
Select the task definition you created.
Configure the task settings and choose "Run Task."
5. Access Your Application:
Once the ECS task is running, you can access your application by finding the public IP or DNS of the associated EC2 instance in the ECS cluster. Check the "Tasks" tab for details on the running task.

These steps cover the process through the AWS Management Console, and it should guide you through setting up ECR, pushing an image, and launching an ECS task using the image you pushed.







