Deploy Pre-requisites:
We use pre-requisites.yaml file and AWS CloudFormation to create the necessary IAM roles, policies, and other resources before creating the VPC.
Copy the below code in a text file and save it as pre-requisites.yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: "Create IAM roles for EC2 instances and Flow Logs and an S3 Bucket for endpoint policy tests"

Resources:
  # Account Level Resources
  EC2Role:
    Type: AWS::IAM::Role
    Properties:
      RoleName: "NetworkingWorkshopEC2Role"
      Path: "/"
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
        - arn:aws:iam::aws:policy/AmazonS3FullAccess
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service:
                - ec2.amazonaws.com
            Action:
              - sts:AssumeRole

  EC2InstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      InstanceProfileName: "NetworkingWorkshopInstanceProfile"
      Path: "/"
      Roles:
        - !Ref EC2Role

  FlowLogsRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: NetworkingWorkshopFlowLogsRole
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service:
                - vpc-flow-logs.amazonaws.com
            Action:
              - 'sts:AssumeRole'
      Description: Role to allow VPC Flow Logs to write to CloudWatch logs
      Policies:
        - PolicyName: CloudWatchLogsWrite
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action: 
                  - "logs:CreateLogGroup"
                  - "logs:CreateLogStream"
                  - "logs:PutLogEvents"
                  - "logs:DescribeLogGroups"
                  - "logs:DescribeLogStreams"
                Resource: !Sub 'arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:NetworkingWorkshopFlowLogsGroup:*'

  GatewayEndpointBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'networking-day-${AWS::Region}-${AWS::AccountId}'
      LifecycleConfiguration:
        Rules:
          - ExpirationInDays: 3
            Status: Enabled
To get started, navigate to the CloudFormation section in the AWS console. Click the Create stack button and select With new resources (standard).
Under Specify template, select Upload a template file, click Choose file, and select the pre-requisites.yaml CloudFormation template that you downloaded. Click Next.

3. Enter a stack name, e.g. NetworkingWorkshopPrerequisites. Click Next.
4. Leave everything on this screen as is. Scroll down and click Next.
5. Review the stack configuration and click the "Create stack" button. CloudFormation will create the specified resources as defined in your template.
6. Wait for CloudFormation to complete the stack creation process. You can monitor the progress in the CloudFormation console.
