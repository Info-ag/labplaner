class Event(object):
    def __init__(self):
        self.timetable = ""
        self.datetime = ""
        self.__selected_by = []

    def save(self):
        # TODO: Database access
        pass

    @staticmethod
    def load():
        # TODO: Database access
        pass
