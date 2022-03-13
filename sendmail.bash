#!bin/bash

sudo apt-get install mutt
echo "This is a Test Email for IPA Assignment 3." | mutt -s "Test Email" -a batman.png -- suhas.s@northeastern.edu
