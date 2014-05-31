# coding=utf-8
#from socket import * 
import socket
import os 
import sys 
import struct 
import time 
import select 
import binascii 
#Author: Kory Kozlowski
#global variables 
ICMP_ECHO_REQUEST = 8 
minRTT = 1000
maxRTT = 0
totalRTT = 0
numTimeouts = 0
totalPings = 0
 
def checksum(str): 
    csum = 0 
    countTo = (len(str) / 2) * 2 
 
    count = 0 
    while count < countTo: 
        thisVal = ord(str[count+1]) * 256 + ord(str[count]) 
        csum = csum + thisVal 
        csum = csum & 0xffffffffL 
        count = count + 2 
 
    if countTo < len(str): 
        csum = csum + ord(str[len(str) - 1]) 
        csum = csum & 0xffffffffL 
 
    csum = (csum >> 16) + (csum & 0xffff) 
    csum = csum + (csum >> 16) 
    answer = ~csum 
    answer = answer & 0xffff 
    answer = answer >> 8 | (answer << 8 & 0xff00) 
    return answer 
 
def receiveOnePing(mySocket, ID, timeout, destAddr): 
    timeLeft = timeout 
 
    while 1: 
        startedSelect = time.time() 
        whatReady = select.select([mySocket], [], [], timeLeft) 
        howLongInSelect = (time.time() - startedSelect) 
        if whatReady[0] == []: # Timeout 
            return "Request timed out." 
 
        timeReceived = time.time() 
        recPacket, addr = mySocket.recvfrom(1024) 
 
        #Fill in start         
        #Fetch the ICMP header from the IP packet 
        #first 20 bytes = IP header
        header = recPacket[20:28]
        #type(8bits), code(8bits), checksum(16bits), id(16bits), sequence(16bits)
        type, code, checksum, id, sequence = struct.unpack("bbHHh", header)
        if id == ID: 
            numBytes = struct.calcsize("d")
            timeLocale = recPacket[28:28 + numBytes]
            timeSent = struct.unpack("d", timeLocale)[0]
            transTime = (timeReceived - timeSent)*1000
            ttlLocale = recPacket[8:9]
            ttl = struct.unpack("b", ttlLocale)[0]
            print "type= %d, code= %d, checksum= %d, id= %d, sequence= %d, TTL= %d"%(type,code,checksum,id,sequence,ttl)
            return  transTime
        #Fill in end 
 
        timeLeft = timeLeft - howLongInSelect 
        if timeLeft <= 0: 
            return "Request timed out." 
            
def sendOnePing(mySocket, destAddr, ID): 
    # Header is type (8), code (8), checksum (16), id (16), sequence (16) 
 
    myChecksum = 0 
    # Make a dummy header with a 0 checksum. 
    # struct -- Interpret strings as packed binary data 
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1) 
    data = struct.pack("d", time.time()) 
    # Calculate the checksum on the data and the dummy header. 
    myChecksum = checksum(header + data) 
 
    # Get the right checksum, and put in the header 
    if sys.platform == 'darwin': 
        myChecksum = socket.htons(myChecksum) & 0xffff 
    #Convert 16-bit integers from host to network byte order. 
    else: 
        myChecksum = socket.htons(myChecksum) 
 
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1) 
    packet = header + data 
 
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str 
    #Both LISTS and TUPLES consist of a number of objects 
    #which can be referenced by their position number within the object 
 
def doOnePing(destAddr, timeout): 
    icmp = socket.getprotobyname("icmp") 
    #SOCK_RAW is a powerful socket type. For more details see: http://sock-raw.org/papers/sock_raw 
 
    #Fill in start 
 
    #Create Socket here 
    try:
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error, (n, error):
        if n == 1: 
            error+=(". Please run as root")
            raise socket.error(error)
        raise
    mySocket.connect((destAddr,80))
    #Fill in end 
 
    myID = os.getpid() & 0xFFFF #Return the current process i 
    sendOnePing(mySocket, destAddr, myID) 
    delay = receiveOnePing(mySocket, myID, timeout, destAddr) 
 
    mySocket.close() 
    return delay 
 
def ping(host, timeout=1): 
    #timeout=1 means: If one second goes by without a reply from the server, 
    #the client assumes that either the client’s ping or the server’s pong is lost 
    try:
        dest = socket.gethostbyname(host) 
    except socket.error, v:
        err = v[0]
        if err == 110: 
            print "ERROR: Host Connection Timed Out"
            return 0
    print "Pinging " + dest + " using Python:" 
    print "" 
    #Send ping requests to a server separated by approximately one second 
    numPing = input('Enter Number of Times to Ping ' + host + ': ')
    global totalPings
    totalPings = numPing
    print "------------------------------------------------------------------------"
    while numPing > 0 :        
        delay = doOnePing(dest, timeout) 
        global numTimeouts
        if delay == "Request timed out.":    
            numTimeouts += 1
            print delay
        else:
            global totalRTT, minRTT, maxRTT
            if delay < minRTT:
                minRTT = delay
            if delay > maxRTT:
                maxRTT = delay 
            totalRTT += delay 
            print "RTT= %.10f(ms)"%(delay) 
        print "------------------------------------------------------------------------"
        time.sleep(1)# one second 
        numPing = numPing - 1
    return delay 

#main function
yesNo = raw_input('Do Ping? (y/n): ')
while yesNo=="y"or yesNo=="Y"or yesNo=="yes"or yesNo=="Yes"or yesNo=="YES":
    #global minRTT, maxRTT, totalRTT, numTimouts, totalPings
    minRTT = 1000
    maxRTT = 0
    totalRTT = 0
    numTimeouts = 0
    totalPings = 0
    dropped = 0
    host = raw_input('Enter URL to Ping: ')
    res = ping(host)    
    #if connect error or timeout
    if minRTT == 1000:
        minRTT = 0; 
    #if socket connection did not timeout
    if res != 0:
        dropped = (numTimeouts/totalPings)*100
        avgPing = totalRTT/totalPings
        print "avgRTT= %.10f, minRTT= %.10f, maxRTT= %.10f"%(avgPing,minRTT,maxRTT)
        print "Packets Dropped= %d"%(dropped)+"%"
        print "------------------------------------------------------------------------"
    yesNo = raw_input('Do Ping? (y/n): ')
print "Goodbye"
