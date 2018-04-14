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
