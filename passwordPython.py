import csv
import hashlib
from datetime import datetime, timedelta

def encryptString(theString): # use a function to encode to hash value
    enc = hashlib.md5(theString.encode()).hexdigest()
    return enc

def isUserNameTaken(userNm): # check if userName which the user wants to use is taken already
    userExists = False
    with open('passwords.csv', 'r') as file: # read only
        reader = csv.reader(file)
        for col in reader:
            if (userNm == col[0]):
                userExists=True
                break
    return userExists

def getEncPw(usrNm):
    with open('passwords.csv', 'r') as file: # read only
        reader = csv.reader(file)
        for col in reader:
            if (usrNm == col[0]):
                return col[1]

def lockDown(): # create a function for blocking more password attempts
    now = datetime.now()
    print("You have been blocked for 2 minutes")
    while(datetime.now() < now + timedelta(seconds=60)):
        continue
    while(datetime.now() < now + timedelta(seconds=120)):
        input("Enter Username: ")
        input("Enter password: ")
        print("unauthorised attempt")


def signup():
    fName = str(input("Enter First Name: "))
    lName = str(input("Enter Last Name: "))
    emailID = str(input("Enter Email Address: "))
    while(True): # loop until user enters valid username
        userName = str(input("Enter Username Name: "))
        
        if(not isUserNameTaken(userName)):
            if(',' in userName): # make sure no commas are in stored data - will disrupt csv columns
                print("Cannot include comma!")
            else:
                break
        else:
            print("Username taken. Try a different username")
        
    while(True):
        num = False
        cap = False
        spec = False
        password = str(input("Enter Password: "))
        for ch in password:
            if ch == ",": # a ',' character will disrupt the storage in csv format
                spec = False # set one of the checks to false and break out so as to not give opportunity for 'True'
                break
            elif ch.isnumeric():
                num = True
            
            elif ch.isalpha():
                if ch.isupper():
                    cap = True
            else:
                if not ch == ' ': # special characters are non alphabetic and non numeric characters excluding the space (' ') character
                    spec = True
        if(num and cap and spec):
            break
        else:   
            print("Error: Password requires a number, capital letter and special character! Try again")

    with open('passwords.csv', 'a', newline="") as file:
        hashedPw = encryptString(password)
        writer = csv.writer(file)
        writer.writerow([userName, hashedPw])

def login(): # function for logging in
    attemptCount = 0
    while(True):
        userName = str(input("Enter Username: "))
        pw = str(input("Enter password: "))
        if(not isUserNameTaken(userName)): # if the userName isn't in the database
            print("Username does not exist. Try Again")
            attemptCount+=1
        elif(getEncPw(userName) == encryptString(pw)): # if the password matches the stored password
            print("Sign-In Successful!")
            break
        else: # if the password is incorrect
            print("Error, Incorrect password entered")
            attemptCount+=1
        if(attemptCount == 3):
            lockDown()

#########################################
#Choose signup() or login()
#########################################
#signup()
login()