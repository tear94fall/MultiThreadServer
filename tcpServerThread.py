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

                # self.commandQueue.put(data)
        except:
            self.connections.remove(self.connection)
            self.tcpServerThreads.remove(self)
            exit(0)

        self.connections.remove(self.connection)
        self.tcpServerThreads.remove(self)

    def request_binder(self, request_number: int):
        request_number = int(request_number)

        # 2번요청
        if request_number == 2:
            print("tcp server :: request :: start :: echo")
            self.send(self.Buffer)
            print("tcp server :: response :: end :: echo")

        # 4번요청
        elif request_number == 4:
            print("tcp server :: request :: start :: Container init")
            self.ContainerInit(self.Buffer)
            print("tcp server :: response :: end :: Container init")

        # 6번요청
        elif request_number == 6:
            print("tcp server :: request :: start :: Container delete")
            self.DeleteContainerTable(self.Buffer)
            print("tcp server :: response :: end :: Container delete")

        # 8번요청
        elif request_number == 8:
            print("tcp server :: request :: start :: Object Insert")
            self.InsertNewContent(self.Buffer)
            print("tcp server :: response :: end :: Object Insert")

        # 10번요청
        elif request_number == 10:
            print("tcp server :: request :: start :: Get All Object")
            self.GetContainerAllOject(self.Buffer)
            print("tcp server :: response :: end :: Get All Object")

        # 12번요청
        elif request_number == 12:
            print("tcp server :: request :: start :: Delete Object")
            self.DeleteContainerObject(self.Buffer)
            print("tcp server :: response :: end :: Delete Object")

    # 2번 요청
    def send(self, message):
        print('tcp server :: send to client : ', message)
        self.connection.send(str(message).encode())

        '''
        try:
            for i in range(len(self.connections)):
                self.connections[i].sendall(message.encode())
        except:
            pass
            '''

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

        response_data = {'current_conatiner_key': current_container_key, 'new_container_key': new_container_idx}
        self.connection.send(str(response_data).encode())

        insert_data = {}
        insert_data['idx'] = new_container_idx
        insert_data['container_key'] = current_container_key

        result = loop.run_until_complete(insert_new_container(loop, str(insert_data)))

        # 테이블 생성

        insert_data = {}
        insert_data['table_id'] = new_container_idx
        create_table = loop.run_until_complete(create_table_function(loop, str(insert_data)))

    # 6번 요청
    # 등록된 컨테이너를 파기 할때 사용함
    def DeleteContainerTable(self, data):
        data_dict = literal_eval(data)
        target_contrainer = data_dict['target_container']
        target_contrainer = str(target_contrainer)

        # 컨테이너 삭제 요청
        insert_data = {}
        insert_data['target_container'] = target_contrainer
        id_from_hash = loop.run_until_complete(find_id_from_hash(loop, str(insert_data)))
        id_from_hash = literal_eval(str(id_from_hash[0]))
        id_from_hash = id_from_hash['idx']

        insert_data = {}
        insert_data['target_container_name'] = id_from_hash
        drop_target_container_table = loop.run_until_complete(delete_target_container(loop, str(insert_data)))

        insert_data = {}
        insert_data['target_container_idx'] = id_from_hash
        drop_target_container_column = loop.run_until_complete(delete_target_container_column(loop, str(insert_data)))

        self.connection.send(target_contrainer.encode())

    # 8번 요청
    # 컨테이너에 물건을 실었을때 항목을 추가하는 함수
    def InsertNewContent(self, data):
        data_dict = literal_eval(data)
        cont_table_name = data_dict['cont_table_name']
        object_weight = data_dict['object_weight']

        # 컨테이너에 정보 삽입
        insert_data = {'table_name': cont_table_name, 'object_weight': object_weight}
        result = loop.run_until_complete(insert_new_object(loop, str(insert_data)))

        self.connection.send(result.encode())

    # 10 번 요청
    # 컨테이너 테이블에 있는 모든 데이터를 전송한다
    def GetContainerAllOject(self, data):
        data_dict = literal_eval(data)
        cont_table_name = data_dict['cont_table_name']

        # 컨테이너에 정보 삽입
        insert_data = {'table_name': cont_table_name}
        result = loop.run_until_complete(get_all_object(loop, str(insert_data)))
        result = str(result)

        self.connection.send(result.encode())

    # 12 번 요청
    # 컨테이너 테이블에 있는 적재 물건을 삭제하는 요청
    def DeleteContainerObject(self, data):
        data_dict = literal_eval(data)
        cont_table_name = data_dict['cont_table_name']
        del_target_object_id = data_dict['del_target_id']

        # 컨테이너에 정보 삽입
        delete_data = {'table_name': cont_table_name, 'del_target_id': del_target_object_id}
        result = loop.run_until_complete(del_target_object(loop, str(delete_data)))
        result = str(result)

        self.connection.send(result.encode())
