# -*- coding: utf-8 -*-

#------------------------------------------------------------
# Table that defines the tourism segments that an operator
# or tourism service operates in
#------------------------------------------------------------
db.define_table('tourism_segment',
    Field('segment_name', requires=IS_NOT_EMPTY()),
    Field('comment', 'text'),
    format='%(segment_name)s')

#------------------------------------------------------------
# Table that defines the tourism country that an operator
# is located at, or a tourism service operates at
#------------------------------------------------------------
db.define_table('country',
    Field('country_name'),
    format='%(country_name)s')

#------------------------------------------------------------
# Table that defines the tourism regions that an operator
# is located at, or a tourism service operates at
#------------------------------------------------------------
db.define_table('region',
    Field('region_name'),
    Field('region_country', 'reference country'),
    Field('mean_temperature', 'integer'),
    Field('comments', 'text'),
    format='%(region_name)s')

#------------------------------------------------------------
# Table that defines the district that a tourism service 
# operates at 
#------------------------------------------------------------
db.define_table('district',
    Field('district_name'),
    Field('district_region', 'reference region'),
    Field('mean_temperature', 'integer'),
    Field('comments', 'text'),
    format='%(district_name)s')


#------------------------------------------------------------
# Table that defines the county that a tourism service 
# operates at 
#------------------------------------------------------------
db.define_table('county',
    Field('county_name'),
    Field('county_district', 'reference district'),
    Field('mean_temperature', 'integer'),
    Field('comments', 'text'),
    format='%(county_name)s')

#------------------------------------------------------------
# Table that defines the city that a tourism service 
# operates at 
#------------------------------------------------------------
db.define_table('city',
    Field('city_name'),
    Field('city_county', 'reference county'),
    Field('mean_temperature', 'integer'),
    Field('comments', 'text'),
    format='%(city_name)s')

