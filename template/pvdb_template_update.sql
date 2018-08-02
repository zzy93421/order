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
exec  p_all_backup_tables('user_source', :v_title);

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
call wh_check_pvdb.check_order_ver(:v_db_version,0);

PROMPT 检查修改对象版本信息
--call wh_check_pvdb.check_modify_obj('p_count_win_4p4y_yu#','2.7#');

PROMPT ==================执行工单更新====================


PROMPT ==================执行更新检查====================
PROMPT 检查修改对象版本信息
--call wh_check_pvdb.check_modify_obj('p_count_win_4p4y_yu#','2.8#');

PROMPT 具体业务代码-完成
--插入版本更新记录
exec  p_all_insert_log(:v_db_version, :v_title,:v_task_no,:v_task_name,:v_developer);
PROMPT 前置检查该工单版本信息
call wh_check_pvdb.check_order_ver(:v_db_version,1);

call DBMS_OUTPUT.put_line('end_time '||TO_CHAR(SYSDATE,'yyyy-mm-dd hh24:mi:ss'));

set linesize 500
set pagesize 0
set heading on
PROMPT
PROMPT ============  检查版本记录  ============
COLUMN db_version FORMAT A22
COLUMN update_time FORMAT A22
COLUMN descriptions FORMAT A58
COLUMN task_no FORMAT A28
COLUMN task_name FORMAT A42
COLUMN developer FORMAT A10
SELECT * FROM log_db_version t where t.db_version = :v_db_version;
EXIT;
