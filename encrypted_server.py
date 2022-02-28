from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
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
    with open('prvt_pem_file.pem',"wb") as prvt:
        prvt.write(prvtPemFile)
    with open('pub_pem_file.pem',"wb") as pub:
        pub.write(pubPemFile)
with open('prvt_pem_file.pem', 'rb') as prvt:
    prvtPemFile = prvt.read()
with open('pub_pem_file.pem', 'rb') as pub:
    pubPemFile = pub.read()
prvtKey = RSA.importKey(prvtPemFile)
pubKey = RSA.importKey(pubPemFile)

#Creating the Socket and verifying the Connection establishment
server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(('', 10000))
server.listen(5)
print ("Server Socket is listening")

#Initiating a loop for the period the socket connection is active
while True:
    (port,addr) = server.accept()
    receivedMessage=port.recv(1024).decode()
    port.send(pubPemFile)
    clntKey = port.recv(1024)
    with open('clnt_pem_file.pem', 'wb') as clnt:
        clnt.write(clntKey)
    client_key= RSA.importKey(clntKey)
    while True:
        aliceHash = port.recv(1024)
        receivedData = port.recv(1024)
        pickleReceivedData = pickle.loads(receivedData)
        cipher = PKCS1_OAEP.new(prvtKey)
        cipherReceivedData = cipher.decrypt(pickleReceivedData)
        receivedData = cipherReceivedData.decode()
        
        receivedData2 = receivedData.encode() 
        bobHash = SHA256.new(receivedData2)
        hashedBob = bobHash.hexdigest()
        hashedBobEncoded = hashedBob.encode()

        if aliceHash == hashedBobEncoded:
            print("The Signature is Verified and Valid!")
        else:
            print("The Signature is not Verified and Invalid")

        print('Bob:', receivedData)
        print(hashedBobEncoded)
        
	#Exiting from the loop and terminating the connection when 'exit' keyword is given as input
        if receivedData == 'exit':
            break
        print('Alice:')

        dataToSend = sys.stdin.readline().strip()
        dataToSendEncoded = dataToSend.encode()
        if dataToSend == 'exit':
            dataToSend = dataToSend.encode()
            cipher = PKCS1_OAEP.new(client_key)
            dataToSend = cipher.encrypt(dataToSend)
            dataToSend = pickle.dumps(dataToSend)
            port.send(dataToSend)
            break

        hashedDataToSend = SHA256.new(dataToSendEncoded)
        hashedAlice = hashedDataToSend.hexdigest()
        hashedAliceEncoded = hashedAlice.encode()
        port.send(hashedAliceEncoded)
        
        dataToSend = dataToSend.encode()
        cipher = PKCS1_OAEP.new(client_key)
        dataToSend = cipher.encrypt(dataToSend)
        dataToSend = pickle.dumps(dataToSend)
        port.send(dataToSend)

    break

port.close()

#Removal of the key after the conversation is finished
os.remove("clnt_pem_file.pem")
