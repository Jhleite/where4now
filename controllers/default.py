# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is the main controller
## - index is the default action of any application
#########################################################################

def index():
    """
    This action redirects to the action show_operators in the administrators.py controller.
    It is intended to be modified soon.
    """
    
    redirect(URL('administrators', 'show_operators'))
    return
    
