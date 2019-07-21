
class Buffer:
    def __init__(self):
        self.data = None

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data


class Dict_Buffer:
    def __init__(self):
        self.message = {}

    def insert_data(self, column,data):
        self.message[str(column)] = data

    def del_data(self, column):
        del self.message[column]

    def get_single_data(self, column):
        temp = {}
        try:
            temp[column] = (self.message[str(column)])
            return temp
        except Exception as err:
            print("Error occured. does not exist column name %s" % column)
            return None

    def get_all_data(self):
        if len(self.message) == 0:
            print("Error occured. buffer is empty")
        else:
            return self.message
