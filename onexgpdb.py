#-*-coding:utf-8-*-
import os
import re
from order_common import Order
class OneXGBDB(Order):
    '''
    一个新高频组数据库类，用于创建只在一组高频库执行的目录文件
    '''
    def __init__(self, order_no, order_name,backup_tabs,xgp_db,rdc_name):
        '''
        初始化函数
        '''
        #调用父类初始化函数
        super(OneXGBDB,self).__init__(order_no,order_name,backup_tabs)
        self.xgp_db=xgp_db.zfill(2)
        #初始化变量
        self.order_info['svn']=r'D:\aeg2\Aegean2_update'
        self.order_info['work_order_path']='D:\\HighFrequencePatch\\'+self.order_info['order_no']+'_'+self.order_info['order_name']+'\\Aeg2'+xgp_db.zfill(2)      
        self.order_info['readme_file']=os.path.join(self.order_info['work_order_path'],'readme.txt')
        self.order_info['all_file']=os.path.join(self.order_info['work_order_path'],'all.sql')
        self.order_info['config_file']=os.path.join(self.order_info['work_order_path'],'config.ini')
        self.order_info['db_range']='第'+self.xgp_db[1:2]+'组高频库'
        self.order_info['rdc_name']=rdc_name
        #获取版本信息
        pathdir=os.listdir(self.order_info['svn'])
        pathdir=[x for x in pathdir if 'Aeg2DB_Build' in x]
        for f in pathdir:
            if self.order_info['order_name'] in f:
                self.order_info['svn_file']=f
                pattern=re.compile('Build\d{2}\.\d{3,}')
                match=pattern.search(f)
                self.order_info['ver']=match.group()+'.30.1.0'
        if not self.order_info['svn_file']:
            print('工单：'+self.order_info['order_name']+'的实施文档不存在，请先创建实施文档！')
        self.order_info['exe_file_name']='Aeg2DB_'+self.order_info['ver']+"_"+self.order_info['order_name']

if __name__=="__main__":
    order_no='XQ_qinzhaohong_20160222003593'
    order_name=r'派奖促销-【河北】11选5派奖（16年3月）'
    backup_tabs='game_definition,promotion_definition'
    xgp_db='01'
    rdc_name='河北'
    oxd=OneXGBDB(order_no, order_name, backup_tabs, xgp_db, rdc_name)
    oxd.createReadmeFile(oxd.order_info['readme_file'], oxd.order_info['db_range'], oxd.order_info['user'])
    oxd.createAllFile(oxd.order_info['all_file'], oxd.order_info['exe_file_name'], oxd.order_info['ver'])
    oxd.createConfigFile(oxd.order_info['config_file'], oxd.order_info['user'], oxd.order_info['pwd'])
        
    
        