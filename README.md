# CNT5106C Socket Programming Assignment (Spring 2022)

## Simple File Server Application in Python 3 using Socket Programming

This repository contains the implementation of a simple File Server application in Python 3 using socket programming. The assignment required both the Client and Server processes to run on the same computer and be executed from different directories. The Server process's current directory contains various files, and the Client process interacts with the Server using TCP and UDP sockets.

### Assignment Overview

The assignment tasks include:

1. **Client-Server Connection**
   - The client process must correctly connect to the server using TCP sockets.

2. **Client Requests**
   - The client process should be able to send four types of requests to the server using TCP, and the server should correctly receive and respond to these requests.
   - Request types:
      - List all files in the server process' current directory.
      - Download one file from the server process' current directory by name using UDP.
      - Download all files from the server process' current directory using either TCP or UDP.
      - Graceful termination of the client and server applications.

3. **Implementation Details**
   - The server's port number is hardcoded in both the server and client code.
   - Different port numbers are used for TCP and UDP connections, both not less than 1024.
   - Correct resources (connections and sockets) should be closed at the correct time to prevent application hanging or crashing.

### Usage Instructions

1. **Run Server:**
   ```bash
   $ python3 server.py
   
2. **Run Client:**
   ```bash
   $ python3 client.py
   
3. **Client Requests:**

  To list all files:
  ```bash
  > listallfiles
  ```

  To download a specific file using UDP:
  ```bash
  > download <filename>
  ```

  To download all files using TCP or UDP:
  ```bash
  > download all
  ```

To gracefully exit:
  ```bash
  > exit
  ```
