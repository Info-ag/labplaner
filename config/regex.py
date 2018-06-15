'''
All regex-expressions used in the project at one place
    --> edit here
'''

class AGRegex(object):
    # name = r'^(?!^.{17})[A-Za-z0-9_-]$'
    name = r'^[A-Za-z0-9_-]{1,16}$'
    display_name = r'^(?!^.{49})([A-Za-z0-9]+([A-Za-z0-9_\s-]*[A-Za-z0-9]+)*)$'
    description = r'^([A-Za-z0-9]+([A-Za-z0-9_\s-]*[A-Za-z0-9]+)*){1,140}$'
class MessageRegex(object):
    subject = r'^(?!^.{49})([A-Za-z0-9]+([A-Za-z0-9_\s-]*[A-Za-z0-9]+)*)$'
    message = r'^([A-Za-z0-9]+([A-Za-z0-9_\s-]*[A-Za-z0-9]+)*){1,140}$'
