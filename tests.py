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
        return b

    def test_wiki_username_follows(self):
        # First, log into the OpenHatch site
        b = self.test_login()
        username = config.get('login', 'username')
        # Now, visit the wiki. Does our username show up
        # in the top-right?
        response = b.open('https://openhatch.org/wiki/')
        username_with_first_letter_cap = (username[0].upper() +
                                          username[1:])
        wiki_userpage_url = ('/wiki/User:' +
                       username_with_first_letter_cap)
        data = response.read()
        self.assertTrue(wiki_userpage_url in data)

        ### whereas, with a clean browser, we don't see that
        clean_b = mechanize.Browser()
        clean_response = clean_b.open('https://openhatch.org/wiki/')
        clean_data = clean_response.read()
        self.assertFalse(wiki_userpage_url in clean_data)
        self.assertTrue('/w/index.php?title=Special:UserLogin' in clean_data)

        ## Return the browser for downstream use
        return b

    def test_wiki_logout_shows_login_link(self):
        b = self.test_wiki_username_follows()
        # Click the logout link
        b.open('https://openhatch.org/wiki/Special:UserLogout').read()
        # Assert that the user is encouraged to log in
        data = b.open('https://openhatch.org/wiki/').read()
        self.assertFalse('The user page for the IP address you are editing as'
                         in data)
        self.assertTrue('/w/index.php?title=Special:UserLogin' in data)

if __name__ == '__main__':
    unittest2.main()

