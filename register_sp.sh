#!/bin/bash
for ip in `seq 1 10`;
do
  echo  ./add_sp.sh "sp-10.10.5.$ip" "10.10.5.$ip"
  ./add_sp.sh "sp-10.10.5.$ip" "10.10.5.$ip"
done
