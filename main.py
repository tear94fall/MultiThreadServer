import tcpServer
import executer
import queue
import datetime


print("tcp server :: start")

# make public queue
commandQueue = queue.Queue()

# init module
andRaspTCP = tcpServer.TCPServer(commandQueue, "127.0.0.1", 8888)
andRaspTCP.start()

# set module to executer
commandExecuter = executer.Executer(andRaspTCP)
while True:
    try:
        command = commandQueue.get()
        commandExecuter.startCommand(command)
    except:
        pass

# while True:
#    time.sleep(3)
#    andRaspTCP.sendAll("321\n")