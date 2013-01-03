import logging

logger = logging.getLogger(__name__)


class SceneStack:

    """
    Essentially a state machine that loops over the current state.

    States are called scenes.  Scenes are tuples with length three.  The first
    item is the function that is called, and the second and third are
    positional arguments and keyword arguments, respectively.

    SceneStack also has slices. You can add a new slice by using `push()`
    instead of `add()` when adding a scene.  Scene functions can have special
    return values.  Returning `-1` will pop itself off of the stack.  Returning
    `-2` will pop the top slice off of the stack.  If the top slice is empty
    after popping a single scene (returning `-1`), it will also be popped.

    """

    def __init__(self):
        self.stack = []

    @property
    def top(self):
        try:
            return self.stack[-1][-1]
        except IndexError:
            return None

    def run(self):
        """Run until stack is empty"""
        while self.stack:
            self.step()

    def step(self):
        """
        Run the top scene once
        If scene returns -1, pop itself
        If scene returns -2, pop a slice

        """
        logger.debug('stack: %s', self.stack)
        try:
            func, args, kwargs = self.top
        except TypeError:
            return
        rv = func(*args, **kwargs)
        if rv == -1:
            self.pop()
        elif rv == -2:
            self.pop_slice()
        print()

    def add(self, scene):
        if not self.stack:
            self.stack.append([])
        self.stack[-1].append(scene)

    def push(self, scene):
        if self.stack:
            self.stack.append([])
        self.add(scene)

    def pop(self):
        self.stack[-1].pop()
        if not self.stack[-1]:
            self.stack.pop()

    def pop_slice(self):
        self.stack.pop()
