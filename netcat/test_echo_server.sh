#!/bin/sh
test_words="hello world"
response=$(echo "$test_words" | nc -v server 12345)
if [ "$test_words" = "$response" ]; then
    echo "action: test_echo_server | result: success"
else 
    echo "action: test_echo_server | result: fail"
fi