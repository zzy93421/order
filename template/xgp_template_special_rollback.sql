PROMPT ����ҵ�����-��ʼ
variable v_db_version VARCHAR2(30)
exec  :v_db_version:= '{xgp_ver}.10.1.0';


PROMPT =================����ά�������===================

PROMPT ����ά���������wh_check
@@wh_check.pck

PROMPT ������˳����wh_rbk
@@wh_rbk.pck

PROMPT ==================ִ��ǰ�ü��====================
PROMPT ǰ�ü��ù����Ƿ��Ѿ�����
call wh_check.check_order_ver(:v_db_version,1);

PROMPT ����޸Ķ���汾��Ϣ
--call wh_check.check_modify_obj('p_count_win_4p4y_yu#lconvert_readable_gp44y#p_count_481_283#pkg_stake_split#','2.8#4.1#1.3#15.0#');

PROMPT ==================ִ�й������˲���====================

--���˰汾��Ϣ
prompt ���˰汾��Ϣ
DELETE FROM log_db_version l WHERE l.db_version =  :v_db_version;
COMMIT;

PROMPT ==================ִ�й������˼��====================

PROMPT ����޸Ķ��������Ϣ
--call wh_check.check_modify_obj('p_count_win_4p4y_yu#lconvert_readable_gp44y#p_count_481_283#pkg_stake_split#','2.7#4.0#1.2#14.0#');

PROMPT ���ù����汾��Ϣ
call wh_check.check_order_ver(:v_db_version,0);

PROMPT ����ҵ�����-���
call dbms_output.put_line('���ݿ�' || :v_db_version || '�汾���˲�������ִ�гɹ�!');