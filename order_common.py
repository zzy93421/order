#-*-coding:utf-8-*-
import os
import re
class Order(object):
    '''
    共用工单类
    '''
    def __init__(self,order_no,order_name,backup_tabs):
        '''
        初始化函数
        '''
        self.order_info={'order_name':order_name,
                         'order_no':order_no,
                         'developer':'张志远',
                         'developer_phone':'7443',
                         'developer_mobile':'13910572957',
                         'manager':'陈伟',
                         'manager_phone':'7526',
                         'manger_mobile':'15010119690',
                         'all_file':'',
                         'readme_file':'',
                         'config_file':'',
                         'exe_file_name':'',
                         'user':'',
                         'pwd':'',
                         'db_range':'',  
                         'ver':'',
                         'svn':r'c:\workshop\gp\db\Aegean2_update',
                         'work_order_path':'',  
                         'backup_tabs':backup_tabs,
                         'rdc_name':'',
                         }
        
    def input_info(self,name,message):
        '''
        共用输入函数
        '''
        while True:
            self.order_info[name]=input(message).strip()
            if self.order_info[name]:
                break
            else:
                print('输入信息为空！\n')
    def createPath(self,path):
        '''
        创建目录
        '''
        #判断工作目录是否存在
        if os.path.exists(path):
            print('目录'+path+'已经存在，无需再创建！')
        else:
            os.makedirs(path)
            print('目录'+path+'创建成功！')
    def createFile(self,file,text):
        '''
        创建文件
        '''
        #分离出目录与文件
        path=os.path.split(file)[0]
        #创建目录
        if not os.path.exists(path):
            self.createPath(path)
        #创建文件
        if os.path.exists(file):
            print('文件'+file+'已经存在！')
        else:
            f=open(os.path.join(path,file),'w')
            f.write(text)
            f.close()
            print('文件'+os.path.join(path,file)+'创建成功！')
    
    def getVer(self,path,order_name,start_str):
        '''
        获取版本信息
        '''
        pattern=re.compile('Build\d+\.\d+')
        pathdir=os.listdir(path)
        pathdir=[x for x in pathdir if start_str in x]
        ver=''
        max_ver_list=['0','0']
        for i in pathdir:
            match=pattern.search(i)
            current_ver=match.group()
            current_ver_list=current_ver[5:].split('.')
            if int(current_ver_list[0])>int(max_ver_list[0]) or (int(current_ver_list[0])==int(max_ver_list[0]) and int(current_ver_list[1])>int(max_ver_list[1])):
                max_ver_list=current_ver_list
            if order_name in i:
                ver=current_ver
        if not ver:
            #工单版本文件不存在，获取下一版本号
            max_ver_list[1]=str(int(max_ver_list[1])+1).zfill(len(max_ver_list[1]))
            ver='Build'+'.'.join(max_ver_list)
        return(ver)
    def createConfigFile(self,config_file,user,pwd):
        '''
        通用创建config.ini文件
        '''
        config_content="[general]\n"
        config_content=config_content+"title="+self.order_info['order_name']+"\n"
        config_content=config_content+"buttonCaption=开始(&E)\n"
        config_content=config_content+"promptMessage=完成!请检查日志\n"
        config_content=config_content+"icoFile=UpdateIt.ico\n\n"
    
        config_content=config_content+"[execute]\n"
        config_content=config_content+"runCount=1\n"
        config_content=config_content+"run1=all.sql\n\n"
    
        config_content=config_content+"[database]\n"
        config_content=config_content+"server=\n"
        config_content=config_content+"user="+user+"\n"
        config_content=config_content+"password="+pwd+"\n"
        config_content=config_content+"parameters=\n"
        config_content=config_content+"successmsg1=更新执行成功\n"
        config_content=config_content+"errmsg1=ORA-\n"
        config_content=config_content+"errmsg2=SP2\n"
        config_content=config_content+"errmsg3=警告\n\n"
    
        config_content=config_content+"[makedir]\n"
        config_content=config_content+";Directory=c:\\result\n\n"
    
        config_content=config_content+"[limit]\n"
        config_content=config_content+"iprange=*.*.*.*\n"
        config_content=config_content+"timebefore=2004-03-08 12:00:00\n"
        config_content=config_content+"timeafter=2004-03-08 12:00:00\n"
    
        self.createFile(config_file,config_content)
        
    def createReadmeFile(self,readme_file,db_range,user):
        '''
        通用创建readme.txt文件函数
        '''
        readme_file_content="1、本工具用于"+self.order_info['order_name']+"；\n\n"
        readme_file_content=readme_file_content+"2、本工具必须在"+db_range+"上执行；\n\n"
        readme_file_content=readme_file_content+"3、本工具需要使用"+user+"用户执行；\n\n"
        readme_file_content=readme_file_content+"4、本工具需要输入数据库密码、服务器名；\n\n"
        readme_file_content=readme_file_content+"5、执行完后请检查当前目录中的日志！\n"
        self.createFile(readme_file,readme_file_content)
    
    def createAllFile(self,all_file,exe_file_name,ver):
        '''
        通用创建all.sql文件函数
        '''
        all_file_content='WHENEVER sqlerror EXIT;\n'
        all_file_content=all_file_content+'set serveroutput on size 1000000 format wrapped\n'
        all_file_content=all_file_content+'set feed on\n'
        all_file_content=all_file_content+'set autop off\n\n'
    
        all_file_content=all_file_content+"call DBMS_OUTPUT.put_line('start_time '||TO_CHAR(SYSDATE,'yyyy-mm-dd hh24:mi:ss'));\n"
        all_file_content=all_file_content+"--updatename,"+exe_file_name+'\n'
        all_file_content=all_file_content+"--svn,99999\n\n"
    
        all_file_content=all_file_content+"variable v_rdc_name VARCHAR2(10)\n"
        all_file_content=all_file_content+"variable v_db_version VARCHAR2(30)\n"
        all_file_content=all_file_content+"variable v_title VARCHAR2(100)\n"
        all_file_content=all_file_content+"variable v_db_type NUMBER\n"
        all_file_content=all_file_content+"variable v_task_no VARCHAR2(100)\n"
        all_file_content=all_file_content+"variable v_task_name VARCHAR2(100)\n"
        all_file_content=all_file_content+"variable v_developer VARCHAR2(100)\n\n"
    
        all_file_content=all_file_content+"--数据库类型：1:热线rdc；2：热线ndc；3：高频；4：归集；\n"
        all_file_content=all_file_content+"exec  :v_db_type:= 3;\n"
        if self.order_info['rdc_name']:
            all_file_content=all_file_content+"exec  :v_rdc_name := '"+self.order_info['rdc_name']+"';\n"
        all_file_content=all_file_content+"exec  :v_db_version:= '"+ver+"';\n"
        all_file_content=all_file_content+"exec  :v_title:= '"+self.order_info['order_name']+"';\n"
        all_file_content=all_file_content+"exec  :v_task_no:='"+self.order_info['order_no']+"';\n"
        all_file_content=all_file_content+"exec  :v_task_name:='"+self.order_info['order_name']+"';\n"
        all_file_content=all_file_content+"exec  :v_developer:='"+self.order_info['developer']+"';\n\n"
    
        all_file_content=all_file_content+"--检查更新数据库和使用的用户是否正确\n"
        all_file_content=all_file_content+"exec  p_all_check_db_user(:v_db_type, :v_rdc_name); \n"
        all_file_content=all_file_content+"--备份数据\n"
        all_file_content=all_file_content+"exec  p_all_backup_tables('"+self.order_info['backup_tabs']+"', :v_title);\n\n"
    
        all_file_content=all_file_content+"PROMPT 具体业务代码-开始\n\n\n"
        all_file_content=all_file_content+"PROMPT 具体业务代码-完成\n"
        all_file_content=all_file_content+"--插入版本更新记录\n"
        all_file_content=all_file_content+"exec  p_all_insert_log(:v_db_version, :v_title,:v_task_no,:v_task_name,:v_developer);\n\n"
    
        all_file_content=all_file_content+"call DBMS_OUTPUT.put_line('end_time '||TO_CHAR(SYSDATE,'yyyy-mm-dd hh24:mi:ss'));\n\n"
    
        all_file_content=all_file_content+"set linesize 500\n"
        all_file_content=all_file_content+"set pagesize 0\n"
        all_file_content=all_file_content+"set heading on\n"
        all_file_content=all_file_content+"PROMPT\n"
        all_file_content=all_file_content+"PROMPT ============  检查版本记录  ============\n"
        all_file_content=all_file_content+"COLUMN db_version FORMAT A22\n"
        all_file_content=all_file_content+"COLUMN update_time FORMAT A22\n"
        all_file_content=all_file_content+"COLUMN descriptions FORMAT A58\n"
        all_file_content=all_file_content+"COLUMN task_no FORMAT A28\n"
        all_file_content=all_file_content+"COLUMN task_name FORMAT A42\n"
        all_file_content=all_file_content+"COLUMN developer FORMAT A10\n"
        all_file_content=all_file_content+"SELECT * FROM log_db_version t where t.db_version = :v_db_version;\n"
        all_file_content=all_file_content+"EXIT;\n"
    
        self.createFile(all_file,all_file_content)            