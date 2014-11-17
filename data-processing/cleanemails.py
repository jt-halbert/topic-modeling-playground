#!/usr/bin/env python

from email.parser import Parser
import json
import os
import multiprocessing

def getFilenames(base):
    l = []
    for root, dirs, files in os.walk(base):
        if len(files) > 0:
            l.extend([os.path.join(root,name) for name in files])
    return l

def convertEmailToJSON(filepointer):
    email = Parser().parse(filepointer)
    return json.dumps({"headers" : dict(email.items()),
        "payload" : email.get_payload(decode=True)})

files = getFilenames("/data/datasets/enron_mail_20110402/maildir")

jsonmessages = []
for fn in files:
    with open(fn) as f:
        try:
            email = Parser().parse(f)
            jsonmessages.append(json.dumps({"headers":email.items(),"payload": email.get_payload(decode=True)}, ensure_ascii=False))
        except:
            print(fn)

def getMessage(filename):
    with open(filename) as f:
        email = Parser().parse(f)
        messageid = email['Message-ID']
        return {"Message-ID":messageid, "headers":email.items(), "payload": email.get_payload(decode=True)}

def payloadParts(message):
    if message.is_multipart():
        return len(message.get_payload())
    else:
        return 1

def getPayloadParts(filename):
    f = open(filename)
    message = Parser().parse(f)
    f.close()
    return payloadParts(message)

pool = multiprocessing.Pool()
all_messages = pool.map(getMessage,files)


# How can I determine if a message is forwarded to someone?
#   * direct message body comparison: if a message was sent after a seed one and contains the entire body of the seed within the body of the next.
#   * message body topic similarity: if a message was sent after a seed and is close in topic space
#   * There is a 'FW: ' prepended to the same subject

# Let's test some assumptions
# How many subjects are there?
withtofrom = filter(lambda d: dict(d["headers"]).has_key("To") and dict(d["headers"]).has_key("From"),all_messages)
withsubject = filter(lambda d: dict(d["headers"]).has_key("Subject"), withtofrom)

# UGLY HACK!!!
subjects = set(map(lambda d: dict(d["headers"])["Subject"], withsubject))
base_subjects = filter(lambda s: not (s.lower().startswith("fw: ") or s.lower().startswith("re: ")),subjects)

