variable v_rdc_name VARCHAR2(10)
variable v_db_version VARCHAR2(30)
variable v_title VARCHAR2(100)
variable v_db_type NUMBER
variable v_task_no VARCHAR2(100)
variable v_task_name VARCHAR2(100)
variable v_developer VARCHAR2(100)

--���ݿ����ͣ�1:����rdc��2������ndc��3����Ƶ��4���鼯��
exec  :v_db_type:= 3;
exec  :v_db_version:= '{clctgp_ver}.2.0';
exec  :v_title:= '{exe_name}';
exec  :v_task_no:='{order_no}';
exec  :v_task_name:='{exe_name}';
exec  :v_developer:='��־Զ';

--���������ݿ��ʹ�õ��û��Ƿ���ȷ
--exec  p_all_check_db_user(:v_db_type, :v_rdc_name); 
--��������
--exec  p_all_backup_tables('', :v_title);

PROMPT ����ҵ�����-��ʼ

PROMPT =================����ά�������===================

PROMPT ����ά���������wh_check
@@wh_check_clctgp.pck


PROMPT ==================ִ��ǰ�ü��====================



PROMPT ==================ִ�й�������====================



PROMPT ==================ִ�и��¼��====================


PROMPT ����ҵ�����-���

CALL DBMS_OUTPUT.put_line('CLCTDB_{clctgp_ver}.2.0_{exe_name}����ִ�гɹ�');
call DBMS_OUTPUT.put_line('end_time '||TO_CHAR(SYSDATE,'yyyy-mm-dd hh24:mi:ss'));

set linesize 500
set pagesize 0
set heading on
PROMPT
PROMPT ============  ���汾��¼  ============
COLUMN db_version FORMAT A22
COLUMN update_time FORMAT A22
COLUMN descriptions FORMAT A58
COLUMN task_no FORMAT A28
COLUMN task_name FORMAT A42
COLUMN developer FORMAT A10
SELECT * FROM log_db_version t where t.db_version = :v_db_version;
EXIT;
