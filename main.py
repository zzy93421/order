#-*-coding:utf-8-*-
import re
import os
import shutil
import time
import datetime
import win32com
from win32com.client import Dispatch, constants
from openpyxl import Workbook, load_workbook
from openpyxl.writer.excel import ExcelWriter
from openpyxl.styles import Font, colors, Alignment

from order_audit import Audit
from order_popularize import OrderPopularize
#from checkdocx import CheckDocx
'''
from allxgpdb import AllXGPDB
from clctgp import CLCTGP
from onexgpdb import OneXGBDB
from PVDB import PVDB
from order_common import Order
from docx import Docx

from dbdd import DBDD
from testdocx import TestDocx
from mysvn import SVN
from order_audit import Audit
from intergrate_docx import IntergrateDocx
from order_popularize import OrderPopularize
'''
from svn import MySvn
class Main(object):
    def __init__(self):
        self.db_range = {
            'xgp': False,
            'clctgp': False,
            'pvdb': False,             
        }
        self.db_ver = {
            'xgp_ver': '',
            'clctgp_ver': '',
            'pvdb_ver': '',
        }
        self.db_exe = {
            'xgp_exe': '',
            'clctgp_exe': '',
            'pvdb_exe': '',
        }
    
    def creFile(self, src, dest, src_list, dest_list):
        '''
        基于模板文件创建新文件，并用新文本替换旧文本
        '''
        if len(src_list) != len(dest_list):
            raise Exception('源列表src_list与目标列表dest_list的记录数不一致！')
        with open(src, 'r') as src_f:
            content = src_f.read()
            for k, v in dict(zip(src_list, dest_list)).items():
                content = content.replace(k, v)
            with open(dest, 'w') as dest_f:
                dest_f.write(content)
        
    def main(self):
        '''
        主函数，将各功能汇总
        '''
        #获取输入信息
        while True:
            self.order_no=input('请输入工单编号：').strip()
            #去掉中间包含的空格
            self.order_no = re.sub(' ', '', self.order_no)
            if self.order_no:
                break;
            else:
                print('输入工单编号无效，请重新输入！\n')
        while True:
            self.order_name=input('请输入工单名称：').strip()
            #去掉字符串中间包含的空格
            self.order_name = re.sub(' ', '', self.order_name)
            if self.order_name:
                self.doc_name = re.sub('项目/产品', '项目产品', self.order_name)
                self.doc_name = re.sub('/', '-', self.doc_name)
                self.exe_name = re.sub('（第.+批）', '', self.doc_name)
                break;
            else:
                print('输入工单名称无效，请重新输入！\n')
        
        while True:
            db_sel = input('''请选择本工单涉及的高频DB：
    1.高频交易库；
    2.高频归集库；
    3.高频计奖验证库。
多项选择，每项之间使用#号隔开，默认选择（1#2#3）:''').strip()
            if db_sel:
                db_list = db_sel.split('#')
            else:
                db_list = ['1', '2', '3']
            if set(['1', '2', '3']) >= set(db_list):
                for i in db_list:
                    if i == '1':
                        self.db_range['xgp'] = True
                    elif i == '2':
                        self.db_range['clctgp'] = True
                    elif i == '3':
                        self.db_range['pvdb'] = True
                    else:
                        raise Exception('无效的DB选项！')
                break
            else:
                print('选择的任务项不对，请重新选择！')
        
        task_list=[]
        while True:
            task=input('''请选择工单任务：
              1.编写实施文档；
              2.编写生产确认单；
              3.编写设计文档；
              4.编写测试报告；
              5.编写应用程序；
              6.填写工单审核意见；
              7.编写综合实施文档；
              8.编写推广工单实施文档；
多项选择，每项之间使用#号隔开，默认选择（1#2#5）:''').strip()
            if task:
                task_list=task.split('#')
            else:
                task_list=['1','2','5']
            all_task_list=['1','2','3','4','5','6','7','8']
            if set(all_task_list)>=set(task_list):
                break;
            else:
                print('选择的任务项不对，请在'+','.join(all_task_list)+'项中选择！')
                
        #更新SVN目录
        svn = MySvn()
        all_group_items = ['XGP11', 'XGP21', 'XGP31', 'XGP41', 'XGP61', 'XGP71']
        if self.db_range['xgp']:
            self.db_ver['xgp_ver'] = svn.getMaxVer('xgp')[0]
            self.db_exe['xgp_exe'] = 'Aeg2DB_' + self.db_ver['xgp_ver'] + '.10.1.0_' + self.exe_name + '.exe'
            
                        
        if self.db_range['clctgp']:
            self.db_ver['clctgp_ver'] = svn.getMaxVer('clctgp')[0]
            self.db_exe['clctgp_exe'] = 'CLCTDB_' + self.db_ver['clctgp_ver'] + '.2.0_' + self.exe_name + '.exe'
        if self.db_range['pvdb']:
            self.db_ver['pvdb_ver'] = svn.getMaxVer('pvdb')[0]
            self.db_exe['pvdb_exe'] = 'Aeg2DBCheck_' + self.db_ver['pvdb_ver'] + '.3.0_' + self.exe_name + '.exe'
        
        #创建实施文档    
        if '1' in task_list:
            #选择进行特殊更新的高频交易组数据库
            while True:                
                special_group_sel = input('''请选择工单更新的特殊交易组数据库：
            0.不选择；
            1.XGP1；
            2.XGP2；
            3.XGP3；
            4.XGP4；
            5.XGP6；
            6.XGP7；
        请选择（每项用#分隔，例如：1#2，默认为0）:''').strip()
        
                if special_group_sel == '0' or not special_group_sel:
                    self.special_group = None
                    #self.normal_group = '、'.join(all_group_items)
                    break
                else:
                    if '#' in special_group_sel:
                        group_list = special_group_sel.split('#')
                    else:
                        group_list = [special_group_sel]
        
                    all_group_list = ['0', '1', '2', '3', '4', '5', '6']                    
                    if set(all_group_list) >= set(group_list) and group_list:
                        if '0' in group_list:
                            print('“0.不选择”与其它项冲突，不能一起选择！')
                        else:
                            #挑选出需要特殊更新的高频交易数据库组
                            group_items_sel = [x for x in all_group_items if str(all_group_items.index(x) + 1) in group_list]
                            if len(group_items_sel) >= 2:                                
                                self.special_group = '、'.join(group_items_sel)
                            elif len(group_items_sel) == 1:
                                self.special_group = group_items_sel[0]                           
                            break
                    else:
                        print('你的选项有错误，请重新选择！')
        
            while True:
                #选择通常更新交易组
                normal_group_sel = input('''
        请选择工单更新的通常交易组数据库：
                    0.不选择；
                    1.XGP1；
                    2.XGP2；
                    3.XGP3；
                    4.XGP4；
                    5.XGP6；
                    6.XGP7；
                    7.选择全部交易数据库组；
        请选择（每项用#分隔，例如：1#2，默认为0）:''').strip()
                if normal_group_sel == '0' or not normal_group_sel:                        
                    self.normal_group = None
                    break
                elif normal_group_sel == '7':
                    self.normal_group = 'XGP11、XGP21、XGP31、XGP41、XGP61、XGP71'
                    break
                else:
                    if '#' in normal_group_sel:
                        group_list = normal_group_sel.split('#')
                    else:
                        group_list = [normal_group_sel]
                    all_group_list = ['0', '1', '2', '3', '4', '5', '6', '7']
        
                    if set(all_group_list) >= set(group_list) and group_list:
                        if '0' in group_list:
                            print('“0.不选择”与其它项冲突，不能一起选择！')
                        elif '7' in group_list:
                            print('“7.选择全部交易数据库组”与其它项冲突，不能一起选择！')
                        else:
                            #挑选出需要特殊更新的高频交易数据库组
                            group_items_sel = [x for x in all_group_items if str(all_group_items.index(x) + 1) in group_list]
                            if len(group_items_sel) >= 2:                                
                                self.normal_group = '、'.join(group_items_sel)
                            elif len(group_items_sel) == 1:
                                self.normal_group = group_items_sel[0]
                            break
                    else:
                        print('你的选项有错误，请重新选择！')
        
            if not self.special_group and not self.normal_group:
                raise Exception('选择了更新高频交易库组，但更新选项即没有配置特殊交易组更新，也没有配置通常交易组更新！')            
            #print(svn.svn_path['gp_direct'][0]+ r'\Aegean2_update')
            doc_path = svn.svn_path['gp_direct'][0]+ r'\Aegean2_update'
            #print(doc_path)
            svn.updateWorkShop(doc_path)
            #获取实施文档的名称
            self.deploy_doc_name = 'Aeg2DB_' + self.db_ver['xgp_ver'] + '.0_' + self.doc_name + '_实施文档.docx'
            self.deploy_doc_name = os.path.join(doc_path, self.deploy_doc_name)
            if self.db_range['xgp'] and self.db_range['clctgp'] and self.db_range['pvdb']:
                template_file = 'deploy_docx_template_all.docx'
            elif self.db_range['xgp'] and self.db_range['clctgp'] and not self.db_range['pvdb']:
                template_file = 'deploy_docx_template_xgp_clctgp.docx'
            elif self.db_range['xgp'] and not self.db_range['clctgp'] and self.db_range['pvdb']:
                template_file = 'deploy_docx_template_xgp_pvdb.docx'
            elif self.db_range['xgp'] and not self.db_range['clctgp'] and not self.db_range['pvdb']:
                template_file = 'deploy_docx_template_xgp.docx'
            #从模板拷贝生成实施文档
            shutil.copy(os.path.join(svn.templat_path, template_file), self.deploy_doc_name)
            
            # 启动独立的进程
            w=win32com.client.Dispatch('Word.Application')
            # 后台运行，不显示，不警告
            w.Visible=0
            w.DisplayAlerts=0
            # 打开新的文件
            doc=w.Documents.Open(self.deploy_doc_name)
            
            if self.db_range['xgp']:
                w.Selection.Find.Execute('{xgp_exe}',False,False,False,False,False,True,1,True,self.db_exe['xgp_exe'],2)
                w.Selection.Find.Execute('{xgp_ver}',False,False,False,False,False,True,1,True,self.db_ver['xgp_ver'] + '.10.1.0',2)
                if self.special_group:                    
                    w.Selection.Find.Execute('{special_group}',False,False,False,False,False,True,1,True,self.special_group,2)
                if self.normal_group:                    
                    w.Selection.Find.Execute('{normal_group}',False,False,False,False,False,True,1,True,self.normal_group,2)
            
            if self.db_range['clctgp']:
                w.Selection.Find.Execute('{clctgp_exe}',False,False,False,False,False,True,1,True,self.db_exe['clctgp_exe'],2)
                w.Selection.Find.Execute('{clctgp_ver}',False,False,False,False,False,True,1,True,self.db_ver['clctgp_ver'] + '.2.0',2)
            
            if self.db_range['pvdb']:                
                w.Selection.Find.Execute('{pvdb_exe}',False,False,False,False,False,True,1,True,self.db_exe['pvdb_exe'],2)
                w.Selection.Find.Execute('{pvdb_ver}',False,False,False,False,False,True,1,True,self.db_ver['pvdb_ver'] + '.3.0',2)
            
            # 填充工单信息表格的内容
            doc.Tables[0].Rows[0].Cells[1].Range.Text=self.order_no
            doc.Tables[0].Rows[1].Cells[1].Range.Text=self.order_name
            
            '''
            if not self.normal_group:
                #删除通常组的更新及回退，即删除第2张表的7-11行和第4张表的7-11行
                for i in range(11, 6, -1):
                    doc.Tables[1].Rows[i].Delete()
                for i in range(11, 6, -1):
                    doc.Tables[4].Rows[i].Delete()
                    
            if not self.special_group:
                #删除特殊组的更新及回退，即删除第2张表的1-6行和第4张表的1-6行
                for i in range(6, 0, -1):
                    doc.Tables[1].Rows[i].Delete()
                for i in range(6, 0, -1):
                    doc.Tables[4].Rows[i].Delete()
                pass
            '''
            
            doc.Close()
            w.Quit()            
            
        
        if '2' in task_list:
            #创建生产确认单
            #print(svn.svn_path['gp_direct'][0]+ r'\Aegean2_update')
            doc_path = svn.svn_path['gp_direct'][0]+ r'\Aegean2_update'
            #print(doc_path)
            svn.updateWorkShop(doc_path)
            #生成生产确认单文件的名称
            self.check_doc_name = 'Aeg2DB_' + self.db_ver['xgp_ver'] + '.0_' + self.doc_name + '_生产确认单.docx'
            self.check_doc_name = os.path.join(doc_path, self.check_doc_name)
            template_file = 'check_docx_template.docx'
            #从模板拷贝生成文档
            shutil.copy(os.path.join(svn.templat_path, template_file),self.check_doc_name)
        
        if '3' in task_list:
            #创建设计文档
            doc_path = svn.svn_path['design_doc'][0]
            svn.updateWorkShop(doc_path)
            #获取设计文档的名称:高频设计文档_DB_VER.ORDER_NO.ORDER_NAME.docx
            self.design_doc_name = '高频设计文档_DB_' + self.db_ver['xgp_ver'].replace('Build', '') + '.' + self.order_no + '.' + self.doc_name + '.docx'
            self.design_doc_name = os.path.join(doc_path, self.design_doc_name )
            template_file = 'dbdd_template.docx'
            #从模板拷贝生成文档
            shutil.copy(os.path.join(svn.templat_path, template_file),self.design_doc_name)
            
            w=win32com.client.DispatchEx('Word.Application')
            w.Visible=0
            w.DisplayAlerts=0
            #打开新的文件
            doc=w.Documents.Open(self.design_doc_name)
        
            w.Selection.Find.ClearFormatting()
            w.Selection.Find.Replacement.ClearFormatting()
            w.Selection.Find.Execute('{create_date}',False,False,False,False,False,True,1,True,time.strftime("%Y-%m-%d"),2)
            w.Selection.Find.Execute('{order_name}',False,False,False,False,False,True,1,True,self.order_name,2)
            w.Selection.Find.Execute('{order_no}',False,False,False,False,False,True,1,True,self.order_no,2)
            
            doc.Close()
            w.Quit()            
            pass
        
        if '4' in task_list:
            #创建测试报告文档
            doc_path = svn.svn_path['test_doc'][0]
            svn.updateWorkShop(doc_path)
            #获取测试报告文档名称：高频单元测试报告_DB_ver.order_no.order_name.docx
            self.test_doc_name = '高频单元测试报告_DB_' + self.db_ver['xgp_ver'].replace('Build', '') + '.' + self.order_no + '.' + self.doc_name + '.docx'
            self.test_doc_name = os.path.join(doc_path, self.test_doc_name)
            template_file = 'testdocx_template.docx'
            template_file = os.path.join(svn.templat_path, template_file)
            #从模板拷贝生成文档
            shutil.copy(os.path.join(svn.templat_path, template_file),self.test_doc_name)
            
            w=win32com.client.DispatchEx('Word.Application')
            w.Visible=0
            w.DisplayAlerts=0
            #打开新的文件        
            doc=w.Documents.Open(self.test_doc_name)
        
            w.Selection.Find.ClearFormatting()
            w.Selection.Find.Replacement.ClearFormatting()
            w.Selection.Find.Execute('{start_date}',False,False,False,False,False,True,1,True,datetime.date.today().strftime('%Y-%m-%d'),2)
            w.Selection.Find.Execute('{end_date}',False,False,False,False,False,True,1,True,(datetime.date.today()+datetime.timedelta(days=2)).strftime('%Y-%m-%d'),2)
            w.Selection.Find.Execute('{order_no}',False,False,False,False,False,True,1,True,self.order_no,2)
            w.Selection.Find.Execute('{order_name}',False,False,False,False,False,True,1,True,self.order_name,2)
        
            doc.Close()
            w.Quit()       
            pass
        
        if '5' in task_list:
            #创建应用程序
            file_path = svn.svn_path['gp_app'][0]
            svn.updateWorkShop(file_path)
            #创建共用的应用程序目录
            self.app_path = self.order_no + '_' + self.doc_name
            self.app_path = file_path + '\\' + self.app_path
            os.makedirs(self.app_path)
            if self.db_range['xgp']:
                #创建高频交易库应用程序
                self.xgp_app_path = self.app_path + '\\' + 'Aeg200'
                os.makedirs(self.xgp_app_path)
                #创建config.ini文件
                dest_file = os.path.join(self.xgp_app_path, 'config.ini')
                template_file = os.path.join(svn.templat_path, 'xgp_template_config.ini')
                self.creFile(template_file, dest_file, ['{order_name}'], [self.exe_name])
                
                #创建readme.txt文件
                dest_file = os.path.join(self.xgp_app_path, 'readme.txt')
                template_file = os.path.join(svn.templat_path, 'xgp_template_readme.txt')
                self.creFile(template_file, dest_file, ['{order_name}'], [self.exe_name])
                                 
                #创建all.sql
                dest_file = os.path.join(self.xgp_app_path, 'all.sql')
                template_file = os.path.join(svn.templat_path, 'xgp_template_all.sql')
                self.creFile(template_file, dest_file, ['{xgp_ver}', '{exe_name}'], [self.db_ver['xgp_ver'], self.exe_name])
                
                #创建normal_update.sql
                dest_file = os.path.join(self.xgp_app_path, 'normal_update.sql')
                template_file = os.path.join(svn.templat_path, 'xgp_template_normal_update.sql')
                self.creFile(template_file, dest_file, ['{xgp_ver}', '{exe_name}', '{order_no}'], [self.db_ver['xgp_ver'], self.exe_name, self.order_no])
                
                #创建normal_rollback.sql
                dest_file = os.path.join(self.xgp_app_path, 'normal_rollback.sql')
                template_file = os.path.join(svn.templat_path, 'xgp_template_normal_rollback.sql')
                self.creFile(template_file, dest_file, ['{xgp_ver}'], [self.db_ver['xgp_ver']])
                
                #创建special_update.sql
                dest_file = os.path.join(self.xgp_app_path, 'special_update.sql')
                template_file = os.path.join(svn.templat_path, 'xgp_template_special_update.sql')
                self.creFile(template_file, dest_file, ['{xgp_ver}', '{exe_name}', '{order_no}'], [self.db_ver['xgp_ver'], self.exe_name, self.order_no])
                
                #创建special_rollback.sql
                dest_file = os.path.join(self.xgp_app_path, 'special_rollback.sql')
                template_file = os.path.join(svn.templat_path, 'xgp_template_special_rollback.sql')
                self.creFile(template_file, dest_file, ['{xgp_ver}'], [self.db_ver['xgp_ver']])                
                pass
            if self.db_range['clctgp']:
                #创建高频归集库应用程序
                self.clctgp_app_path = self.app_path + '\\' + 'CLCTGP'
                os.makedirs(self.clctgp_app_path)
                
                #创建config.ini
                dest_file = os.path.join(self.clctgp_app_path, 'config.ini')
                template_file = os.path.join(svn.templat_path, 'clctgp_template_config.ini')
                self.creFile(template_file, dest_file, ['{order_name}'], [self.exe_name])
                
                #创建readme.txt
                dest_file = os.path.join(self.clctgp_app_path, 'readme.txt')
                template_file = os.path.join(svn.templat_path, 'clctgp_template_readme.txt')
                self.creFile(template_file, dest_file, ['{order_name}'], [self.exe_name])
                
                #创建all.sql
                dest_file = os.path.join(self.clctgp_app_path, 'all.sql')
                template_file = os.path.join(svn.templat_path, 'clctgp_template_all.sql')
                self.creFile(template_file, dest_file, ['{clctgp_ver}', '{exe_name}'], [self.db_ver['clctgp_ver'], self.exe_name])
                
                #创建clctgp_update.sql
                dest_file = os.path.join(self.clctgp_app_path, 'clctgp_update.sql')
                template_file = os.path.join(svn.templat_path, 'clctgp_template_update.sql')
                self.creFile(template_file, dest_file, ['{clctgp_ver}', '{exe_name}', '{order_no}'], [self.db_ver['clctgp_ver'], self.exe_name, self.order_no])                 
                
                #创建clctgp_rollback.sql
                dest_file = os.path.join(self.clctgp_app_path, 'clctgp_rollback.sql')
                template_file = os.path.join(svn.templat_path, 'clctgp_template_rollback.sql')
                self.creFile(template_file, dest_file, ['{clctgp_ver}', '{exe_name}', '{order_no}'], [self.db_ver['clctgp_ver'], self.exe_name, self.order_no])                 

            if self.db_range['pvdb']:
                #创建计奖验证库应用程序
                self.pvdb_app_path = self.app_path + '\\' + 'CheckDB'
                os.makedirs(self.pvdb_app_path)
                
                #创建config.ini
                dest_file = os.path.join(self.pvdb_app_path, 'config.ini')
                template_file = os.path.join(svn.templat_path, 'pvdb_template_config.ini')
                self.creFile(template_file, dest_file, ['{order_name}'], [self.exe_name])
                
                #创建readme.txt
                dest_file = os.path.join(self.pvdb_app_path, 'readme.txt')
                template_file = os.path.join(svn.templat_path, 'pvdb_template_readme.txt')
                self.creFile(template_file, dest_file, ['{order_name}'], [self.exe_name])
                
                #创建all.sql
                dest_file = os.path.join(self.pvdb_app_path, 'all.sql')
                template_file = os.path.join(svn.templat_path, 'pvdb_template_all.sql')
                self.creFile(template_file, dest_file, ['{pvdb_ver}', '{exe_name}'], [self.db_ver['pvdb_ver'], self.exe_name])
                
                #创建pvdb_update.sql
                dest_file = os.path.join(self.pvdb_app_path, 'pvdb_update.sql')
                template_file = os.path.join(svn.templat_path, 'pvdb_template_update.sql')
                self.creFile(template_file, dest_file, ['{pvdb_ver}', '{exe_name}', '{order_no}'], [self.db_ver['pvdb_ver'], self.exe_name, self.order_no])                
                
                #创建pvdb_rollback.sql
                dest_file = os.path.join(self.pvdb_app_path, 'pvdb_rollback.sql')
                template_file = os.path.join(svn.templat_path, 'pvdb_template_rollback.sql')
                self.creFile(template_file, dest_file, ['{pvdb_ver}', '{exe_name}', '{order_no}'], [self.db_ver['pvdb_ver'], self.exe_name, self.order_no])
        
        if '6' in task_list:
            #填写工单审核意见
            file_path = svn.svn_path['group_direct'][0]
            svn.updateWorkShop(file_path)
                       
            audit_advice = input('请输入工单审核意见，不输入表示无意见：\n').strip()
            if not audit_advice:
                audit_advice = '无意见。'
            commit_message = '增加工单审核记录'
            
            ad = Audit(self.order_no, self.order_name)
            ad.audit(audit_advice)            
            audit_file = os.path.join(file_path, r'_数据库组需求工单审核记录表.xlsx')            
            svn.commit([audit_file], commit_message)            
            print(ad.audit_info['url'])            

        if '7' in task_list:
            #编写综合实施文档
            #print(svn.svn_path['gp_direct'][0]+ r'\Aegean2_update')
            doc_path = svn.svn_path['gp_direct'][0]+ r'\Aegean2_update'
            #print(doc_path)
            svn.updateWorkShop(doc_path)
            
            ig = IntergrateDocx(self.order_no, self.exe_name, '')
            #svn.updateWorkShop(ig.order_info['svn'])
            ig.createIntergateFile()            
            pass
        if '8' in task_list:
            #编写推广工单实施文档
            doc_path = svn.svn_path['gp_direct'][0]+ r'\Aegean2_update'
            svn.updateWorkShop(doc_path)
            op = OrderPopularize(self.order_no, self.order_name, '')
            op.createOPFile()            
            pass
        
        
if __name__=="__main__":
    m=Main()
    m.main()
    print('程序执行完毕！')
        
        
    
    
        
        
    
    