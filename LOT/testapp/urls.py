from django.urls import path
from . import views

urlpatterns = [
    # path('', views.movein_1, name='movein_1'),
    # path('', views.mv_in_1, name='mv_in_1'),
    path('mv_in_1', views.mv_in_1, name='mv_in_1'),
    path('test2', views.test2, name='test2'),
    path('working', views.working, name='working'),
    path('mv_in_2', views.mv_in_2, name='mv_in_2'),
    path('mv_in_3', views.mv_in_3, name='mv_in_3'),
    path('confirm', views.confirm, name='confirm'),
    path('total_cnt', views.total_cnt, name='total_cnt'),
    path('insertTest', views.insertTest, name='insertTest'),
    path('insertRes', views.insertRes, name='insertRes'),
    path('dropdownList', views.dropdownList, name='dropdownList'),
    path('slideList', views.slideList, name='slideList'),
    path('QRcode', views.QRcode, name='QRcode'),
    path('test', views.test, name='test'),
    path('ajax_test1', views.ajax_test1, name='ajax_test1'),
    path('ajax_test2', views.ajax_test2, name='ajax_test2'),
#     --------------------------------------------------------
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('movein_1', views.movein_1, name='movein_1'),
    path('P_TM', views.P_TM, name='P_TM'),
    path('P_SAW', views.P_SAW, name='P_SAW'),

    path('lot_select', views.lot_select, name='lot_select'),
    path('lot_select_2', views.lot_select_2, name='lot_select_2'),

    path('er_return_chk', views.er_return_chk, name='er_return_chk'),
    path('er_return_update', views.er_return_update, name='er_return_update'),
    
    path('movein_2', views.movein_2, name='movein_2'),
    path('moveout', views.moveout, name='moveout'),

    path('movein_3', views.movein_3, name='movein_3'),
    
    path('emp_chk', views.emp_chk, name='emp_chk'),
    path('mat_insert', views.mat_insert, name='mat_insert'),
    path('lot_start_insert', views.lot_start_insert, name='lot_start_insert'),
    path('MCN_LIST', views.MCN_LIST, name='MCN_LIST'),
    path('move_out_check', views.move_out_check, name='move_out_check'),

#     ccs-----------------------------------------------------------------------------
    path('ccs', views.ccs, name='ccs'),
    path('ccsInformation', views.ccsInformation, name='ccsInformation'),
    path('ccsContent', views.ccsContent, name='ccsContent'),
    # path('ccsNewNO', views.ccsNewNO, name='ccsNewNO'),
    path('ccs_mas_Insert', views.ccs_mas_Insert, name='ccs_mas_Insert'),
    # path('ccsglobalno', views.ccsglobalno, name='ccsglobalno'),
    path('ccs_dtl_Insert', views.ccs_dtl_Insert, name='ccs_dtl_Insert'),
    path('ccs_value_arr', views.ccs_value_arr, name='ccs_value_arr')
    
    





]