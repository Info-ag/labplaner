#pylint: disable-all

class User(object):

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
