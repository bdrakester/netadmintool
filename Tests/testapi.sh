#!/bin/bash
HOST_NAME=$1
DEVICE=$2
NEWNAME=$3

echo "Testing Net Admin Tool API at ${HOST_NAME}"
echo ""
echo "Get all devices ... "
echo "curl -i http://${HOST_NAME}:5000/api/devices"
echo ""
curl -i http://${HOST_NAME}:5000/api/devices
echo ""
echo "Getting device ${DEVICE} ..."
echo "curl -i http://${HOST_NAME}:5000/api/devices/${DEVICE}"
echo ""
curl -i http://${HOST_NAME}:5000/api/devices/${DEVICE}
echo ""
echo "Adding device ${NEWNAME} ..."
#POSTDATA="'{\"name\":\"${NEWNAME}\", \"device_type\":\"Type of ${NEWNAME}\",\"description\":\"Description of ${NEWNAME}\"}'"
#posting with spaces caused issues
POSTDATA="{\"name\":\"${NEWNAME}\",\"device_type\":\"cisco_ios\",\"description\":\"descriptionof${NEWNAME}\"}"
echo "curl -i -H \"Content-Type: application/json\" -X POST -d ${POSTDATA} http://${HOST_NAME}:5000/api/devices"
#curl -i -H "Content-Type: application/json" -X POST -d "'"<$POSTDATA>"'" http://${HOST_NAME}:5000/api/devices
curl -i -H "Content-Type: application/json" -X POST -d ${POSTDATA} http://${HOST_NAME}:5000/api/devices
echo "Get all devices again ..."
echo "curl -i http://${HOST_NAME}:5000/api/devices"
echo ""
curl -i http://${HOST_NAME}:5000/api/devices
echo ""
echo "Updating device ${DEVICE} ..."
PUTDATA="{\"description\":\"PUT_Description_NEW\"}"
echo "curl -i -H \"Content-Type: application/json\" -X PUT -d ${PUTDATA} http://${HOST_NAME}:5000/api/devices"
curl -i -H "Content-Type: application/json" -X PUT -d ${PUTDATA} http://${HOST_NAME}:5000/api/devices
echo ""
