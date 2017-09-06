#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) Philipp Wagner. All rights reserved.
# Licensed under the BSD license. See LICENSE file in the project root for full license information.

import json
import base64
import urllib2
import setlcd
from .. import secret

SERVER_ADDRESS = "http://192.168.0.100:5000"

class FaceRecClient(object):

    def __init__(self, url):
        self.url = url
        
    def getBase64(self, filename):
        with open(filename, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string

    def request(self, api_func, request_data):
        url_func = "%s/api/%s" % (self.url, api_func)
        req = urllib2.Request(url=url_func, data = json.dumps(request_data), headers = {'content-type': 'application/json'})
        res = urllib2.urlopen(req)
        return res.read()

    def recognize(self, filename):
        base64Image = self.getBase64(filename)
        json_data = { "image" : base64Image }
        api_result = self.request("recognize", json_data)
        re = eval(api_result)
        if secret.face_flag:
            setlcd.lcdDisplay(str(re['name']),(255,0,0)).start()
            secret.face_flag=False
        