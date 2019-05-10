class Executer:
    def __init__(self, tcp_server):
        self.andRaspTCP = tcp_server

    def startCommand(self, command):
        if command == "123":
            self.andRaspTCP.sendAll("321")