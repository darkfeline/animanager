import logging

logger = logging.getLogger(__name__)


class SceneStack:

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
