# Steps to Connect to the Linux Linux Server instance: 


 ## Microsoft Windows users:
 
These instructions are specifically for Microsoft Windows users. If you are using macOS or Linux, skip to the next section.

* Download the PPK file while creating EC2 instance and save it as labsuser.ppk file.

  Note: Typically, your browser saves the file to the Downloads directory.


* Note down the Linux Instance IP address.
 

* To use SSH to access the EC2 instance, you must use PuTTY. If you do not have PuTTY installed on your computer, download PuTTY.

* Open putty.exe.

* To keep the PuTTY session open for a longer period of time, configure the PuTTY timeout:

* Choose Connection

* Seconds between keepalives: 30

* Configure your PuTTY session by using the following settings.

* Choose Session

* Host Name (or IP address): Paste the Linux Instance for the instance you noted earlier

* Alternatively, return to the Amazon EC2 console and choose Instances .
  
* Select the instance you want to connect to - In the Description tab, copy the IPv4 Public IP value

* Back in PuTTY, in the Connection list, expand  SSH

* Choose Auth and expand  Credentials

* Under Private key file for authentication: Choose Browse

* Browse to and select the labsuser.ppk file that you downloaded

* To select the file, choose Open

* Choose Open again
  
* To trust and connect to the host, choose Accept.

* When you are prompted with login as, enter: ec2-user

* This action connects you to the EC2 instance.

--------------------------------------------------------------------

## macOS  and Linux  Users:

These instructions are specifically for macOS or Linux users. If you are a Windows user, skip ahead to the next task.
 
* Choose the Download PEM file while launching EC2 insatnce and save it as  labsuser.pem file.

* Note down the Linux Instance IP address.

* Open a terminal window, and change directory to the directory where the labsuser.pem file was downloaded by using the cd command.

* For example, if the labsuser.pem file was saved to your Downloads directory, run this command:

      cd ~/Downloads
 
* Change the permissions on the key to be read-only, by running this command:

      chmod 400 labsuser.pem
 

* Run the following command (replace <public-ip> with the Linux Instance IP address that you copied earlier).

* Alternatively, to find the IP address of the EC2 instance, return to the Amazon EC2 console and select Instances

* Select the Linux Server instance that you want to connect to - In the Details tab, copy the Public IPv4 address value

      ssh -i labsuser.pem ec2-user@<public-ip>
 

* When you are prompted to allow the first connection to this remote SSH server, enter yes.

* Because you are using a key pair for authentication, you are not prompted for a password.

You should now be connected to the instance.
