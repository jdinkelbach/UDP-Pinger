# Justin Dinkelbach
# Date: 9/25/2020
# Project: Programming Assignment 2
# Client.py
# Allows creation of sockets within program
from socket import *
import time
serverName = 'Justin-PC'
serverPort = 12000
numPings = 10
rtt = []
loss = 0.0
# Create the client's socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)
for i in range(numPings):
    startTime = time.time()
    message = "Ping" + str(i+1)
    print("Mesg sent: " + message)
    # Start time (ms)
    # Send ping message through the socket to the host destination
    # encode() - converts string to byte type
    # sendTo() = attaches the destination address (serverName, serverPOrt)
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    try:
        # Receives the packet from the Internet at the client's socket
        message, serverAddress = clientSocket.recvfrom(2048)
        returnTime = time.time()
        message = message.decode()
        # Calculate packet RTT
        elapsedTime = returnTime - startTime
        rtt.append(elapsedTime)
        # Display packet results
        print("Mesg rcvd: " + message.upper())
        print("Start Time:" + str((startTime * 1000) / 10 ** 12) + "e+12")
        print("Return Time:" + str((returnTime * 1000) / 10 ** 12) + "e+12")
        print("Pong " + str(i+1) + " RTT: " + str(elapsedTime) + " ms\n")
    except timeout:
        loss += 1.0
        print("No Mesg rcvd\nPONG " + str(i+1) + " Request timed out.\n")
# Calculate estimated RTT
estimatedRTT = rtt[0]
estimatedArr = [rtt[0]]
for i in range(1, len(rtt)):
    estimatedRTT = (1-0.125) * rtt[i] + (0.125 * estimatedRTT)
    estimatedArr.append(estimatedRTT)
# Calculate Deviation RTT
devRTT = estimatedRTT
for i in range(len(rtt)):
    devRTT = (1-0.25) * devRTT + 0.25 * abs(rtt[i] - estimatedArr[i])
# Calculate timeout interval
timeout = estimatedRTT + 4 * devRTT
# Calculate avg RTT
avg = sum(rtt) / len(rtt)
# Display results
print("Min RTT:         " + str(min(rtt)) + " ms")
print("Max RTT:         " + str(max(rtt)) + " ms")
print("Avg RTT:         " + str(avg) + " ms")
print("Packet Loss:     " + str(loss * 10) + "%")
print("Estimated RTT:   " + str(estimatedRTT) + " ms")
print("Dev RTT:         " + str(devRTT) + " ms")
print("Timeout Interval:" + str(timeout) + " ms")
