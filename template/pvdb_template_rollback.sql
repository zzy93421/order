variable v_rdc_name VARCHAR2(10)
variable v_db_version VARCHAR2(30)
variable v_title VARCHAR2(100)
variable v_db_type NUMBER
variable v_task_no VARCHAR2(100)
variable v_task_name VARCHAR2(100)
variable v_developer VARCHAR2(100)


--���ݿ����ͣ�1:����rdc��2������ndc��3����Ƶ��4���鼯��
exec  :v_db_version:= '{pvdb_ver}.3.0';
exec  :v_title:= '{exe_name}';
exec  :v_task_no:='{order_no}';
exec  :v_task_name:='{exe_name}';
exec  :v_developer:='��־Զ';


--��������
--exec  p_all_backup_tables('user_source', :v_title);

PROMPT ����ҵ�����-��ʼ
PROMPT ��дά���������wh_check_pvdb
@@wh_check_pvdb.pck

PROMPT ==================��ʼǰ�ü��========================

PROMPT ����Ƿ��ڸ�Ƶ�ƽ���֤�����
DECLARE
  v_exception EXCEPTION;
BEGIN
  IF USER <> 'XGP_CHECK' THEN
    dbms_output.put_line('���θ��±���ʹ��XGP_CHECK�û�ִ��');
    RAISE v_exception;
  END IF;
END;
/

PROMPT ǰ�ü��ù����Ƿ��Ѿ�����
call wh_check_pvdb.check_order_ver(:v_db_version,1);

PROMPT ����޸Ķ���汾��Ϣ
--call wh_check_pvdb.check_modify_obj('p_count_win_4p4y_yu#','2.8#');

PROMPT ==================ִ�й�������====================


PROMPT ==================ִ�л��˼��====================
PROMPT ����޸Ķ���汾��Ϣ
--call wh_check_pvdb.check_modify_obj('p_count_win_4p4y_yu#','2.7#');

PROMPT ����ҵ�����-���
--���˰汾��¼
PROMPT ���˰汾��¼
DELETE FROM log_db_version WHERE db_version =:v_db_version;
COMMIT;
PROMPT ���ù������˺�汾��Ϣ
call wh_check_pvdb.check_order_ver(:v_db_version,0);

call DBMS_OUTPUT.put_line('end_time '||TO_CHAR(SYSDATE,'yyyy-mm-dd hh24:mi:ss'));

call dbms_output.put_line('���ݿ�' || :v_db_version || '�汾���˲�������ִ�гɹ�!');

EXIT;
