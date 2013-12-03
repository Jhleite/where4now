# -*- coding: utf-8 -*-

db = DAL('sqlite://storage.sqlite')
#db = DAL('postgres://Hugo:Satriani@localhost/db')
#db = DAL('postgres://postgres:Satriani@localhost:5432/where4now')

from gluon.tools import *
#auth = Auth(db)
#auth.define_tables()
#crud = Crud(db)

#------------------------------------------------------------
# Table that defines a touristic operator
# - GPS coordinates of the building, operator code, NIF and
#   NIB shopuld be unique
# - segments : Tourism segments of operation (list)
# - regions  : Regions of operation (list)
#------------------------------------------------------------
db.define_table('operator',
    Field('name'),
    Field('code', 'integer'),
    Field('nif', 'integer'),
    Field('nib', 'integer'),
    Field('address'),
    Field('postal_code'),
    Field('town'),
    Field('country', 'string'),
    Field('email'),
    Field('website'),
    Field('gpscoord', unique=True),
    Field('tourism_segments', 'list:string'),
    Field('regions', 'list:string'),
    format='%(name)s')

db.operator.id.writable = False
db.operator.name.requires = IS_NOT_IN_DB(db, 'operator.name')
db.operator.code.requires = IS_NOT_IN_DB(db, 'operator.code')
db.operator.nif.requires  = IS_NOT_IN_DB(db, 'operator.nif')
db.operator.nib.requires  = IS_NOT_IN_DB(db, 'operator.nib')
db.operator.email.requires = IS_EMAIL()
db.operator.country.requires = IS_IN_SET(('Portugal', 'Spain'))
db.operator.tourism_segments.requires = IS_IN_SET(('Cultural and Landscape',
                                                   'City Break',
                                                   'Nature',
                                                   'Nautical',
                                                   'Golf',
                                                   'Gastronomy and Whine',
                                                   'Integrated Resorts',
                                                   'Residential',
                                                   'Health and Wellbeing',
                                                   'Sun and Sea',
                                                   'Business'), multiple=True)
db.operator.regions.requires = IS_IN_SET(('Algarve',
                                          'Alentejo',
                                          'Madeira',
                                          'Azores',
                                          'Lisboa',
                                          'Porto',
                                          'Center',
                                          'North'), multiple=True)

#--------------------------------------------------------
# People of contact for a given touristic operator
#--------------------------------------------------------
db.define_table('contact',
    Field('operator_id', 'reference operator'),
    Field('name'),
    Field('surname'),
    Field('professional_position'),
    Field('phone', 'integer'),
    Field('mobile', 'integer'),
    Field('fax', 'integer'),
    Field('email'),
    Field('observations', 'text'),
    format='%(name)s')

db.contact.operator_id.requires = IS_IN_DB(db, db.operator.id)
db.contact.operator_id.writable = db.contact.operator_id.readable = False


#---------------------------------------------------------
# Services available for a given touristic operator
#---------------------------------------------------------
db.define_table('service',
    Field('operator_id', 'reference operator'),
    Field('name'),
    Field('code'),
    Field('risk_level', 'integer'),
    Field('selling_price', 'float'),
    Field('operator_price', 'float'),
    Field('comission', 'float'),
    Field('opening_time', 'time'),
    Field('closing_time', 'time'),
#    Field('start_time', 'time'),
    Field('duration', 'time'),
    Field('mean_rating', 'float'),
    Field('gpscoord'),
    Field('tourism_segments', 'list:string'),
    Field('region', 'string'),
    format='%(name)s')
   
db.service.operator_id.requires = IS_IN_DB(db, db.operator.id)
db.service.name.requires = IS_NOT_EMPTY() 
db.service.code.requires = IS_NOT_IN_DB(db, 'service.code')
db.service.risk_level.requires = IS_IN_SET((1,2,3,4,5,6))
db.service.selling_price.readable = db.service.selling_price.writable = False
db.service.comission.requires = IS_FLOAT_IN_RANGE(0, 2)
db.service.comission.readable = db.service.comission.writable = False
db.service.mean_rating.requires = IS_FLOAT_IN_RANGE(1, 5)
db.service.mean_rating.readable = db.service.mean_rating.writable = False
db.service.gpscoord.requires = IS_NOT_IN_DB(db, db.service.gpscoord)
db.service.tourism_segments.requires = IS_IN_SET(('Cultural and Landscape',
                                                  'City Break',
                                                  'Nature',
                                                  'Nautical',
                                                  'Golf',
                                                  'Gastronomy and Whine',
                                                  'Integrated Resorts',
                                                  'Residential',
                                                  'Health and Wellbeing',
                                                  'Sun and Sea',
                                                  'Business'))
db.service.region.requires = IS_IN_SET(('Algarve',
                                        'Alentejo',
                                        'Madeira',
                                        'Azores',
                                        'Lisboa',
                                        'Porto',
                                        'Center',
                                        'North'))
db.service.operator_id.writable = db.service.operator_id.readable = False   

#-------------------------------------------------------------
# Service extensions for a given touristic service
#-------------------------------------------------------------
db.define_table('service_extension',
    Field('service_id', 'reference service'),
    Field('name'),
    Field('selling_price', 'float'),
    Field('operator_price', 'float'),
    Field('comission', 'float'),
    format='%(name)s')

db.service_extension.service_id.requires = IS_IN_DB(db, db.service.id)    
db.service_extension.service_id.writable = db.service_extension.service_id.readable = False
db.service_extension.selling_price.writable = db.service_extension.selling_price.readable = False
db.service_extension.comission.requires = IS_FLOAT_IN_RANGE(0, 2)
db.service_extension.comission.writable = db.service_extension.comission.readable = False

#------------------------------------------------------------
# Photos for a given touristic service
#------------------------------------------------------------
db.define_table('photo',
    Field('service_id', 'reference service'),
    Field('title'),
    Field('file', 'upload'),
    format='%(title)s')

db.photo.service_id.requires = IS_IN_DB(db, db.service.id)
db.photo.title.requires = IS_NOT_IN_DB(db, 'photo.title')   
db.photo.service_id.writable = db.photo.service_id.readable = False

#------------------------------------------------------------
# Customer comments for a given touristic service
#------------------------------------------------------------
db.define_table('cust_comment',
    Field('service_id', 'reference service'),
    Field('rating', 'integer'),
    Field('comment', 'text'))
    
db.cust_comment.rating.requires = IS_IN_SET((1,2,3,4,5))
db.cust_comment.service_id.requires = IS_IN_DB(db, db.service.id)
db.cust_comment.service_id.writable = db.cust_comment.service_id.readable = False
