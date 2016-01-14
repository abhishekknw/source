#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import base64, hmac, sha
from sys import argv
 
private_key = 'RBn1G4qJsZfIZoNtho2ZN4Snmwcv/QmM4EEMLyqP'
input = open("./p.txt", "rb")
policy = input.read()
policy_encoded = base64.b64encode(policy)
signature = base64.b64encode(hmac.new(private_key, policy_encoded, sha).digest())
print "Your policy base-64 encoded is %s." % (policy_encoded)
print "Your signature base-64 encoded is %s." % (signature)
#Correct signature below provided by AWS
print "Your signature encoded should be 2qCp0odXe7A9IYyUVqn0w2adtCA="

