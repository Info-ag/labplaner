class ag_regex(object):
    #name = r'^(?!^.{17})[A-Za-z0-9_-]$'
    name = r'^[A-Za-z0-9_-]{1,16}$'
    display_name = r'^(?!^.{49})([A-Za-z0-9]+([A-Za-z0-9_\s-]*[A-Za-z0-9]+)*)$'
    description = r'^(?!^.{141})([A-Za-z0-9]+([A-Za-z0-9_\s-]*[A-Za-z0-9]+)*)$'