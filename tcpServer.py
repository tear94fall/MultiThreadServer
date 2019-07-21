import asyncio
import socket
import threading
import tcpServerThread

from mysql_connector import test_example


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

        self.loop = asyncio.get_event_loop()

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

    # 연결된 클라이언트 모두에게 전송하는 기능 (되도록 사용 자제)
    def sendAll(self, message):
        try:
            self.tcpServerThreads[0].send(message)
        except:
            pass