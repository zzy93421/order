WHENEVER sqlerror EXIT;
SET serveroutput ON
SET feed ON
SET autop off
call DBMS_OUTPUT.put_line('start_time '||TO_CHAR(SYSDATE,'yyyy-mm-dd hh24:mi:ss'));
--updatename,CLCTDB_{clctgp_ver}.2.0_{exe_name}
--svn,99999

DECLARE
  --本工具在归集库上执行；
  v_username    VARCHAR2(100);
  v_dbname 	VARCHAR2(100);
  e_app 	EXCEPTION;
BEGIN
  SELECT NAME INTO v_dbname FROM v$database;
  dbms_output.put_line('数据库：'||v_dbname);
  IF upper(v_dbname) LIKE 'CSL%' OR upper(SUBSTR(v_dbname,1,3)) IN ('AEG', 'XGP') THEN
    dbms_output.put_line('本脚本必须在归集数据库上执行');
    RAISE e_app;
  END IF;
  IF user <> 'AEG2' THEN
    dbms_output.put_line('本次更新必须使用AEG2用户执行');
    RAISE e_app;
  END IF;
END;
/

PROMPT 具体业务代码-开始

--fileadr,http://svnserver:8088/Repository/Aegean2/trunk/product/db/高频常用维护程序/wh_check_clctgp.pck


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
