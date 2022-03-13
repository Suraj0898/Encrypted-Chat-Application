#!bin/bash

read -p "Please enter a Postal Code: " postalcode
#echo Postal Code entered is $postalcode
if [[ "$postalcode" =~ [0-9]{5} ]]; then
 echo "USA Postal Code"
elif [[ "$postalcode" =~ ([A-Z]{1}[0-9]{1}){3} ]]; then
 echo "Canada Postal Code"
else
 echo "None of these"
fi
exit 0
