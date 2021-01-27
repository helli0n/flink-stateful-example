#!/usr/bin/env bash
url="http://127.0.0.1:8888"
time {
  runtime=$((end-start))
  cur_number=$(curl -s $url/users-count | jq .count)
  count_add="${1:-"0"}"
  echo "Current users count is "$cur_number
  echo "Will be added ${count_add} users"
  for (( count=1; count<=${count_add}; count++ )); do
        curl -s --header "Content-Type: application/json" --request POST --data '{"name":"'"xyz1${count}"'","full_name":"'"xyz1${count}"'"}' $url/add-user > /dev/null
      i=$i+1
  done
  cur_number_new=$cur_number
  expect_num=$((cur_number + count_add))

  while [ $expect_num -ne $cur_number_new ]; do
      cur_number_new=$(curl -s $url/users-count | jq .count)
      echo "Left" $(($expect_num - $cur_number_new))
  done
}

