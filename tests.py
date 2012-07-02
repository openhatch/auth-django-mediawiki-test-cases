#!/usr/bin/python
import unittest2

import ConfigParser

config = ConfigParser.SafeConfigParser().read('config.ini')

class LoginGenerallyWorks(unittest2.TestCase):
    def test(self):
        pass

if __name__ == '__main__':
    unittest2.main()

