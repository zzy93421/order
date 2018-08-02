#-*-coding:utf-8-*-
import shutil
import os
from order_common import Order
class CheckDocx(Order):
    '''
    生成检查确认单
    '''
    def __init__(self, order_no, order_name, backup_tabs):
        '''
        初始化函数
        '''
        super(CheckDocx,self).__init__(order_no,order_name,backup_tabs)
        self.order_info['svn']=r'D:\aeg2\Aegean2_update'
        self.order_info['work_order_path']=r'D:\aeg2\Aegean2_update'
        self.checkdocx_info={'template_file':r'D:\workorder\template\check_docx_template.docx',
                             'checkdocx_file':'',
                             }
    def createCheckDocx(self):
        '''
        创建生产确认单
        '''
        self.order_info['ver']=self.getVer(self.order_info['svn'], self.order_info['order_name'], 'Aeg2DB_Build')
        f='Aeg2DB_'+self.order_info['ver']+'.0_'+self.order_info['order_name']+'_生产确认单.docx'
        self.checkdocx_info['checkdocx_file']=os.path.join(self.order_info['work_order_path'],f)
        shutil.copy(self.checkdocx_info['template_file'],self.checkdocx_info['checkdocx_file'])
        