from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from socket import *
from os import path
import pickle
import sys
import os

#Step1: Checking if the RSA Key Pair exists and creating them if necessary
if path.exists('pub_pem_file.pem') and path.exists('prvt_pem_file.pem'):
    print('Both the Keys - Public & Private Exists. No need of Generating Again!')
else:
    print('There are no Public/Private keys. Generating new keys!')
    prvtKey = RSA.generate(1024)
    pubKey = prvtKey.publickey()
    prvtPemFile = prvtKey.exportKey()
    pubPemFile = pubKey.exportKey()

with open('prvt_pem_file.pem', 'wb') as prvt:
    prvt.write(prvtPemFile)
with open('pub_pem_file.pem', 'wb') as pub:
    pub.write(pubPemFile)
    
with open('prvt_pem_file.pem', 'rb') as prvt:
    prvtPemFile = prvt.read()
with open('pub_pem_file.pem', 'rb') as pub:
    pubPemFile = pub.read()
prvtKey = RSA.importKey(prvtPemFile)
pubKey = RSA.importKey(pubPemFile)

#Creating the Socket and verifying the Connection establishment
client = socket(AF_INET, SOCK_STREAM)
client.connect(('192.168.160.131',10000))
receivedMessage ='A Successful Connected Established between Client & Server!'
client.send(receivedMessage.encode())
srvrKey=client.recv(1024)
with open('srvr_pem_file.pem', 'wb') as srvr:
    srvr.write(srvrKey)
server_key= RSA.importKey(srvrKey)
client.send(pubPemFile)

#Initiating a loop for the period the socket connection is active
while True:
    print("Bob:")
    dataToSend = sys.stdin.readline().strip()
    dataToSendEncoded = dataToSend.encode()
    if dataToSend == 'exit':
        dataToSend = dataToSend.encode()
        cipher = PKCS1_OAEP.new(server_key)
        dataToSend = cipher.encrypt(dataToSend)
        dataToSend = pickle.dumps(dataToSend)
        client.send(dataToSend)
        break

    bobHash = SHA256.new(dataToSendEncoded)
    hashedBob = bobHash.hexdigest()
    hashedBobEncoded = hashedBob.encode()
    client.send(hashedBobEncoded)

    dataToSend = dataToSend.encode()
    cipher = PKCS1_OAEP.new(server_key)
    dataToSend = cipher.encrypt(dataToSend)
    dataToSend = pickle.dumps(dataToSend)
    client.send(dataToSend)

    encodedHash = client.recv(1024)

    receivedData = client.recv(1024)
    receivedData = pickle.loads(receivedData)
    cipher = PKCS1_OAEP.new(prvtKey)
    receivedData = cipher.decrypt(receivedData)
    receivedData = receivedData.decode()
    newReceivedData = receivedData.encode()

    dataHash = SHA256.new(newReceivedData)
    hashedData = dataHash.hexdigest()
    encodedHash2 = hashedData.encode()

    if encodedHash == encodedHash2:
        print("The Signature is Verified and Valid!")
    else:
        print("The Signature is not Verified and Invalid")
    print("Alice:", receivedData)
    print(encodedHash2)

    #Exiting from the loop and terminating the connection when 'exit' keyword is given as input
    if receivedData == 'exit':
        break

client.close()

#Removal of the key after the conversation is finished
os.remove("srvr_pem_file.pem")
