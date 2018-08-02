WHENEVER sqlerror EXIT;
SET serveroutput ON
SET feed ON
SET autop off
call DBMS_OUTPUT.put_line('start_time '||TO_CHAR(SYSDATE,'yyyy-mm-dd hh24:mi:ss'));
--updatename,CLCTDB_{clctgp_ver}.2.0_{exe_name}
--svn,99999

DECLARE
  --�������ڹ鼯����ִ�У�
  v_username    VARCHAR2(100);
  v_dbname 	VARCHAR2(100);
  e_app 	EXCEPTION;
BEGIN
  SELECT NAME INTO v_dbname FROM v$database;
  dbms_output.put_line('���ݿ⣺'||v_dbname);
  IF upper(v_dbname) LIKE 'CSL%' OR upper(SUBSTR(v_dbname,1,3)) IN ('AEG', 'XGP') THEN
    dbms_output.put_line('���ű������ڹ鼯���ݿ���ִ��');
    RAISE e_app;
  END IF;
  IF user <> 'AEG2' THEN
    dbms_output.put_line('���θ��±���ʹ��AEG2�û�ִ��');
    RAISE e_app;
  END IF;
END;
/

PROMPT ����ҵ�����-��ʼ

--fileadr,http://svnserver:8088/Repository/Aegean2/trunk/product/db/��Ƶ����ά������/wh_check_clctgp.pck


variable v_operator_type VARCHAR2(30);
exec :v_operator_type:='&1';

col sql_file_name noprint new_value sql_file_name;

SELECT decode(lower(:v_operator_type),
               'clctgp_update',
               'clctgp_update.sql',
               'clctgp_rollback',
               'clctgp_rollback.sql',
               NULL) AS sql_file_name
  FROM dual;
@&&sql_file_name

EXIT;
