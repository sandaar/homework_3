import json

import requests
import vk
import argparse
from selenium import webdriver

import config


class VkApp(object):
    def __init__(self, firefox=None):
        self.base_url = 'https://api.vk.com/method/'
        if not firefox:
            self.access_token = config.ACCESS_TOKEN
        else:
            self.email = config.EMAIL
            self.password = config.PASSWORD
            self.client_id = config.CLIENT_ID
            self.client_secret = config.CLIENT_SECRET
            self.scope = config.SCOPE
            self.access_token = self.authorize()

    def authorize(self):
        driver = webdriver.Firefox()

        url = 'https://oauth.vk.com/authorize?client_id=%s&' \
            'redirect_uri=https://oauth.vk.com/blank.html&' \
            'response_type=token&scope=%s' % (self.client_id, self.scope)

        driver.get(url)
        user_input = driver.find_element_by_name('email')
        user_input.send_keys(self.email)
        password_input = driver.find_element_by_name('pass')
        password_input.send_keys(self.password)

        submit = driver.find_element_by_id('install_allow')
        submit.click()

        current = driver.current_url
        access_list = (current.split("#"))[1].split("&")
        access_token = (access_list[0].split("="))[1]
        expires_in = (access_list[1].split("="))[1]

        driver.close()
        return access_token

    def get_user_id(self, user_id_or_nickname):
        if not user_id_or_nickname.isdigit():
            response = self.get_users(user_id_or_nickname)
            user_id = response[0]['uid']
        else:
            user_id = user_id_or_nickname
        return int(user_id)

    def get_audios(self, user_id_or_nickname):
        method_name = 'audio.get'
        user_id = self.get_user_id(user_id_or_nickname)
        payload = {
            'owner_id': user_id,
            'access_token': self.access_token
        }
        url = "%s%s" % (self.base_url, method_name)
        r = requests.get(url, params=payload)
        response_dict = r.json()
        if 'error' in response_dict:
            error = response_dict['error']
            print "Couldn't get audios.\nError code: %s\nError message: %s" %\
                (error['error_code'], error['error_msg'])
            return None
        audios_response = response_dict['response']
        return audios_response

    def get_audios_list(self, user_id_or_nickname):
        audios_response = self.get_audios(user_id_or_nickname)
        if audios_response:
            audios = audios_response[1:]
            return audios
        return None

    def get_audios_count(self, user_id_or_nickname):
        audios_response = self.get_audios(user_id_or_nickname)
        if audios_response:
            audios_count = audios_response[0]
            return audios_count
        return None

    def print_audios(self, user_id_or_nickname):
        user = self.get_users(user_id_or_nickname)
        user_id = self.get_user_id(user_id_or_nickname)
        print "\n\nUID: %s" % user_id
        print "First name: %s" % user[0]["first_name"]
        print "Last name: %s\n" % user[0]["last_name"]
        audios = self.get_audios_list(user_id_or_nickname)
        if audios:
            print "Total: %s" % len(audios)
            for audio in audios:
                print "%s - %s" % (audio['artist'], audio['title'])
        else:
            print None

    def get_friends(self, user_id_or_nickname):
        method_name = 'friends.get'
        user_id = self.get_user_id(user_id_or_nickname)
        payload = {'user_id': user_id}
        url = "%s%s" % (self.base_url, method_name)
        r = requests.get(url, params=payload)
        response_text = r.json()
        friends = response_text['response']
        return friends

    def get_friends_extended(self, user_id_or_nickname):
        friends = self.get_friends(user_id_or_nickname)
        friends_extended = []
        for friend in friends:
            a_count = self.get_audios_count(str(friend))
            url = "https://vk.com/id%s" % friend
            friends_extended.append((friend, a_count, url))
        return friends_extended

    def get_users(self, user_ids):
        method_name = 'users.get'
        payload = {'user_ids': user_ids, 'fields': 'counters'}
        url = "%s%s" % (self.base_url, method_name)
        r = requests.get(url, params=payload)
        response_text = r.json()
        users = response_text['response']
        return users

    def print_sorted_friends(self, user_id_or_nickname):
        friends = self.get_friends_extended(user_id_or_nickname)
        friends_sorted = sorted(friends, key=lambda f: f[1])
        for friend in friends_sorted:
            print "uid: %s, audios count: %s, url:%s" % friend
        print "Retrieved info about %s friends of %s" % \
            (len(friends), user_id_or_nickname)


def parse_args():
    parser = argparse.ArgumentParser(description='Get vk audios')
    parser.add_argument('--user_id', help='vk user id', required=True)
    parser.add_argument('--firefox', help='use firefox to authorize')
    args = vars(parser.parse_args())
    return args

if __name__ == '__main__':
    args = parse_args()
    user_id = args['user_id']
    firefox = args['firefox']
    vk_app = VkApp(firefox)
    print vk_app.get_audios(user_id)
    vk_app.print_audios(user_id)
    vk_app.print_sorted_friends(user_id)
