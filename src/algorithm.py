# Check for intersection between two events with start and end Datetime
def intersects(start_a, end_a, start_b, end_b):
    if start_a < start_b:
        start = end_a
        end = start_b
    else:
        start = end_b
        end = start_a

    if end < start:
        return True
    else:
        return False

# Check for intersection between multiple events
def intersects_multiple(events):
    for event_a in events:
        events.remove(event_a)
        for event_b in events:
            if intersects(event_a[0], event_a[1], event_b[0], event_b[1]):
                return True

    return False

