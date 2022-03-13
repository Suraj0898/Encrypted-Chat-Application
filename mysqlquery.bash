#!bin/bash

sudo mysql <<EOF
USE student;
CREATE TABLE student1 (fname VARCHAR(100), lname VARCHAR(100), dob DATE);
INSERT INTO student1 VALUES("Suraj","Suhas","1998-10-08"),("Rafael","Nadal","1986-06-03"),("Roger","Federer","1981-08-08"),("Andy","Murray","1987-05-15");
SELECT fname,lname,dob from student1;
DROP TABLE student1;
EOF
