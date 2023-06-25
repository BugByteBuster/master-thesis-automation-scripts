#!/bin/bash

add_sp() {
  local sp_name=$1
  local sp_ip=$2
  echo "./add_sp.sh \"$sp_name\" \"$sp_ip\""
  ./add_sp.sh "$sp_name" "$sp_ip"
}

for ip in {1..10}; do
  sp_name="sp-10.10.5.$ip"
  sp_ip="10.10.5.$ip"
  add_sp "$sp_name" "$sp_ip"
done
