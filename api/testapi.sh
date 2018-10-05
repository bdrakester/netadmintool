#!/bin/bash
HOST_NAME=""
echo "Testing Net Admin Tool API at ${HOST_NAME}"
echo ""
echo "Get all devices ... "
echo ""
curl -i http://${HOST_NAME}:5000/api/devices
echo ""
echo "Getting device 1 ..."
echo ""
curl -i http://${HOST_NAME}:5000/api/devices/1
