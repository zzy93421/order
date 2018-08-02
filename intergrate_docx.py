#-*- coding:utf-8 -*-
import os
import shutil
import win32com
from win32com.client import DispatchEx, constants
from order_common import Order
class IntergrateDocx(Order):
    '''
    生成综合实施文档类
    '''
    def __init__(self, order_no, order_name, backup_tabs):
        '''
        初始化函数
        '''
        #调用父类函数
        super(IntergrateDocx, self).__init__(order_no, order_name, backup_tabs)
        self.intergrate_info = {'template_file': r'C:\workshop\python\order\template\intergrate_docx_template.docx',
                                'intergrate_file': '',
                                }        
        
        
    def createIntergateFile(self):
        '''
        由模板创建工单综合实施文档
        '''
        self.order_info['ver'] = self.getVer(self.order_info['svn'], self.order_info['order_name'], 'Aeg2DB_Build')
        #print(self.order_info['ver'])
        self.intergrate_info['intergrate_file'] = os.path.join(self.order_info['svn'], 'Aeg2DB_' + self.order_info['ver'] + '.0_' + self.order_info['order_name'] + '_综合实施文档.docx')
        #由模板文件复制成实施文档
        shutil.copy(self.intergrate_info['template_file'], self.intergrate_info['intergrate_file'])
        #启动独立的进程
        w = DispatchEx('Word.Application')
        #后台运行，不显示，不警告
        w.Visible=0
        w.DisplayAlerts=0
        #打开新的文档
        doc = w.Documents.Open(self.intergrate_info['intergrate_file'])
        w.Selection.Find.ClearFormatting()
        w.Selection.Find.Replacement.ClearFormatting()
        w.Selection.Find.Execute('{ver}',False,False,False,False,False,True,1,True,self.order_info['ver'],2)
        w.Selection.Find.Execute('{order_name}',False,False,False,False,False,True,1,True,self.order_info['order_name'],2)
    
        doc.Close()
        w.Quit()        
        