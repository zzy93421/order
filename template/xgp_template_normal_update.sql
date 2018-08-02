variable v_rdc_name VARCHAR2(10)
variable v_db_version VARCHAR2(30)
variable v_title VARCHAR2(100)
variable v_db_type NUMBER
variable v_task_no VARCHAR2(100)
variable v_task_name VARCHAR2(100)
variable v_developer VARCHAR2(100)

--数据库类型：1:热线rdc；2：热线ndc；3：高频；4：归集；
exec  :v_db_type:= 3;
exec  :v_db_version:= '{xgp_ver}.10.1.0';
exec  :v_title:= '{exe_name}';
exec  :v_task_no:='{order_no}';
exec  :v_task_name:='{exe_name}';
exec  :v_developer:='张志远';

--检查更新数据库和使用的用户是否正确
exec  p_all_check_db_user(:v_db_type, :v_rdc_name); 
--备份数据
--exec  p_all_backup_tables('', :v_title);

PROMPT 具体业务代码-开始

PROMPT =================编译维护程序包===================

PROMPT 部署维护检查程序包wh_check
@@wh_check.pck

PROMPT 部署回退程序包wh_rbk
@@wh_rbk.pck

PROMPT ==================执行前置检查====================
PROMPT 前置检查该工单是否已经部署
call wh_check.check_order_ver(:v_db_version,0);

PROMPT 检查修改对象版本信息
--call wh_check.check_modify_obj('lconvert_readable_gp44y#pkg_stake_split#','4.0#14.0#');



PROMPT ==================执行工单更新====================



PROMPT ==================执行更新检查====================
PROMPT 检查修改对象版本信息
--call wh_check.check_modify_obj('lconvert_readable_gp44y#pkg_stake_split#','4.1#15.0#');

PROMPT 具体业务代码-完成
--插入版本更新记录
exec  p_all_insert_log(:v_db_version, :v_title,:v_task_no,:v_task_name,:v_developer);
PROMPT 前置检查该工单版本信息
call wh_check.check_order_ver(:v_db_version,1);

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
