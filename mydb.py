# -*- coding:utf-8 -*-
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
import os

#engine = create_engine('sqlite:///C:\workshop\python\order\db\mydb.sqlite3',echo=True)
#engine = create_engine('sqlite:///:memory:',echo=True)
#Session = sessionmaker(bind=engine)
Base = declarative_base()

class MyDB(object):
    '''
    数据库类
    '''
    def __init__(self):
        '''
        初始化函数
        '''
        self.engine = create_engine('sqlite:///C:\workshop\python\order\db\mydb.sqlite3',echo=True)
        Session = sessionmaker(bind= self.engine)
        self.session = Session()
        self.metadata = Base.metadata
    
    def add(self, rec):
        '''
        向表中插入一条记录
        '''
        try:
            self.session.add(rec)
        except:
            pass
        else:
            self.session.commit()
        
    def initialData(self):
        '''
        初始化数据
        '''
        #初始化person
        self.session.query(Person).delete()      
       
        person = Person(id = 1, name = '张志远', telephone = '7443', mobile = '13910572957')
        self.add(person)
        
        person = Person(id = 2, name = '张春生', telephone = '7563', mobile = '13651172210')
        self.add(person)
        
        person = Person(id = 3, name = '陈伟', telephone = '7526', mobile = '15010119690')
        self.add(person)
        
        person = Person(id = 4, name = '王羿', telephone = '7558', mobile = '15311424097')
        self.add(person)
        
        person = Person(id = 5, name = '邓力飞', telephone = '7511', mobile = '13810247501')
        self.add(person)
        
        person = Person(id = 6, name = '田恩辉', telephone = '7524', mobile = '13522051280')
        self.add(person)
        
        self.session.commit()
        
        #初始化db
        self.session.query(DB).delete()
        
        db = DB(id = 1, name = 'XGP11', user = 'helios', password = 'helios', tns = 'XGP1', deploy_time = '00:05')
        self.session.add(db)
    
        db = DB(id = 2, name = 'XGP21', user = 'helios', password = 'helios', tns = 'XGP2', deploy_time = '00:05')
        self.session.add(db)
    
        db = DB(id = 3, name = 'XGP31', user = 'helios', password = 'helios', tns = 'XGP3', deploy_time = '00:05')
        self.session.add(db)
    
        db = DB(id = 4, name = 'XGP41', user = 'helios', password = 'helios', tns = 'XGP4', deploy_time = '02:05')
        self.session.add(db)
    
        db = DB(id = 5, name = 'XGP61', user = 'helios', password = 'helios', tns = 'XGP6', deploy_time = '22:05')
        self.session.add(db)
    
        db = DB(id = 6, name = 'XGP71', user = 'helios', password = 'helios', tns = 'XGP7', deploy_time = '02:35')
        self.session.add(db)
    
        db = DB(id = 7, name = 'CLCTGP', user = 'aeg2', password = 'aeg2', tns = 'CLCT', deploy_time = '')
        self.session.add(db)
    
        db = DB(id = 8, name = 'Aegean2', user = 'xgp_check', password = 'xgp_check', tns = 'aegean2', deploy_time = '10:30')
        self.session.add(db)
        self.session.commit()
        
        #初始化product        
        self.session.query(Product).delete()
        
        p = Product(id = 1, product_name = '实施文档')
        self.session.add(p)
    
        p = Product(id = 2, product_name = '生产确认单')
        self.session.add(p)
        
        p = Product(id = 3, product_name = '设计文档')
        self.session.add(p)
        
        p = Product(id = 4, product_name = '单元测试报告')
        self.session.add(p)
        
        p = Product(id = 5, product_name = '应用程序')
        self.session.add(p)
        
        p = Product(id = 6, product_name = '普通工单审核')
        self.session.add(p)
        
        p = Product(id = 8, product_name = '关键工单审核')
        self.session.add(p)
        
        p = Product(id = 9, product_name = '综合实施文档')
        self.session.add(p)
    
        p = Product(id = 10, product_name = '推广工单实施文档')
        self.session.add(p)
        self.session.commit()
        
        #初始化template
        self.session.query(Template).delete()
        template_path = r'C:\workshop\python\order\template'
        t = Template(id = 1, file_name = os.path.join(template_path, 'deploy_docx_template_all.docx'), \
                     remark = '实施文档模板')
        self.session.add(t)
    
        t = Template(id = 2, file_name = os.path.join(template_path, 'check_docx_template.docx'), \
                     remark = '生产确认单模板')
        self.session.add(t)
    
        t = Template(id = 3, file_name = os.path.join(template_path, 'dbdd_template.docx'), \
                         remark = '设计文档模板')
        self.session.add(t)
        
        t = Template(id = 4, file_name = os.path.join(template_path, 'testdocx_template.docx'), \
                         remark = '测试报告模板')
        self.session.add(t)
        
        t = Template(id = 5, file_name = os.path.join(template_path, 'intergrate_docx_template.docx'), \
                         remark = '综合实施文档模板')
        self.session.add(t)
        
        t = Template(id = 6, file_name = os.path.join(template_path, 'xgp_template_all.sql'), \
                         remark = '高频交易库all.sql模板')
        self.session.add(t)
        
        t = Template(id = 7, file_name = os.path.join(template_path, 'xgp_template_config.ini'), \
                         remark = '高频交易库config.ini模板')
        self.session.add(t)
        
        t = Template(id = 8, file_name = os.path.join(template_path, 'xgp_template_readme.txt'), \
                         remark = '高频交易库readme.txt模板')
        self.session.add(t)
        
        t = Template(id = 9, file_name = os.path.join(template_path, 'xgp_template_special_update.sql'), \
                         remark = '高频交易库special_update.sql模板')
        self.session.add(t)
        
        t = Template(id = 10, file_name = os.path.join(template_path, 'xgp_template_special_rollback.sql'), \
                         remark = '高频交易库special_rollback.sql模板')
        self.session.add(t)
        
        t = Template(id = 11, file_name = os.path.join(template_path, 'xgp_template_normal_update.sql'), \
                         remark = '高频交易库normal_update.sql模板')
        self.session.add(t)
        
        t = Template(id = 12, file_name = os.path.join(template_path, 'xgp_template_normal_rollback.sql'), \
                         remark = '高频交易库normal_rollback.sql模板')
        self.session.add(t)
        
        t = Template(id = 13, file_name = os.path.join(template_path, 'clctgp_template_all.sql'), \
                         remark = '高频归集库all.sql模板')
        self.session.add(t)
    
        t = Template(id = 14, file_name = os.path.join(template_path, 'clctgp_template_config.ini'), \
                         remark = '高频归集库config.ini模板')
        self.session.add(t)
    
        t = Template(id = 15, file_name = os.path.join(template_path, 'clctgp_template_readme.txt'), \
                         remark = '高频归集库readme.txt模板')
        self.session.add(t)
        
        t = Template(id = 16, file_name = os.path.join(template_path, 'clctgp_template_update.sql'), \
                         remark = '高频归集库clctgp_update.sql模板')
        self.session.add(t)         
        
        t = Template(id = 17, file_name = os.path.join(template_path, 'clctgp_template_rollback.sql'), \
                         remark = '高频归集库clctgp_rollback.sql模板')
        self.session.add(t)
        
        t = Template(id = 18, file_name = os.path.join(template_path, 'pvdb_template_all.sql'), \
                         remark = '高频计奖验证库all.sql模板')
        self.session.add(t)
    
        t = Template(id = 19, file_name = os.path.join(template_path, 'pvdb_template_config.ini'), \
                         remark = '高频计奖验证库config.ini模板')
        self.session.add(t)
    
        t = Template(id = 20, file_name = os.path.join(template_path, 'pvdb_template_readme.txt'), \
                         remark = '高频计奖验证库readme.txt模板')
        self.session.add(t)
        
        t = Template(id = 21, file_name = os.path.join(template_path, 'pvdb_template_update.sql'), \
                         remark = '高频计奖验证库pvdb_update.sql模板')
        self.session.add(t)         
    
        t = Template(id = 22, file_name = os.path.join(template_path, 'pvdb_template_rollback.sql'), \
                         remark = '高频计奖验证库pvdb_rollback.sql模板')
        self.session.add(t)        
        
        self.session.commit()
        
        #初始化task
        self.session.query(Task).delete()
        
        task = Task(id = 1, task_name = '编写实施文档')
        self.session.add(task)
        
        task = Task(id = 2, task_name = '编写生产确认单')
        self.session.add(task)
        
        task = Task(id = 3, task_name = '编写设计文档')
        self.session.add(task)
        
        task = Task(id = 4, task_name = '编写测试报告')
        self.session.add(task)
        
        task = Task(id = 5, task_name = '编写应用程序')
        self.session.add(task)
        
        task = Task(id = 6, task_name = '普通工单审核')
        self.session.add(task)
        
        task = Task(id = 7, task_name = '关键工单审核')
        self.session.add(task)        
        
        task = Task(id = 9, task_name = '编写综合实施文档')
        self.session.add(task)
        
        task = Task(id = 10, task_name = '编写推广工单实施文档')
        self.session.add(task)
        
        self.session.commit()
        pass
        

class Person(Base):
    '''
    人员信息表
    '''
    __tablename__= 'person'
    id= Column(Integer, primary_key=True)
    name = Column(String , unique = True)
    telephone = Column(String)
    mobile = Column(String)

class Order(Base):
    '''
    工单信息表
    '''
    __tablename__ = 'order'
    order_no = Column(String, primary_key = True)
    order_name = Column(String)
    developer_id = Column(Integer)
    director_id = Column(Integer)

class Product(Base):
    '''
    产出物信息表
    '''
    __tablename__ = 'product'
    id = Column(Integer, primary_key = True)
    product_name = Column(String)

class Order_Product(Base):
    '''
    工单产出物表
    '''
    __tablename__ = 'order_product'
    id = Column(Integer, primary_key = True)
    order_no = Column(String)
    product_id = Column(Integer)

class Order_App(Base):
    '''
    工单应用程序表
    '''
    __tablename__ = 'order_app'
    id = Column(Integer, primary_key = True)
    order_no = Column(String)
    program_name = Column(String)
    url = Column(String)
    rbk_program_name = Column(String)
    current_ver = Column(String)
    old_ver = Column(String)

class DB(Base):
    '''
    数据库信息表
    '''
    __tablename__ = 'db'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    user = Column(String)
    password = Column(String)
    tns = Column(String)
    deploy_time = Column(String)
    remark = Column(String)

class Order_Batch(Base):
    '''
    工单分批情况
    '''
    __tablename__ = 'order_batch'
    id = Column(Integer, primary_key = True)
    order_no = Column(String)
    batch_order_no = Column(String)
    batch_order_name = Column(String)
    batch_developer_id = Column(Integer)
    batch_director_id = Column(Integer)

class Template(Base):
    '''
    模板相关信息
    '''
    __tablename__ = 'template'
    id = Column(Integer, primary_key = True)
    file_name = Column(String)
    url = Column(String)
    remark = Column(String)

class Task(Base):
    '''
    通用工单任务信息表
    '''
    __tablename__ = 'task'
    id = Column(Integer, primary_key = True)
    task_name = Column(String)
    
class Order_Task(Base):
    '''
    工单任务表
    '''
    __tablename__ = 'order_task'
    id = Column(Integer, primary_key = True)
    order_no = Column(String)
    task_id = Column(Integer)
    task_status = Column(String)
    


if __name__ == '__main__':
    mydb = MyDB()
    mydb.metadata.create_all(mydb.engine)
    mydb.initialData()
    mydb.session.close()
#Base.metadata.create_all(engine)
'''
session = Session()
#ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)
session.commit()
#session.rollback()
'''
