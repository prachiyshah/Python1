__author__ = 'Sina'

import couchdb
from couchdb.mapping import Document, TextField


class Storage(object):
    def __init__(self, url, dbName):

        couch = couchdb.Server()  # Assuming localhost:5984
        # If your CouchDB server is running elsewhere, set it up like this:
        couch = couchdb.Server(url)

        # select database
        self.db = couch[dbName]

    def register(self, email, firstName, lastName, password):
        #create a document and insert it into the db:
        user = self.db.get(email)
        if(user):
            msg = 'User account already exists'
            print msg
        else:
            id = self.inc_user_count()
            doc = {'userId': id, 'email': email, 'firstName': firstName, 'lastName': lastName, 'password': password,
                   'type': 'User'}
            self.db[email] = doc
            #self.db.save(doc)
            msg = "success"
        return msg

    def validate(self, email, password):
        if email in self.db:
            doc = self.db[email]
            print doc['password']
            print password
            if doc['password'] in password:
                print 'login successful'
                return doc['userId']
            else:
                print 'Invalid password'
        else:
            print 'Invalid Username'

#couchdb view for getting a user based on userid. Note: email is _id of the document, not userid
    def get_user(self, userid):
        view = '''function(doc) { if(doc.type == "User" && doc.userId == '''+userid+''') emit(doc.userId, doc); }'''
        user = self.db.query(view).rows[0]
        return user

    def createboard(self, userid, boardName, boardDesc, category, isPrivate):
        user = self.get_user(userid)
        if(user):
            board = self.db.get(boardName)
            if(board):
                msg = "Board already exists"
                print msg
            else:
                doc = {'boardName': boardName, 'description': boardDesc, 'category': category, 'isPrivate': isPrivate,
                       'owner': userid, 'type': 'Board'}
                self.db[boardName] = doc
                msg = 'success'
        else:
            msg = 'Invalid user!'
            print msg
        return msg

    def createPin(self, userid, boardName, pinName, imageUrl, description):
        user = self.get_user(userid)
        if(user):
            if boardName in self.db:
                id = self.inc_pin_count()
                document = {'pinId': id, 'pinName': pinName, 'image': imageUrl, 'description': description,
                            'boardName': boardName, 'owner': userid, 'type': 'Pin'}
                self.db[str(id)] = document
                msg = 'success'
            else:
                msg = 'No such Board exists'
                print msg
        else:
            msg = 'Invalid User'
            print msg
        return id



    def get_board(self, userid, board_name):
        user = self.get_user(userid)
        if (user):
            if board_name in self.db:
                doc = self.db.get(board_name)
                if str(doc['type']) == 'Board':
                    if str(doc['owner']) == userid:
                        print doc['boardName']
                        return doc
                    else:
                        print 'No such board exists for the user'
                else:
                    print 'Invalid board'
            else:
                print 'No such board exists'
        else:
            print 'No such user exists'



    def fetchBoards(self, userid):
        user = self.get_user(userid)
        boards = []
        if (user):
            for name in self.db:
                doc = self.db[name]
                if str(doc['type']) == 'Board':
                    if str(doc['owner']) == userid:
                        print doc['boardName']
                        boards.append(doc)
        else:
            print 'No such user exists'
        return boards


    def fetchPins(self, userid, boardname):
        user = self.get_user(userid)
        pins = []
        if (user):
            if boardname in self.db:
                for name in self.db:
                    doc = self.db[name]
                    if str(doc['type']) == "Pin":
                        if str(doc['boardName'])== boardname:
                            if str(doc['owner']) == userid:
                                print doc['pinName']
                                pins.append(doc)
                            else:
                                print 'The pin does not belong to the user'
                        else:
                             print 'The pin does not belong to the board'
            else:
                print 'No such board exists'
        else:
            print 'No such user exists'
        return pins


    def initiate(self):
        doc = {'counter': 1, 'type': 'userCounter'}
        self.db['userCounter'] = doc
        doc1 = {'counter': 1, 'type': 'pinCounter'}
        self.db['pinCounter'] = doc1
        doc2 = {'counter': 1, 'type': 'commentCounter'}
        self.db['commentCounter'] = doc2


    def inc_user_count(self):
        doc = self.db['userCounter']
        current_count = doc['counter']
        doc['counter'] = current_count + 1
        self.db['userCounter'] = doc
        return current_count + 1


    def inc_pin_count(self):
        doc = self.db['pinCounter']
        current_count = doc['counter']
        doc['counter'] = current_count + 1
        self.db['pinCounter'] = doc
        return current_count + 1

    def inc_comment_count(self):
        doc = self.db['commentCounter']
        current_count = doc['counter']
        doc['counter'] = current_count + 1
        self.db['commentCounter'] = doc
        return current_count + 1

    def fetchSinglePin(self, userid, boardName, pinId):
        user = self.get_user(userid)
        if(user):
            board = self.db.get(boardName)
            if(board):
                doc=self.db[pinId]
                if doc['type'] in "Pin":
                    if str(doc['owner']) == userid:
                        if str(doc['boardName']) == boardName:
                            msg="pin found successfully"
                            print msg
                            return doc
                        else:
                            msg="Invalid Board Name!"
                            print msg
                    else:
                        msg="This pin does not belong to you!"
                        print msg
                else:
                    msg="No such pin "
                    print msg
            else:
                msg="Invalid Board Name!"
                print msg
        else:
            msg="Invalid user!"
            print msg

    def update_pin(self,pin_name,image,description,userid,boardname,pinid):
        user = self.get_user(userid)
        if(user):
            if boardname in self.db:
                doc = self.db[pinid]
                if (doc):
                    if(pin_name):
                        doc['pinName'] = pin_name
                        self.db[pinid] = doc
                    if(image):
                        doc['image'] = image
                        self.db[pinid] = doc
                    if(description):
                        doc['description'] = description
                        self.db[pinid] = doc
                    print doc['pinName']+' updated'
                    return doc
                else:
                    print 'No such pin!'
            else:
                print 'No such board!'
        else:
            print 'Invalid userId!'

    def delete_pin(self,userid,boardname,pinid):
       user = self.get_user(userid)
       if(user):
           if boardname in self.db:
               doc = self.db[pinid]
               if doc['type'] in 'Pin':
                   if doc['owner'] in userid:
                       self.db.delete(doc)
                       msg = 'success'
                   else:
                       print 'The pin does not belong to the user'
               else:
                   print 'No such pin!'
           else:
               print 'No such board!'
       else:
           print 'Invalid userId!'
       return msg

    def updateboard(self, userid, boardName, boardDesc, category, isPrivate):
        user = self.get_user(userid)
        if(user):
            board = self.db.get(boardName)
            if(board):
                # class Board(Document):
                #     boardName = TextField()
                #     description = TextField()
                #     category = TextField()
                #     isPrivate = TextField()
                # board = Board.load(self.db, boardName)
                if (boardDesc):
                    print boardDesc
                    board['description'] = boardDesc
                    self.db[boardName] = board
                if (category):
                    board['category'] = category
                    self.db[boardName] = board
                if (isPrivate):
                    board['isPrivate'] = isPrivate
                    self.db[boardName] = board
                msg="success"
                print msg
                return board
            else:
                msg="Invalid Board Name"
                print msg
        else:
            print 'Invalid user!'

    def deleteBoard(self, userid, boardName):
        user = self.get_user(userid)
        if(user):
            board = self.db.get(boardName)
            if(board):
                if str(board['owner']) == userid:
                    self.db.delete(board)
                    msg="success"
                    print msg
                else:
                    msg="The board does not belong to the user"
                    print msg
            else:
                msg="Invalid Board Name!"
                print msg
        else:
            msg="Invalid User!"
            print msg
        return msg

    def postComment(self,userid, boardName,pinid, comment, commenter):
        print'--> in storage postCOmment'
        doc = self.db[pinid]
        pinname = doc['pinName']
        commentName = 'comment for '+pinname
        user = self.get_user(userid)
        if(user):
            if boardName in self.db:
                if pinid in self.db:
                    id = self.inc_comment_count()
                    commentId = 'comment'+str(id)
                    document = {'commentId': commentId, 'pinId': pinid, 'commenter': commenter, 'type': 'Comment', 'description':comment,'boardName':boardName}
                    self.db[commentId] = document
                    return id
                else:
                    print 'No such pin'
            else:
                print 'No such board'
        else:
            print 'User does not exist'
        return



    def delete_comment(self,userId,boardName,pinId,commentId):
        user = self.get_user(userId)
        if(user):
                comment='comment'+commentId
                doc = self.db.get(comment)
                if str(doc['type'])=='Comment':
                    if str(doc['boardName'])== boardName:
                        if str(doc['pinId'])== pinId:
                            self.db.delete(doc)
                            msg="success"
                            return msg
                        else:
                            msg= 'Comment with id :'+commentId+'does not exist for the pin'
                            print msg
                    else:
                        msg='No comments found  for the board'
                        print msg
                else:
                    msg='Please provide a valid comment Id'
                    print msg
        else:
            msg='Please provide a valid userId'
            print msg
            return msg

    def update_comment(self,comment,userId,boardName,pinId,commentId):
        user = self.get_user(userId)
        if(user):
             print comment
             if(comment):
                strCommentId='comment'+commentId
                doc = self.db.get(strCommentId)
                if str(doc['type'])=='Comment':
                    if str(doc['boardName'])== boardName:
                        if str(doc['pinId'])== pinId:
                            doc['description'] = comment
                            self.db[strCommentId] = doc
                            print self.db[strCommentId]
                            return doc
                        else:
                            print 'Comment with id :'+commentId+'does not exist for the pin'
                    else:
                        print 'No comments found  for the board'
                else:
                    print 'No comments exists'
             else:
                print 'please enter a comment'
        else:
            print 'Invalid user'

    def get_single_comment(self,userId,boardName,pinId,commentId):
        user = self.get_user(userId)
        if(user):
            comment='comment'+commentId
            doc = self.db.get(comment)
            if str(doc['type'])=='Comment':

                    if str(doc['boardName'])== boardName:
                        if str(doc['pinId'])== pinId:
                            print doc['description']
                            return doc
                        else:
                            msg='No comments for the PinId :'+pinId
                            print msg

                    else:

                        print 'No pins exist for the board :'+boardName

            else:
                print 'Invalid Comment Id'
        else:
            print 'Invalid User'

    def getAllComments(self, userid, boardname, pinId):
        user = self.get_user(userid)
        Comments = []
        if (user):
            if boardname in self.db:
                for name in self.db:
                    doc = self.db[name]
                    if str(doc['type']) == "Comment":
                        if str(doc['boardName'])== boardname:
                            if str(doc['pinId']) == pinId:
                                Comments.append(doc)
                            else:
                                print 'The comment does not exist in the pin'
            else:
                print 'No such board exists'
        else:
            print 'No such user exists'
        return Comments
