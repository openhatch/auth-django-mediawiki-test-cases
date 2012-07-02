#!/usr/bin/python
import unittest2
import mechanize

import ConfigParser

config = ConfigParser.SafeConfigParser()
config.read('config.ini')

class LoginGenerallyWorks(unittest2.TestCase):
    def test_login(self):
        # First, log in
        b = mechanize.Browser()
        b.open('https://openhatch.org/account/login/old')
        b.select_form(nr=0)
        username = config.get('login', 'username')
        b['username'] = username
        b['password'] = config.get('login', 'password')
        b.submit()
        # Then, go visit the front page and ensure the username appears
        response = b.open('https://openhatch.org/')
        data = response.read()
        self.assertTrue(username in data)

if __name__ == '__main__':
    unittest2.main()

