variable v_rdc_name VARCHAR2(10)
variable v_db_version VARCHAR2(30)
variable v_title VARCHAR2(100)
variable v_db_type NUMBER
variable v_task_no VARCHAR2(100)
variable v_task_name VARCHAR2(100)
variable v_developer VARCHAR2(100)


--数据库类型：1:热线rdc；2：热线ndc；3：高频；4：归集；
exec  :v_db_version:= '{pvdb_ver}.3.0';
exec  :v_title:= '{exe_name}';
exec  :v_task_no:='{order_no}';
exec  :v_task_name:='{exe_name}';
exec  :v_developer:='张志远';


--备份数据
--exec  p_all_backup_tables('user_source', :v_title);

PROMPT 具体业务代码-开始
PROMPT 编写维护检查程序包wh_check_pvdb
@@wh_check_pvdb.pck

PROMPT ==================开始前置检查========================

PROMPT 检查是否在高频计奖验证库更新
DECLARE
  v_exception EXCEPTION;
BEGIN
  IF USER <> 'XGP_CHECK' THEN
    dbms_output.put_line('本次更新必须使用XGP_CHECK用户执行');
    RAISE v_exception;
  END IF;
END;
/

PROMPT 前置检查该工单是否已经部署
call wh_check_pvdb.check_order_ver(:v_db_version,1);

PROMPT 检查修改对象版本信息
--call wh_check_pvdb.check_modify_obj('p_count_win_4p4y_yu#','2.8#');

PROMPT ==================执行工单回退====================


PROMPT ==================执行回退检查====================
PROMPT 检查修改对象版本信息
--call wh_check_pvdb.check_modify_obj('p_count_win_4p4y_yu#','2.7#');

PROMPT 具体业务代码-完成
--回退版本记录
PROMPT 回退版本记录
DELETE FROM log_db_version WHERE db_version =:v_db_version;
COMMIT;
PROMPT 检查该工单回退后版本信息
call wh_check_pvdb.check_order_ver(:v_db_version,0);

call DBMS_OUTPUT.put_line('end_time '||TO_CHAR(SYSDATE,'yyyy-mm-dd hh24:mi:ss'));

call dbms_output.put_line('数据库' || :v_db_version || '版本回退操作更新执行成功!');

EXIT;
