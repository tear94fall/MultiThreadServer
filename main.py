import tcpServer
import executer
import queue
import datetime


print("tcp server :: start")

# make public queue
commandQueue = queue.Queue()

server_ip = "0.0.0.0"
server_port = 8888

# init module
# 아이피를 0.0.0.0 으로 바꿈
andRaspTCP = tcpServer.TCPServer(commandQueue, server_ip, server_port)
andRaspTCP.start()

# set module to executer
'''
commandExecuter = executer.Executer(andRaspTCP)
while True:
    try:
        command = commandQueue.get()
        commandExecuter.startCommand(command)
    except:
        pass
'''

# 모든 클라이언트에게 데이터 전송
# while True:
#    time.sleep(3)
#    andRaspTCP.sendAll("321\n")