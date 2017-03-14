#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#Autor: Antoine "0x010C" Lamielle
#Date: 18 March 2016
#License: GNU GPL v3

import sys
import os
import time
import json
import requests


NS_MAIN = 0
NS_TALK = 1
NS_USER = 2
NS_USER_TALK = 3
NS_WIKIPEDIA = 4
NS_WIKIPEDIA_TALK = 5
NS_FILE = 6
NS_FILE = 7
NS_MEDIAWIKI = 8
NS_MEDIAWIKI_TALK = 9
NS_TEMPLATE = 10
NS_TEMPLATE_TALK = 11
NS_HELP = 12
NS_HELP_TALK = 13
NS_CATEGORY = 14
NS_CATEGORY_TALK = 15
NS_PORTAL = 100
NS_PORTAL_TALK = 101
NS_PROJECT = 102
NS_PROJECT_TALK = 103
NS_REFERENCE = 104
NS_REFERENCE_TALK = 105
NS_MODULE = 828
NS_MODULE_TALK = 829

class Pywiki:

    def __init__(self, config_name):
        user_path = os.path.dirname(os.path.realpath(__file__)) + "/users/"
        if not os.path.exists(user_path):
            os.makedirs(user_path)
        if(os.path.isfile(user_path+config_name+".py") == False):
            print "The user configuration file called '"+config_name+"' seems missing. Don't worry, we will create it yet :\n"
            print "user:"
            print "> ",;user = sys.stdin.readline().split("\n")[0]
            print "password:"
            print "> ",;password = sys.stdin.readline().split("\n")[0]
            print "assertion ('user' or 'bot'):"
            print "> ",;assertion = sys.stdin.readline().split("\n")[0]
            print "api endpoint (ex. 'https://en.wikipedia.org/w/api.php'):"
            print "> ",;api_endpoint = sys.stdin.readline().split("\n")[0]
            file = open("users/"+config_name+".py", "w")
            file.write("# -*- coding: utf-8  -*-\nuser = u'"+user+"'\npassword = u'"+password+"'\nassertion = u'"+assertion+"'\napi_endpoint = u'"+api_endpoint+"'")
            file.close()
        sys.path.append(user_path)
        config = __import__(config_name, globals(), locals(), [], -1)
        
        self.user = config.user
        self.password = config.password
        self.api_endpoint = config.api_endpoint
        self.assertion = config.assertion
        if self.assertion == "bot":
            self.limit = 5000
        else:
            self.limit = 500
        
        self.session = requests.Session()

    """
    Perform a given request with a simple but usefull error managment
    """
    def request(self, data, files=None):        
        relogin = 3
        while relogin:
            try:
                if files == None:
                    r = self.session.post(self.api_endpoint, data=data)
                else:
                    r = self.session.post(self.api_endpoint, data=data, files=files)
                response = json.loads(r.text)
                if response.has_key("error"):
                    if response['error']['code'] == 'assertuserfailed':
                        self.login()
                        relogin -= 1
                        continue
                    break
                return response
            except requests.exceptions.ConnectionError,OpenSSL.SSL.ZeroReturnError:
                time.sleep(5)
                self.session = requests.Session()
                self.login()
                relogin -= 1
        raise Exception('API error', response['error'])


    """
    Login into the wiki
    """
    def login(self):
        r = self.session.post(self.api_endpoint, data={
            "action":"login",
            "lgname":self.user,
            "lgpassword":self.password,
            "format":"json"
        })
        token = json.loads(r.text)["login"]["token"];
        r = self.session.post(self.api_endpoint, data={
            "action":"login",
            "lgname":self.user,
            "lgpassword":self.password,
            "lgtoken":token,
            "format":"json"
        })
        if json.loads(r.text)["login"]["result"] != "Success":
            return -1
        return 0


    """
    Get a crsf token from frwiki to be able to edit a page
    """
    def get_csrf_token(self):
        r = self.request({
            "action":"query",
            "meta":"tokens",
            "type":"csrf",
            "assert":self.assertion,
            "format":"json"
        })
        return r["query"]["tokens"]["csrftoken"]

