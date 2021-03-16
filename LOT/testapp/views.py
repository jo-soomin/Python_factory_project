from django.shortcuts import render
from django.http import HttpResponse
import simplejson as json
import cx_Oracle
import base64
from io import BytesIO
from PIL import Image
from tkinter import *
from tkinter import messagebox

# Create your views here.
item_cd = ''
cnt = 0


def index(request):
    return render(request, 'index.html')


def mv_in_1(request):
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()
    sql = """
                   select cmp_cd, cmp_nm from tf_company where cmp_sec = 'FK02'
             """
    cursor.execute(sql)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        dic = {'CMP_CD': row[0], 'CMP_NM': row[1]}
        data.append(dic)

    return render(request, 'mv_in_1.html', {'data': data})


def test2(request):
    name = request.GET['LOT_NO']
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()
    sql = """
          SELECT FNP_GETCMPNM(CMP_CD) CMP_NM, 
         FNP_GETPACKAGE(ITEM_CD) PKG, 
         FNS_SALECODE(ITEM_CD) SALE_CD, 
         FNP_GETCUSTLOTNO(LOT_NO) RUN_NO,
         WM_CURR_QTY CURR_QTY,
         ITEM_CD
         FROM TP_WM WHERE LOT_NO = '%s'
         AND WM_CURR_QTY = 0
    """ % (name)
    cursor.execute(sql)
    rows = cursor.fetchall()

    name = rows[0]
    global item_cd
    item_cd = rows[0][5]
    return HttpResponse(json.dumps(name), content_type="application/json")


def working(request):
    # SELECT 예시-------------------------------------------------------------------------
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()
    sql = """
              SELECT ITEM_BDSPECPATH FROM TD_ITEMMAS WHERE ITEM_cD = 'PIGK3A9A010'
        """
    cursor.execute(sql)
    rows = cursor.fetchall()
    img_url = rows[0]
    ls_lot_no = request.POST['LOT_NO']
    CMP_NM = request.POST['CMP_NM']
    PKG = request.POST['PKG']
    SALE_CD = request.POST['SALE_CD']
    RUN_NO = request.POST['RUN_NO']
    CURR_QTY = request.POST['CURR_QTY']

    # INSERT 예시------------------------------------------------------------------------------
    # connection2 = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    # cursor2 = connection2.cursor()
    # sql = """
    #               INSERT INTO TP_SUMIN_TEST VALUES('%s','%s','%s','%s','%s','%s')
    #         """%(LOT_NO,CMP_NM,PKG,SALE_CD,RUN_NO,CURR_QTY)
    # cursor2.execute(sql)
    # cursor2.close()
    # connection2.commit()
    # connection2.close()

    return render(request, 'working.html')


def mv_in_2(request):
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()
    sql = """
            SELECT  'LEAD FRAME' GUBUN,
            FNP_GETCMPNM(B.CMP_CD) CMP_NM,
            B.MAT_DESC,
            A.MAT_CD,        
            ITEM_USAGE 
            FROM TD_ITEMMAS_LF A, TM_MATMAS B 
            WHERE ITEM_cD = 'PDIR2M0A510'
            AND A.MAT_CD = B.MAT_CD
            UNION ALL
            SELECT  'WIRE' GUBUN,
            FNP_GETCMPNM(B.CMP_CD) CMP_NM, 
            B.MAT_DESC,
            A.MAT_CD, 
            ITEM_USAGE 
            FROM TD_ITEMMAS_WIRE A, TM_MATMAS B 
            WHERE ITEM_cD = 'PDIR2M0A510'
            AND A.MAT_CD = B.MAT_CD
            UNION ALL
            SELECT  'EMC' GUBUN,
            FNP_GETCMPNM(B.CMP_CD) CMP_NM,
            B.MAT_DESC, 
            A.MAT_CD, 
            ITEM_USAGE 
            FROM TD_ITEMMAS_EMC A, TM_MATMAS B 
            WHERE ITEM_cD = 'PPOQ3A5A290'
            AND A.MAT_CD = B.MAT_CD
            """
    cursor.execute(sql)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        dic = {'GUBUN': row[0], 'CMP_NM': row[1], 'MAT_DESC': row[2], 'MAT_CD': row[3], 'ITEM_USAGE': row[4]}
        data.append(dic)

    return render(request, 'movein_2.html', {'data': data})


def mv_in_3(request):
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()
    sql = """
            SELECT LT_CD, LT_AL_NM FROM TQ_LOSSTYPE
            """
    cursor.execute(sql)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        dic = {'LT_CD': row[0], 'LT_AL_NM': row[1]}
        data.append(dic)

    return render(request, 'mv_in_3.html', {'data': data})


def confirm(request):
    in_qty = '1200'

    return render(request, 'workingRes.html',
                  {'in_qty': int(in_qty), 'cnt': int(cnt), 'out_qty': int(in_qty) - int(cnt)})


def total_cnt(request):
    total_cnt = request.GET['cnt']
    global cnt
    cnt = total_cnt

    return HttpResponse(json.dumps(total_cnt), content_type="application/json")


def insertTest(request):
    if (request.method == 'POST'):
        img = request.FILES['imgs']

    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()

    imgdata = img.read()  #
    # image = Image.open('C:\\Users\\user\\Desktop\\Web용 이미지\\images.jpg')
    # buffer = BytesIO()
    # image.convert("RGB")
    # image.save(buffer, format='jpeg',quality=85)
    # image_str = base64.b64encode(buffer.getvalue())
    # print(image_str)
    # # im = base64.decodestring(image_str)
    # # im = Image.open(BytesIO(im))
    # # im.show()
    cursor.execute("""
            insert into AAA(COL1,IMAGE)
            values (:COL1,:blobdata)""",
                   COL1='2020-12-10', blobdata=imgdata)
    cursor.close()
    connection.commit()

    return render(request, 'insertTest.html')


from sqlalchemy import create_engine
from PIL import Image
import base64
from io import BytesIO


def insertRes(request):
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()
    cursor.execute("""
                select IMAGE from aaa where COL1 = '2020-12-10'
                """)
    rows = cursor.fetchall()

    f = open('C:\\Users\\user\\Desktop\\Web용 이미지\\' + 'test이미지.jpg', "wb")
    f.write(rows[0][0].read())
    f.close()

    cursor.close()
    connection.commit()

    return render(request, 'mv_in_1.html')


def dropdownList(request):
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()
    sql = """
                select cmp_cd, cmp_nm from tf_company where cmp_sec = 'FK02'
          """
    cursor.execute(sql)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        dic = {'CMP_CD': row[0], 'CMP_NM': row[1]}
        data.append(dic)

    return render(request, 'dropdownList.html', {'data': data})


def slideList(request):
    return render(request, 'slideList.html')


def QRcode(request):
    return render(request, 'QRcode.html')


def test(request):
    return render(request, 'test.html')


def ajax_test1(request):
    ls_lot_no = request.GET['LOT_NO']
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
                       WM_MAT_YN
                  FROM TP_WM 
                 WHERE WM_CURR_QTY > 0 
                   AND LOT_NO = '%s' 
              """ % (ls_lot_no)
    cursor.execute(sql)
    rows = cursor.fetchone()
    return HttpResponse(json.dumps(rows), content_type="application/json")


def ajax_test2(request):
    ls_item_cd = request.GET['ls_item_cd']
    # print(ls_item_cd)
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()

    sql = """
            Select ITEM_WF_RT, ITEM_TYPE from TD_ITEMMAS where ITEM_CD = '%s' 
        """ % (ls_item_cd)
    cursor.execute(sql)
    rows = cursor.fetchone()

    return HttpResponse(json.dumps(rows), content_type="application/json")


def movein_1(request):
    return render(request, 'movein_1.html')


def lot_select(request):
    global ls_lot_no, ls_test_week, ls_test_week2, ls_lot_cnt, ls_pra_cd, ls_curr_qty, ls_item_mcd
    global ls_cmp_cd, ls_lot_type, ls_item_cd, ls_run_no, ls_site_no, ls_pakgrp

    ls_lot_no = request.GET['LOT_NO']
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
                       FNP_GETITEMPAKGRP(ITEM_CD) GUBUN,
                       NVL(WM_TEST_WEEK2, '*') WM_TEST_WEEK2
               FROM TP_WM 
              WHERE WM_CURR_QTY > 0
                AND LOT_NO = '%s'
        """ % (ls_lot_no)
    cursor.execute(sql)
    rows = cursor.fetchone()

    ls_cmp_cd = rows[2]
    ls_lot_type = rows[13]
    ls_item_cd = rows[6]
    ls_run_no = rows[3]
    ls_pra_cd = rows[1]
    ls_site_no = rows[12]
    ls_lot_cnt = int(rows[9]) + 1
    ls_curr_qty = rows[10]
    ls_test_week = rows[15]
    ls_item_mcd = rows[25]
    ls_pakgrp = rows[31]
    ls_test_week2 = rows[32]
    # print('1.' + ls_pra_cd)
    # print(ls_lot_cnt)

    return HttpResponse(json.dumps(rows), content_type="application/json")


def lot_select_2(request):
    ls_emp_no = request.GET['EMP_NO']
    ls_lot_no = request.GET['LOT_NO']
    loss_total_cnt = request.GET['total_cnt']

    if (loss_total_cnt is None or loss_total_cnt == ''):
        loss_total_cnt = 0

    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    ccd_cursor = connection.cursor()

    # 사번별 근무조 조회 쿼리
    sql = """
             SELECT X.EMP_NMK, Y.CCD_TOP 
             FROM TA_EMP_MAS X, TT_COMCD Y 
             WHERE X.EMP_NO = '%s' 
             AND X.EMP_PART = Y.CCD_CD
            """ % (ls_emp_no)
    ccd_cursor.execute(sql)
    rows = ccd_cursor.fetchone()
    ccd_cursor.close()
    WKG_CD = rows[1]

    # TP_WM select
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
                       FNP_GETITEMPAKGRP(ITEM_CD) GUBUN,
                       WM_TEST_WEEK2,
                       NVL(WM_MARK_YN, 'N'),
                       WM_CUST_LOT_TYPE,
                       WM_PID_YN,
                       NVL(WM_TEST_WEEK2, '*'),
                       WM_WIRE_YN,
                       fnp_getnextpracd(RUT_CD, PRA_CD) NEXT_PRA_CD                       
               FROM TP_WM 
              WHERE WM_CURR_QTY > 0
                AND LOT_NO = '%s'
        """ % (ls_lot_no)
    cursor.execute(sql)
    rows = cursor.fetchone()
    cursor.close()

    # TV_WT insert
    cursor2 = connection.cursor()
    sql = """
                 INSERT INTO TP_WT
    (BSN_CD,                  LOT_NO,                   PRA_CD,               WT_TRANS_CNT,        PRE_PRA_CD,
    WT_PRE_QTY,              WT_CURR_QTY,              WKG_CD,               WT_ACT_DT,          WT_EMP_NO,          WT_STATUS,         WT_SITE_NO ,
    CMP_CD,                 WT_LOT_TYPE,             ITEM_CD,             WT_RUN_NO,             WT_MAT_CHANGE,     WT_MAT_MCNCD,     WT_MOVE_CNT)
    VALUES
    ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','PFMO','%s','%s','%s','%s','%s','%s','%s','%s')
           """ % (
    rows[0], ls_lot_no, rows[38], rows[9] + 1, rows[1], int(rows[10]), int(rows[10] - int(loss_total_cnt)), WKG_CD,
    rows[21], ls_emp_no, rows[12], rows[2], rows[13], rows[6], rows[3], '*', rows[19], '*')
    cursor2.execute(sql)
    cursor2.close()
    # TV_MV insert
    cursor3 = connection.cursor()
    sql = """
            INSERT INTO TP_MV
    	( BSN_CD,           LOT_NO,               PRA_CD,             MV_TRANS_CNT,       ITEM_CD,   
    	  MV_IN_QTY,        MV_OUT_QTY,           MCN_CD,             MV_START_DT,        MV_END_DT,
    	  MV_SWKG_CD,       MV_EWKG_CD,           MV_SEMP_NO,         MV_EEMP_NO,         MV_WORK_QTY,
    	  CMP_CD,           MV_LOT_TYPE,          NEXT_PRA_CD,        MV_SITE,            MV_CARR_NO, 
    	  MV_STRIP_QTY,     MV_MAT_CHANGE,        MV_MAT_YN,          MCN_CD2,            MV_MOLD_PS,       MV_MOLD_TURN,         MV_IR_YIELD_CHK)
    VALUES
    	('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')

        """ % (
    rows[0], ls_lot_no, rows[38], rows[9] + 1, rows[6], int(rows[10]), int(rows[10] - int(loss_total_cnt)), rows[19],
    rows[20], rows[28], 'GY', 'DY', ls_emp_no, ls_emp_no, int(rows[10] - int(loss_total_cnt)), rows[2], rows[13],
    rows[38],
    rows[12], rows[16], '1', '*', rows[27], '*', '*', '*', '*')
    cursor3.execute(sql)
    cursor3.close()

    # TV_LS insert
    LOSS_CNT_arr = request.GET.getlist('LOSS_CNT_arr')
    LOSS_CD_arr = request.GET.getlist('LOSS_CD_arr')

    for i in range(0, len(LOSS_CD_arr)):
        cursor4 = connection.cursor()
        sql = """
                    INSERT INTO TP_LS
                ( BSN_CD,       LOT_NO,      PRA_CD,     LS_TRANS_CNT,       LS_CD,
                  ITEM_CD,      MCN_CD,      LS_QTY,     LS_ACT_DT,          LS_EMP_NO,
                  WKG_CD,       CMP_CD,      LS_LOT_TYPE)
            VALUES
                ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')

                """ % (
        rows[0], ls_lot_no, rows[38], rows[9] + 1, LOSS_CD_arr[i], rows[6], rows[19], LOSS_CNT_arr[i], rows[21],
        ls_emp_no, WKG_CD, rows[2], rows[13])
        cursor4.execute(sql)
        cursor4.close()

    # TP_WM update
    cursor5 = connection.cursor()
    sql = """
                UPDATE TP_WM
                SET WM_STATUS     = 'PFMO',
                    PRA_CD        = '%s',
                    WM_CURR_QTY   = '%s',
                    WM_LS_QTY     = '%s',
                    WM_TRANS_CNT  = '%s',
                    WM_CARR_NO    = '%s',
                    WM_ACT_DT     = '%s'
                WHERE BSN_CD      = '%s'
                AND  LOT_NO       = '%s'
                AND  WM_TRANS_CNT = (SELECT MAX(WM_TRANS_CNT) FROM TP_WM WHERE LOT_NO = '%s')
        """ % (
    rows[38], rows[10] - int(loss_total_cnt), loss_total_cnt, rows[9] + 1, '*', rows[21], rows[0], rows[8], rows[8])
    cursor5.execute(sql)
    cursor5.close()

    # TP_RSRCCONST update
    cursor6 = connection.cursor()
    sql = """
                UPDATE TP_RSRCCONST
                SET MCN_USESEC = DECODE(MCN_CD, 'CMALL', 'X', 'N')
                WHERE ( MCN_CD = '%s' ) AND ( MCN_USESEC = 'Y' )
        """ % (rows[19])
    cursor6.execute(sql)
    cursor6.close()

    connection.commit()
    connection.close()

    return render(request, 'moveout.html')


def movein_2(request):
    EMP_NO = request.POST['EMP_NO']
    ls_lot_no = request.POST['LOT_NO']
    ITEM_CD = request.POST['ITEM_CD']
    PRA_CD = request.POST['PRA_CD']
    LOT_CNT = request.POST['LOT_CNT']

    # print(item_cd)
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()
    sql = """
                SELECT  'LEAD FRAME' GUBUN,
                FNP_GETCMPNM(B.CMP_CD) CMP_NM,
                B.MAT_DESC,
                A.MAT_CD,        
                ITEM_USAGE 
                FROM TD_ITEMMAS_LF A, TM_MATMAS B 
                WHERE ITEM_cD = '%s'
                AND A.MAT_CD = B.MAT_CD
                UNION ALL
                SELECT  'WIRE' GUBUN,
                FNP_GETCMPNM(B.CMP_CD) CMP_NM, 
                B.MAT_DESC,
                A.MAT_CD, 
                ITEM_USAGE 
                FROM TD_ITEMMAS_WIRE A, TM_MATMAS B 
                WHERE ITEM_cD = '%s'
                AND A.MAT_CD = B.MAT_CD
                UNION ALL
                SELECT  'EMC' GUBUN,
                FNP_GETCMPNM(B.CMP_CD) CMP_NM,
                B.MAT_DESC, 
                A.MAT_CD, 
                ITEM_USAGE 
                FROM TD_ITEMMAS_EMC A, TM_MATMAS B 
                WHERE ITEM_cD = '%s'
                AND A.MAT_CD = B.MAT_CD
                """ % (ITEM_CD, ITEM_CD, ITEM_CD)

    cursor.execute(sql)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        dic = {'GUBUN': row[0], 'CMP_NM': row[1], 'MAT_DESC': row[2], 'MAT_CD': row[3], 'ITEM_USAGE': row[4]}
        data.append(dic)
    # print(data)

    return render(request, 'movein_2.html',
                  {'data': data, 'EMP_NO': EMP_NO, 'LOT_NO': ls_lot_no, 'PRA_CD': PRA_CD, 'LOT_CNT': LOT_CNT,
                   'ITEM_CD': ITEM_CD})


def moveout(request):
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()
    sql = """
                SELECT LT_CD, LT_AL_NM FROM TQ_LOSSTYPE
                """
    cursor.execute(sql)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        dic = {'LT_CD': row[0], 'LT_AL_NM': row[1]}
        data.append(dic)
    return render(request, 'moveout.html', {'data': data})


def movein_3(request):
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()
    sql = """
                SELECT LT_CD, LT_AL_NM FROM TQ_LOSSTYPE
                """
    cursor.execute(sql)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        dic = {'LT_CD': row[0], 'LT_AL_NM': row[1]}
        data.append(dic)

    return render(request, 'movein_3.html', {'data': data})


def P_TM(request):
    # return render(request, 'P_TM.html')
    EMP_NO = request.POST['EMP_NO']
    ls_lot_no = request.POST['LOT_NO']
    ITEM_CD = request.POST['ITEM_CD']
    PRA_CD = request.POST['PRA_CD']
    LOT_CNT = request.POST['LOT_CNT']
    MCN_NO = request.POST['MCN_NO']
    # print(EMP_NO)
    # print(MCN_NO)
    return render(request, 'P_TM.html',
                  {'EMP_NO': EMP_NO, 'LOT_NO': ls_lot_no, 'PRA_CD': PRA_CD, 'LOT_CNT': LOT_CNT, 'ITEM_CD': ITEM_CD,
                   'MCN_NO': MCN_NO})


def P_SAW(request):
    EMP_NO = request.POST['EMP_NO']
    ls_lot_no = request.POST['LOT_NO']
    ITEM_CD = request.POST['ITEM_CD']
    PRA_CD = request.POST['PRA_CD']
    LOT_CNT = request.POST['LOT_CNT']
    MCN_NO = request.POST['MCN_NO']

    # print(MCN_NO)
    return render(request, 'P_SAW.html',
                  {'EMP_NO': EMP_NO, 'LOT_NO': ls_lot_no, 'PRA_CD': PRA_CD, 'LOT_CNT': LOT_CNT, 'ITEM_CD': ITEM_CD,
                   'MCN_NO': MCN_NO})
    # return render(request, 'P_SAW.html')


def lot_result(request):
    ls_lot_no = request.GET['LOT_NO']

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
                       TO_CHAR(SYSDATE, 'YYYYMMDDHH24MISS') TRANS_DT
                  FROM TP_WM 
                 WHERE WM_CURR_QTY > 0 
                   AND LOT_NO = '%s' 
              """ % (ls_lot_no)
    cursor.execute(sql)
    rows = cursor.fetchone()

    cursor.close()
    connection.close()

    return HttpResponse(json.dumps(rows), content_type="application/json")


def er_return_chk(request):
    ls_item_cd = request.GET['ls_item_cd']

    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()

    sql = """
            Select ITEM_WF_RT, 
                   ITEM_TYPE,
                   TO_CHAR(SYSDATE, 'YYYYMMDDHH24MISS')
              from TD_ITEMMAS 
             where ITEM_CD = '%s' 
        """ % (ls_item_cd)

    cursor.execute(sql)
    rows = cursor.fetchone()

    return HttpResponse(json.dumps(rows), content_type="application/json")


def er_return_update(request):
    ls_lot_no = request.GET['lot_no']

    if request.GET['return_yn'] == 'true':
        ls_return_yn = 'Y'
        ls_date = request.GET['date']
        ls_emp_no = request.GET['emp_no']
    else:
        ls_return_yn = 'N'
        ls_date = ''
        ls_emp_no = ''

    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()

    sql = """
        	UPDATE TP_WAFERRT
		       SET CHK_1 = '%s',
				   EMP_NO_1 = '%s',
				   DATE_1 = '%s'
		     WHERE RUN_NO = '%s'
        """ % (ls_return_yn, ls_emp_no, ls_date, ls_lot_no)

    try:
        cursor.execute(sql)
    except cx_Oracle.IntegrityError as e:
        errorObj, = e.args
        print("Error Code:", errorObj.code)
        print("Error Message:", errorObj.message)
    else:
        print("TP_WAFERRT UPDATE ok")

    cursor.close()
    connection.commit()
    connection.close()

    return HttpResponse()


def emp_chk(request):
    global ls_wkg_cd_org, ls_emp_no
    ls_emp_no = request.GET['emp_no']

    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()

    sql = """
            SELECT X.EMP_NMK, Y.CCD_TOP FROM TA_EMP_MAS X, TT_COMCD Y WHERE X.EMP_NO = '%s' AND X.EMP_PART = Y.CCD_CD
        """ % (ls_emp_no)
    cursor.execute(sql)
    rows = cursor.fetchone()

    ls_wkg_cd_org = rows[1]
    # print('--------------------------')
    # print(ls_wkg_cd_org)
    # print('--------------------------')

    return HttpResponse(json.dumps(rows), content_type="application/json")


def mat_insert(request):
    ls_lot_no = request.GET['lot_no']
    ls_emp_no = request.GET['emp_no']
    ls_mat_cd = request.GET['mat_cd']
    ls_item_cd = request.GET['item_cd']
    ls_mat_lot_no = request.GET['mat_lot_no']
    ls_pra_cd = request.GET['pra_cd']
    ls_lot_cnt = request.GET['lot_cnt']

    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()

    sql = """
            INSERT INTO TP_PROD_MAT                    
                    (BSN_CD,    PRA_CD,     LOT_NO,     ITEM_CD,    MTD_TRANS_CNT,      MAT_CD,     MAT_LOT_NO,     MTD_EMP_NO, MTD_ACT_DT)
            VALUES  ('S1',      '%s',       '%s',       '%s',       '%s',               '%s',       '%s',           '%s',   TO_CHAR(SYSDATE, 'YYYYMMDDHH24MISS'))
        """ % (ls_pra_cd, ls_lot_no, ls_item_cd, int(ls_lot_cnt), ls_mat_cd, ls_mat_lot_no, ls_emp_no)

    cursor.execute(sql)
    cursor.close()
    connection.commit()
    connection.close()

    return HttpResponse()


def lot_start_insert(request):
    ls_lot_no = request.GET['lot_no']
    ls_emp_no = request.GET['emp_no']
    ls_mcn_cd = request.GET['mcn_no']
    # ls_wkg_cd = 'ZZ'

    data = []

    # print('---------------------------')
    # print(ls_lot_cnt)
    # print(ls_test_week)
    # print(ls_test_week2)
    # print(ls_lot_no)
    # print(ls_lot_no)
    # print(ls_wkg_cd_org)
    # print('---------------------------')

    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()

    sql = """
            UPDATE TP_WM
                SET WM_STATUS     = 'PFMI',
                    WM_TRANS_CNT  = '%s',
                    WM_TEST_WEEK  = '%s',	  
                    WM_TEST_WEEK2  = '%s',
                    MCN_CD        = '%s',
                    WM_ACT_DT     = TO_CHAR(SYSDATE, 'YYYYMMDDHH24MISS')                    
                WHERE BSN_CD      = 'S1'
                AND LOT_NO        = '%s'
                AND WM_TRANS_CNT = (SELECT MAX(WM_TRANS_CNT) FROM TP_WM WHERE LOT_NO = '%s')
        """ % (ls_lot_cnt, ls_test_week, ls_test_week2, ls_mcn_cd, ls_lot_no, ls_lot_no)

    try:
        cursor.execute(sql)
        print('1.ok')
    except cx_Oracle.IntegrityError as e:
        connection.rollback()
        errorObj, = e.args
        dic = {'error_code': errorObj.code, 'error_message': errorObj.message}
        data.append(dic)
        print('exp')
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        print('1.else')

    cursor.close()

    cursor = connection.cursor()
    sql = """
            INSERT INTO TP_WT
                    (BSN_CD,            LOT_NO,             PRA_CD,             WT_TRANS_CNT,   PRE_PRA_CD,
                    WT_PRE_QTY,         WT_CURR_QTY,        WKG_CD,             WT_ACT_DT,  
                    WT_EMP_NO,          WT_STATUS,          WT_SITE_NO ,
                    CMP_CD,             WT_LOT_TYPE,        ITEM_CD,            WT_RUN_NO, 
                    WT_MAT_CHANGE,      WT_MAT_MCNCD,       WT_MOVE_CNT) 
                VALUES 
                    ('S1',              '%s',               '%s',               '%s',           '%s',
                    '%s',               '%s',               '%s',               TO_CHAR(SYSDATE, 'YYYYMMDDHH24MISS'),   
                    '%s',               'PFMI',             '%s',
                    '%s',               '%s',               '%s',               '%s',
                    '',                 '',                 '')
            """ % (ls_lot_no, ls_pra_cd, ls_lot_cnt, ls_pra_cd,
                   int(ls_curr_qty), int(ls_curr_qty), ls_wkg_cd_org,
                   ls_emp_no, ls_site_no,
                   ls_cmp_cd, ls_lot_type, ls_item_cd, ls_run_no)

    try:
        cursor.execute(sql)
        print('2.ok')
    except cx_Oracle.IntegrityError as e:
        connection.rollback()
        print('2.exp')
        errorObj, = e.args
        dic = {'error_code': errorObj.code, 'error_message': errorObj.message}
        data.append(dic)

        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        print('2.else')

    cursor.close()
    connection.commit()

    connection.close()

    return HttpResponse()


def MCN_LIST(request):
    ls_pra_cd = request.GET['pra_cd']
    # print(ls_pra_cd)
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()

    sql = """
            SELECT DISTINCT MCN_CD
		  FROM TP_RSRCCONST
		  WHERE BSN_CD = 'S1'
		  AND   PRA_CD IN ( '%s' )
		  AND   MCN_USESEC IN ( 'N', 'X' )
        """ % (ls_pra_cd)

    cursor.execute(sql)
    rows = cursor.fetchall()
    # print(rows)
    return HttpResponse(json.dumps(rows), content_type="application/json")


# ccs---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def ccs(request):
    return render(request, 'ccs.html')


def ccsInformation(request):
    ccs_lot_no = request.GET['lot_no']
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()

    sql = """
              SELECT FNS_SALECODE(ITEM_CD), 
                     LOT_NO,
                     PRA_CD
               FROM TP_WM 
              WHERE LOT_NO = '%s'
        """ % (ccs_lot_no)
    cursor.execute(sql)
    rows = cursor.fetchone()

    return HttpResponse(json.dumps(rows), content_type="application/json")

def ccsContent(request):
    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()
    cursor.execute("""
                        SELECT  SHEET_NM,
                                SHEET_HINT
                        FROM TE_CCS_SHEET
                        WHERE PRA_CD = 'A010'
                        AND CCS_GB = 'EC01'
                        AND SHEET_CD = 'EK03'
                    """)
    rows = cursor.fetchall()
    cursor.close()
    data = []
    for row in rows:
        dic = {'SHEET_NM': row[0], 'SHEET_HINT': row[1]}
        data.append(dic)

    connection.commit()
    return HttpResponse(json.dumps(data), content_type="application/json")

# def ccsNewNO(request):
#     connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
#     cursor = connection.cursor()

#     sql = """
#              SELECT TE_CCS_NEW.NEXTVAL
#              FROM DUAL
#           """
#     cursor.execute(sql)
#     rows = cursor.fetchone()

#     return HttpResponse(json.dumps(rows), content_type="application/json")

# def ccsglobalno(request):
#     global gs_new_ccs_no
#     gs_new_ccs_no = request.GET['ccs_no']

#     return HttpResponse(json.dumps(data), content_type="application/json")


def ccs_mas_Insert(request):
    ls_emp_no = request.GET['emp_no']
    ls_lot_no = request.GET['lot_no']
    ls_mcn_cd = request.GET['mcn_cd']
    ls_sale_cd = request.GET['sale_cd']
    ls_sysdt = request.GET['sysdt']
    ls_pra_cd = request.GET['pra_cd']
    ls_request_cd = request.GET['request_cd']

    chk_yn = 'Y'

    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')

    cursor = connection.cursor()

    sql = """
             SELECT TE_CCS_NEW.NEXTVAL , TO_CHAR(SYSDATE, 'YYYYMMDD')
             FROM DUAL
          """
    cursor.execute(sql)
    rows = cursor.fetchone()

    global gs_new_ccs_no
    ls_ccs_str = str(rows[0])
    ls_ccs_seq = ls_ccs_str.zfill(4)
    ls_ccs_date = str(rows[1])
    gs_new_ccs_no = "C" + ls_ccs_date + ls_ccs_seq
 
    cursor.close()

    cursor = connection.cursor()

    cursor.execute("""
                        SELECT FNP_GETITEMMCD(ITEM_CD) FROM TP_WM WHERE LOT_NO = '%s'
                        """ % (ls_lot_no)
                   )
    rows = cursor.fetchall()
    cursor.close()

    # connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()

    sql = """
        	INSERT INTO TE_CCS_MAS (CCS_NO, PRA_CD, MCN_CD, LOT_NO, REQUEST_CD, REQUEST_STDT, TRANS_DT, CCS_GB, SHEET_CD, CCS_DEVICE, REQUEST_EMP, CCS_GUBUN)
            VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', 'EC01', 'EK01', '%s', '%s', '1')
          """ % (
    gs_new_ccs_no, ls_pra_cd, ls_mcn_cd, ls_lot_no, ls_request_cd, ls_sysdt, ls_sysdt, ls_sale_cd, ls_emp_no)

    errod_code = ''
    errod_message = ''
    data = []
    try:
        cursor.execute(sql)
    except cx_Oracle.IntegrityError as e:
        errorObj, = e.args
        dic = {'error_code': errorObj.code, 'error_message': errorObj.message}
        data.append(dic)

        chk_yn = 'N'

        print("Error Code:", errorObj.code)
        print("Error Message:", errorObj.message)
    else:
        print("에러없음")

    cursor.close()
    # connection.commit()
    # connection.close()

    # connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()

    cursor.execute("""
                        SELECT  PRA_CD,
                                CCS_GB,
                                SHEET_CD,
                                SHEET_NO,
                                SHEET_NM,
                                SHEET_HINT,
                                SHEET_TYPE,
                                SHEET_CNT,
                                SHEET_PRINTNO,
                                USE_YN,
                                INPUT_EMP,
                                TRANS_DT 
                        FROM TE_CCS_SHEET
                        WHERE PRA_CD = 'A010'
                        AND CCS_GB = 'EC01'
                        AND SHEET_CD = 'EK03'
                        ORDER BY SHEET_NO
                        """)
    rows = cursor.fetchall()
    cursor.close()

    ccs_cnt = int(len(rows))

    for i in range(0, ccs_cnt):
        cursor = connection.cursor()
        sql = """
                 INSERT INTO TE_CCS_DTL (CCS_NO, PRA_CD, MCN_CD, CCS_GB, SHEET_CD, SHEET_NO, SHEET_NM, SHEET_HINT, SHEET_PRINTNO, TRANS_DT)
                 VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
                 """ % (
            gs_new_ccs_no, ls_pra_cd, ls_mcn_cd, rows[i][1], rows[i][2], rows[i][3], rows[i][4], rows[i][5], rows[i][8],
            ls_sysdt)

        try:
            cursor.execute(sql)
        except cx_Oracle.IntegrityError as e:
            errorObj, = e.args
            dic = {'error_code': errorObj.code, 'error_message': errorObj.message}
            data.append(dic)

            chk_yn = 'N'

            print("Error Code:", errorObj.code)
            print("Error Message:", errorObj.message)
        else:
            print("에러없음")

        cursor.close()

    if (chk_yn == 'Y'):
        connection.commit()

    connection.close()

    return HttpResponse()


def ccs_dtl_Insert(request):
    ls_mcn_cd = request.GET['mcn_cd']
    ls_sysdt = request.GET['sysdt']
    ls_pra_cd = request.GET['pra_cd']

    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()

    cursor.execute("""
                        SELECT  PRA_CD,
                                CCS_GB,
                                SHEET_CD,
                                SHEET_NO,
                                SHEET_NM,
                                SHEET_HINT,
                                SHEET_TYPE,
                                SHEET_CNT,
                                SHEET_PRINTNO,
                                USE_YN,
                                INPUT_EMP,
                                TRANS_DT 
                        FROM TE_CCS_SHEET
                        WHERE PRA_CD = 'A010'
                        AND CCS_GB = 'EC01'
                        AND SHEET_CD = 'EK03'
                        ORDER BY SHEET_NO
                        """)
    rows = cursor.fetchall()
    cursor.close()

    ccs_cnt = int(len(rows))

    for i in range(0, ccs_cnt):
        cursor = connection.cursor()
        sql = """
                 INSERT INTO TE_CCS_DTL (CCS_NO, PRA_CD, MCN_CD, CCS_GB, SHEET_CD, SHEET_NO, SHEET_NM, SHEET_HINT, SHEET_PRINTNO, TRANS_DT)
                 VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
                 """ % (
            gs_new_ccs_no, ls_pra_cd, ls_mcn_cd, rows[i][1], rows[i][2], rows[i][3], rows[i][4], rows[i][5], rows[i][8],
            ls_sysdt)
        cursor.execute(sql)
        cursor.close()

    connection.commit()

    # 데이터 넘기기 위한 구문
    # data = []
    # for row in rows:
    #     dic = {'PRA_CD': row[0], 'CCS_GB': row[1], 'SHEET_CD': row[2], 'SHEET_NO': row[3], 'SHEET_NM':row[4]}
    #     data.append(dic)

    connection.close()

    return HttpResponse()


def ccs_value_arr(request):
    arr = request.GET.getlist('arr')

    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')

    k = 0
    for i in range(0, 15):
        cnt = str(i + 1).zfill(3)

        cursor = connection.cursor()
        sql = """
                UPDATE TE_CCS_DTL SET CCS_DATA1 = '%s',
                                    CCS_DATA2 = '%s',
                                    CCS_DATA3 = '%s',
                                    CCS_DATA4 = '%s',
                                    CCS_DATA5 = '%s'                                  
                WHERE CCS_NO = '%s'      
                AND SHEET_NO = '%s'         
                """ % (arr[k], arr[k + 1], arr[k + 2], arr[k + 3], arr[k + 4], gs_new_ccs_no, cnt)
        cursor.execute(sql)
        cursor.close()

        k = k + 5

    connection.commit()

    connection.close()

    return HttpResponse()


def move_out_check(request):
    ls_lot_no = request.GET['LOT_NO']

    connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
    cursor = connection.cursor()

    sql = """
          select nvl(sm_mark,' ') from tp_sm where lot_no = '%s'
    """ % (ls_lot_no)

    cursor.execute(sql)
    rows = cursor.fetchone()
    cursor.close()

    ls_sm_mark = rows[0]

    # print(ls_item_cd)

    if ls_pra_cd == 'A005':
        # IXYS(미국)
        if ls_cmp_cd == '002009':
            # IXYS 주코드 길이 Check
            if len(ls_sm_mark) == 6 or len(ls_sm_mark) == 8:
                print('ok')
            else:
                return HttpResponse(json.dumps({'error_message': "IXYS 주코드가 미등록 되었습니다! 전산팀에 문의 바랍니다."}),
                                    content_type="application/json")

        # IXYS(독일)
        elif ls_cmp_cd == '002011':
            # IXYS 주코드 길이 Check
            if len(ls_sm_mark) == 6 or len(ls_sm_mark) == 8:
                print('ok')
            else:
                return HttpResponse(json.dumps({'error_message': "IXYS 주코드가 미등록 되었습니다! 전산팀에 문의 바랍니다."}),
                                    content_type="application/json")

            # IXYS RO Check
            cursor2 = connection.cursor()
            sql = """
                    SELECT COUNT(Z.ORD_REL_NO) 
				      FROM TP_WM X,TS_ORDERD Z
				     WHERE X.LOT_NO   = '%s'
				       AND	X.WM_RUN_NO = Z.ORD_CUST_LOT_NO
                  """ % (ls_lot_no)
            cursor2.execute(sql)
            rows = cursor2.fetchone()
            cursor2.close()

            li_ro_cnt = rows[0]

            if li_ro_cnt != 1:
                return HttpResponse(json.dumps({'error_message': "IXYS Rel No가 미등록/중복이 되었습니다! 영업팀에 문의 바랍니다."}),
                                    content_type="application/json")

            if ls_item_cd != '*':
                cursor = connection.cursor()

                sql = """                    
                    SELECT FNP_GETRCHSLIPNO('%s') FROM DUAL
                """ % (ls_lot_no)

                cursor.execute(sql)
                rows = cursor.fetchone()
                cursor.close()

                ls_rch_slipno = rows[0]

                cursor = connection.cursor()

                sql = """                    
                    SELECT NVL(TRIM(RO_START_DT), 'N'), TO_CHAR(SYSDATE, 'YYYYMMDDHH24MISS') TRANS_DT FROM TP_RO_HIST WHERE CMP_CD = '%s' AND RO_NO = '%s'
                """ % (ls_cmp_cd, ls_rch_slipno)

                cursor.execute(sql)
                rows = cursor.fetchone()
                cursor.close()

                ls_rost_dt = rows[0]
                ls_trans_dt = rows[1]

                if ls_rost_dt == 'N':
                    # print('update')
                    cursor = connection.cursor()
                    sql = """
                            UPDATE TP_RO_HIST SET RO_START_DT = '%s'                                
                            WHERE CMP_CD = '%s'      
                            AND RO_NO = '%s'         
                            """ % (ls_trans_dt, ls_cmp_cd, ls_rch_slipno)
                    cursor.execute(sql)
                    cursor.close()
                    connection.commit()

                    # SANKEN
        elif ls_cmp_cd == '002013':
            if ls_item_mcd == 'N2' or ls_item_mcd == 'L3':
                if len(ls_sm_mark) != 4:
                    return HttpResponse(json.dumps({'error_message': "TRACE(Mark:4) CODE가 미등록 되었습니다! 전산팀에 문의 바랍니다."}),
                                        content_type="application/json")
            else:
                if len(ls_sm_mark) != 6:
                    return HttpResponse(json.dumps({'error_message': "TRACE(Mark:6) CODE가 미등록 되었습니다! 전산팀에 문의 바랍니다."}),
                                        content_type="application/json")

        # SANSHA
        elif ls_cmp_cd == '002014':
            # mark 3자리 check 추가하기
            if len(ls_sm_mark) != 3:
                return HttpResponse(json.dumps({'error_message': "투입 주 CODE가 미등록 되었습니다! 전산팀에 문의 바랍니다."}),
                                    content_type="application/json")

        # RENESAS
        elif ls_cmp_cd == '002022':
            if len(ls_sm_mark) != 6:
                return HttpResponse(json.dumps({'error_message': "TRACE(Mark) CODE가 미등록 되었습니다! 전산팀에 문의 바랍니다."}),
                                    content_type="application/json")
            else:
                # MARK NAME Check
                cursor2 = connection.cursor()
                sql = """
                        SELECT RCH_MARKNM FROM TP_RECEIVEHIS WHERE RCH_FLAG = 'Y' AND RCH_RUNNO = '%s'
                    """ % (ls_run_no)
                cursor2.execute(sql)
                rows = cursor2.fetchone()
                cursor2.close()

                if rows[0] is None:
                    ls_marknm = ''
                else:
                    ls_marknm = rows[0]

                if ls_sm_mark[3:6] != ls_marknm:
                    return HttpResponse(json.dumps({
                                                       'error_message': "RECEIVE Mark Name(" + ls_marknm + ")과 현 Mark Name(" + ls_sm_mark + ")이 다릅니다. 전산팀에 문의 바랍니다."}),
                                        content_type="application/json")

        # STM
        elif ls_cmp_cd == '002023':
            # print(ls_pakgrp)
            # print(ls_item_cd)
            if ls_pakgrp == 'RL02' or ls_item_cd == '*':
                print('pass 자재')
            else:
                if len(ls_sm_mark) != 6:
                    return HttpResponse(json.dumps({'error_message': "TRACE(Mark) CODE가 미등록 되었습니다! 전산팀에 문의 바랍니다."}),
                                        content_type="application/json")

        # ON-SEMI
        elif ls_cmp_cd == '002046':
            # MARK NAME Check
            cursor2 = connection.cursor()
            sql = """
                    SELECT ITEM_MARKRULE FROM TD_ITEMMAS WHERE ITEM_CD = (select item_Cd from tp_is where lot_no = '%s')
                """ % (ls_lot_no)
            cursor2.execute(sql)
            rows = cursor2.fetchone()
            cursor2.close()

            ls_markrule = rows[0]

            if ls_markrule == "R007" or ls_markrule == "R008":
                if len(ls_sm_mark) != 3:
                    return HttpResponse(json.dumps({'error_message': "주코드가 미등록 되었습니다! 전산팀에 문의 바랍니다."}),
                                        content_type="application/json")

        # ROHM
        elif ls_cmp_cd == '002054':
            # 주코드 조회
            cursor2 = connection.cursor()
            sql = """
                    SELECT SUBSTR(CAL_NO, 3, 4) 
                      FROM TP_CALENDAR  
			 	     WHERE CAL_SEC = (SELECT CMP_CAL_SEC FROM TF_COMPANY WHERE CMP_CD = '002054')
            	       AND CAL_ST <= (SELECT SUBSTR(IS_ACT_DT, 1, 8) FROM TP_IS WHERE LOT_NO = '%s')
					   AND CAL_ET >= (SELECT SUBSTR(IS_ACT_DT, 1, 8) FROM TP_IS WHERE LOT_NO = '%s')
                """ % (ls_lot_no, ls_lot_no)

            cursor2.execute(sql)
            rows = cursor2.fetchone()
            cursor2.close()

            ls_week = rows[0]

            # Option Code 조회
            cursor3 = connection.cursor()
            sql = """
                    SELECT NVL(ITEM_PKG_OPT,' ') FROM TD_ITEMMAS WHERE ITEM_CD = '%s'
                """ % (ls_item_cd)

            cursor3.execute(sql)
            rows = cursor3.fetchone()
            cursor3.close()

            ls_item_opt = rows[0]

            if ls_week != ls_sm_mark[0:4]:
                return HttpResponse(json.dumps({'error_message': "ROHM 주코드 형식 오류입니다! 전산팀에 문의 바랍니다."}),
                                    content_type="application/json")

            if (ls_item_mcd == 'Z3' and ls_item_opt != 'RY10') or ls_item_mcd == 'J3':
                if len(ls_sm_mark) != 6:
                    return HttpResponse(json.dumps({'error_message': "ROHM 주코드가 미등록(6 Digit) 되었습니다! 전산팀에 문의 바랍니다."}),
                                        content_type="application/json")
            else:
                if len(ls_sm_mark) != 4:
                    return HttpResponse(json.dumps({'error_message': "ROHM 주코드가 미등록(4 Digit) 되었습니다! 전산팀에 문의 바랍니다."}),
                                        content_type="application/json")

        # TRINNO
        elif ls_cmp_cd == '002059':
            if len(ls_sm_mark) != 6:
                return HttpResponse(json.dumps({'error_message': "TRINNO 주코드가 미등록 되었습니다! 전산팀에 문의 바랍니다."}),
                                    content_type="application/json")

        # LITTELFUSE
        elif ls_cmp_cd == '002087':
            if len(ls_sm_mark) != 5:
                return HttpResponse(json.dumps({'error_message': "LITTELFUSE 주코드가 미등록 되었습니다! 전산팀에 문의 바랍니다."}),
                                    content_type="application/json")

        # YESPOWER
        elif ls_cmp_cd == '002103':
            if len(ls_sm_mark) != 3:
                return HttpResponse(json.dumps({'error_message': "YESPOWERTECHNIX 주코드가 미등록 되었습니다! 전산팀에 문의 바랍니다."}),
                                    content_type="application/json")

        # iA semi
        elif ls_cmp_cd == '002104':
            if len(ls_sm_mark) != 6:
                return HttpResponse(json.dumps({'error_message': "iA semi 주코드가 미등록 되었습니다! 전산팀에 문의 바랍니다."}),
                                    content_type="application/json")

        else:
            return HttpResponse(json.dumps({'error_message': "등록되지 않는 고객입니다. 전산팀에 문의하세요."}),
                                content_type="application/json")

    else:
        return HttpResponse(json.dumps({'error_message': "PDA용으로 개발되지 않은 고객입니다. ERP에서 처리를 해주시길 바랍니다."}),
                            content_type="application/json")

    # OK Commit

    return HttpResponse()
