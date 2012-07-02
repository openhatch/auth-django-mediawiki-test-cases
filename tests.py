#!/usr/bin/python
import unittest2
import mechanize

import ConfigParser

config = ConfigParser.SafeConfigParser()
config.read('config.ini')

### Nab cookies:
### b._ua_handlers['_cookies'].cookiejar

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
        self.assertTrue('zomg_oh_wiki__session' in get_cookie_names(b))
        self.assertTrue('sessionid' in get_cookie_names(b))
        # Click the logout link
        b.open('https://openhatch.org/wiki/Special:UserLogout').read()
        # Logging out should:
        # - remove the Django-created sessionid cookie, and the wiki-specific
        #   session cookie
        b.open('https://openhatch.org/w/extensions/AuthDjango/destroy_session.php').read()
        self.assertFalse('sessionid' in get_cookie_names(b))
        #self.assertFalse('zomg_oh_wiki__session' in get_cookie_names(b))

        # Assert that the user is encouraged to log in
        data = b.open('https://openhatch.org/wiki/').read()
        ### Verify that just visiting the wiki does not cause you to get
        ### a wiki session ID cookie.
        #self.assertFalse('zomg_oh_wiki__session' in get_cookie_names(b))
        self.assertFalse('The user page for the IP address you are editing as'
                         in data)
        self.assertTrue('/w/index.php?title=Special:UserLogin' in data)

def get_cookies(b):
    cookies = b._ua_handlers['_cookies'].cookiejar
    cookies_we_care_about = cookies._cookies['.openhatch.org']['/']
    cookies_we_care_about.update(
        cookies._cookies['openhatch.org']['/'])
    return cookies_we_care_about
#    cookie_names = cookies_we_care_about.keys()
#    return cookie_names

def get_cookie_names(b):
    cookies = get_cookies(b)
    return cookies.keys()

if __name__ == '__main__':
    unittest2.main()

