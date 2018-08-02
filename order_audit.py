#-*- coding:utf-8 -*-
import os
import time, datetime
from win32com.client import DispatchEx, constants
from mysvn import SVN
#from order_common import Order
class Audit(object):
    '''
    工单审核类
    '''
    def __init__(self, order_no, order_name):
        '''
        初始化函数
        '''
        self.audit_info = {'work_path': r'C:\workshop\小组文档',
                           'work_file': r'_数据库组需求工单审核记录表.xlsx',
                           'order_no': order_no,
                           'order_name': order_name,
                           'order_exist': 0,
                           'start_date': '',
                           'end_date': '',
                           'developer': '',
                           'auditer': '志远',
                           'audit_advice': '',
                           'url': r'http://svnserver:8088/SVN/Department/RD/05小组目录/01交易系统/小组文档/_数据库组需求工单审核记录表.xlsx',
                           }
        self.person_info = ['志远', '春生', '珂玮', '李靖', '陈伟', '丁一', '刘杰', '苑苑', '凤林', '首阳', '晓桥']
            
    def audit(self, audit_advice): 
        '''
        完成工单审核函数
        '''
        if audit_advice:
            self.audit_info['audit_advice'] = audit_advice
        else:
            self.audit_info['audit_advice'] = '无意见。'
        f = os.path.join(self.audit_info['work_path'], self.audit_info['work_file'])
        self.excelApp = DispatchEx('Excel.Application')
        self.excelApp.Visible = 0
        self.excelApp.DisplayAlerts = 0
        self.book = self.excelApp.Workbooks.Open(f)
        self.sheet = self.book.Worksheets(5)
        #print(self.sheet.Name)
        row, col = 1, 1
        while True:
            if self.sheet.Cells(row, col).Value:
                if self.audit_info['order_no'] in self.sheet.Cells(row, col).Value:
                    if self.sheet.Cells(row, 6).Value:
                        self.sheet.Cells(row, 6).Value = self.sheet.Cells(row, 6).Value + '\n' + self.audit_info['audit_advice']
                    else:
                        self.sheet.Cells(row, 6).Value = self.audit_info['audit_advice']
                    self.audit_info['order_exist'] = 1
                    #self.sheet.Rows[row].Insert()                    
            else:
                break
            row = row + 1
        if not self.audit_info['order_exist']:
            #如果没有该工单，那么添加到工单审核表中，并增加审核意见            
            #输入开始日期
            while True:
                start_date = input('请输入工单开始日期（格式：yyyy/mm/dd）:').strip().replace('-', '/')                
                if start_date:
                    self.audit_info['start_date'] = datetime.datetime.strptime(start_date, '%Y/%m/%d')
                    break
                else:
                    print('你输入的日期为空，请重新输入！')
            #输入结束日期
            while True:
                end_date = input('请输入工单结束日期（格式：yyyy/mm/dd）:').strip().replace('-', '/')
                if end_date:
                    self.audit_info['end_date'] = datetime.datetime.strptime(end_date, '%Y/%m/%d')
                    break
                else:
                    print('你输入的日期为空，请重新输入！')
            #输入研发人员
            while True:
                persons = zip(range(1, len(self.person_info)), self.person_info)
                print('请选择工单研发人员：')
                for person in persons:
                    print('    ' + str(person[0]) + ' ' + person[1])
                developer = input('请输入数字选择，多项选择使用#分隔每个单项，例如1#2#3：').strip()
                if developer:
                    if developer[-1:] == '#':
                        developer = developer[0:-1]
                    person_index = [int(x) - 1 for x in developer.split('#')]
                    developer_list = [self.person_info[x] for x in person_index]
                    self.audit_info['developer'] = '\n'.join(developer_list)
                    break
                else:
                    print('你的选择为空，请重新选择！')
            
            #输入审核人员
            while True:
                persons = zip(range(1, len(self.person_info)), self.person_info)
                print('请选择工单审核人员：')
                for person in persons:
                    print('    ' + str(person[0]) + ' ' + person[1])
                developer = input('请输入数字选择，多项选择使用#分隔每个单项，例如1#2#3：').strip()
                if developer:                    
                    if developer[-1:] == '#':
                        developer = developer[0:-1]
                    person_index = [int(x) - 1 for x in developer.split('#')]
                    auditer_list = [self.person_info[x] for x in person_index]
                    self.audit_info['auditer'] = '\n'.join(auditer_list)
                    break
                else:
                    print('你的选择为空，请重新选择！')
                    
            #寻找结束日期与该工单结束日期的行
            if self.audit_info['order_no'][0:2].upper() == "XQ":
                order_type = '需求工单'
            elif self.audit_info['order_no'][0:2].upper() == "WT":
                order_type             = '问题工单'
            order_info = self.audit_info['order_no'] + ' ' + order_type + ' ' + self.audit_info['order_name']
            
            row, col = 2, 5
            while True:
                if self.sheet.Cells(row, col).Text:
                    dt = datetime.datetime.strptime(self.sheet.Cells(row, col).Text , '%Y-%m-%d')                 
                    if self.audit_info['end_date'] == dt:
                        #进一步比较开始日期
                        dt1 = datetime.datetime.strptime(self.sheet.Cells(row, col - 1).Text, '%Y-%m-%d')                        
                        if self.audit_info['start_date'] < dt1:                            
                            self.sheet.Rows[row - 1].Insert()
                            #输入工单信息                        
                            self.sheet.Cells(row , 1).Value = order_info
                            #开发人员
                            self.sheet.Cells(row , 2).Value = self.audit_info['developer']
                            #审核人员
                            self.sheet.Cells(row , 3).Value = self.audit_info['auditer']
                            #开始日期
                            self.sheet.Cells(row, 4).Value = self.audit_info['start_date'].strftime('%Y-%m-%d')
                            #结束日期
                            self.sheet.Cells(row, 5).Value = self.audit_info['end_date'].strftime('%Y-%m-%d')
                            #审核意见
                            self.sheet.Cells(row , 6).Value = self.audit_info['audit_advice']
                            break
                    elif self.audit_info['end_date'] < dt:
                        self.sheet.Rows[row - 1].Insert()
                        #输入工单信息                        
                        self.sheet.Cells(row , 1).Value = order_info
                        #开发人员
                        self.sheet.Cells(row , 2).Value = self.audit_info['developer']
                        #审核人员
                        self.sheet.Cells(row , 3).Value = self.audit_info['auditer']
                        #开始日期
                        self.sheet.Cells(row, 4).Value = self.audit_info['start_date'].strftime('%Y-%m-%d')
                        #结束日期
                        self.sheet.Cells(row, 5).Value = self.audit_info['end_date'].strftime('%Y-%m-%d')
                        #审核意见
                        self.sheet.Cells(row , 6).Value = self.audit_info['audit_advice']
                        break                       
                    
                else:
                    #输入工单信息                        
                    self.sheet.Cells(row , 1).Value = order_info
                    #开发人员
                    self.sheet.Cells(row , 2).Value = self.audit_info['developer']
                    #审核人员
                    self.sheet.Cells(row , 3).Value = self.audit_info['auditer']
                    #开始日期
                    self.sheet.Cells(row, 4).Value = self.audit_info['start_date'].strftime('%Y-%m-%d')
                    #结束日期
                    self.sheet.Cells(row, 5).Value = self.audit_info['end_date'].strftime('%Y-%m-%d')                   
                    #审核意见
                    self.sheet.Cells(row , 6).Value = self.audit_info['audit_advice']                    
                    break
                row = row + 1
        self.book.Save()
        self.book.Close()
        self.excelApp.Quit()