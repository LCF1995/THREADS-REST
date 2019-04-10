import requests
import json
import socket
import select
import multiprocessing
from os.path import join
import time

#Lista de processos
jobs = []
 
class SocketServer:
    """ Simple socket server that listens to one single client. """
 
    def __init__(self, host = '192.168.43.229', port = 2010):
        """ Initialize the server with a host and port to listen to. """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.sock.bind((host, port))
        self.sock.listen(10)
 
    def close(self):
        """ Close the server socket. """
        print('Closing server socket (host {}, port {})'.format(self.host, self.port))
        if self.sock:
            self.sock.close()
            self.sock = None
 
    def run_server(self):
        """ Accept and handle an incoming connection. """
        print('Starting socket server (host {}, port {})'.format(self.host, self.port))
 
        client_sock, client_addr = self.sock.accept()
 
        print('Client {} connected'.format(client_addr))
 
        stop = False
        while not stop:
            if client_sock:
                # Check if the client is still connected and if data is available:
                try:
                    rdy_read, rdy_write, sock_err = select.select([client_sock,], [], [])
                except select.error:
                    print('Select() failed on socket with {}'.format(client_addr))
                    return 1
 
                if len(rdy_read) > 0:
                    read_data = client_sock.recv(255)
                    # Check if socket has been closed
                    if len(read_data) == 0:
                        print('{} closed the socket.'.format(client_addr))
                        stop = True
                    else:
                        print('>>> Received: {}'.format(read_data.rstrip()))

                        jobs.append(multiprocessing.Process(target=myThread, args=['upper', read_data.rstrip(), client_sock, '192.168.43.55', '5009']))
                        jobs.append(multiprocessing.Process(target=myThread, args=['concate', read_data.rstrip(), client_sock, '192.168.43.35', '5001']))
                        
                        jobsTmp = jobs
                        for j in jobsTmp:
                                j.start()

                        #finalizar
                        for j in jobsTmp:
                                j.join()
                            
            else:
                print("No client is connected, SocketServer can't receive data")
                stop = True
 
        # Close socket
        print('Closing connection with {}'.format(client_addr))
        client_sock.close()
        return 0

def myThread(type, text, client_sock, server, port):
    data = requests.post('http://'+server+':'+port, json={"text": text, "type" : type})
    data_json = data.json()
    client_sock.send(json.dumps(data_json)+"\n")
    
 
def main():
    server = SocketServer()
    server.run_server()
    print 'Exiting'
 
if __name__ == "__main__":
    main()

