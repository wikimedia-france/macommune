#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Autor: Antoine "0x010C" Lamielle
# Date: 18 March 2016
# License: GNU GPL v3

import os
import time
import json
import requests
import configparser
from OpenSSL import SSL


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
    def __init__(self, section_name):

        config = configparser.ConfigParser()
        config.read('config.ini')

        self.user = config.get(section_name, 'user')
        self.password = config.get(section_name, 'password')
        self.api_endpoint = config.get(section_name, 'endpoint')
        self.assertion = config.get(section_name, 'assertion')
        if self.assertion == "bot":
            self.limit = 5000
        else:
            self.limit = 500

        self.session = requests.Session()

    def request(self, data, files=None):
        """
        Perform a given request with a simple but useful error managment
        """
        relogin = 3
        while relogin:
            try:
                if files is None:
                    r = self.session.post(self.api_endpoint,
                                          data=data)
                else:
                    r = self.session.post(self.api_endpoint,
                                          data=data,
                                          files=files)
                response = json.loads(r.text)
                if "error" in response:
                    if response['error']['code'] == 'assertuserfailed':
                        self.login()
                        relogin -= 1
                        continue
                    break
                return response
            except (requests.exceptions.ConnectionError,
                    SSL.Error, SSL.ZeroReturnError):
                time.sleep(5)
                self.session = requests.Session()
                self.login()
                relogin -= 1
        raise Exception('API error', response['error'])

    def login(self):
        """
        Login into the wiki
        """
        r = self.session.post(self.api_endpoint, data={
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        })
        token = json.loads(r.text)["query"]["tokens"]["logintoken"]
        r = self.session.post(self.api_endpoint, data={
            "action": "login",
            "lgname": self.user,
            "lgpassword": self.password,
            "lgtoken": token,
            "format": "json"
        })
        if json.loads(r.text)["login"]["result"] != "Success":
            return -1
        return 0

    def get_csrf_token(self):
        """
        Get a crsf token from frwiki to be able to edit a page
        """
        r = self.request({
            "action": "query",
            "meta": "tokens",
            "type": "csrf",
            "assert": self.assertion,
            "format": "json"
        })
        return r["query"]["tokens"]["csrftoken"]

    def replace(self, title, text, summary, nocreate=False, createonly=False):
        """
        Replace the content of a page (or a list of pages) with the given text
        @param string title : A list of pages to append the text
            (if only a page has to be processed,
            it could be passed as a string)
        @param string text : The text to append ; all the "$(title)" will
            be replaced by the title of the page.
        @param string summary : the summary of the edit; all the "$(title)"
            will be replaced by the title of the page.
        @param bool nocreate : if it's set to True, the edit will fail when
            the page doesn't exist
        @param bool createonly : if it's set to True, the edit will fail when
            the page already exists
        """
        data = {
            "action": "edit",
            "assert": self.assertion,
            "title": title,
            "text": text,
            "summary": summary,
            "token": self.get_csrf_token(),
            "format": "json",
        }
        if self.assertion == "bot":
            data["bot"] = 1
        if nocreate:
            data["nocreate"] = ""
        elif createonly:
            data["createonly"] = ""

        r = self.request(data)
