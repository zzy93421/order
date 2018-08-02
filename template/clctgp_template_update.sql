variable v_rdc_name VARCHAR2(10)
variable v_db_version VARCHAR2(30)
variable v_title VARCHAR2(100)
variable v_db_type NUMBER
variable v_task_no VARCHAR2(100)
variable v_task_name VARCHAR2(100)
variable v_developer VARCHAR2(100)

--数据库类型：1:热线rdc；2：热线ndc；3：高频；4：归集；
exec  :v_db_type:= 3;
exec  :v_db_version:= '{clctgp_ver}.2.0';
exec  :v_title:= '{exe_name}';
exec  :v_task_no:='{order_no}';
exec  :v_task_name:='{exe_name}';
exec  :v_developer:='张志远';

--检查更新数据库和使用的用户是否正确
--exec  p_all_check_db_user(:v_db_type, :v_rdc_name); 
--备份数据
--exec  p_all_backup_tables('', :v_title);

PROMPT 具体业务代码-开始

PROMPT =================编译维护程序包===================

PROMPT 部署维护检查程序包wh_check
@@wh_check_clctgp.pck


PROMPT ==================执行前置检查====================



PROMPT ==================执行工单更新====================



PROMPT ==================执行更新检查====================


PROMPT 具体业务代码-完成

CALL DBMS_OUTPUT.put_line('CLCTDB_{clctgp_ver}.2.0_{exe_name}更新执行成功');
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
