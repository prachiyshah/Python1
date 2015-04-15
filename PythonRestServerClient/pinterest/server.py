__author__ = 'Sina'
import sys
import os
import socket
import json
from bottle import error
# bottle framework
from bottle import request, response, Response, route, run, template
from storage import Storage

def setup(base,conf_fn):
    host = socket.gethostname()
    base = base
    conf = {}
    # should emit a failure (file not found) message
    if os.path.exists(conf_fn):
        with open(conf_fn) as cf:
            for line in cf:
                name, var = line.partition("=")[::2]
                conf[name.strip()] = var.strip()
    else:
        raise Exception("configuration file not found.")

    # create storage
    #__store = Storage()
    setupDB()
def setupDB():
    print '\n**** service initialization ****\n'
    global db
    db = Storage('http://127.0.0.1:5984/','pinterest')
#
# setup the configuration for our service


@route('/')
def root():
    output = 'Welcome to our Pinterest!'
    return output

#
#
@route('/users/login', method='GET')
def login():
    return 'Please Enter your Username and Password using a POST method'


@route('/users/login', method='POST')
def user_login():
   print '---> Users Credentials'

   #json_request = request.json
   # if(json_request):
   #     username = json_request.get('emailId')
   #     password = json_request.get('password')
   # else:
   username = request.forms.get('emailId')
   password = request.forms.get('password')

   id = db.validate(username,password)
   if(id is None):
       response.status = 400
       return
   else:
       links = {'links': [{'url': '/users/'+str(id)+'/boards', 'method': 'GET'},
                          {'url': '/users/'+str(id)+'/boards', 'method': 'POST'}],
                'userId':str(id)}
       response.set_header('content-type', 'application/json')
       response.status = 201
       return json.dumps(links)

@route('/users/signup', method='GET')
def signup():
    return 'Please Enter your Email Address, First Name, Last Name, Password using a POST method'


@route('/users/signup', method='POST')
def user_signup():
   print '---> Users Credentials'
   #json_request = request.json
   # if (json_request):
   #     username = json_request.get('emailId')
   #     password = json_request.get('password')
   #     firstName = json_request.get('firstName')
   #     lastName = json_request.get('lastName')
   #else:
   username = request.forms.get('emailId')
   password = request.forms.get('password')
   firstName = request.forms.get('firstName')
   lastName = request.forms.get('lastName')

   msg = db.register(username, firstName, lastName, password)
   if(msg ==  'success'):
       links = {'links': [{'url': '/users/login', 'method': 'POST'}]}
       response.set_header('content-type', 'application/json')
       response.status = 201
       return json.dumps(links)
   else:
       response.status = 400
       return

@route('/users/:userid/boards', method='POST')
def createboard(userid):
   print '---> Board input data'

   boardName = request.forms.get('boardName')
   boardDesc = request.forms.get('boardDesc')
   category = request.forms.get('category')
   isPrivate = request.forms.get('isPrivate','False')
   #print userid+' '+boardName+' '+boardDesc+' '+category+' '+isPrivate
   msg = db.createboard(userid,boardName, boardDesc, category, isPrivate)
   if(msg == 'success'):
       links = {'links': [{'url': '/users/'+userid+'/boards/'+boardName, 'method': 'GET'},
                          {'url': '/users/'+userid+'/boards/'+boardName, 'method': 'PUT'},
                          {'url': '/users/'+userid+'/boards/'+boardName, 'method': 'DELETE'},
                          {'url': '/users/'+userid+'/boards/'+boardName+'/pins', 'method': 'GET'}]}
       response.set_header('content-type', 'application/json')
       response.status = 201
       return json.dumps(links)
   else:
       response.status = 400
       return

@route('/users/:userid/boards/:boardname', method='GET')
def getboarddetails(userid, boardname):
    print '---> getboard details of'
    print userid+' '+boardname
    doc = db.get_board(userid, boardname)
    if(doc):
        links = {'links': [{'url': '/users/'+userid+'/boards/'+boardname, 'method': 'PUT'},
                           {'url': '/users/'+userid+'/boards/'+boardname, 'method': 'DELETE'},
                           {'url': '/users/'+userid+'/boards/'+boardname+'/pins', 'method': 'POST'},
                           {'url': '/users/'+userid+'/boards/'+boardname+'/pins', 'method': 'GET'}]}
        response.set_header('content-type', 'application/json')
        response.status = 200
        json_content = {'Board': doc, 'Links':links }
        return json.dumps(json_content)
    else:
       response.status = 400
       return

@route('/users/:userid/boards',method='GET')
def getAllBoards(userid):
    print'---> Get all boards for a user'
    boards = db.fetchBoards(userid)
    if(boards):
        response.set_header('content-type', 'application/json')
        response.status = 200
        return json.dumps(boards)
    else:
       response.status = 400
       return

@route('/users/:userid/boards/:boardname/pins/:pinid', method='PUT')
def updatepin(userid,boardname,pinid):
    print '--->Update Pin'
    pin_name = request.forms.get('pinName')
    image = request.forms.get('image')
    description = request.forms.get('description')
    pin = db.update_pin(pin_name,image,description,userid,boardname,pinid)
    if(pin):
        response.set_header('content-type', 'application/json')
        response.status = 201
        links = {'links': [{'url': '/users/'+userid+'/boards/'+boardname+'/pins/'+str(pinid), 'method': 'GET'},
                           {'url': '/users/'+userid+'/boards/'+boardname+'/pins/'+str(pinid), 'method': 'DELETE'},
                           {'url': '/users/'+userid+'/boards/'+boardname+'/pins', 'method': 'GET'},
                           {'url': '/users/'+userid+'/boards/'+boardname+'/pins', 'method': 'POST'}]}
        json_content = {'Pin': pin, 'Links':links }
        return json.dumps(json_content)
    else:
       response.status = 400
       return

@route('/users/:userid/boards/:boardname/pins/:pinid', method='DELETE')
def deletepin(userid,boardname,pinid):
    print '---> Delete Pin'
    msg = db.delete_pin(userid,boardname,pinid)
    if (msg == 'success'):
        links = {'links': [{'url': '/users/'+userid+'/boards/'+boardname+'/pins', 'method': 'GET'},
                          {'url': '/users/'+userid+'/boards/'+boardname+'/pins', 'method': 'POST'}]}
        response.set_header('content-type', 'application/json')
        response.status = 201
        return json.dumps(links)
    else:
       response.status = 400
       return

@route('/users/:userid/boards/:boardname/pins/:pinid',method='GET')
def getSinglePin(userid, boardname, pinid):
    print '---> inside get pin'
    doc = db.fetchSinglePin(userid,boardname,pinid)
    if(doc):
        links = {'links': [{'url': '/users/'+userid+'/boards/'+boardname+'/pins/'+str(pinid), 'method': 'PUT'},
                          {'url': '/users/'+userid+'/boards/'+boardname+'/pins/'+str(pinid), 'method': 'DELETE'},
                          {'url': '/users/'+userid+'/boards/'+boardname+'/pins/'+str(pinid)+'/comments', 'method': 'POST'}]}
        response.set_header('content-type', 'application/json')
        response.status=200
        json_content = {'Pin': doc, 'Links': links}
        return json.dumps(json_content)
    else:
        response.status=400
        return

@route('/users/:userid/boards/:boardname/pins',method='POST')
def createpin(userid,boardname):
    print'---> Pin Details'

    pinName = request.forms.get('pinName')
    imageUrl =request.forms.get('image')
    description = request.forms.get('description')
    pinId = db.createPin(userid,boardname,pinName,imageUrl,description)
    print userid+boardname+pinName+imageUrl+description
    if(pinId):
        links = {'links': [{'url': '/users/'+userid+'/boards/'+boardname+'/pins/'+str(pinId), 'method': 'GET'},
                          {'url': '/users/'+userid+'/boards/'+boardname+'/pins/'+str(pinId), 'method': 'PUT'},
                          {'url': '/users/'+userid+'/boards/'+boardname+'/pins/'+str(pinId), 'method': 'DELETE'}]}
        response.set_header('content-type', 'application/json')
        response.status = 201
        return json.dumps(links)
    else:
       response.status = 400
       return


@route('/users/:userid/boards/:boardname/pins',method='GET')
def getAllPins(userid ,boardname):
    print'---> Get All Pins For a particular board'
    pins = db.fetchPins(userid,boardname)
    if(pins):
        response.set_header('content-type', 'application/json')
        response.status = 200
        return json.dumps(pins)
    else:
       response.status = 400
       return


@route('/users/:userid/boards/:boardname', method='PUT')
def update_board(userid,boardname):
    print '---> Board input data'
    boardDesc = request.forms.get('boardDesc')
    category = request.forms.get('category')
    isPrivate = request.forms.get('isPrivate')
    board = db.updateboard(userid,boardname,boardDesc,category,isPrivate)
    if(board):
        links = {'links': [{'url': '/users/'+userid+'/boards/'+boardname, 'method': 'GET'},
                           {'url': '/users/'+userid+'/boards/'+boardname, 'method': 'DELETE'},
                          {'url': '/users/'+userid+'/boards/'+boardname+'/pins/', 'method': 'POST'}]}
        response.set_header('content-type', 'application/json')
        response.status = 201
        json_content = {'Board': board, 'Links':links}
        return json.dumps(json_content)
    else:
       response.status = 400
       return


@route('/users/:userid/boards/:boardname', method='DELETE')
def deleteboard(userid,boardname):
    msg = db.deleteBoard(userid,boardname)
    if (msg == 'success'):
        links = {'links': [{'url': '/users/'+userid+'/boards', 'method': 'GET'},
                          {'url': '/users/'+userid+'/boards', 'method': 'POST'}]}
        response.set_header('content-type', 'application/json')
        response.status = 201
        return json.dumps(links)
    else:
       response.status = 400
       return

@route('/users/:userid/boards/:boardName/pins/:pinId/comment', method='POST')
def postcomment(pinId,userid,boardName):
    print'-->comment on a pin'
    comment = request.forms.get('description')
    commenter = request.forms.get('commenter','anonymous')
    #print'--> '+comment
    commentId = db.postComment(userid, boardName,pinId, comment, commenter)
    if(commentId):
        links = {'links': [{'url': '/users/'+userid+'/boards/'+boardName+'/pins/'+pinId+'/comment/'+str(commentId), 'method': 'DELETE'},
                           {'url': '/users/'+userid+'/boards/'+boardName+'/pins/'+pinId+'/comment/'+str(commentId), 'method': 'PUT'},
                           {'url': '/users/'+userid+'/boards/'+boardName+'/pins/'+pinId+'/comment/'+str(commentId), 'method': 'GET'}]}
        response.set_header('content-type', 'application/json')
        response.status = 201
        return json.dumps(links)
    else:
        response.status = 400
        return

@route('/users/:userid/boards/:boardName/pins/:pinId/comment/:commentId', method='GET')
def viewComment(userid,boardName,pinId,commentId):
    print '---> view comment'
    doc=db.get_single_comment(userid,boardName,pinId,commentId)
    if(doc):
        links = {'links': [{'url': '/users/'+userid+'/boards/'+boardName+'/pins/'+str(pinId)+'/comment/'+commentId, 'method': 'PUT'},
                          {'url': '/users/'+userid+'/boards/'+boardName+'/pins/'+str(pinId)+'/comment/'+commentId, 'method': 'DELETE'},
                          {'url': '/users/'+userid+'/boards/'+boardName+'/pins/'+str(pinId)+'/comment', 'method': 'POST'}]}
        response.set_header('content-type', 'application/json')
        response.status=200
        json_content = {'Comment': doc, 'Links': links}
        return json.dumps(json_content)
    else:
        response.status=400
        return

@route('/users/:userid/boards/:boardName/pins/:pinId/comment/:commentId', method='DELETE')
def deleteComment(userid,boardName,pinId,commentId):
    print '---> Delete comment'
    msg=db.delete_comment(userid,boardName,pinId,commentId)
    if (msg == 'success'):
        links = {'links': [{'url': '/users/'+userid+'/boards'+boardName+'/pins/'+pinId+'/comment', 'method': 'GET'},
                          {'url': '/users/'+userid+'/boards'+boardName+'/pins/'+pinId+'/comment', 'method': 'POST'}]}
        response.set_header('content-type', 'application/json')
        response.status = 201
        return json.dumps(links)
    else:
       response.status = 400
       return

@route('/users/:userid/boards/:boardName/pins/:pinId/comment/:commentId', method='PUT')
def updateComment(userid,boardName,pinId,commentId):
    print'--> updateComment'
    comment = request.forms.get('description')
    doc=db.update_comment(comment,userid,boardName,pinId,commentId)
    if(doc):
        links = {'links': [{'url': '/users/'+userid+'/boards/'+boardName+'/pins/'+pinId+'/comment/'+commentId, 'method': 'GET'},
                           {'url': '/users/'+userid+'/boards/'+boardName+'/pins/'+pinId+'/comment/'+commentId, 'method': 'DELETE'}
                          ]}
        response.set_header('content-type', 'application/json')
        response.status = 201
        json_content = {'Comment': doc, 'Links':links}
        return json.dumps(json_content)
    else:
       response.status = 400
       return

@route('/users/:userid/boards/:boardName/pins/:pinId/comment', method='GET')
def getAllComments(userid,boardName,pinId):
    print'--> get all comments'
    doc=db.getAllComments(userid,boardName,pinId)
    if(doc):
        response.set_header('content-type', 'application/json')
        response.status = 201
        return json.dumps(doc)
    else:
       response.status = 400
       return

@error(405)
def error405(error):
    return 'Method not allowed!'

@error(404)
def error404(error):
    return 'Sorry, that page is not available'

	
