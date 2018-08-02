PROMPT 具体业务代码-开始
variable v_db_version VARCHAR2(30)
exec  :v_db_version:= '{xgp_ver}.10.1.0';

PROMPT =================编译维护程序包===================

PROMPT 部署维护检查程序包wh_check
@@wh_check.pck

PROMPT 部署回退程序包wh_rbk
@@wh_rbk.pck

PROMPT ==================执行前置检查====================
PROMPT 前置检查该工单是否已经部署
call wh_check.check_order_ver(:v_db_version,1);

PROMPT 检查修改对象版本信息
--call wh_check.check_modify_obj('lconvert_readable_gp44y#pkg_stake_split#','4.1#15.0#');

PROMPT ==================执行工单回退操作====================


--回退版本信息
prompt 回退版本信息
DELETE FROM log_db_version l WHERE l.db_version =  :v_db_version;
COMMIT;

PROMPT ==================执行工单回退检查====================
PROMPT 检查修改对象回退信息
--call wh_check.check_modify_obj('lconvert_readable_gp44y#pkg_stake_split#','4.0#14.0#');


PROMPT 检查该工单版本信息
call wh_check.check_order_ver(:v_db_version,0);

PROMPT 具体业务代码-完成
call dbms_output.put_line('数据库' || :v_db_version || '版本回退操作更新执行成功!');