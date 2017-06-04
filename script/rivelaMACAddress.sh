#!/bin/bash
echo " ---" `date +"%Y-%m-%d %T"`
for i in {10..50}
do
  eval  ping -q -c 1  "192.168.1.$i" >> /dev/null
  ret_code=$?
  if [ $ret_code == 0 ]; then
    /usr/sbin/arp -a "192.168.1.$i" | awk '{if ($4~/:/) print $4}'
  fi
  
done

