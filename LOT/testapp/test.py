import cx_Oracle

connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
cursor = connection.cursor()

sql = """
            SELECT BSN_CD,
                    PRA_CD,
                    CMP_CD,
                    WM_RUN_NO,
                    WM_DIE_NO,
                    WM_PART_NO,
                    ITEM_CD,
                    RUT_CD, 
                    LOT_NO,
                    WM_TRANS_CNT,
                    WM_CURR_qTY,
                    WM_STATUS,
                    WM_SITE_NO,
                    WM_LOT_TYPE,
                    WM_PLAN_WEEK,
                    WM_TEST_WEEK,
                    WM_CARR_NO,
                    WM_LABEL_YN,
                    WM_HOLD_YN,
                    MCN_CD,
                    WM_START_DT,
                    WM_ACT_DT,
                    CLOT_NO,
                    WM_SMARK,
                    WM_TEST_YN,
                    WM_ITEM_MCD,
                    WM_CHLGO_CMP,
                    WM_MAT_YN,
                    TO_CHAR(SYSDATE, 'YYYYMMDDHH24MISS') TRANS_DT,
                    FNS_SALECODE(ITEM_CD) SALE_CD,
                    FNP_GETITEMCD(ITEM_CD) ITEM_MCD,
                    FNP_GETITEMPAKGRP(ITEM_CD) GUBUN
            FROM TP_WM 
            WHERE WM_CURR_QTY > 0
            AND LOT_NO = '%s'
    """ % ('X0C18T3A2403P')
cursor.execute(sql)
rows = cursor.fetchone()   

print(rows[0])