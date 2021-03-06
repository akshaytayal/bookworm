# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

import datetime
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
   
    redirect (URL('home'))


def user():
    """

    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    return service()


@auth.requires_signature()
def data():
    return dict(form=crud())

def home():

    msg=''
    msgs=''
    if request.vars.Submit:
        session.email = request.vars.email
        session.password = request.vars.password

        rs=db((db.user_info.email==session.email) & (db.user_info.password== session.password)).select(db.user_info.ALL)
        if not rs:
            message="Incorrect Credentials..Try again!"
            session.user_id=''
            return dict(msg=message,msgs='')
        else:
            session.login='Y'
            for rows in rs:
                session.user_id=rows.id
                session.user_name=rows.first_name,' ',rows.last_name          
            message="You are now Logged in "
            return response.render('default/home.html',msgs=message)
    else:
        return dict(msg="",msgs=msgs)


def addRemove():
        transaction_id=''
        book_id=''
        countErr=''
        if session.login == 'Y':
            borrowedBooks=db((db.transactions.user_id==session.user_id)&(db.transactions.is_open=='Y')&(db.transactions.book_id==db.user_books.id)
                             &(db.transactions.borrower_conf=='Y')).select(db.user_books.ALL)

            tempL=db((db.transactions.user_id==session.user_id)&(db.transactions.is_open=='Y')&(db.transactions.book_id==db.user_books.id)&(db.transactions.borrower_conf=='N')).select(db.transactions.id,db.transactions.book_id)
            borrNotColl=[]
            for row in tempL:
                transaction_id=row.id
                book_id=row.book_id
                borrNotColl +=( db(book_id==db.user_books.id).select(db.user_books.title))


            uploadedBooks=db(db.user_books.user_id==session.user_id).select(db.user_books.ALL)
            return dict(br=borrowedBooks,ub=uploadedBooks,bnc=borrNotColl,tran_id=transaction_id,countErr=countErr)
        else:
            redirect (URL('home'))

def library():
        msg=''
        fetch=''
        if session.login == 'Y':
            genre='All' if not request.vars.genre else request.vars.genre
            author='All' if not request.vars.author else request.vars.author
            available=request.vars.available
            if genre=='All' and author=='All' and not available:
                return dict(rows=db(db.user_books.user_id!=session.user_id).select(db.user_books.ALL),msg=msg)
            if not available:
                if genre == 'All' and author !='All':
                    return dict(rows=db((db.user_books.user_id!=session.user_id)&(db.user_books.author==author)).select(db.user_books.ALL),msg=msg)
                elif author=='All' and genre != 'All':
                    return dict(rows=db((db.user_books.user_id!=session.user_id)&(db.user_books.genre==genre)).select(db.user_books.ALL),msg=msg)
                elif author !='All' and genre != 'All':
                    return dict(rows=db((db.user_books.user_id!=session.user_id)&(db.user_books.genre==genre)&(db.user_books.author==author)).select(db.user_books.ALL),msg=msg)
            else:
                if genre == 'All' and author !='All':
                    return dict(rows=db((db.user_books.user_id!=session.user_id)&(db.user_books.author==author)&(db.user_books.is_available=='Y')).select(db.user_books.ALL),msg=msg)
                elif author=='All' and genre != 'All':
                    return dict(rows=db((db.user_books.user_id!=session.user_id)&(db.user_books.genre==genre)&(db.user_books.is_available=='Y')).select(db.user_books.ALL),msg=msg)
                elif author !='All' and genre != 'All':
                    return dict(rows=db((db.user_books.user_id!=session.user_id)&(db.user_books.genre==genre)&(db.user_books.author==author)&(db.user_books.is_available=='Y')).select(db.user_books.ALL),msg=msg)
                else:
                    return dict(rows=db((db.user_books.user_id!=session.user_id)&(db.user_books.is_available=='Y')).select(db.user_books.ALL),msg=msg)
                     

                        
        else:
            redirect(URL('home'))

def register():
    errMsg=''
    if request.vars.Submit:
        if request.vars.password1 != request.vars.password2:
            return dict(errMsg="Passwords doesn't match ")
        db.user_info.insert(first_name=request.vars.FirstName,last_name=request.vars.LastName,email=request.vars.Email,
                            password=request.vars.password1,address=request.vars.address,mobile_no=request.vars.mobile,isactive='Y')
        db.commit;
        for row in  db(db.user_info.email==request.vars.Email).select(db.user_info.id):
            user_id=row.id
        isbn=(request.vars.isbn1,request.vars.isbn2,request.vars.isbn3,request.vars.isbn4,request.vars.isbn5)           
        price=(request.vars.price1,request.vars.price2,request.vars.price3,request.vars.price4,request.vars.price5)
        fromm=(request.vars.fromm1,request.vars.fromm2,request.vars.fromm3,request.vars.fromm4,request.vars.fromm5)
        to=(request.vars.to1,request.vars.to2,request.vars.to3,request.vars.to4,request.vars.to1)
        
        for i in range(5):
            for r in db(db.isbn.isbn==isbn[i]).select(db.isbn.title,db.isbn.genre,db.isbn.author):
                title=r.title
                genre=r.genre
                author=r.author
                
            db.user_books.insert(title=title,user_id=user_id,genre=genre,available_from=fromm[i],author=author,
                                 available_upto=to[i],isbn=isbn[i],price_per_day=price[i],is_available='Y')
        db.commit;
        session.statusMessage="Congratulations !!! You have successfully registered. Please login to continue. You can add more books under 'My account' tab "
        redirect (URL('status'))
    else:
        return dict(errMsg=errMsg)
    
def logout():
        session.login='N'
        redirect (URL('home'))

def status():
    return dict(statusMessage=session.statusMessage)

def book():
    msg=''
    count=db((db.transactions.user_id==session.user_id)&(db.transactions.is_open=='Y')).count()
    print count
    if  count < 6 :
        db(request.args(0)==db.user_books.id).update(is_available='N')
        db.transactions.insert(user_id=session.user_id,book_id=request.args(0),lender_conf='N',borrower_conf='N',is_open='Y')
        msg="You have successfully blocked the book. Please contact the user and get the book. Once you get the book please update the same under 'My Account' section"
    else:
         msg=" Sorry !!! You can't book a new book as you have alrady taken 5 books. Please return the books with you to get new books"
    rows=dict(rows=db().select(db.user_books.ALL),msg=msg)
    return response.render('default/library.html',rows)

def bookInfo():
    bookFlag= 'Y'  if not request.args(1) else request.args(1)
    return dict(bookInfo=db(request.args(0)==db.user_books.id).select(),bf=bookFlag)

def reviews():
    errMsg=''
    if session.login == 'Y':
        if request.vars.Submit:
            if request.vars.review:
                db.reviews.insert(title=request.vars.title,user_id=session.user_id,review=request.vars.review)
            else:
                errMsg="Please Fill this field "         
            
        if request.vars.SubmitR:
            reviews=db(request.vars.titleR==db.reviews.title).select(db.reviews.ALL)
        else:
            reviews=db().select(db.reviews.ALL)            
        books=db().select(db.isbn.title,db.isbn.id)        
        return dict(reviews=reviews,books=books,errMsg=errMsg)
    else:
        redirect(URL('home'))
        
def reportAbuse():
    actMsg=''
    if session.login == 'Y':
            reasons=db().select(db.abuse_reasons.ALL)
            if request.vars.Submit:
                if db((db.user_info.email==request.vars.mail)&(db.user_info.isactive=='N')).count()>0:
                    actMsg="User already de activated"
                elif db((db.abuses.abused_by==session.user_id)&(db.abuses.abused_on==request.vars.mail)).count()> 0:
                    actMsg="You have already reported abuse on this user. You can't report abuse more than once on a single user"            
                else:
                    db.abuses.insert(abused_on=request.vars.mail,abused_by=session.user_id,abused_time=datetime.datetime.today())
                    db.commit
                    if db(request.vars.mail==db.abuses.abused_on).count() > 4:
                        db(db.user_info.email==request.vars.mail).update(isactive='N')
        
            return dict(reasons=reasons,actMsg=actMsg)
    else:      
        redirect(URL('home'))        

def userinfo():
    info=''
    if request.args(0):
        info=db(db.user_info.id==request.args(0)).select()
    return dict(info=info)

def updateCollect():
        db(request.args(0)==db.transactions.id).update(borrower_conf='Y')
        db.commit
        redirect(URL('addRemove'))
    
def updateRelease():
        db(request.args(0)==db.transactions.id).delete()
        db.commit
        redirect(URL('addRemove'))
      
def updateRemove():
    countErr=''
    if db(session.user_id==db.user_books.user_id).count() > 5:
        db(request.args(0)==db.user_books.id).delete()
        db.commit
        redirect (URL('addRemove'))
    else:
        session.statusMessage='Total no. of books is 5. Please add an another book to remove this book'
        redirect (URL('status'))
        
def isbnInfo():
    return dict()

def addBooks():
    if request.vars.Submit:
        book=db(db.isbn.isbn==request.vars.isbn).select(db.isbn.ALL)
        for book in book:
            title=book.title
            genre=book.genre
            author=book.author
            db.user_books.insert(title=title,user_id=session.user_id,genre=genre,available_from=request.vars.fromm,author=author,
                                     available_upto=request.vars.to,isbn=request.vars.isbn,price_per_day=request.vars.price,is_available='Y')
            db.commit;
            session.statusMessage='Congratulation !!! You have successfully added the book.'
            redirect (URL('status'))
    else:
            return dict()
