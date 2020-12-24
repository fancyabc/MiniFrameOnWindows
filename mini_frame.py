import time

def login():
    return "i-----login--welcome hahahh to our website.......time:%s" % time.ctime()

def register():
    return "------register--welcome hahahah to our website....time:%s" % time.ctime()

def profile():
    return "------profile--welcome hahahah to our website....time:%s" % time.ctime()

def application(file_name):
    if file_name == "/login.py":
        return login()
    elif file_name == "/register.py":
        return register()
    else:
        return "not found you page..."