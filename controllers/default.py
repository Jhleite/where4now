# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is the main controller
## - index is the default action of any application
#########################################################################

def index():
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
    form = SQLFORM(db.operator).process(next=URL('index'))
    return dict(form=form)
    
def show_operator():
    """
    This action shows a tourism operator and its contacts.
    """
    this_operator = db.operator(request.args(0,cast=int)) or redirect(URL(index))
    db.contact.operator_id.default = this_operator.id
    operator_contacts = db(db.contact.operator_id==this_operator.id).select()
    return dict(operator=this_operator, contacts=operator_contacts)
    
###########################################################################################
def contact_form_processing(form):
    if (not form.vars.name and not form.vars.surname):
        form.errors.name = 'Name or surname cannot be empty'
        form.errors.surname = 'Name or surname cannot be empty'
    if (not form.vars.phone and not form.vars.mobile):
        form.errors.phone = 'Please enter one contact number'
        form.errors.mobile = 'Please enter one contact number'
    if (IS_EMAIL()(form.vars.email)[1] != None):
        form.errors.email = IS_EMAIL()(form.vars.email)[1]

def create_contact():
    """
    This action creates an tourism operator's contact in the database.
    It creates a form with the fields corresponding to a table row.
    """
    this_operator = db.operator(request.args(0,cast=int)) or redirect(URL(index))
    db.contact.operator_id.default = this_operator.id
    form = SQLFORM(db.contact)
    if form.process(onvalidation=contact_form_processing).accepted:
        redirect(URL('show_operator', args=this_operator.id))
    return dict(form=form, operator=this_operator)
    
def show_contact():
    """
    This action shows a tourism operator contact details.
    """
    this_contact = db.contact(request.args(0,cast=int)) or redirect(URL(index))
    return dict(contact=this_contact)

###########################################################################################        
def create_service():
    """
    This action creates an tourism operator's service in the database.
    It creates a form with the fields corresponding to a table row.
    """
    this_operator = db.operator(request.args(0,cast=int)) or redirect(URL(index))
    db.service.operator_id.default = this_operator.id
    db.service.mean_rating.default = 1.00
    db.service.comission.default = 0.15
    form = SQLFORM(db.service).process(next=URL('show_operator', args=this_operator.id))
    return dict(form=form, operator=this_operator)
    
def show_services():
    """
    This action lists all the services available for a tourism operator.
    It orders them by service name.
    """
    this_operator = db.operator(request.args(0,cast=int)) or redirect(URL(index))
    services = db(db.service.operator_id==this_operator.id).select(db.service.id, db.service.name, orderby=db.service.name)
    return dict(services=services, operator=this_operator)
    
def show_service():
    """
    This action shows a tourism service details.
    """
    this_service = db.service(request.args(0,cast=int)) or redirect(URL(index))
    # Correct selling price
    if (not this_service.selling_price):
        mult = 1 + this_service.comission
        price = this_service.operator_price * mult
        this_service.selling_price = price
    # Select service extensions
    db.service_extension.service_id.default = this_service.id
    service_extensions = db(db.service_extension.service_id==this_service.id).select()
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
        this_service.mean_rating = float(sm)/float(i)
    else:
        this_service.mean_rating = 1.00
    # Add a new comment
    db.cust_comment.service_id.default = this_service.id
    form = SQLFORM(db.cust_comment).process(next=URL('show_service', args=this_service.id))
    return dict(service=this_service, extensions=service_extensions, photos=photos, comments=comments, form=form)

###########################################################################################
def create_service_extension():
    """
    This action creates an extension to a  tourism operator's service in the database.
    It creates a form with the fields corresponding to a table row.
    """
    this_service = db.service(request.args(0,cast=int)) or redirect(URL(index))
    db.service_extension.service_id.default = this_service.id
    form = SQLFORM(db.service_extension).process(next=URL('show_service', args=this_service.id))
    return dict(form=form, service=this_service)


###########################################################################################
def upload_photo():
    """
    This action adds a photo to the database and assigns it to a Service.
    """
    this_service = db.service(request.args(0,cast=int)) or redirect(URL(index))
    db.photo.service_id.default = this_service.id
    form = SQLFORM(db.photo).process(next=URL('show_service', args=this_service.id))
    return dict(form=form, service=this_service)
    
def download_photo():
    """
    This action downloads a photo to be shown on screen.
    """
    return response.download(request, db)
