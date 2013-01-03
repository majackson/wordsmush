
def loop_input(message):
    """Repeats input until user inputs valid data"""
    user_input = ''
    while not user_input.strip():
        user_input = raw_input('%s: ' % message)

    return user_input

