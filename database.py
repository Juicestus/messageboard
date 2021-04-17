
def saveUsersToDatabase(users_repository, fn):

    f = open(fn,'w')
    usernameList = users_repository.list_users()

    for username in usernameList:

        user = users_repository.get_user(username)
        password = user.password
        identifier = user.get_id()

        f.write(f'{username}@{password}@{identifier}\n')
    
    f.close()

def loadUsersFromDatabase(fn):

    f = open(fn, 'r')
    r = []

    for l in f:
        r.append(l.split('@'))

    return r
        

