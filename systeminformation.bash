#!bin/bash

echo "Linux VM SYSTEM INFORMATION - "
echo ""
echo "Kernel Release: " `uname -r`
echo "**************************"
echo "Bash Version: " `bash --version`
echo "**************************"
echo "Amount of Free Storage: " `df -k`
echo "**************************"
echo "Amount of Free Memory: " `free -m`
echo "**************************"
echo "Total Files in the current directory: " `ls /home/client/Desktop/IPA_Assignment_3 | wc -l`
echo "**************************"
echo "IP Address of the Linux VM is: " `hostname -I`
echo "**************************"
echo "The Active Interface(s) is/are as follows: " `ifconfig -a`
echo "**************************"
exit 0
