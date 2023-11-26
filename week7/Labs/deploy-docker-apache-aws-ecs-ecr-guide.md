# Deploying a Docker Containerized Apache Web Application on AWS ECS with ECR and Fargate: Step-by-Step Guide




Creating a Docker image for an Apache web application on local machine, pushing it to Amazon Elastic Container Registry (ECR), and then launching an Amazon ECS (Elastic Container Service) task using the ECR image involves several steps. Below are the steps you can follow:

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



## Step 4: Write Dockerfile

  * Open the Dockerfile using a text editor. Add the following content:

        # Use the official Apache image as the base image
        FROM httpd:latest

        # Copy the local index.html file to the Apache server directory
        COPY ./index.html /usr/local/apache2/htdocs/

        # Expose port 80
        EXPOSE 80


    
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

  * Open a web browser and enter http://localhost:8080 in the address bar. You should see the content of      your index.html file served by Apache running inside the Docker container.

        Note: To stop the container, use docker stop <container_id> where <container_id> is the ID of the            running container. You can find the container ID by running docker ps.
           If you make changes to your index.html or Dockerfile, you'll need to rebuild the image (docker            build -t my-apache-server.) and then rerun the container (docker run -d -p 8080:80 my-apache-             server).


<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/fed82401-1671-4d1f-8981-015d1e065a09">

  

## Step 8: Create an ECR Repository

 * Open the AWS Management Console.
 * Navigate to the Amazon ECR service.
 * In the ECR dashboard, choose "Create repository."
 * Enter a meaningful repository name, e.g., "my-project-repo".
 * Choose "Create repository."

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/68a27a25-efbd-440a-b9c4-883baf667539">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/47443e05-cc59-407b-97ea-d119fb63eb1e">


<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/8cd36d20-a03c-40b9-b327-1450f29f0236">

## Step 9: Push Docker Image to ECR:

 * You can push your container images to an Amazon ECR repository with the docker push command.
 * To push a Docker image to an Amazon ECR repository the Amazon ECR repository must exist before you        push the image.
 * Click the "my-project-repo" ECR repository created in the previous step, click on the " View push         commands".

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/074c1c62-841a-4ba7-9e88-efe2625b0257">


 * Execute the commands on your local terminal or command-line interfcae to push the docker image.
 
       Note: If you receive an error, install or upgrade to the latest version of the AWS CLI. For more information, see Installing the AWS Command Line Interface in the [AWS Command Line Interface User Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). And Configure AWS CLI using aws configure,check [here](https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/blob/main/week7/Labs/How_to_configure_AWS_CLI.md) for instructions.

 
   
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/7f708821-92d3-4d04-a6da-5b14734a5a22">

 * Once image is sucessfully pushed, you should be able to see the image in the ECR repository .

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/c751cdfe-252c-4113-bcc4-d19ec3c14781">

 * Click on the the latest image link , you can see the image details. Notedown the URI of the image to use later.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/f18be8dc-4fda-44d3-9061-744a5919aa0f">


## Step 10: Create  ECS Cluster (Elastic Container Service):

 * In the ECS Console, choose "Clusters" in the navigation pane.
 * Choose "Create Cluster." with Cluster name "my-project-cluster".
 * Configure your ECS cluster settings and choose "Create."



<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/d60faee2-dab2-4279-8ddf-32de1d4996ec">



<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/ade2ab08-fd4a-4f79-90ec-df9f97c50d49">



<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/67d4242a-3f1b-4c06-8610-3e7e56dec9c8">



## Step 11: Create an ECS Task Definition:

 * Open the Amazon ECS Console.
 * In the navigation pane, choose "Task Definitions" under "Amazon ECS."
 * Choose "Create new Task Definition." with name "my-project-taskdef".
 * Select the launch type compatibility (EC2 or Fargate).
 * Configure your task definition, including the container definition. 

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/a269777c-070c-4d57-b222-0200c03cae81">

 * Choose Task size CPU: 1 vCPU and Memory: 3GB
 * Select Task role and Task execution role as : ecsTaskExecutionRole

   
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/8f25579e-af0e-4fc4-8aeb-78a22a905657">

 * In the Container-1 section Specify the Name and URI : Pushed ECR image URI( copied earlier)

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/8553593c-9672-422b-b830-b5681ee6ba69">

 * In the Log collection section, unselect Use log collection checkbox.

 * Click on create , Task definition will be created.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/ade61867-211c-4597-8c6f-87aaff6327d5">


## Step 12: Create ECS Service:

 * From Task definition console, select the previously created Task defintion.
 * Select "Create service" option From the "Deploy" button.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/c676a93b-1cbe-47aa-a96f-231d6e11d261">

 * In the deployment configuration, select "Service" as Application type, give service name: "my-project-service" and Desired tasks: 2

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/0f015761-f929-4196-8549-1126da1a41c4">

 * In the Network section: select VPC:default VPC and choose available subnets.
 * Create a new security group allowing HTTP protocol on port 80 from Anywhere.
 * Enable Public IP. Click on create.It will take couple of minutes to complete.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/e9292c67-f6c6-40c2-bcde-c55cfe63fa2b">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/bfe043cd-64de-46b7-9a49-2233a7fddc82">

 * Once service is successfully created , click on the Task tab section in the bottom section of the screen.Your two tasks should be up and running.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/959605a5-c2b2-4a65-8cd0-9c3293f4743d">


## Step 13: Access Your Application:


 * Click on the one task and goto Networking section ,copy the Public IP.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/25e9d01f-446f-46b7-92a9-697a9d51b4b3">

 * Open New Incognito window browser and paste the public ip you copied earlier and press enter, you should be able to view application html page.

<image src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/ddfd4ce3-65e3-4b12-ad53-f26edd7d8729">

 * Repeat the above two steps for the second task also to access the application.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/c9e6f5e1-9c3e-4c4f-b248-7e28d365d4a6">

   
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/627c694f-33c0-4901-a12a-e82a23500177">

##### Congratulations!!! You have successfully created a Docker image for an Apache web application on local machine, pushed it to Amazon Elastic Container Registry (ECR), and then launched an Amazon ECS (Elastic Container Service) task using the ECR image.

## Step 14 : Cleanup Resources

 * Don't forget to delete the resources created earlier to avoid unnecessary billing . 

 * Goto ECS Console - Clutsers - select the cluster "my-project-cluster" and click on the Delete cluster, which will delete the all the related resources.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/4729b04e-039f-422d-b542-d5c8ed63ede2">

 * You can check the deletion status in cloud formation .

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/ca556f45-bfb6-4a33-af9e-1677af6a0384">

 * Goto ECR console, select the created repository "my-project-repo" and click on the delete buttion.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/22c64bc8-77ed-4da0-be62-9dd8b1fad923">









