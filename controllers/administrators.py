'''
Created on 08/12/2013

@author: Hugo
'''
# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is the controller for users with Administration privileges
## to administrate the database
#########################################################################

import math

def show_operators():
    """
    This action lists all the tourism operators that exist in the database.
    It orders them by operator name.
    """
    operators = db().select(db.operator.id, db.operator.name, orderby=db.operator.name)
    return dict(operators=operators)
    
def create_operator():
    """
    This action creates an tourism operator in the database.
    It creates a form with the fields corresponding to a table row.
    """
    form = SQLFORM(db.operator).process(next=URL('show_operators'))
    return dict(form=form)
    
def show_operator():
    """
    This action shows a tourism operator and its contacts.
    """
    this_operator = db.operator(request.args(0,cast=int)) or redirect(URL('show_operators'))
    db.contact.operator_id.default = this_operator.id
    operator_contacts = db(db.contact.operator_id==this_operator.id).select()
    return dict(operator=this_operator, contacts=operator_contacts)

def modify_operator_form_processing(form, this_operator):
    """
    Check if operator is empty on deletion
    """
    if form.deleted:
        contacts = db(db.contact.operator_id==this_operator.id).select()
        services = db(db.service.operator_id==this_operator.id).select()
        if(contacts or services):
            form.errors.deleted  = T("Operator contains services.\nDelete them first.")

def modify_operator():
    """
    This action allows the user to modify or delete an operator in the database.
    """
    this_operator = db.operator(request.args(0,cast=int)) or redirect(URL('show_operators'))
    #form = SQLFORM(db.operator, this_operator, deletable=True).process(next=URL('show_operator', args=this_operator.id))
    form = SQLFORM(db.operator, this_operator, deletable=True)
    if form.validate():
        # If selected for deletion
        if form.deleted:
            contacts = db(db.contact.operator_id==this_operator.id).select()
            services = db(db.service.operator_id==this_operator.id).select()
            i = 0
            #for contact in contacts:
            #    i = i+1
            for service in services:
                i = i+1
            # If operator has no contacts or services associated
            if(i==0):
                db(db.operator.id==this_operator.id).delete()
                session.flash  = T("Operator deleted")
                redirect(URL('show_operators'))
            # If operator contains contacts or services associated
            else:
                session.flash  = T("Operator contains services. Delete them first.")
                #redirect(URL('show_operator', args=this_operator.id))
        else:
            this_operator.update_record(**dict(form.vars))
            session.flash = T('record updated')
            #redirect(URL('show_operator', args=this_operator.id))          
        redirect(URL('show_operator', args=this_operator.id))
    return dict(form=form, operator=this_operator)

def search_operator():
    """An AJAX to search operators by name"""
    form = FORM(INPUT(_id='keyword', _name='keyword', _onkeyup="ajax('callback_operator', ['keyword'], 'target');"))
    return dict(form=form, target_div=DIV(_id='target'))

def callback_operator():
    """An AJAX callback function that returns a list of links to operators"""
    query = db.operator.name.contains(request.vars.keyword)
    operators = db(query).select(orderby=db.operator.name)
    links = [DIV(A(op.name, _href=URL('show_operator', args=op.id))) for op in operators]
    return SPAN(*links)

###########################################################################################
def contact_form_processing(form):
    if (not form.vars.name and not form.vars.surname):
        form.errors.name = T('Name or surname cannot be empty')
        form.errors.surname = T('Name or surname cannot be empty')
    if (not form.vars.phone and not form.vars.mobile):
        form.errors.phone = T('Please enter one contact number')
        form.errors.mobile = T('Please enter one contact number')
    if (IS_EMAIL()(form.vars.email)[1] != None):
        form.errors.email = IS_EMAIL()(form.vars.email)[1]

def create_contact():
    """
    This action creates an tourism operator's contact in the database.
    It creates a form with the fields corresponding to a table row.
    """
    this_operator = db.operator(request.args(0,cast=int)) or redirect(URL('show_operators'))
    db.contact.operator_id.default = this_operator.id
    form = SQLFORM(db.contact)
    if form.process(onvalidation=contact_form_processing).accepted:
        redirect(URL('show_operator', args=this_operator.id))
    return dict(form=form, operator=this_operator)
    
def show_contact():
    """
    This action shows a tourism operator contact details.
    """
    this_contact = db.contact(request.args(0,cast=int)) or redirect(URL('show_operators'))
    return dict(contact=this_contact)

def modify_contact():
    """
    This action modifies or deletes an operator contact.
    """
    this_contact = db.contact(request.args(0,cast=int)) or redirect(URL('show_operators'))
    form = SQLFORM(db.contact, this_contact, deletable=True).process(next=URL('show_operator', args=this_contact.operator_id))
    #form = SQLFORM(db.operator, this_operator, deletable=True)
    return dict(form=form, contact=this_contact)

###########################################################################################        
def create_service():
    """
    This action creates an tourism operator's service in the database.
    It creates a form with the fields corresponding to a table row.
    """
    this_operator = db.operator(request.args(0,cast=int)) or redirect(URL('show_operators'))
    db.service.operator_id.default = this_operator.id
    db.service.mean_rating.default = 1.00
    db.service.comission.default = 0.15
    form = SQLFORM(db.service).process(next=URL('show_services', args=this_operator.id))
    return dict(form=form, operator=this_operator)
    
def show_services():
    """
    This action lists all the services available for a tourism operator.
    It orders them by service name.
    """
    this_operator = db.operator(request.args(0,cast=int)) or redirect(URL('show_operators'))
    services = db(db.service.operator_id==this_operator.id).select(db.service.id, db.service.name, orderby=db.service.name)
    return dict(services=services, operator=this_operator)
    
def show_service():
    """
    This action shows a tourism service details.
    """
    this_service = db.service(request.args(0,cast=int)) or redirect(URL('show_services', args=request.args(1,cast=int))) or redirect(URL('show_operators'))
    # Correct selling price
    if (not this_service.selling_price):
        this_service.selling_price = this_service.operator_price * (1 + this_service.comission)
    # Select service extensions
    db.service_extension.service_id.default = this_service.id
    service_extensions = db(db.service_extension.service_id==this_service.id).select()
    # Correct service extensions selling price
    for extension in service_extensions:
        if (not extension.selling_price):
            extension.selling_price = extension.operator_price * (1 + extension.comission)
    # Select photos
    photos = db(db.photo.service_id==this_service.id).select()
    # Select comments
    comments = db(db.cust_comment.service_id==this_service.id).select()
    # Determine service 'mean_rating'
    i = 0
    sm = 0
    for comment in comments:
        i = i+1
        sm = sm + comment.rating
    if (i != 0 and sm != 0):
        this_service.mean_rating = round(float(sm)/float(i), 2)
    else:
        this_service.mean_rating = 0.00
    # Add a new comment
    db.cust_comment.service_id.default = this_service.id
    form = SQLFORM(db.cust_comment).process(next=URL('show_service', args=this_service.id))
    return dict(service=this_service, extensions=service_extensions, photos=photos, comments=comments, form=form)

def modify_service():
    """
    This action modifies or deletes an operator service.
    """
    this_service = db.service(request.args(0,cast=int)) or redirect(URL('show_service', request.args(0,cast=int)))
    form = SQLFORM(db.service, this_service, deletable=True).process(next=URL('show_service', args=[this_service.id, this_service.operator_id]))
    return dict(form=form, service=this_service)

def search_service():
    """An AJAX to search this operator services by name"""
    this_operator = db.operator(request.args(0,cast=int)) or redirect(URL('show_operators'))
    form = FORM(INPUT(_id='keyword', _name='keyword', _onkeyup="ajax('callback_service', ['keyword'], 'target2');"))
    return dict(form=form, target_div=DIV(_id='target2'), operator=this_operator)

def callback_service():
    """An AJAX callback function that returns a <ul> of links to this operator services"""
    query = db.service.name.contains(request.vars.keyword)
    #services = db(query.operator_id==request.vars.this_operator.id).select(orderby=db.service.name)
    services = db(query).select(orderby=db.service.name)
    links = [A(serv.name, _href=URL('show_service', args=serv.id)) for serv in services]
    return UL(*links)

###########################################################################################
def delete_comment():
    """
    This action deletes a comment associated with a tourism service.
    """
    this_comment = db.cust_comment(request.args(0,cast=int)) or redirect(URL('show_operators'))
    this_service = db.service(this_comment.service_id)
    db(db.cust_comment.id==this_comment.id).delete()
    session.flash  = T("Comment deleted")
    redirect(URL('show_service', args=this_service.id))
    return

###########################################################################################
def create_service_extension():
    """
    This action creates an extension to a  tourism operator's service in the database.
    It creates a form with the fields corresponding to a table row.
    """
    this_service = db.service(request.args(0,cast=int)) or redirect(URL('show_operators'))
    db.service_extension.service_id.default = this_service.id
    db.service_extension.comission.default = 0.15
    form = SQLFORM(db.service_extension).process(next=URL('show_service', args=this_service.id))
    return dict(form=form, service=this_service)

def modify_service_extension():
    """
    This action modifies or deletes a service extension associated with a tourism service.
    """
    this_extension = db.service_extension(request.args(0,cast=int)) or redirect(URL('show_operators'))
    this_service = db.service(this_extension.service_id)
    form = SQLFORM(db.service_extension, this_extension, deletable=True).process(next=URL('show_service', args=this_service.id))
    #db(db.service_extension.id==this_extension.id).delete()
    #session.flash  = "Service extension deleted"
    #redirect(URL('show_service', args=this_service.id))
    return dict(form=form, service=this_service)


###########################################################################################
def upload_photo():
    """
    This action adds a photo to the database and assigns it to a Service.
    """
    this_service = db.service(request.args(0,cast=int)) or redirect(URL('show_operators'))
    db.photo.service_id.default = this_service.id
    form = SQLFORM(db.photo).process(next=URL('show_service', args=this_service.id))
    return dict(form=form, service=this_service)
    
def download_photo():
    """
    This action downloads a photo to be shown on screen.
    """
    return response.download(request, db)

def show_photo():
    """
    This action shows a photo on screen.
    """
    this_photo = db.photo(request.args(0,cast=int)) or redirect(URL('show_operators'))
    return dict(photo=this_photo)

def show_photos():
    """
    This action shows all photos on screen of a given service.
    """
    this_service = db.service(request.args(0,cast=int)) or redirect(URL('show_operators'))
    photos = db(db.photo.service_id==this_service.id).select()
    return dict(service=this_service, photos=photos)

def modify_photo():
    """
    This action modifies or deletes a photo.
    """
    this_photo = db.photo(request.args(0,cast=int)) or redirect(URL('show_operators'))
    form = SQLFORM(db.photo, this_photo, deletable=True).process(next=URL('show_service', args=this_photo.service_id))
    return dict(form=form, photo=this_photo)

