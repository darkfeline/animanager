#!/usr/bin/env python3

import sys


class ServiceLocator:

    def __init__(self):
        self.db = None

sys.modules[__name__] = ServiceLocator()
