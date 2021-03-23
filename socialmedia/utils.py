import re
from django.contrib.auth.models import User
import enum

def checkPasswordMatches(paswd, repPaswd):
    if(paswd == repPaswd):
        return True
    else:
        return False


def checkPasswordSecurity(password):
    flag = 0
    while True:   
        if (len(password)<8): 
            flag = -1
            break
        elif not re.search("[a-z]", password): 
            flag = -1
            break
        elif not re.search("[A-Z]", password): 
            flag = -1
            break
        elif not re.search("[0-9]", password): 
            flag = -1
            break
        elif re.search("\s", password): 
            flag = -1
            break
        else: 
            flag = 0
            return True
            break
  
    if flag ==-1: 
        return False
