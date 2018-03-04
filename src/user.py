from hashlib import sha256

class User(object):

    def __init__(self, name):
        data = self.__load(name)

        self.__username = name
        self.__hashed_password = data["password"]
        self.__id = data[""]
        self.__uuid = data["userid"]
        self.__events = []
        self.__mentor_of = []
        self.__ag = []

    # Move to Database class #####################################
    def add(self, data, name, password):
        password = password.encode('UTF-8')
        rawid = 0
        for value in self.data:
            if int(self.data[value]['id']) > rawid:
                rawid = int(self.data[value]['id']) +1
        userid = sha256(bytes(name + str(rawid), 'UTF-8')).hexdigest()

        data[name] = {'password': password, 'id': str(rawid), 'userid':userid}
        return data

    def remove(self, data, userid):
        for user in self.data:
            if self.data[user]['userid'] == userid:
                self.data[user] = None
    ###############################################################

    def select_event(self, event):
        self.__events.append(event)
        event.get_selected(self)
        self.save()

    def save(self):
        # TODO: Database access
        pass

    @staticmethod
    def __load(username):
        # TODO: Database access
        pass
