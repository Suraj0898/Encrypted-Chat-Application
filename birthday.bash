#!bin/bash

echo "Birthday is: 10/08/1998"

let total=0
for num in 1 0 0 8 1 9 9 8
do
 total=$((total+num))
done

echo "Sum of the digits is: $total"

exit 0

