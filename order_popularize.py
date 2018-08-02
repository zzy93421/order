#-*- coding:utf-8 -*-
import os
import shutil
import win32com
from win32com.client import DispatchEx, constants
from order_common import Order
import re
class OrderPopularize(Order):
    '''
    工单推广类，从旧工单复制到新工单，并替换部分内容
        1.重新新的工单标题（实施文档第一个表格内容）；
        2.替换实施的高频组；
        3.工单版本信息保持不变；
        4.加入工单依赖项。
    '''
    def __init__(self, order_no, order_name, backup_tabs):
        '''
        初始化函数
        '''
        #调用父类初始化函数
        super(OrderPopularize, self).__init__(order_no, order_name, backup_tabs)
        self.op_info = {'old_order_name': '',
                        'old_order_no': '',
                        'before_replace_list': [],
                        'after_replace_list': [],
                        'old_deploy_docx': '',
                        'new_deploy_docx': '',
                        'delay_item': '',
                        }
        self.order_info['work_order_path'] = self.order_info['svn']
        self.order_info['ver'] = self.getVer(self.order_info['work_order_path'], order_name, 'Aeg2DB_Build')
        self.op_info['new_deploy_docx'] = os.path.join(self.order_info['work_order_path'], 'Aeg2DB_' + self.order_info['ver'] + '.0_' + re.sub('/', '-', order_name) + '_实施文档.docx')
    def createOPFile(self):
        '''
        创建推广工单实施文档
        '''
        #输入原工单名称
        while True:
            self.op_info['old_order_name'] = input('请输入原工单名称：').strip()
            if self.op_info['old_order_name']:
                for x in os.listdir(self.order_info['work_order_path']):
                    if self.op_info['old_order_name'] in x and x[0:12] == 'Aeg2DB_Build' and '综合实施文档' not in x and '生产确认单' not in x:
                        self.op_info['old_deploy_docx'] = x
                if not self.op_info['old_deploy_docx']:
                    print('输入的原工单不存在，请重新输入！')
                else:                                     
                    break
            else:
                print('你的输入为空，请重新输入！')
        #由原实施文档拷贝生成新的实施文档
        self.op_info['old_deploy_docx'] = os.path.join(self.order_info['work_order_path'],self.op_info['old_deploy_docx'])
        shutil.copy(self.op_info['old_deploy_docx'], self.op_info['new_deploy_docx'])
        #对新的实施文档进行修改
        w = DispatchEx('Word.Application')
        #后台运行，不显示，不警告
        w.Visible = 0
        w.DisplayAlerts = 0
        #打开新的实施文档
        doc = w.Documents.Open(self.op_info['new_deploy_docx'])
        #替换工单标题表格，即工单名称、工单编号、工单依赖等
        t = doc.Tables[0]
        #读取旧工单编号，用于生成依赖工单
        self.op_info['old_order_no'] = t.Rows[0].Cells[1].Range.Text
        self.op_info['old_order_no'] = self.op_info['old_order_no'].strip().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
        #使用新工单号替换旧工单号
        t.Rows[0].Cells[1].Range.Text = self.order_info['order_no']
        #使用新工单名称替换旧工单名称
        t.Rows[1].Cells[1].Range.Text = self.order_info['order_name']
        #生成新工单的更新依赖
        '''self.op_info['delay_item'] = '本工单依赖工单“' + self.op_info['old_order_no'] + '_' + self.op_info['old_order_name'] + '”，实施本工单前，请确认所依赖工单已部署完成。'
        print(self.op_info['delay_item'])
        t.Rows[3].Cells[1].Range.Text = self.op_info['delay_item']'''
        #对新生成的工单进行替换
        #输入新旧工单替换项
        w.Selection.Find.ClearFormatting()
        w.Selection.Find.Replacement.ClearFormatting()
        replace_list = []
        while True:
            replace_str = input('请输入新旧工单需要替换的项目\n（格式：old_word1#new_word1|old_word2#new_word2|old_word3#new_word3）。\n请输入（退出请输入99）：').strip()
            
            if replace_str:
                if replace_str == '99':
                    break
                else:
                    for rec in replace_str.split('|'):
                        for item in rec.split('#'):
                            replace_list.append(item)
                    pass
            else:
                print('你的输入为空，请重新输入！')
        #取出被替换项
        self.op_info['before_replace_list'] = replace_list[::2]
        print(self.op_info['before_replace_list'])
        #取出对应的替换项
        self.op_info['after_replace_list'] = replace_list[1::2]
        print(self.op_info['after_replace_list'])
        
        #执行替换
        for i in range(len(self.op_info['before_replace_list'])):
            w.Selection.Find.Execute(self.op_info['before_replace_list'][i],False,False,False,False,False,True,1,True, self.op_info['after_replace_list'][i],2)
        #保存文档
        doc.Save()
        doc.Close()
        w.Quit()
            
        
        
        
        
        