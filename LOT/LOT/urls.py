"""LOT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test2', include('testapp.urls')),
    path('mv_in_2', include('testapp.urls')),
    path('mv_in_3', include('testapp.urls')),
    path('confirm', include('testapp.urls')),
    path('total_cnt', include('testapp.urls')),
    path('insertTest', include('testapp.urls')),
    path('insertRes', include('testapp.urls')),
    path('dropdownList', include('testapp.urls')),
    path('slideList',include('testapp.urls')),
    path('QRcode',include('testapp.urls')),
    path('test', include('testapp.urls')),
    path('ajax_test1', include('testapp.urls')),
    path('ajax_test2', include('testapp.urls')),
    # ---------------------------------------------
    path('', include('testapp.urls')),
    path('ccs', include('testapp.urls')),
    path('ccsInformation', include('testapp.urls')),
    path('ccsContent', include('testapp.urls')),
    path('movein_1', include('testapp.urls')),
    path('movein_1_data', include('testapp.urls')),
    path('movein_2', include('testapp.urls')),
    path('moveout', include('testapp.urls')),
    path('movein_3', include('testapp.urls')),
    path('total_cnt', include('testapp.urls')),
    path('P_TM', include('testapp.urls')),
    path('P_SAW', include('testapp.urls')),
    path('MCN_LIST', include('testapp.urls')),
    path('move_out_check', include('testapp.urls')),
    path('lot_select', include('testapp.urls')),
    path('lot_select_2', include('testapp.urls')),



]
