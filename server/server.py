import socket
import time
import os

def getAllFiles(type):
    fileList = os.listdir(path='./server/')
    fileListString = fileList[0]
    for i in range(1, len(fileList)):
        if fileList[i] != "server.py":
            fileListString = fileListString + " " + fileList[i]
    if type == "str":
        return fileListString
    elif type == "list":
        return fileList

def checkFile(fileName):
    fileList = getAllFiles("list")
    for f in fileList:
        if f == fileName:
            return fileName
    
    return "invalid"
        

def createConnectionTCP(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    return conn,s

def createConnectionUDP(PORT):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = "ready UDP"
    server = ("127.0.0.1", PORT)
    serverSocket.sendto(msg.encode(), server)
    return serverSocket, server[0]

def sendFile(msg, s, conn):
    add = ("127.0.0.1", 12345)
    with  open("./server/"+ msg, 'rb') as f:
                        data = f.read(1024)
                        while(data):
                            s.sendto(data, add)
                            data = f.read(1024)
    s.close()


def sendAllFiles(conn):
    S = "----------------"
    fileList = getAllFiles("list")
    conn.send(str(len(fileList)).encode())
    msg = conn.recv(1024).decode()
    if msg == "received number of files":
        for fName in fileList:
            time.sleep(0.5)
            filesize = os.path.getsize("./server/"+fName)
            conn.send(f"{fName}{S}{filesize}".encode())
            while True:
                resp = conn.recv(1024)
                if resp.decode() == "READY TO RECEIVE":
                    with  open("./server/"+fName, 'rb') as f:
                        data = f.read(1024)
                        while(data):
                            conn.send(data)
                            data = f.read(1024)
                    break


def main():
    conn,s = createConnectionTCP("127.0.0.1" , 65432)
    flag = True
    while flag:
        if not conn:
            conn = createConnectionTCP("127.0.0.1", 65432)
        data = conn.recv(1024)
        if data == bytes('listallfiles', 'utf-8'):
            conn.send(os.fsencode(getAllFiles("str")))
        elif data == bytes('download all', 'utf-8'):
            sendAllFiles(conn)
        elif data == bytes('exit', 'utf-8'):
            s.close()
            conn.sendall(bytes('exit', 'utf-8'))
            flag = False
            break
        else:
            cmd = data[9:].decode()
            msg = checkFile(cmd)
            if msg != "invalid":
                c, add = createConnectionUDP(12345)
                time.sleep(1)
                sendFile(msg, c, conn)
            else:
                conn.sendall(bytes(msg, 'utf-8'))


if __name__ == "__main__":
    main()