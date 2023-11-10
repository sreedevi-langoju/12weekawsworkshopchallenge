CREATE DATABASE IF NOT EXISTS awschallenge;

use awschallenge;


CREATE TABLE Cohort ( Cohort_Num INT NOT NULL PRIMARY KEY AUTO_INCREMENT , Cohort_Name VARCHAR(25) NOT NULL,No_Of_Students INT NOT NULL );


CREATE TABLE Students_Details (Student_Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, Student_Name VARCHAR(25) NOT NULL,Student_Email  VARCHAR(25) NOT NULL,Student_Contact_Num VARCHAR(25) NOT NULL, Cohort_Num INT NOT NULL ,FOREIGN KEY (Cohort_Num) REFERENCES Cohort(Cohort_Num) );



INSERT INTO Cohort (Cohort_Name,No_Of_Students) Values ('Cohort-Fall-23',50);
INSERT INTO Cohort (Cohort_Name,No_Of_Students) Values ('Cohort-Summer-23',75);

 INSERT INTO Cohort (Cohort_Name,No_Of_Students) Values ('Cohort-Spring-23',60);



INSERT INTO Students_Details ( Student_Name ,Student_Email ,Student_Contact_Num,Cohort_Num) VALUES ('Student 1','student1@gmail.com','123456',1);

INSERT INTO Students_Details ( Student_Name ,Student_Email ,Student_Contact_Num,Cohort_Num) VALUES ('Student 2','student2@gmail.com','123456',1);

INSERT INTO Students_Details ( Student_Name ,Student_Email ,Student_Contact_Num,Cohort_Num) VALUES ('Student 3','student3@gmail.com','123456',1);

INSERT INTO Students_Details ( Student_Name ,Student_Email ,Student_Contact_Num,Cohort_Num) VALUES ('Student 4','student4@gmail.com','123456',1);


INSERT INTO Students_Details ( Student_Name ,Student_Email ,Student_Contact_Num,Cohort_Num) VALUES ('Student 5','student5@gmail.com','13579',2);


INSERT INTO Students_Details ( Student_Name ,Student_Email ,Student_Contact_Num,Cohort_Num) VALUES ('Student 6','student6@gmail.com','7865757456',2);


INSERT INTO Students_Details ( Student_Name ,Student_Email ,Student_Contact_Num,Cohort_Num) VALUES ('Student 7','student7@gmail.com','1234212312',3);


INSERT INTO Students_Details ( Student_Name ,Student_Email ,Student_Contact_Num,Cohort_Num) VALUES ('Student 8','student8@gmail.com','123456',3);


INSERT INTO Students_Details ( Student_Name ,Student_Email ,Student_Contact_Num,Cohort_Num) VALUES ('Student 9','student9@gmail.com','12334354',3);


INSERT INTO Students_Details ( Student_Name ,Student_Email ,Student_Contact_Num,Cohort_Num) VALUES ('Student 10','student10@gmail.com','12379',3);

