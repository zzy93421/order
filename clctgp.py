#-*-coding:utf-8-*-
import os
import re
from order_common import Order
class CLCTGP(Order):
    '''
    高频归集库类
    '''
    def __init__(self,order_no,order_name,backup_tabs):
        '''
        高频归集库初始化函数
        '''
        super(CLCTGP,self).__init__(order_no,order_name,backup_tabs)
        self.order_info['svn']=r'D:\高频归集\trunk\script\update'
        self.order_info['work_order_path']='D:\\HighFrequencePatch\\'+self.order_info['order_no']+'_'+self.order_info['order_name']+'\\CLCTGP'    
        self.order_info['readme_file']=os.path.join(self.order_info['work_order_path'],'readme.txt')
        self.order_info['all_file']=os.path.join(self.order_info['work_order_path'],'all.sql')
        self.order_info['config_file']=os.path.join(self.order_info['work_order_path'],'config.ini')
        self.order_info['db_range']='高频归集库' 
        self.order_info['user']='aeg2'
        self.order_info['pwd']='aeg2'
        #获取版本信息
        self.order_info['ver']=self.getVer(self.order_info['svn'], self.order_info['order_name'], 'CLCTDB_Build')+'.4.1.0'
        self.order_info['exe_file_name']='CLCTDB_'+self.order_info['ver']+'_'+self.order_info['order_name']
    def createAllFile(self):
        '''
        个性化创建all.sql函数
        '''
        all_content="WHENEVER sqlerror EXIT;\n"
        all_content=all_content+"SET serveroutput ON\n"
        all_content=all_content+"SET feed ON\n"
        all_content=all_content+"SET autop off\n"
        all_content=all_content+"call DBMS_OUTPUT.put_line('start_time '||TO_CHAR(SYSDATE,'yyyy-mm-dd hh24:mi:ss'));\n"
        all_content=all_content+"--updatename,"+self.order_info['exe_file_name']+"\n"
        all_content=all_content+"--svn,99999\n\n"
        
        all_content=all_content+"DECLARE\n"
        all_content=all_content+"  --本工具在归集库上执行；\n"
        all_content=all_content+"  v_username    VARCHAR2(100);\n"
        all_content=all_content+"  v_dbname 	VARCHAR2(100);\n"
        all_content=all_content+"  e_app 	EXCEPTION;\n"
        all_content=all_content+"BEGIN\n"
        all_content=all_content+"  SELECT NAME INTO v_dbname FROM v$database;\n"
        all_content=all_content+"  dbms_output.put_line('数据库：'||v_dbname);\n"
        all_content=all_content+"  IF upper(v_dbname) LIKE 'CSL%' OR upper(SUBSTR(v_dbname,1,3)) IN ('AEG', 'XGP') THEN\n"
        all_content=all_content+"    dbms_output.put_line('本脚本必须在归集数据库上执行');\n"
        all_content=all_content+"    RAISE e_app;\n"
        all_content=all_content+"  END IF;\n"
        all_content=all_content+"  IF user <> 'AEG2' THEN\n"
        all_content=all_content+"    dbms_output.put_line('本次更新必须使用AEG2用户执行');\n"
        all_content=all_content+"    RAISE e_app;\n"
        all_content=all_content+"  END IF;\n"
        all_content=all_content+"END;\n"
        all_content=all_content+"/\n\n"
        
        all_content=all_content+"PROMPT 具体业务代码-开始\n\n\n"
        all_content=all_content+"PROMPT 具体业务代码-完成\n"
        
        all_content=all_content+"PROMPT \n"
        all_content=all_content+"PROMPT ############  下面是实施检查内容  ################################################################\n"
        all_content=all_content+"PROMPT\n"
        all_content=all_content+"PROMPT ============  函数更新情况  ============\n\n\n"
        all_content=all_content+"PROMPT\n"
        all_content=all_content+"CALL DBMS_OUTPUT.put_line('"+self.order_info['exe_file_name']+" 更新执行成功');\n"
        all_content=all_content+"CALL DBMS_OUTPUT.put_line('end_time '||TO_CHAR(SYSDATE,'yyyy-mm-dd hh24:mi:ss'));\n"
        all_content=all_content+"EXIT;\n"
        self.createFile(self.order_info['all_file'], all_content)
        

if __name__=="__main__":
    cg=CLCTGP('XQ_qinzhaohong_20160222003593','派奖促销-【河北】11选5派奖（16年3月）','promotion_definition,game_definition')
    cg.createReadmeFile(cg.order_info['readme_file'], cg.order_info['db_range'], cg.order_info['user'])
    cg.createConfigFile(cg.order_info['config_file'], cg.order_info['user'], cg.order_info['pwd'])
    cg.createAllFile()