def dir_to_angle(direction):
    dirs = {
    None:None,
    "right" : 0,
    "down": 90,
    "left" : 180,
    "up": 270
    }
    return dirs[direction]

def add_in_range(a, b, down, up):
    result = a+b
    if result > up:
        result = up
    if result < down:
        result = down
    return result
