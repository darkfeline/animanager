def get_choice(choices, default=-1):
    """Prompt for user to pick a choice.

    Args:
        choices: A list of choices

    Returns:
        An int index of the given choice: choices[i].

    """
    for i, name in enumerate(choices):
        print("{}: {}".format(i, name))
    try:
        i = int(input("Pick one\n"))
    except ValueError:
        i = default
    return i
