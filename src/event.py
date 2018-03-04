class Event(object):
    def __init__(self):
        self.__timetable = ""
        self.__datetime = ""
        self.__selected_by = []

    def get_timetable(self):
        return self.__timetable

    def get_selected_by(self):
        return self.__selected_by

    def get_selected(self, user):
        self.__selected_by.append(user)
        self.save()

    def deselect(self, user):
        self.__selected_by.remove(user)
        self.save()

    def save(self):
        # TODO: Database access
        pass

    @staticmethod
    def load():
        # TODO: Database access
        pass
