def get_choice(choices):
    """Prompt for user to pick a choice.

    Args:
        choices: A list of choices, with each value indexable with length at
        least two.

    Returns:
        An int index of the given choice: choices[i].

    Raises:
        Cancel: User cancelled selection

    """
    for i, name in enumerate(choices):
        print("{} - {}: {}".format(i, name[0], name[1]))
    try:
        i = int(input("Pick one\n"))
    except ValueError:
        i = -1
    confirm = input("{}: {}\nOkay? [Y/n]".format(
        choices[i][0], choices[i][1]))
    if confirm.lower() in ('n', 'no'):
        raise Cancel
    return i


class Cancel(Exception):
    pass
