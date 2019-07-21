import asyncio
import socket
import threading
from time import sleep
from buffer import Buffer
from ast import literal_eval
import hashlib

from mysql_connector import *

loop = asyncio.get_event_loop()


class TCPServerThread(threading.Thread):
    def __init__(self, command_queue, tcp_server_threads, connections, connection, client_address):
        threading.Thread.__init__(self)

        self.commandQueue = command_queue
        self.tcpServerThreads = tcp_server_threads
        self.connections = connections
        self.connection = connection
        self.clientAddress = client_address
        self.Buffer = None

    def run(self):
        try:
            while True:
                data = self.connection.recv(1024).decode()

                self.Buffer = data
                dictionary = literal_eval(data)

                request_number = int(dictionary['cmd_number'])

                # when break connection
                if not data:
                    print('tcp server :: exit :', self.clientAddress)
                    break
                print('tcp server :: recv from client :', data)

                self.request_binder(request_number)

                #self.commandQueue.put(data)
        except:
            self.connections.remove(self.connection)
            self.tcpServerThreads.remove(self)
            exit(0)

        self.connections.remove(self.connection)
        self.tcpServerThreads.remove(self)

    def request_binder(self, request_number: int):
        request_number = int(request_number)
        if request_number == 2:
            self.send(self.Buffer)

        elif request_number == 4:
            self.ContainerInit(self.Buffer)

        elif request_number == 6:
            self.DeleteContainerTable(self.Buffer)

        elif request_number == 8:
            pass

        elif request_number == 10:
            pass

        elif request_number == 12:
            pass

    # 2번 요청
    def send(self, message):
        print('tcp server :: send to client : ', message)
        try:
            for i in range(len(self.connections)):
                self.connections[i].sendall(message.encode())
        except:
            pass

    # 4번 요청
    # 컨테이너 초기화 진행
    def ContainerInit(self, data):
        result = loop.run_until_complete(get_last_container_idx(loop))
        result = result[0]
        last_containter_idx = result['max(idx)']
        if last_containter_idx is None:
            last_containter_idx = 0

        last_containter_idx = int(last_containter_idx)
        new_container_idx = last_containter_idx + 1
        new_container_idx = str(new_container_idx)

        encode_new_container_idx = new_container_idx.encode()
        sha256 = hashlib.new('sha256')
        sha256.update(encode_new_container_idx)

        current_container_key = sha256.hexdigest()

        self.connection.send(current_container_key.encode())

        insert_data = {}
        insert_data['idx'] = new_container_idx
        insert_data['container_key'] = current_container_key

        result = loop.run_until_complete(insert_new_container(loop, str(insert_data)))

        # 테이블 생성

        insert_data ={}
        insert_data['table_id'] = new_container_idx
        create_table = loop.run_until_complete(create_table_function(loop, str(insert_data)))

    # 6번 요청
    # 등록된 컨테이너를 파기 할때 사용함
    def DeleteContainerTable(self, data):
        data_dict = literal_eval(data)
        target_contrainer = data_dict['target_container']
        target_contrainer = str(target_contrainer)

        # 컨테이너 삭제 요청
        insert_data ={}
        insert_data['target_container'] = target_contrainer
        id_from_hash = loop.run_until_complete(find_id_from_hash(loop, str(insert_data)))
        id_from_hash = literal_eval(str(id_from_hash[0]))
        id_from_hash = id_from_hash['idx']

        insert_data ={}
        insert_data['target_container_name'] = id_from_hash
        drop_target_container_table = loop.run_until_complete(delete_target_container(loop, str(insert_data)))

        insert_data ={}
        insert_data['target_container_idx'] = id_from_hash
        drop_target_container_column = loop.run_until_complete(delete_target_container_column(loop, str(insert_data)))

        self.connection.send(target_contrainer.encode())