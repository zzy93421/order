#-*- coding:utf-8 -*-
import win32com
import os
import shutil
from win32com.client import Dispatch, constants
from order_common import Order


class Docx(Order):
    '''
    创建word文档类
    '''

    def inputTask(self, index, db_info):
        '''
        获取所有高频组、单个高频组、高频归集库及计奖验证库的工单任务
        index取值:allxgp,onexgp,pvdb,clctgp
        db_info取值：所有高频组、单个高频组、高频计奖验证库和高频归集库
        '''
        while True:
            sel = input('''请选择实施文档与''' + db_info + '''相关的工单任务：
            0.不包含与之相关内容；
            1.仅实施文档；
            2.实施文档及应用程序。
            请输入0、1或2选择（默认为0）:''').strip()
    if not sel or sel == '0':
                self.docx_info[index + '_task'] = 0
                break
            elif sel=='1':
                self.docx_info[index+'_task']=1
                break
            elif sel=='2':
                self.docx_info[index+'_task']=2
                break
            else:
                print('你的选择有误！')
    def __init__(self, order_no, order_name, backup_tabs):
        '''
        初始化函数
        '''
        # 调用父类初始化函数
        super(Docx,self).__init__(order_no,order_name,backup_tabs)
        self.docx_info={'doc_file':'',
                        'template_file':r'C:\workshop\python\order\template\deploy_docx_template.docx',
                        'spend_time':'30',
                        'notice':'',
                        'dependent_order':'无',
                        'start_time':'02:10',
                        'xgp_user':'helios',
                        'xgp_pwd':'helios',
                        'allxgp_exe':'',
                        'allxgp_ver':'',
                        'allxgp_task':0,#0表示不包含，1表示仅实施文档，2表示实施文档和应用程序
                        'onexgp_exe':'',
                        'onexgp_db':'XGP11',
                        'onexgp_ver':'',
                        'onexgp_task':0,#0表示不包含，1表示仅实施文档，2表示实施文档和应用程序
                        'pvdb_user':'xgp_check',
                        'pvdb_pwd':'xgp_check',
                        'pvdb_ver':'',
                        'pvdb_exe':'',
                        'pvdb_task':0,#0表示不包含，1表示仅实施文档，2表示实施文档和应用程序
                        'clctgp_user':'aeg2',
                        'clctgp_pwd':'aeg2',
                        'clctgp_svn':'',
                        'clctgp_ver':'',
                        'clctgp_exe':'',
                        'clctgp_task':0,#0表示不包含，1表示仅实施文档，2表示实施文档和应用程序
                        }
        
        self.order_info['svn']=r'C:\workshop\gp\db\Aegean2_update'
        self.docx_info['clctgp_svn']=r'C:\workshop\gp\高频归集\trunk\script\update'
        self.order_info['ver']=self.getVer(self.order_info['svn'], self.order_info['order_name'], 'Aeg2DB_Build')
        self.docx_info['doc_file']=os.path.join(self.order_info['svn'],'Aeg2DB_'+self.order_info['ver']+'.0_'+self.order_info['order_name']+'_实施文档.docx')
        self.docx_info['allxgp_ver']=self.order_info['ver']+'.10.1.0'
        self.docx_info['allxgp_exe']='Aeg2DB_'+self.order_info['ver']+'.10.1.0_'+self.order_info['order_name']+'.exe'
        self.docx_info['onexgp_ver']=self.order_info['ver']+'.30.1.0'
        self.docx_info['onexgp_exe']='Aeg2DB_'+self.order_info['ver']+'.30.1.0_'+self.order_info['order_name']+'.exe'        
        self.docx_info['clctgp_ver']=self.getVer(self.docx_info['clctgp_svn'], self.order_info['order_name'], 'CLCTDB_Build')+'.4.1.0'
        self.docx_info['clctgp_exe']='CLCTDB_'+self.docx_info['clctgp_ver']+'_'+self.order_info['order_name']+'.exe'        
        self.docx_info['pvdb_ver']=self.getVer(self.order_info['svn'], self.order_info['order_name'], 'Aeg2DBCheck_Build')+'.1.0'
        self.docx_info['pvdb_exe']='Aeg2DBCheck_'+self.docx_info['pvdb_ver']+''+self.order_info['order_name']+'.exe'
        self.inputTask('allxgp','所有高频组')
        self.inputTask('onexgp','单个高频组')
        # 获取该工单要在哪个单个高频库上部署
        if self.docx_info['onexgp_task'] in (1,2):
            while True:
                onexgp_db=input('''请选择该工单需要在哪个高频组库部署：
                1.XGP11;
                2.XGP21;
                3.XGP31;
                4.XGP41;
                6.XGP61;
                7.XGP71.
                请输入1、2、3、4、6、7选择(默认为XGP11)：''').strip()
                if onexgp_db in ('1','2','3','4','6','7'):
                    self.docx_info['onexgp_db']='XGP'+onexgp_db+'1'
                    break
                elif not onexgp_db:
                    self.docx_info['onexgp_db']='XGP11'
                    break
                else:
                    print('你的选择项不正确！')
            
        self.inputTask('clctgp','高频归集库')
        self.inputTask('pvdb','高频计奖验证库') 
        
        # 输入开始操作时间
        while True:
            start_time=input('请输入该工单部署开始时间（格式HH24:MI）：').strip()
            if not start_time:
                print('你的输入为空，请重新输入！')
            else:
                self.docx_info['start_time']=start_time
                break
        
            
    def plsqlLogin(self,user,db_group,tab):
        '''
        plsql登录操作
        '''
        row=tab.Rows.Count-1        
        tab.Rows[row].Cells[1].Range.Text='pl/sql登录\n填入相关信息'
        tab.Rows[row].Cells[2].Range.Text='用户名：'+user+'\n数据库：'+db_group
        if row==1:
            tab.Rows[row].Cells[4].Range.Text=self.docx_info['start_time']
        tab.Rows.Add()
    
    def preCheck(self,tab, w, ole_name):
        '''
        在数据库更新部分插入前置检查部分
        '''
        row=tab.Rows.Count-1
        tab.Rows[row].Cells[1].Range.Text='执行前置检查脚本'
        # 嵌入前置检查脚本
        tab.Rows[row].Cells[2].Select()
        a = w.Selection
        f = r'C:\workshop\python\order\template\pre_check_' + ole_name.lower() + '.sql'
        f = shutil.copy(r'C:\workshop\python\order\template\pre_check.sql', f)
        a.InlineShapes.AddOLEObject(ClassType='SQL',FileName= f)
        os.remove(f)
        tab.Rows[row].Cells[3].Range.Text='无错误窗口弹出，表示检查正确。'
        tab.Rows.Add()
    def updateCheck(self, tab, w, ole_name):
        '''
        更新检查部分
        '''
        row=tab.Rows.Count-1
        tab.Rows[row].Cells[1].Range.Text='执行更新检查脚本'
        tab.Rows[row].Cells[2].Select()
        a = w.Selection
        f = r'C:\workshop\python\order\template\update_check_' + ole_name.lower() + '.sql'
        f = shutil.copy(r'C:\workshop\python\order\template\pre_check.sql', f)
        a.InlineShapes.AddOLEObject(ClassType='SQL',FileName= f)
        os.remove(f)
        tab.Rows[row].Cells[3].Range.Text='无错误窗口弹出，表示检查正确。'
        tab.Rows.Add()        
    def insVer(self, tab, ver):
        '''
        插入版本信息
        '''
        sql_str = "DECLARE\n"
        sql_str = sql_str + "  v_order_name       VARCHAR2(200) := '" + self.order_info['order_name'] + "';\n"
        sql_str = sql_str + "  v_order_no         VARCHAR2(200) := '" + self.order_info['order_no'] + "';\n"
        sql_str = sql_str + "  v_db_version       VARCHAR2(20) := '" + ver + "';\n"
        sql_str = sql_str + "  v_developer        VARCHAR2(20) := '" + self.order_info['developer'] + "';\n"
        sql_str = sql_str + "BEGIN\n"
        sql_str = sql_str + "  --插入版本信息\n"
        sql_str = sql_str + "  p_all_insert_log(v_db_version, v_order_name, v_order_no, v_order_name, v_developer);\n"
        sql_str = sql_str + "END;\n"
        sql_str = sql_str + "/"
        
        row=tab.Rows.Count-1
        tab.Rows[row].Cells[1].Range.Text = '插入版本信息'
        tab.Rows[row].Cells[2].Range.Text = sql_str
        tab.Rows.Add()
        
    def verCheck(self, tab, ver):
        '''
        版本检查
        '''
        row=tab.Rows.Count-1
        tab.Rows[row].Cells[1].Range.Text = '检查版本信息'
        tab.Rows[row].Cells[2].Range.Text = "select * from log_db_version where db_version='"+ ver+ "';"
        tab.Rows[row].Cells[3].Range.Text = '有记录返回则正确。'
        tab.Rows.Add()
    def backup(self, tab):
        '''
        在实施文档中插入备份脚本
        '''
        sql_str = "DECLARE\n"
        sql_str = sql_str + "  v_order_name VARCHAR2(400) := '" + self.order_info['order_name'] + "';\n"
        sql_str = sql_str + "  PROCEDURE wh_backup_data(p_tab IN VARCHAR2, p_condition IN VARCHAR2, p_comment IN VARCHAR2) IS\n"
        sql_str = sql_str + "    v_tab VARCHAR2(4000) := substr(p_tab, 1, 18) || to_char(SYSDATE, 'YYMMDDHH24MISS');\n"
        sql_str = sql_str + "    v_sql VARCHAR2(4000) := 'create table ' || v_tab || ' as select * from ' || p_tab || chr(10) || p_condition;\n"
        sql_str = sql_str + "  BEGIN\n"
        sql_str = sql_str + "    EXECUTE IMMEDIATE v_sql;\n"
        sql_str = sql_str + "    v_sql := 'comment on table ' || v_tab || ' is ''' || p_comment || '''';\n"
        sql_str = sql_str + "    EXECUTE IMMEDIATE v_sql;\n"
        sql_str = sql_str + "  END;\n"
        sql_str = sql_str + "BEGIN\n"
        sql_str = sql_str + "  --执行备份脚本\n"
        sql_str = sql_str + "  NULL;\n"
        sql_str = sql_str + "END;\n"
        sql_str = sql_str + "/\n"
        row=tab.Rows.Count-1
        tab.Rows[row].Cells[1].Range.Text = '执行数据备份脚本'
        tab.Rows[row].Cells[2].Range.Text = sql_str
        tab.Rows.Add()
        
    def insApp(self,exe_name,user,db_group,tab):
        '''
        向实施文档中插入应用信息
        '''
        row=tab.Rows.Count-1
        tab.Rows[row].Cells[1].Range.Text='下载更新包'
        tab.Rows[row].Cells[2].Range.Text='更新包：'+exe_name+'\n来源端：运维补充\n目标端：运维补充'
        
        tab.Rows.Add()
        row=row+1
        tab.Rows[row].Cells[1].Range.Text='打开“数据库更新工具”，输入更新程序的相对路径名称，确认无误点击开始后，出现选择认证账号的界面'
        tab.Rows[row].Cells[2].Range.Text=exe_name   
        
        tab.Rows.Add()
        row=row+1
        tab.Rows[row].Cells[1].Range.Text='执行更新包\n填入相关信息'
        tab.Rows[row].Cells[2].Range.Text='用户名：'+user+'\n服务器：'+ db_group+'\n参数列表：'   
        
        tab.Rows.Add()
        row=row+1
        tab.Rows[row].Cells[1].Range.Text='检查更新操作日志'
        
        tab.Rows.Add()
    
    def insRow(self, tab, row_list):
        '''
        向操作表中插入一条记录，row_list为列表
        '''
        row=tab.Rows.Count-1
        for i in range(len(row_list)):
            if row_list[i]:
                # tab.Rows[row].Cells[i] = row_list[i]
                tab.Rows[row].Cells[i].Range.Text = row_list[i]
        # 增加一行
        tab.Rows.Add()
    
    def rbk(self, tab, ole_name, w):
        '''
        回退函数，完成新增对象回退、数据回退和修改程序回退
        '''
        row = tab.Rows.Count - 1
        # 回退新增的对象
        tab.Rows[row].Cells[1].Range.Text = '执行新增对象回退脚本'
        tab.Rows[row].Cells[2].Select()
        a = w.Selection
        f = r'C:\workshop\python\order\template\new_obj_rollback_' + ole_name.lower() + '.sql'
        f = shutil.copy(r'C:\workshop\python\order\template\new_obj_rollback.sql', f)
        a.InlineShapes.AddOLEObject(ClassType='SQL',FileName= f)
        os.remove(f)
        tab.Rows.Add()
        
        # 回退数据
        row = row + 1
        tab.Rows[row].Cells[1].Range.Text = '执行数据回退脚本'
        tab.Rows[row].Cells[2].Select()
        a = w.Selection
        f = r'C:\workshop\python\order\template\data_rollback_' + ole_name.lower() + '.sql'
        f = shutil.copy(r'C:\workshop\python\order\template\data_rollback.sql', f)
        a.InlineShapes.AddOLEObject(ClassType='SQL',FileName= f)
        os.remove(f)
        tab.Rows.Add()
        
        # 回退修改的程序
        row = row + 1
        tab.Rows[row].Cells[1].Range.Text = '执行回退修改的程序脚本'
        tab.Rows[row].Cells[2].Select()
        a = w.Selection
        f = r'C:\workshop\python\order\template\program_rollback_' + ole_name.lower() + '.sql'
        f = shutil.copy(r'C:\workshop\python\order\template\program_rollback.sql', f)
        a.InlineShapes.AddOLEObject(ClassType='SQL',FileName= f)
        os.remove(f)
        tab.Rows.Add()
        row = row + 1
        tab.Rows[row].Cells[1].Range.Text = '将output窗口的输出内容拷贝到sql命令窗口执行，完成回退修改的程序。'
        tab.Rows[row].Cells[3].Range.Text = '注意检查回退程序的状态是否有效。'
        tab.Rows.Add()
    
    def createDocFile(self):
        '''
        由模板文件创建工单的实施文档
        '''
        # 由模板文件复制成实施文档
        shutil.copy(self.docx_info['template_file'],self.docx_info['doc_file'])
        # 启动独立的进程
        w=win32com.client.Dispatch('Word.Application')
        # 后台运行，不显示，不警告
        w.Visible=0
        w.DisplayAlerts=0
        # 打开新的文件
        doc=w.Documents.Open(self.docx_info['doc_file'])
        # 填充工单信息表格的内容
        doc.Tables[0].Rows[0].Cells[1].Range.Text=self.order_info['order_no']
        doc.Tables[0].Rows[1].Cells[1].Range.Text=self.order_info['order_name']
        doc.Tables[0].Rows[1].Cells[5].Range.Text=self.docx_info['spend_time']
        doc.Tables[0].Rows[2].Cells[1].Range.Text=self.docx_info['notice']
        doc.Tables[0].Rows[3].Cells[1].Range.Text=self.docx_info['dependent_order']
        
        # 填充数据库更新部分(所有高频组数据库)
        if self.docx_info['allxgp_task'] in (1,2):
            db_group='XGP11、XGP21、XGP31、XGP41、XGP61、XGP71'
            # plsql 登录
            self.plsqlLogin(self.docx_info['xgp_user'], db_group, doc.Tables[1])
            # 前置检查
            self.preCheck(doc.Tables[1], w, 'all')
            # 数据备份
            self.backup(doc.Tables[1])
            if self.docx_info['allxgp_task']==2:
                # 在实施文档中增加操作可执行程序信息
                self.insApp(self.docx_info['allxgp_exe'], self.docx_info['xgp_user'], db_group,doc.Tables[1])
            # 如果没有应用程序，那么插入版本信息
            if self.docx_info['allxgp_task'] == 1:
                self.insVer(doc.Tables[1], self.docx_info['allxgp_ver'])
            # 更新检查
            self.updateCheck(doc.Tables[1], w, 'all')
            # 检查版本信息
            self.verCheck(doc.Tables[1], self.docx_info['allxgp_ver'])
            
        # 填充数据库更新部分（单个高频组数据库）
        if self.docx_info['onexgp_task'] in (1, 2):
            # plsql 登录
            self.plsqlLogin(self.docx_info['xgp_user'], self.docx_info['onexgp_db'], doc.Tables[1])
            
            # 前置检查
            self.preCheck(doc.Tables[1], w, self.docx_info['onexgp_db'])
            
            # 数据备份
            self.backup(doc.Tables[1])
            
            if self.docx_info['onexgp_task'] == 2:
                # 增加可执行程序部分
                self.insApp(self.docx_info['onexgp_exe'], self.docx_info['xgp_user'], self.docx_info['onexgp_db'], doc.Tables[1])
            elif self.docx_info['onexgp_task'] == 1:
                # 增加更新操作内容
                rec = ['', '执行更新脚本', '', '', '', '']
                self.insRow(doc.Tables[1], rec)
            
            # 更新检查
            self.updateCheck(doc.Tables[1], w, self.docx_info['onexgp_db'])
            
            # 如果没有应用程序，那么插入版本信息
            if self.docx_info['onexgp_task'] == 1:
                self.insVer(doc.Tables[1], self.docx_info['onexgp_ver'])
            
            # 检查版本信息
            self.verCheck(doc.Tables[1], self.docx_info['onexgp_ver'])
        
        # 填充数据库更新部分（高频归集库）
        if self.docx_info['clctgp_task'] in (1, 2):
            # plsql登录
            self.plsqlLogin(self.docx_info['xgp_user'], 'CLCTGP', doc.Tables[1])
            
            # 前置检查
            self.preCheck(doc.Tables[1], w, 'CLCTGP')
            
            # 数据备份
            self.backup(doc.Tables[1])
            
            # 增加应用程序部分
            if self.docx_info['clctgp_task'] == 2:
                self.insApp(self.docx_info['clctgp_exe'], self.docx_info['clctgp_user'], 'CLCTGP', doc.Tables[1])
            # 更新检查
            self.updateCheck(doc.Tables[1], w, 'CLCTGP')
        
        # 填充数据库更新部分（高频计奖验证库）
        if self.docx_info['pvdb_task'] in (1, 2):
            # plsql 登录
            self.plsqlLogin(self.docx_info['pvdb_user'], 'aegean2', doc.Tables[1])
            
            # 前置检查
            self.preCheck(doc.Tables[1], w, 'aegean2')
            
            # 数据备份
            self.backup(doc.Tables[1])
            
            # 增加应用程序部分
            if self.docx_info['pvdb_task'] == 2:
                self.insApp(self.docx_info['pvdb_exe'], self.docx_info['pvdb_user'], 'aegean2', doc.Tables[1])
            
            # 更新检查
            self.updateCheck(doc.Tables[1], w, 'aegean2')
            
            # 如果没有应用程序，那么插入版本信息
            if self.docx_info['pvdb_task'] == 1:
                self.insVer(doc.Tables[1], self.docx_info['pvdb_ver'])
            
            # 检查版本信息
            self.verCheck(doc.Tables[1], self.docx_info['pvdb_ver'])
        
        # 填充数据库回退部分
        
        # 填充所有高频库回退部分
        if self.docx_info['allxgp_task'] in (1, 2):
            # plsql登录
            db_group='XGP11、XGP21、XGP31、XGP41、XGP61、XGP71'
            self.plsqlLogin(self.docx_info['xgp_user'], db_group, doc.Tables[2])
            self.rbk(doc.Tables[2], 'allxgp', w)
            
        
        # 填充单组高频库回退部分
        if self.docx_info['onexgp_task'] in (1, 2):
            # plsql登录
            self.plsqlLogin(self.docx_info['xgp_user'], self.docx_info['onexgp_db'], doc.Tables[2])
            self.rbk(doc.Tables[2], self.docx_info['onexgp_db'], w)            
        
        # 填充高频归集库回退部分
        if self.docx_info['clctgp_task'] in (1, 2):
            # plsql登录
            self.plsqlLogin(self.docx_info['clctgp_user'], 'clctgp', doc.Tables[2])
            self.rbk(doc.Tables[2], 'clctgp', w) 
        
        # 填充高频计奖验证库回退部分
        if self.docx_info['pvdb_task'] in (1, 2):
            # plsql 登录
            self.plsqlLogin(self.docx_info['pvdb_user'], 'aegean2', doc.Tables[2])
            self.rbk(doc.Tables[2], 'aegean2', w)
                
        doc.Close()
        w.Quit()

