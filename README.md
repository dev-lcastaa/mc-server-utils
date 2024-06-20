# Mc Server Utils

## Why?
Why not lol. The thought of manually doing this every time you want to play sucks, it can get boring real quick. 

This Util was created to:
- Return a list of EC2 instances you have in AWS
- Return a list of Elastic IPs you have in AWS
- If the EC2 Server has no Elastic IP you can auto associate it
- If the EC2 Server has an Elastic IP you can auto dissociate it
- It also Starts an EC2 instance
- It also Stops an EC2 instance
- Set up launch sequences

## Pre-requites

- You MUST have the AWS CLI working on your machine where this script will run
- You MUST have the appropriate permissions an policies in place.
- You MUST have System Manager attached to the EC2 instance you are using in this script
- You MUST use an Elastic IP with your AWS Instance
- You MUST have RCON installed on your machine and Enabled in your { server.properties }

## Features:

### Start-up
- Automatically associate elastic IP to EC2 instance
- Automatically Starts EC2 instance
- Automatically Launches MC Server using RCON

### Shut-down
- Automatically sends a Save-all CMD to MC Server
- Automatically sends a Stop CMD to the MC Server
- Automatically Stops the EC2 instance
- Automatically Disassociates the Elastic-IP from the EC2 Instance