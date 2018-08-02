#-*- coding:utf-8 -*-
import os
class SVN():
    '''
    版本控制相关操作类
    '''
    def __init__(self):
        '''
        初始化函数
        '''
        self.svn_info = {'deploy_docx_path': r'c:\workshop\gp\db\Aegean2_update',
                         'check_docx_path': r'c:\workshop\gp\db\Aegean2_update',
                         'clctgp_path': r'C:\workshop\gp\高频归集\trunk\script\update',
                         'app_path': r'C:\workshop\gp\app',
                         'pvdb_path': r'c:\workshop\gp\db\Aegean2_update',
                         'dbdd_path': r'C:\workshop\单项设计文档',
                         'test_docx_path': r'C:\workshop\单元测试报告',                         
                         }
    
    def update(self, path):
        '''
        更新SVN目录，获取最新的文件
        '''
        os.system(r'tortoiseproc.exe /command:update /path:"'+path+'" /closeonend:1')
    def add(self, path, file):
        '''
        向svn目录增加文件
        '''
        svn_add=r'tortoiseproc.exe /command:add /path:"'+ os.path.join(path, file)+r'" /closeonend:1'
        os.system(svn_add)
    def commit(self, path, file, msg):
        '''
        向svn目录提交文件
        '''
        svn_commit=r'tortoiseproc.exe /command:commit /path:"'+os.path.join(path, file)+r'" /logmsg:"'+msg+'" /closeonend:1'
        os.system(svn_commit)        