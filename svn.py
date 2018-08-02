# -*- coding:utf-8 -*-
import pysvn
import os
import urllib
import urllib.parse
import datetime
import time
import re
class MySvn:
    def __init__(self):
        self.svn_path = {
            'gp_direct': [r'c:\workshop\gp\db', r'http://svnserver:8088/Repository/Aegean2/trunk/product/db'],
            'gp_app': [r'c:\workshop\gp\app', r'http://svnserver:8088/SVN/Department/RD/05小组目录/01交易系统/ProductTickectDB'], 
            'gp_clctgp': [r'c:\workshop\gp\高频归集', r'http://172.16.17.29:8088/Repository/Guiji/'], 
            'gp_dbdd': [r'c:\workshop\gp\dbdd', 'http://svnserver:8088/SVN/Department/RD/08开发文档/00系统文档/05数据库'], 
            'rx_direct': [r'c:\workshop\tiger\db', r'http://svnserver:8088/SVN/Project/Tiger/15联合项目/66code/trunk/product/db'], 
            'group_direct': [r'c:\workshop\小组文档', r'http://svnserver:8088/SVN/Department/RD/05小组目录/01交易系统/小组文档'], 
            'design_doc': [r'c:\workshop\单项设计文档', r'http://svnserver:8088/SVN/Project/Tiger/15联合项目/05概要设计/02下一代系统/03最终成果/05DB/单项设计文档'], 
            'test_doc': [r'c:\workshop\单元测试报告', 'http://svnserver:8088/SVN/Project/Tiger/15联合项目/05概要设计/02下一代系统/03最终成果/05DB/单元测试报告'], 
            'code_review': [r'c:\workshop\代码评审记录', r'http://svnserver:8088/SVN/Project/Tiger/15联合项目/05概要设计/02下一代系统/03最终成果/05DB/代码评审记录'],
            'discard_direct': ['AEG21_SRC', 'AEG21_update', 'Aegean2_update', 'aegean数据库改动', 'branch', '促销和需求', \
                               '废弃代码', '高频二次验奖', '高频库迁移', '优化'],
            'program_direct': ['奖期流程', '售票取消兑奖','table_structure', '二代高频', '高频4花选4', '高频8选3', \
                               '高频11选5', '高频12选5', '高频22选5', '高频30选3', '高频52选3', '高频百变王牌', \
                               '高频常用维护程序', '高频金7上线版', '高频泳坛夺金', '高频游戏新促销模板', \
                               '幸运号促销（高频游戏）', '赠票促销(高频游戏)'],
        }
        self.templat_path = r'C:\workshop\python\order\template'
        self.client = pysvn.Client()
    def copyWorkShop(self):
        for key, val in self.svn_path.items():
            if not os.path.exists(val[0]):
                os.makedirs(val[0])
            self.client.checkout(val[1], val[0])
            #print(key, val)
    def updateWorkShop(self, svn_path):
        if svn_path == 'all':
            for key, val in self.svn_path.items():
                self.client.update(val[0])
                print(val[0])
        else:
            self.client.update(svn_path)
        pass
    def commit(self, modify_file_list, message):
        '''
        提交修改的文件到SVN
        '''
        self.client.checkin(modify_file_list, message)
        pass
    
    def copyRevisionFiles(self, file_list, before_date, dest_path):
        '''
        获取小于指定日期(before_date)最大版本的文件，并拷贝到指定目录dest_path
        '''
        #检查输入参数的有效性
        if not file_list or not before_date or not dest_path:
            raise Exception('输入参数file_list、before_date及dest_path不能为空！')
        
        try:
            limit_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
        except ValueError as e:
            print('输入日期参数before_date错误，请按照YYYY-MM-DD格式输入！')
            
        url_file_list = []
        my_file_list = [x.lower() for x in file_list]
        pre_path = self.svn_path['gp_direct'][1] + r'/'
        for path in [pre_path+x for x in self.svn_path['program_direct']]:
            entry_list = self.client.list(path, depth = pysvn.depth.files)[1:]
            entry_list = [x[0] for x in entry_list]
            #获取文件的SVN目录路径，并对url进行decode
            entry_list = [urllib.parse.unquote(x['path']) for x in entry_list]
            #挑选出满足要求的文件的url
            #file_list = [(y, x) for x in entry_list for y in my_file_list if os.path.basename(x).lower() = y.lower()]
            current_file_list = [(x, y) for x in my_file_list for y in entry_list \
                                 if x.lower() == os.path.basename(y).lower()]
            if current_file_list:
                url_file_list.extend(current_file_list)
                del current_file_list
            pass
        
        #开始读取指定日期之前的版本的文件，并拷贝到目标目录
        start_rev = pysvn.Revision(pysvn.opt_revision_kind.head)
        end_rev = pysvn.Revision(pysvn.opt_revision_kind.number, 0)        
        for f in url_file_list:
            #print(f[1])            
            log_list = self.client.log(f[1],start_rev, end_rev, limit = 0 )
            for log in log_list:
                if time.localtime(log.date) < limit_date.timetuple():
                    revision_num = log.revision.number
                    file_text = self.client.cat(f[1],pysvn.Revision(pysvn.opt_revision_kind.number, \
                                                                    revision_num))
                    file_text = file_text.decode('gb2312').replace('\r\n', '\n')
                    ver_search = re.search('/\*.*([0-9]+\.[0-9]+).*\*/', file_text, re.I)
                    if ver_search:
                        ver = ver_search.group(1)
                        print(f[0], ver)
                    name_list = os.path.splitext(f[0])
                    name = name_list[0] + '-' + str(revision_num) + name_list[1]
                    dest_file = os.path.join(dest_path, name)
                    with open(dest_file, 'w') as dest_f:
                        dest_f.write(file_text)
                    break
        print(url_file_list)
        return url_file_list
    def getMaxVer(self, db_type):
        '''
        获取各个数据库类型(高频库、高频归集库及计奖验证库)的版本信息
        '''
        db_str = db_type.lower()
        ver_set = set()
        if db_str == 'xgp':
            path_list = [self.svn_path['gp_direct'][0] + '\\' + 'Aegean2_update']
            self.updateWorkShop(self.svn_path['gp_direct'][0])
            for root, dirs, files in os.walk(path_list[0]):
                for file in files:
                    if 'Aeg2DB_Build' in file and os.path.splitext(file)[1] in ['.doc', '.docx', '.txt']:
                        ver_set.add(file.split('_')[1])
            ver_id = 0
            current_ver = ''
            for i in ver_set:
                if int(i.split('.')[1]) > ver_id:
                    ver_id = int(i.split('.')[1])
                    current_ver = i
            next_ver = current_ver.split('.')[0] + '.' + str(ver_id + 1)
            return [next_ver]
        elif db_str == 'clctgp':
            path_list = [self.svn_path['gp_clctgp'][0] + r'\trunk\script\update']
            self.updateWorkShop(self.svn_path['gp_clctgp'][0])
            for root, dirs, files in os.walk(path_list[0]):
                for file in files:
                    if 'CLCTDB_Build' in file and os.path.splitext(file)[1] in ['.doc', '.docx', '.txt']:
                        ver_set.add(file.split('_')[1])
            ver_id = 0
            current_ver = ''
            for i in ver_set:
                if int(i.split('.')[1]) > ver_id:
                    ver_id = int(i.split('.')[1])
                    current_ver = i
            next_ver = current_ver.split('.')[0] + '.' + str(ver_id + 1).zfill(3)
            return [next_ver]            
        elif db_str == 'pvdb':
            path_list = [self.svn_path['gp_direct'][0] + '\\' + 'Aegean2_update']
            self.updateWorkShop(self.svn_path['gp_direct'][0])
            for root, dirs, files in os.walk(path_list[0]):
                for file in files:
                    if 'Aeg2DBCheck_Build' in file and os.path.splitext(file)[1] in ['.doc', '.docx', '.txt']:
                        ver_set.add(file.split('_')[1])
            ver_id = 0
            current_ver = ''
            for i in ver_set:
                if int(i.split('.')[1]) > ver_id:
                    ver_id = int(i.split('.')[1])
                    current_ver = i
            next_ver = current_ver.split('.')[0] + '.' + str(ver_id + 1).zfill(3)
            return [next_ver]             
        elif db_str == 'all':
            ver_list = []
            next_ver = self.getMaxVer('xgp')
            ver_list.extend(next_ver)
            next_ver = self.getMaxVer('clctgp')
            ver_list.extend(next_ver)
            next_ver = self.getMaxVer('pvdb')
            ver_list.extend(next_ver)            
            return ver_list

if __name__ == '__main__':
    mysvn = MySvn()
    #mysvn.copyWorkShop()
    #mysvn.updateWorkShop('all')
    #next_ver = mysvn.getMaxVer('all')
    #print(next_ver)
    mysvn.copyRevisionFiles(['p_get_draw_time.prc', 'p_move_draw.prc'], \
                            '2017-12-28', r'c:\pythontest\mytest')
    #mysvn.copyRevisionFiles('', None, None)