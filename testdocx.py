#-*- coding:utf-8 -*-
import os
import shutil
import datetime
import win32com
from win32com.client import DispatchEx,constants
from order_common import Order

class TestDocx(Order):
    '''
    生成单元测试报告文档
    '''
    def __init__(self, order_no, order_name, backup_tabs):
        '''
        初始化函数
        '''
        #调用父类的初始化函数
        super(TestDocx,self).__init__(order_no,order_name,backup_tabs)
        self.order_info['svn']=r'D:\aeg2\Aegean2_update'
        self.order_info['ver']=self.getVer(self.order_info['svn'], self.order_info['order_name'], 'Aeg2DB_Build')
        self.order_info['work_order_path']=r'D:\05概要设计\02下一代系统\03最终成果\05DB\单元测试报告'        
        self.testdocx_info={'template_file':r'D:\workorder\template\testdocx_template.docx',
                            'testdocx_file':'',
                            'start_date':'',
                            'end_date':'',
                            }
    def createTestDocx(self):
        '''
        创建测试报告文档
        '''
        self.testdocx_info['start_date']=datetime.date.today().strftime('%Y-%m-%d')
        self.testdocx_info['end_date']=(datetime.date.today()+datetime.timedelta(days=2)).strftime('%Y-%m-%d')
        f='高频单元测试报告_DB_'+self.order_info['ver'][5:]+'.'+self.order_info['order_no']+'.'+self.order_info['order_name']+'.docx'
        self.testdocx_info['testdocx_file']=os.path.join(self.order_info['work_order_path'],f)
        shutil.copy(self.testdocx_info['template_file'],self.testdocx_info['testdocx_file'])
        w=DispatchEx('Word.Application')
        w.Visible=0
        w.DisplayAlerts=0
        #打开新的文件        
        doc=w.Documents.Open(self.testdocx_info['testdocx_file'])
        
        w.Selection.Find.ClearFormatting()
        w.Selection.Find.Replacement.ClearFormatting()
        w.Selection.Find.Execute('{start_date}',False,False,False,False,False,True,1,True,self.testdocx_info['start_date'],2)
        w.Selection.Find.Execute('{end_date}',False,False,False,False,False,True,1,True,self.testdocx_info['end_date'],2)
        w.Selection.Find.Execute('{order_no}',False,False,False,False,False,True,1,True,self.order_info['order_no'],2)
        w.Selection.Find.Execute('{order_name}',False,False,False,False,False,True,1,True,self.order_info['order_name'],2)
        
        doc.Close()
        w.Quit()