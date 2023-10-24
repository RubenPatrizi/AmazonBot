from cryptography.fernet import Fernet

def get_key(key):
    h = 3
    new_key = ""
    for char in key:
        new_key += chr(ord(char)-h)
        h += 1
        if h > 7:
            h = 3
    return new_key

def hide(key):
    new_key = ""
    h = 3
    for char in key:
        new_key += chr(ord(char)+h)
        h += 1
        if h > 7:
            h = 3
    return new_key

def get_credentials():
    keys = read_keys()
    if len(keys) == 0:
        return "",""
    else:
        key = get_key(keys[1]).encode()
    f = Fernet(key)
    mail = f.decrypt(get_key(keys[0]).encode())
    password = f.decrypt(get_key(keys[2]).encode())
    return mail.decode(), password.decode()

def store_credentials(mail, password):
    keys = read_keys()
    if len(keys) == 0:
        key = Fernet.generate_key()
    else:
        key = get_key(keys[1]).encode()
    f = Fernet(key)
    mail = f.encrypt(mail.encode())
    password = f.encrypt(password.encode())
    file = open(r"keys.txt", "w", encoding="utf-8")
    file.write(f"{hide(mail.decode())}\n"
               f"{hide(key.decode())}\n"
               f"{hide(password.decode())}\n")
    file.close()

def delete_credentials():
    keys = read_keys()
    if len(keys) == 0:
        return
    file = open(r"keys.txt", "w+")
    file.close()

def read_keys():
    file = open(r"keys.txt", "a+", encoding="utf-8")
    file.close()
    file = open(r"keys.txt", "r+", encoding="utf-8")
    keys = file.readlines()
    file.close()
    for i in range(0, len(keys)):
        keys[i] = keys[i][:-1]
    return keys
