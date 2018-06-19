#!/bin/bash
for i in `seq 0 19`;
do

echo $i

./VPNaas_testrun.sh 10.2.10.146 & ./vpntest.sh 10.2.10.161 &
wait
./ssh_delete.sh
wait


done
