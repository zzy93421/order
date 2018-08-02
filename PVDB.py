#-*-coding:utf-8-*-
import os
import re
from order_common import Order
class PVDB(Order):
    '''
    高频计奖验证库类
    '''
    def __init__(self,order_no,order_name,backup_tabs):
        '''
        初始化函数
        '''
        super(PVDB,self).__init__(order_no,order_name,backup_tabs)
        
        self.order_info['svn']=r'D:\aeg2\Aegean2_update'
        self.order_info['work_order_path']='D:\\HighFrequencePatch\\'+self.order_info['order_no']+'_'+self.order_info['order_name']+'\\CheckDB'  
        self.order_info['readme_file']=os.path.join(self.order_info['work_order_path'],'readme.txt')
        self.order_info['all_file']=os.path.join(self.order_info['work_order_path'],'all.sql')
        self.order_info['config_file']=os.path.join(self.order_info['work_order_path'],'config.ini')
        self.order_info['db_range']='高频计奖验证库' 
        self.order_info['user']='xgp_check'
        self.order_info['pwd']='xgp_check'
        self.createVerFile()
        self.order_info['exe_file_name']='Aeg2DBCheck_'+self.order_info['ver']+'_'+self.order_info['order_name']

    def createVerFile(self):
        '''
        获取计奖验证库的版本
        '''
        #pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
        pattern = re.compile(r'\d+\.\d+')
        pathDir=os.listdir(self.order_info['svn'])        
        #检查该工单是否已存在
        p=[x for x in pathDir if "Aeg2DBCheck" in x]
        for i in p:
            if self.order_info['order_name'] in i:
                self.order_info['ver']='Build'+pattern.search(i).group()
                print('工单'+self.order_info['order_name']+'版本占位符文件已经存在！')
                return 0 
        #max_ver=['0','0','0','0']
        max_ver=['0','0']
        for i in p:
            #print(i)
            match=pattern.search(i)
            cur_ver=match.group().split('.')
            if max_ver[0]<cur_ver[0] or (max_ver[0]==cur_ver[0] and max_ver[1]<cur_ver[1]):
                max_ver=cur_ver
        length=len(max_ver[1])
        max_ver[1]=str(int(max_ver[1])+1).zfill(length)
        max_ver.extend(['1', '0'])
        self.order_info['ver']='Build'+'.'.join(max_ver) 
        print(self.order_info['ver'])
        self.order_info['svn_file']='Aeg2DBCheck_Build'+'.'.join(max_ver)+'_'+self.order_info['order_name'] + '.txt'
        self.order_info['svn_file']=os.path.join(self.order_info['svn'],self.order_info['svn_file'])
        f=open(self.order_info['svn_file'],'w')
        f.write(self.order_info['order_no']+':'+self.order_info['order_name'])
        f.close()
        return 1
         

if __name__=="__main__":
    pd=PVDB('XQ_qinzhaohong_20160222003593','派奖促销-【河北】11选5派奖（16年3月）','promotion_definition,game_definition')
    result=pd.createVerFile()
    if result:
        print('创建版本占位符文件成功！')
    else:
        print('创建版本占位符文件失败！')
    pd.createReadmeFile(pd.order_info['readme_file'], pd.order_info['db_range'], pd.order_info['user'])
    pd.createConfigFile(pd.order_info['config_file'], pd.order_info['user'], pd.order_info['pwd'])
    print(pd.order_info['exe_file_name'])
    pd.createAllFile(pd.order_info['all_file'], pd.order_info['exe_file_name'], pd.order_info['ver'])