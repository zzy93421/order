# -*- coding:utf-8 -*-
import mydb
import re
db = mydb.MyDB()

#为测试，先清理数据
def delmany(items):
    if items:        
        for item in items:
            db.session.delete(item)
    db.session.commit()
    
order = db.session.query(mydb.Order).all()
delmany(order)
    
op = db.session.query(mydb.Order_Product).all()
delmany(op)

obd = db.session.query(mydb.Order_Batch_DB).all()
delmany(obd)
ob = db.session.query(mydb.Order_Batch).all()
delmany(ob)

def check_sel(input_item):
    result = re.match('([0-9]+#?)+[0-9]*',input_item)
    if result and result.group() == input_item:
        return True
    else:
        return False

#输入工单编号
while True:
    order_no_input = input('请输入工单编号：').strip()
    if order_no_input:
        break
    else:
        print('工单编号不能为空，请重新输入！')
        
#查询该工单是否已经存在
order_rec = db.session.query(mydb.Order).filter_by(order_no = order_no_input).all()
if order_rec:
    print(order_rec)
else:
    #输入工单名称
    while True:
        order_name_input = input('请输入工单名称：').strip()
        if order_name_input:
            break
        else:
            print('工单名称不能为空，请重新输入！')
        
    #向数据库记录工单信息
    order = mydb.Order(order_no = order_no_input, order_name = order_name_input)
    db.session.add(order)
    
    #选择当前工单的研发人员及研发负责人
    persons = db.session.query(mydb.Person.id, mydb.Person.name).order_by(mydb.Person.id).all()
    while True:        
        print('请选择工单研发人员及负责人：')
        for row in persons:
            print('\t' + str(row[0]) + '.' + row[1])
        person_str = input('请输入数字选择研发人员和研发负责人（格式：2#3，2表示研发人员ID，3表示研发负责人ID）：').strip()
        
        #检查输入的合法性
        if check_sel(person_str):
            person_list = person_str.split('#')
            developer_id = int(person_list[0])
            director_id = int(person_list[1])
            #向数据库记录工单的当前批次
            ob = mydb.Order_Batch(order_no = order_no_input, batch_order_no = order_no_input, \
                                  batch_order_name = order_name_input, batch_developer_id = developer_id, \
                                  batch_director_id = director_id, batch_id = 1)
            break
    
    #输入该工单部署的DB范围
    all_db_rows = db.session.query(mydb.DB).order_by(mydb.DB.id).all()
    while True:
        db_all_list = []
        print('请选择当前工单部署的DB范围：')
        for rec in all_db_rows:
            db_all_list.append(rec.id)
            print('\t', str(rec.id) + '.', rec.remark)
        db_str = input('请输入数字选择（格式：2#3）：').strip()
        if db_str and check_sel(db_str):
            if '#' in db_str:
                db_sel_list = db_str.split('#')
            else:
                db_sel_list = [db_str]
            db_sel_list = [int(x) for x in db_sel_list]
            db_err_list = [x for x in db_sel_list if x not in db_all_list]
            if db_err_list:
                print('选择了无效的选项：', db_err_list)
                print('请重新选择！')
            else:
                #向数据库记录该工单对应的DB范围
                for db_id in db_sel_list:
                    obd = mydb.Order_Batch_DB(order_no = order_no_input, batch_id = 1, db_id = db_id)
                    db.session.add(obd)
                break
    db.session.commit()
    
    #输入工单发布物
    while True:
        print('请选择工单发布物：')
        pds = db.session.execute("""select sc.name,kv.key,kv.val from kv,system_code sc
        where kv.system_code_id=sc.id
        and sc.name='ORDER_PRODUCT' order by kv.key""")
        pd_all_list = []
        for row in pds:
            pd_all_list.append(row[1])
            print('\t', str(row[1]) + '.', row[2])
        pd_str = input('请输入数字选择（格式：2#3#4）：').strip()
        if pd_str and check_sel(pd_str):
            pd_list = pd_str.split('#')
            pd_list = [int(x) for x in pd_list]
            pd_err_list = [x for x in pd_list if x not in pd_all_list]
            if pd_err_list:
                print('存在不正确的选项:' , pd_err_list)
                print('请重新选择！')
            else:
                #向DB记录工单发布物order_product
                for product_id in pd_list:
                    op = mydb.Order_Product(order_no = order_no_input, product_id = product_id)
                    db.session.add(op)
                db.session.commit()
                break
    #products = db.session.query(mydb.KV).filter_by(mydb.KV.system_code_id = 2)
    #输入工单分批情况
    #输入工单分批对应的DB情况
    #输入工单变更的应用程序
    #输入变更的应用程序与DB对应情况
    
    
        

print('程序执行完毕！')
    