__author__ = 'shaji'

import requests
import json
global server
global userId

#####Boards section#####
def go_to_boards():
    option = raw_input("Boards menu >\n1. Create board 2. View board 3. Update board 4. Delete board 5. Get all boards 6. Back to main menu 7. Quit\n")
    if option == '1':
        create_board()
        go_to_boards()
    elif option == '2':
        view_board()
        go_to_boards()
    elif option == '3':
        update_board()
        go_to_boards()
    elif option == '4':
        delete_board()
        go_to_boards()
    elif option == '5':
        get_all_boards()
        go_to_boards()
    elif option == '6':
        show_menu()
    elif option == '7':
        exit()


def create_board():
    boardName = raw_input('board name: ')
    boardDesc = raw_input('description: ')
    category = raw_input('category: ')
    isPrivate = raw_input('isPrivate: ')
    payload = {'boardName': boardName, 'boardDesc': boardDesc, 'category':category, 'isPrivate':isPrivate}
    url = 'http://' + server + '/users/'+userId+'/boards'
    reply = requests.post(url, data=payload)
    print reply.status_code
    print reply.text

def view_board():
    boardName = raw_input('board name: ')
    #payload = {'boardName': boardName}
    url = 'http://' + server + '/users/'+userId+'/boards/'+boardName
    reply = requests.get(url)
    print reply.status_code
    print reply.text

def update_board():
    boardName = raw_input('board name: ')
    boardDesc = raw_input('description: ')
    category = raw_input('category: ')
    isPrivate = raw_input('isPrivate: ')
    payload = {'boardName': boardName, 'boardDesc': boardDesc, 'category':category, 'isPrivate':isPrivate}
    url = 'http://' + server + '/users/'+userId+'/boards/'+boardName
    reply = requests.put(url, data=payload)
    print reply.status_code
    print reply.text

def delete_board():
    boardName = raw_input('board name: ')
    url = 'http://' + server + '/users/'+userId+'/boards/'+boardName
    reply = requests.delete(url)
    print reply.status_code
    print reply.text

def get_all_boards():
    url = 'http://' + server + '/users/'+userId+'/boards'
    reply = requests.get(url)
    print reply.status_code
    print reply.text

#####Pins section#####
def go_to_pins():
    option = raw_input("Pins menu >\n1. Create pin 2. View pin 3. Update pin 4. Delete pin 5. Get all pins 6. Back to main menu 7. Quit\n")
    if option == '1':
        create_pin()
        go_to_pins()
    elif option == '2':
        view_pin()
        go_to_pins()
    elif option == '3':
        update_pin()
        go_to_pins()
    elif option == '4':
        delete_pin()
        go_to_pins()
    elif option == '5':
        get_all_pins()
        go_to_pins()
    elif option == '6':
        show_menu()
    elif option == '7':
        exit()

def create_pin():
    boardName = raw_input('board name: ')
    pinName = raw_input('pin name: ')
    image_url = raw_input('image: ')
    description = raw_input('description: ')
    payload = {'pinName': pinName, 'image': image_url, 'description':description}
    url = 'http://' + server + '/users/'+userId+'/boards/'+boardName+'/pins'
    reply = requests.post(url, data=payload)
    print reply.status_code
    print reply.text

def view_pin():
    boardName = raw_input('board name: ')
    pinId = raw_input('pin Id: ')

    url = 'http://' + server + '/users/'+userId+'/boards/'+boardName+'/pins/'+pinId
    reply = requests.get(url)
    print reply.status_code
    print reply.text

def update_pin():
    boardName = raw_input('board name: ')
    pinId = raw_input('pin Id: ')

    pinName = raw_input('pin name: ')
    image_url = raw_input('image: ')
    description = raw_input('description: ')
    payload = {'pinName': pinName, 'image': image_url, 'description':description}
    url = 'http://' + server + '/users/'+userId+'/boards/'+boardName+'/pins/'+pinId
    reply = requests.put(url, data=payload)
    print reply.status_code
    print reply.text

def delete_pin():
    boardName = raw_input('board name: ')
    pinId = raw_input('pin Id: ')

    url = 'http://' + server + '/users/'+userId+'/boards/'+boardName+'/pins/'+pinId
    reply = requests.delete(url)
    print reply.status_code
    print reply.text

def get_all_pins():
    boardName = raw_input('board name: ')
    url = 'http://' + server + '/users/'+userId+'/boards/'+boardName+'/pins'
    reply = requests.get(url)
    print reply.status_code
    print reply.text

#####Comments section#####
def go_to_comments():
    option = raw_input("Comments menu >\n1. Post comment 2. View comment 3. Update comment 4. Delete comment 5. Get all comments 6. Back to main menu 7. Quit\n")
    if option == '1':
        post_comment()
        go_to_comments()
    elif option == '2':
        view_comment()
        go_to_comments()
    elif option == '3':
        update_comment()
        go_to_comments()
    elif option == '4':
        delete_comment()
        go_to_comments()
    elif option == '5':
        get_all_comments()
        go_to_comments()
    elif option == '6':
        show_menu()
    elif option == '7':
        exit()

def post_comment():
    boardName = raw_input('board name: ')
    pinId = raw_input('pin Id: ')
    description = raw_input('Comments: ')
    commenter = raw_input('Your userid: ')
    payload = {'description': description, 'commenter': commenter}
    url = 'http://' + server + '/users/'+userId+'/boards/'+boardName+'/pins/'+pinId+'/comment'
    reply = requests.post(url, data=payload)
    print reply.status_code
    print reply.text

def view_comment():
    boardName = raw_input('board name: ')
    pinId = raw_input('pin Id: ')
    commentId = raw_input('comment Id: ')
    url = 'http://' + server + '/users/'+userId+'/boards/'+boardName+'/pins/'+pinId+'/comment/'+commentId
    reply = requests.get(url)
    print reply.status_code
    print reply.text

def update_comment():
    boardName = raw_input('board name: ')
    pinId = raw_input('pin Id: ')
    commentId = raw_input('comment Id: ')
    description = raw_input('Comments: ')
    #commenter = raw_input('Your userid: ')
    payload = {'description': description}
    url = 'http://' + server + '/users/'+userId+'/boards/'+boardName+'/pins/'+pinId+'/comment/'+commentId
    reply = requests.put(url, data=payload)
    print reply.status_code
    print reply.text

def delete_comment():
    boardName = raw_input('board name: ')
    pinId = raw_input('pin Id: ')
    commentId = raw_input('comment Id: ')
    url = 'http://' + server + '/users/'+userId+'/boards/'+boardName+'/pins/'+pinId+'/comment/'+commentId
    reply = requests.delete(url)
    print reply.status_code
    print reply.text

def get_all_comments():
    boardName = raw_input('board name: ')
    pinId = raw_input('pin Id: ')
    url = 'http://' + server + '/users/'+userId+'/boards/'+boardName+'/pins/'+pinId+'/comment'
    reply = requests.get(url)
    print reply.status_code
    print reply.text

#####User registration/login section#####
def login():
    email = raw_input('email address: ')
    password = raw_input('password: ')
    url = 'http://' + server + '/users/login'
    payload = {'emailId': email, 'password': password}
    reply = requests.post(url, data=payload)
    print reply.status_code
    print reply.text
    if reply.status_code == 201:
        json_reply = json.loads(reply.text)
        userId = json_reply['userId']
        #print 'Your userId is :'+userId
        print 'You have logged in!'
        return userId
    else:
        print "Authentication failed!"
        return

def register():
    email = raw_input('email address: ')
    password = raw_input('password: ')
    firstName = raw_input('first name: ')
    lastName = raw_input('last name: ')
    payload = {'emailId': email, 'password': password, 'firstName': firstName, 'lastName': lastName }
    url = 'http://' + server + '/users/signup'
    reply = requests.post(url, data=payload)
    print reply.status_code
    print reply.text


#####Menu section#####
def show_menu():
    menu = raw_input("Select a menu option 1. Boards 2. Pins 3. Comments 4. Quit \n")
    if menu == '1':
        go_to_boards()
        show_menu()
    elif menu == '2':
        go_to_pins()
        show_menu()
    elif menu == '3':
        go_to_comments()
        show_menu()
    elif menu == '4':
        exit()


if __name__ == '__main__':
    server = raw_input("Welcome to our pinterest client!\nPlease enter pinterest server ip and port in <ip>:<port> format:\n")
    while True:
        input = raw_input("Do you want to: 1. signup 2. login \n")
        if input == '1':
            print "user wants to signup"
            register()
            print "proceed to login"
            userId = login()
            if userId:
                show_menu()
        elif input == '2':
            print "user wants to login"
            userId = login()
            if userId:
                show_menu()
        else:
            print 'Exit from client'
            exit()


