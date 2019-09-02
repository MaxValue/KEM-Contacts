# -*- coding: utf-8 -*-

import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base as sqla_declarative_base

Base = sqla_declarative_base()

class Spider(Base):
	'''Used to declare a spider'''
	__tablename__ = 'spiders'
	id = sqla.Column('id', sqla.Integer, primary_key=True)
	project = sqla.Column('project', sqla.String)
	name = sqla.Column('name', sqla.String, nullable=False)

class FinishReason(Base):
	'''Used to declare a finishing reason'''
	__tablename__ = 'finishingreasons'
	id = sqla.Column('id', sqla.Integer, primary_key=True)
	name = sqla.Column('name', sqla.String, nullable=False)
	description = sqla.Column('description', sqla.String)

class Job(Base):
	'''Used to declare a crawling job'''
	__tablename__ = 'jobs'
	id = sqla.Column('id', sqla.Integer, primary_key=True)
	finishingReason_id = sqla.Column('finishingReason_id', None, sqla.ForeignKey('finishingreasons.id'))
	spider_id = sqla.Column('spider_id', None, sqla.ForeignKey('spiders.id'), nullable=False)
	timeStart = sqla.Column('timeStart', sqla.TIMESTAMP, nullable=False)
	timeEnd = sqla.Column('timeEnd', sqla.TIMESTAMP)

	finishingReason = sqla.orm.relationship('FinishReason', back_populates='jobs')
	spider = sqla.orm.relationship('Spider', back_populates='jobs')

FinishReason.jobs = sqla.orm.relationship('Job', order_by=Job.timeStart, back_populates='finishingReason')
Spider.jobs = sqla.orm.relationship('Job', order_by=Job.timeStart, back_populates='spider')

class Item(Base):
	'''Used to declare an item'''
	__tablename__ = 'items'
	id = sqla.Column('id', sqla.Integer, primary_key=True)
	job_id = sqla.Column('job_id', None, sqla.ForeignKey('jobs.id'))

	job = sqla.orm.relationship('Job', back_populates='items')

Job.items = sqla.orm.relationship('Item', order_by=Item.id, back_populates='job')

class Data(Base):
	'''Used to declare a data field of an item'''
	__tablename__ = 'data'
	id = sqla.Column('id', sqla.Integer, primary_key=True)
	item_id = sqla.Column('item_id', None, sqla.ForeignKey('items.id'), nullable=False)
	name = sqla.Column('name', sqla.String, nullable=False)
	value = sqla.Column('value', sqla.String)

	item = sqla.orm.relationship('Item', back_populates='fields')

Item.fields = sqla.orm.relationship('Data', order_by=Data.name, back_populates='item')

def init_session(database_path, echo_commands=False):
	full_database_path = 'sqlite+pysqlite:///{}'.format(database_path)
	engine = sqla.create_engine(full_database_path, echo=echo_commands)
	Base.metadata.create_all(engine)
	Session = sqla.orm.sessionmaker(bind=engine)
	session = Session()
	return session
