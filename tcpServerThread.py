import socket
import threading
from time import sleep


class TCPServerThread(threading.Thread):
    def __init__(self, command_queue, tcp_server_threads, connections, connection, client_address):
        threading.Thread.__init__(self)

        self.commandQueue = command_queue
        self.tcpServerThreads = tcp_server_threads
        self.connections = connections
        self.connection = connection
        self.clientAddress = client_address

    def run(self):
        try:
            while True:
                data = self.connection.recv(1024).decode()

                # when break connection
                if not data:
                    print('tcp server :: exit :', self.connection)
                    break
                print('tcp server :: client :', data)

                # 받은 데이터만 다시 보내는 경우
                self.send(data)

                self.commandQueue.put(data)
        except:
            self.connections.remove(self.connection)
            self.tcpServerThreads.remove(self)
            exit(0)

        self.connections.remove(self.connection)
        self.tcpServerThreads.remove(self)

    def send(self, message):
        print('tcp server :: server ', message)
        try:
            for i in range(len(self.connections)):
                self.connections[i].sendall(message.encode())
        except:
            pass
