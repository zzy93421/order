#-*- coding:utf-8 -*-
import os
import shutil
import win32com
import time
from win32com.client import Dispatch,constants
from order_common import Order

class DBDD(Order):
    '''
    生成数据库设计文档
    '''
    def __init__(self, order_no, order_name, backup_tabs):
        '''
        初始化函数
        '''
        #调用父类的初始化函数
        super(DBDD,self).__init__(order_no,order_name,backup_tabs)
        self.order_info['svn']=r'D:\aeg2\Aegean2_update'
        self.order_info['ver']=self.getVer(self.order_info['svn'], self.order_info['order_name'], 'Aeg2DB_Build')
        self.order_info['work_order_path']=r'D:\05概要设计\02下一代系统\03最终成果\05DB\单项设计文档'
        self.dbdd_info={'create_date':time.strftime("%Y-%m-%d"),
                        'template_file':r'D:\workorder\template\dbdd_template.docx',
                        'dbdd_file':'',
                        }
    def createDBDD(self):
        '''
        创建DB设计文档
        '''
        f='高频设计文档_DB_'+self.order_info['ver'][5:]+'_'+self.order_info['order_name']+'.docx'
        self.dbdd_info['dbdd_file']=os.path.join(self.order_info['work_order_path'],f)
        shutil.copy(self.dbdd_info['template_file'],self.dbdd_info['dbdd_file'])
        
        w=win32com.client.DispatchEx('Word.Application')
        w.Visible=0
        w.DisplayAlerts=0
        #打开新的文件
        doc=w.Documents.Open(self.dbdd_info['dbdd_file'])
        
        w.Selection.Find.ClearFormatting()
        w.Selection.Find.Replacement.ClearFormatting()
        w.Selection.Find.Execute('{create_date}',False,False,False,False,False,True,1,True,self.dbdd_info['create_date'],2)
        w.Selection.Find.Execute('{order_name}',False,False,False,False,False,True,1,True,self.order_info['order_name'],2)
        w.Selection.Find.Execute('{order_no}',False,False,False,False,False,True,1,True,self.order_info['order_no'],2)
        
        
        doc.Close()
        w.Quit()
        