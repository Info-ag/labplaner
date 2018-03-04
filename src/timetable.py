class Timetable(object):
    def __init__(self):
        self.__ag = ""
        self.events = []

    def create_event(self):
        new_event = ""  # TODO: Database access
        self.events.append(new_event)
        self.save()

    def save(self):
        # TODO: Database access
        pass

    @staticmethod
    def load():
        # TODO: Database access
        pass
