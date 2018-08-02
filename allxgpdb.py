#-*-coding:utf-8-*-
import os
import re
from order_common import Order
class AllXGPDB(Order):
    '''
    所有组高频库类
    '''
    def __init__(self,order_no,order_name,backup_tabs):
        '''
        初始化函数
        '''
        super(AllXGPDB,self).__init__(order_no,order_name,backup_tabs)
        self.order_info['svn']=r'D:\aeg2\Aegean2_update'
        self.order_info['work_order_path']='D:\\HighFrequencePatch\\'+self.order_info['order_no']+'_'+self.order_info['order_name']+'\\Aeg200'
        self.order_info['db_range']='所有高频组数据库'
        self.order_info['all_file']=os.path.join(self.order_info['work_order_path'],'all.sql')
        self.order_info['readme_file']=os.path.join(self.order_info['work_order_path'],'readme.txt')
        self.order_info['config_file']=os.path.join(self.order_info['work_order_path'],'config.ini')
        self.order_info['ver']=self.getVer(self.order_info['svn'], self.order_info['order_name'], 'Aeg2DB_Build')+'.10.1.0'
        self.order_info['exe_file_name']='Aeg2DB_'+self.order_info['ver']+'_'+self.order_info['order_name']
        self.order_info['user'] = 'helios'
        
if __name__=="__main__":
    axd=AllXGPDB('XQ_qinzhaohong_20160222003593','派奖促销-【河北】11选5派奖（16年3月）','promotion_definition,game_definition')
    axd.createAllFile(axd.order_info['all_file'], axd.order_info['exe_file_name'], axd.order_info['ver'])
    axd.createConfigFile(axd.order_info['config_file'], axd.order_info['user'],axd.order_info['pwd'])
    axd.createReadmeFile(axd.order_info['readme_file'], axd.order_info['db_range'], axd.order_info['user'])
        