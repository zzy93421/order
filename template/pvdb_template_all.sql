WHENEVER sqlerror EXIT;
set serveroutput on size 1000000 format wrapped
set feed on
set autop off

call DBMS_OUTPUT.put_line('start_time '||TO_CHAR(SYSDATE,'yyyy-mm-dd hh24:mi:ss'));
--updatename,Aeg2DBCheck_{pvdb_ver}.3.0_{exe_name}
--svn,99999

--fileadr,http://svnserver:8088/Repository/Aegean2/trunk/product/db/高频常用维护程序/wh_check_pvdb.pck

variable v_operator_type VARCHAR2(30);
exec :v_operator_type:='&1';

col sql_file_name noprint new_value sql_file_name;

SELECT decode(lower(:v_operator_type),
               'pvdb_update',
               'pvdb_update.sql',
               'pvdb_rollback',
               'pvdb_rollback.sql',               
               NULL) AS sql_file_name
  FROM dual;
@&&sql_file_name

exit;
