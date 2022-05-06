
import socket
import os

def createConnectionTCP(serverName, serverPort):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    return clientSocket

def createConnectionUDP(serverPort):
    # print("inside create UDP")
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.bind(("127.0.0.1", serverPort))
    msg = "hello"
    bytesAddressPair = clientSocket.recvfrom(1024)
    # print("address received")
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)   
    # print(clientMsg)
    # print(clientIP)
    # print("msg sent")
    #Hritik Baweja
    return clientSocket

def receiveAllFiles(conn):
    S = "----------------"
    i = 0
    # print("Receiving all files")
    numOfFiles = conn.recv(1024).decode()
    # print("number of files ", numOfFiles)
    msg = "received number of files"
    conn.send(msg.encode())
    fileList = []
    while(len(fileList) < int(numOfFiles)):
        i = 0
        # print(len(fileList))
        received = conn.recv(1024).decode()
        fName, fSize = received.split(S)
        fSize = int(fSize)
        if fName not in fileList: 
            fileList.append(fName)
        # print("receiving fName", fName, fSize)
        with open(fName, "wb") as f:
            # print("file opened")
            conn.send("READY TO RECEIVE".encode())
            while True:
                content = conn.recv(1024)
                contentSize = len(content)
                # print(content.decode())
                if fSize>0:
                    # print("writing chunks", contentSize)
                    if fSize-contentSize>0:
                        fSize-=contentSize
                        f.write(content)
                    else:
                        f.write(content[:fSize])
                        fSize-=contentSize
                        break
                else:
                    print("BREAKING")
                    break
    print("Downloaded all files")

def receiveFile(s, conn, fName):
    # print("inside receive file")
    f = open(fName, "wb")
    # print("file opened")
    data,addr = s.recvfrom(1024)
    try:
        while(data):
            f.write(data)
            s.settimeout(2)
            data,addr = s.recvfrom(1024)
    except socket.timeout:
        f.close()
        s.close()
        print("Downloaded", fName)

def main():
    clientSocket = createConnectionTCP("127.0.0.1", 65432)
    flag = True
    while flag:
        sentence = input()
        clientSocket.send(sentence.encode())
        if sentence == "exit":
            flag = False
        elif sentence == "download all":
            receiveAllFiles(clientSocket)
        elif sentence == "listallfiles":
            data = clientSocket.recv(1024)
            print(data.decode())
        else:
            # print("inside else")
            data = sentence[9:]
            # print(data)
            if data == "invalid":
                print(data + " file")
            else: 
                # print("inside else create")
                c = createConnectionUDP(12345)
                receiveFile(c, clientSocket, data)
    clientSocket.close()


if __name__ == "__main__":
    main()
