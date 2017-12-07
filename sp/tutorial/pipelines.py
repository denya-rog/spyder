# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Session
import os
from items import DataItem

"""creating database for datafrom site"""

Base = declarative_base()

class SpecTable(Base):
    __tablename__ = 'specdata'
    id = Column(Integer, primary_key=True)
    spec = Column(String)
    spectitle = Column(String)

    def __init__(self, spec, spectitle):
        self.spec= spec
        self.spectitle = spectitle

    def __repr__(self):
        return "<Data %s, %s>" % (self.spec, self.spectitle)


class DataTable(Base):
    """initing database"""
    __tablename__ = 'pars_data'
    id = Column(Integer, primary_key=True)
    ip_adress = Column(String)
    port = Column(Integer)

    def __init__(self, ip_adress,port):
        self.ip_adress = ip_adress
        self.port = port
       
    def __repr__(self):
        return "<Data %s, %s>" % (self.ip_adress, self.port)


class DataPipeline(object):
    """way of filling database"""
    
    def __init__(self):
        basename = 'data_scraped'
        self.engine = create_engine("sqlite:///%s" % basename, echo=False)
        if not os.path.exists(basename):
            Base.metadata.create_all(self.engine)
        

    def process_item(self, item, spider):
        if isinstance(item, DataItem): 
            
            dt = DataTable(item['ip_adresss'],item['port'])
            self.session.add(dt)
        return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)


