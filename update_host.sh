#! /bin/bash

if [ -z "$1" ]
then
      >&2 echo "No hostname addres provided. You should call '$0 <hostname>'"
fi

echo "Changing to hostname '$1'"

sed -i "s/serverIP = \".*\"/serverIP = \"$1\"/g" ./server/static/index.html
sed -i "s/SERVER_IP = \".*\"/SERVER_IP = \"$1\"/g" ./elli/elli.py