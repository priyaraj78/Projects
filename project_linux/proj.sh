#! /bin /bash

#User_ID = ""
#Group_ID = ""
#Path = ""

if [ $# == 0 ] 
then 
	read -p  "Enter User ID:" User_ID
	read -p " Emter Group ID:" Group_ID
	read -p "Enter the required path:" Path
	echo $User_ID $Group_ID $Path

elif [ $# == 1 ]
then
	read -p  "Enter Group ID:" Group_ID
	read -p "Enter the required path:" Path
	User_ID=$1
	echo $User_ID $Group_ID $Path


elif [ $# == 2 ]
then
	read -p  "Enter the required path:" Path
	User_ID=$1
	Group_ID=$2
else
	User_ID=$1
	Group_ID=$2
	Path=$3
fi
echo $User_ID $Group_ID $Path 

validation=$(cat /etc/passwd | grep $User_ID )

if [ $? != 0 ]
then 
	echo "User not Valid! Try again and make sure Capslock is turned off "

else
	echo "User is Valid "
fi

validation=$(getent group $Group_ID)
if [ $? != 0 ] 
then 
	echo "Group ID is not Valid"
else
	echo "Group ID Valid"
	validation=$(id -G $User_ID | grep $Group_ID)
	if [ $? == 0 ]
	then 
		echo "User is part of the group $Group_ID"
	else
		echo "Sorry! User is not the part of a given group"
	fi	



fi

if [[ "$Path" = /* ]]
then
	echo " Path $Path is absolute as / is given "
else
       echo "Path not valid"	
fi

#validation=$(ls -l $Path | grep '^d' > /dev/null 2>&1)
if [ -d "$Path" ]
then
	echo "Path is a given directory ..thus validated yaaaay"
else
	echo "Path is not a valid directory"
fi	

recurring_path=$(du -a $Path | awk -F ' ' '{print $2}')
recurpath_list=$(echo $recurring_path | tr " " "\n")
for temp in $recurpath_list #took temp variable for iteration in the recurring path's list
do
	echo $temp >> /home/user7/project/acl_files.txt
	ls -ald $temp >> /home/user7/project/acl_files.txt
	getfacl -p $temp >> /home/user7/project/acl_files.txt 
	

done	
