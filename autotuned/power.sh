#!/usr/bin/bash

#Checking battery mode

STATE=""
#The value of BAT won't change in both circumstances
BAT=$(ls /sys/class/power_supply | grep BAT)
if [[ "$1" == "BAT" || "$1" == "AC" ]]; then
  STATE="$1"
fi

#TODO: Find a solution to check for laptop battery status which I don't have and is different from the path
#make sure we are not on a desktop
if [[  $BAT == "" ]]; then
echo -e "We are on a Desktop!! Enable desktop settings"
sudo tuned-adm profile desktop
else
	if [[ $STATE == "" ]]; then
 	 if [[ $(upower -i /org/freedesktop/UPower/devices/battery_${BAT} | grep state | grep discharging) == "" ]]; then
    		STATE="AC"
 	 	else STATE="BAT"
  		fi
	fi
	echo $STATE
	if [ $STATE == "BAT"   ]
	then        
  echo "Discharging, set system to powersave"
    /usr/sbin/tuned-adm profile powersave
    /usr/sbin/tuned-adm active 
 	echo "Setting Wifi"
 	#It's told not to screenscape this tool however after doing tests we got what we wanted
 	/usr/sbin/iw @@WIFIDEV@@ set power_save on
        /usr/sbin/iw @@WIFIDEV@@ get power_save       
	else [ $STATE == "AC"   ]      
  echo "AC plugged in, set system to performance"
  #We are using ondemand here. Performance is always not necessary
    /usr/sbin/tuned-adm profile balanced
    /usr/sbin/tuned-adm active
    echo "Setting Wifi"
 #It's told not to screenscape this tool however after doing tests we got what we wanted
 	/usr/sbin/iw @@WIFIDEV@@ set power_save off
        /usr/sbin/iw @@WIFIDEV@@ get power_save   
	fi
fi
