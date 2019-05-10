class Executer:
    def __init__(self, tcp_server):
        self.andRaspTCP = tcp_server

    def startCommand(self, command):
        if command == "@@@@@":
            self.andRaspTCP.sendAll("321")