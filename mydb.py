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
        self.engine = create_engine('sqlite:///C:\workshop\python\order\db\mydb.sqlite3',echo=False)
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
        
        db = DB(id = 1, name = 'XGP11', user = 'helios', password = 'helios', tns = 'XGP1', deploy_time = '00:05', \
                remark = '第1组高频交易库')
        self.session.add(db)
    
        db = DB(id = 2, name = 'XGP21', user = 'helios', password = 'helios', tns = 'XGP2', deploy_time = '00:05', \
                remark = '第2组高频交易库')
        self.session.add(db)
    
        db = DB(id = 3, name = 'XGP31', user = 'helios', password = 'helios', tns = 'XGP3', deploy_time = '00:05', \
                remark = '第3组高频交易库')
        self.session.add(db)
    
        db = DB(id = 4, name = 'XGP41', user = 'helios', password = 'helios', tns = 'XGP4', deploy_time = '02:05', \
                remark = '第4组高频交易库')
        self.session.add(db)
    
        db = DB(id = 5, name = 'XGP61', user = 'helios', password = 'helios', tns = 'XGP6', deploy_time = '22:05', \
                remark = '第6组高频交易库')
        self.session.add(db)
    
        db = DB(id = 6, name = 'XGP71', user = 'helios', password = 'helios', tns = 'XGP7', deploy_time = '02:35', \
                remark = '第7组高频交易库')
        self.session.add(db)
    
        db = DB(id = 7, name = 'CLCTGP', user = 'aeg2', password = 'aeg2', tns = 'CLCT', deploy_time = '02:10', \
                remark = '高频归集库')
        self.session.add(db)
    
        db = DB(id = 8, name = 'Aegean2', user = 'xgp_check', password = 'xgp_check', tns = 'aegean2', deploy_time = '10:30', \
                remark = '高频计奖验证库')
        self.session.add(db)
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
        
        #初始化系统编码数据
        #应用变更类型
        sc = System_Code_Def(id = 1, name = 'APP_CHANGE_TYPE', remark = '应用程序变更类型')
        self.session.add(sc)
        
        kv = KV(id = 101, system_code_id = 1, key = 1, val = '新增')
        self.session.add(kv)
        
        kv = KV(id = 102, system_code_id = 1, key = 2, val = '修改')
        self.session.add(kv)
        
        kv = KV(id = 103, system_code_id = 1, key = 3, val = '删除')
        self.session.add(kv)
        
        kv = KV(id = 104, system_code_id = 1, key = 4, val = '数据维护')
        self.session.add(kv)
        
        sc = System_Code_Def(id = 2, name = 'ORDER_PRODUCT', remark = '工单发布物')
        self.session.add(sc)
        
        kv = KV(id = 201, system_code_id = 2, key = 1, val = '实施文档')
        self.session.add(kv)
        
        kv = KV(id = 202, system_code_id = 2, key = 2, val = '生产确认单')
        self.session.add(kv)
        
        kv = KV(id = 203, system_code_id = 2, key = 3, val = '设计文档')
        self.session.add(kv)
        
        kv = KV(id = 204, system_code_id = 2, key = 4, val = '单元测试报告')
        self.session.add(kv)
        
        kv = KV(id = 205, system_code_id = 2, key = 5, val = '应用程序')
        self.session.add(kv)
        
        kv = KV(id = 206, system_code_id = 2, key = 6, val = '普通工单审核')
        self.session.add(kv)
        
        kv = KV(id = 207, system_code_id = 2, key = 7, val = '关键工单审核')
        self.session.add(kv)
        
        kv = KV(id = 208, system_code_id = 2, key = 8, val = '综合实施文档')
        self.session.add(kv)
        
        kv = KV(id = 209, system_code_id = 2, key = 9, val = '推广工单实施文档')
        self.session.add(kv)
              
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
    app_id = Column(Integer)
    program_name = Column(String)
    url = Column(String)
    rbk_program_name = Column(String)
    current_ver = Column(String)
    old_ver = Column(String)
    app_change_type = Column(Integer)

class System_Code_Def(Base):
    '''
    系统编码定义表
    '''
    __tablename__ = 'system_code'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    remark = Column(String)

class KV(Base):
    '''
    系统编码key、value表
    '''
    __tablename__ = 'kv'
    id = Column(Integer, primary_key = True)
    system_code_id = Column(Integer)
    key = Column(Integer)
    val = Column(String)
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
    batch_id = Column(Integer)

class Order_Batch_DB(Base):
    '''
    工单分批与DB的对应关系，即每批实施的工单对应的数据库
    '''
    __tablename__ = 'order_batch_db'
    id = Column(Integer, primary_key = True)
    order_no = Column(String)
    batch_id = Column(Integer)
    db_id = Column(Integer)

class Order_App_DB(Base):
    '''
    应用程序对应DB
    '''
    __tablename__ = 'order_app_db'
    id = Column(Integer, primary_key = True)
    order_no = Column(String)
    app_id = Column(Integer)
    db_id = Column(Integer)

class Template(Base):
    '''
    模板相关信息
    '''
    __tablename__ = 'template'
    id = Column(Integer, primary_key = True)
    file_name = Column(String)
    url = Column(String)
    remark = Column(String)


if __name__ == '__main__':
    mydb = MyDB()
    mydb.metadata.create_all(mydb.engine)
    mydb.initialData()
    mydb.session.close()
    print('应用程序执行完毕！')
#Base.metadata.create_all(engine)
'''
session = Session()
#ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)
session.commit()
#session.rollback()
'''
