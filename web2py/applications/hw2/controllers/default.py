# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import datetime

def get_user_name_from_email(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


def index():
    user_posts = None
    print db.auth_user

    posts = db(db.post).select(orderby=~db.post.created_on, limitby=(0, 20))
    return dict(posts=posts)


@auth.requires_login()
def edit():
    if request.args(0) == None:
        form = SQLFORM(
            db.post,
            deletable=True
        )
        if form.process().accepted:
            session.flash = T('Post Added.')
            redirect(URL('default', 'index'))
        elif form.errors:
            session.flash = T('Please enter correct value.')
        return dict(form=form,)

    elif request.args(0) == 'edit':
        button = A('Cancel', _href=URL('default', 'index'), _class='btn btn-default')
        form = SQLFORM(db.post, request.vars.postid, deletable=True)
        #form = SQLFORM.factory(
            #db.post.post_content,
            #db.post.updated_on,
            #deletable = True
        #)

        if form.process().accepted:
            #rows = db(db.post).select()
            #for row in rows:
                #if row.id == int(request.vars.postid):
                    #row.update_record(post_content=form.vars.post_content, updated_on=datetime.datetime.utcnow())

            session.flash = T('Post Edited.')
            redirect(URL('default', 'index'))
        elif form.errors:
            session.flash = T('Please enter correct value.')
        return dict(form=form, button=button)

    elif request.args(0) == 'delete':
        db(db.post.id == request.vars.postid).delete()
        redirect(URL('default', 'index'))
        return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
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
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()