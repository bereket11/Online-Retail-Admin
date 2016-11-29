# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(B('web', SPAN(2), 'py'), XML('&trade;&nbsp;'),
                  _class="navbar-brand", _href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

DEVELOPMENT_MENU = True


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def check_user():
    if auth.user != None:
        return True
    else:
        return False

def check_admin():
    if check_user():
        user_permission = db.executesql("SELECT * FROM user_permissions WHERE user_id='" + str(auth.user.id) + "'")
        print user_permission[0][1]
        if user_permission:
            if user_permission[0][1] == "admin":
                return True
            else:
                return False
    else:
        return False

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and external resources
    # ------------------------------------------------------------------------------------------------------------------

    if check_user():
        response.menu += [
            (T('Inventory'), False, URL('default', 'inventory')),
        ]

    if check_admin():
        response.menu += [
            (T('Suppliers'), False, URL('default', 'supplier')),
            (T('Statistics'), False, URL('default', 'stats')),
            (T('Products'), False, URL('default', 'products')),
            (T('Staff'), False, URL('default', 'staff')),
            (T('Data Normalization'), False, URL('default', 'normalization')),
            (T('Image Manager'), False, URL('default', 'image')),
            (T('Tag Manager'), False, URL('default', 'tag')),
        ]

if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()
