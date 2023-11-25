# Deploying a Dockerized Apache Web Server on AWS ECS with ECR: A Step-by-Step Guide

Creating a Docker image for an Apache web server on local machine, pushing it to Amazon Elastic Container Registry (ECR), and then launching an Amazon ECS (Elastic Container Service) task using the ECR image involves several steps. Below are the steps you can follow:

## Step 1: Install Docker:

  * Make sure Docker is installed on your local machine. You can download and install Docker from the official website: [Install Docker](https://docs.docker.com/engine/install/)

## Step 2: Create a Folder Structure

  * Create a directory for your project. Inside this directory, create two files: Dockerfile and index.html.

## Step 3: Create index.html

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

<img src="<img width="734" alt="image" src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/900f15a1-b1fb-4014-89d5-31d1a3211038">
">

## Step 4: Write Dockerfile

  * Open the Dockerfile using a text editor. Add the following content:

        # Use the official Apache image as the base image
        FROM httpd:latest

        # Copy the local index.html file to the Apache server directory
        COPY ./index.html /usr/local/apache2/htdocs/

        # Expose port 80
        EXPOSE 80

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/900f15a1-b1fb-4014-89d5-31d1a3211038">
    
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
    To stop the container, use docker stop <container_id> where <container_id> is the ID of the running       container. You can find the container ID by running docker ps.
    If you make changes to your index.html or Dockerfile, you'll need to rebuild the image (docker build      -t my-apache-server.) and then rerun the container (docker run -d -p 8080:80 my-apache-server).
  

## Step 8: Create an ECR Repository

 * Open the AWS Management Console.
 * Navigate to the Amazon ECR service.
 * In the ECR dashboard, choose "Create repository."
 * Enter a meaningful repository name, e.g., "my-project-repo".
 * Choose "Create repository."

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/68a27a25-efbd-440a-b9c4-883baf667539">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/47443e05-cc59-407b-97ea-d119fb63eb1e">

## Step 9: Push Docker Image to ECR:

 * You can push your container images to an Amazon ECR repository with the docker push command.
 * To push a Docker image to an Amazon ECR repository the Amazon ECR repository must exist before you        push the image.
 * Click the "my-project-repo" ECR repository created in the previous step, click on the " View push         commands".

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/074c1c62-841a-4ba7-9e88-efe2625b0257">

 * Execute the commands on your local terminal or command-line interfcae to push the docker image.If you receive an error, install or upgrade to the latest version of the AWS CLI. For more information, see Installing the AWS Command Line Interface in the [AWS Command Line Interface User Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
   
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/7f708821-92d3-4d04-a6da-5b14734a5a22">





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







