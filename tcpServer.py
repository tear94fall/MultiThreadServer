import socket, threading
import tcpServerThread


class TCPServer(threading.Thread):
    def __init__(self, command_queue, host, port):
        threading.Thread.__init__(self)

        self.commandQueue = command_queue
        self.HOST = host
        self.PORT = port

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.HOST, self.PORT))
        self.serverSocket.listen(1)

        self.connections = []
        self.tcpServerThreads = []

    def run(self):
        try:
            while True:
                print('tcp server :: server wait...')
                connection, client_address = self.serverSocket.accept()
                self.connections.append(connection)
                print("tcp server :: connect :", client_address)

                sub_thread = tcpServerThread.TCPServerThread(self.commandQueue, self.tcpServerThreads,
                                                            self.connections, connection, client_address)

                sub_thread.start()
                self.tcpServerThreads.append(sub_thread)
        except:
            print("tcp server :: serverThread error")

    def sendAll(self, message):
        try:
            self.tcpServerThreads[0].send(message)
        except:
            pass