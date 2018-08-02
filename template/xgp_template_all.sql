WHENEVER sqlerror EXIT;
set serveroutput on size 1000000 format wrapped
set feed on
set autop off
set sqlblanklines on

call DBMS_OUTPUT.put_line('start_time '||TO_CHAR(SYSDATE,'yyyy-mm-dd hh24:mi:ss'));
--updatename,Aeg2DB_{xgp_ver}.10.1.0_{exe_name}
--svn,99999

--fileadr,http://svnserver:8088/Repository/Aegean2/trunk/product/db/高频常用维护程序/wh_check.pck
--fileadr,http://svnserver:8088/Repository/Aegean2/trunk/product/db/高频常用维护程序/wh_rbk.pck

variable v_operator_type VARCHAR2(30);
exec :v_operator_type:='&1';

col sql_file_name noprint new_value sql_file_name;

SELECT decode(lower(:v_operator_type),
               'special_update',
               'special_update.sql',
               'special_rollback',
               'special_rollback.sql',
               'normal_update',
               'normal_update.sql',
               'normal_rollback',
               'normal_rollback.sql',
               NULL) AS sql_file_name
  FROM dual;
@&&sql_file_name

exit;
