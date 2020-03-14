from django.conf.urls import include, url
from django.urls import path

from . import views
from Powerapp.views import *


app_name = "Powerapp"

urlpatterns=[
    path('', ListModules.as_view(),name='default' ),
    path('addmodule/', CreateModule.as_view(),name='addmodule' ),
    path('deletemodule/<str:pk>/', DeleteModule.as_view(), name='deletemodule'),
    path('updatemodule/<str:pk>', UpdateModule.as_view(), name='updatemodule' ),
    path('detailmodule/<str:pk>', DetailModule.as_view(), name='detailmodule' ),
    path('listmodule', ListModules.as_view(), name = 'listmodules'),
    path('listmodule', ListModules.as_view(), name = 'home'),
    path('btsoff/<str:ip>', BTSOFF.as_view(), name = 'btsoff'),
    path('btson/<str:ip>', BTSON.as_view(), name = 'btson'),
    path('hvacon/<str:ip>', HVACON.as_view(), name = 'hvacon'),
    path('hvacoff/<str:ip>', HVACOFF.as_view(), name = 'hvacoff'),
    path('genon/<str:ip>', GENON.as_view(), name = 'genon'),
    path('genoff/<str:ip>', GENOFF.as_view(), name = 'genoff'),
    path('update/', ModuleUpdateView.as_view(), name = 'moduleview'),
    path('hello/', ModuleHelloView.as_view(), name = 'helloview'),
    path('history/<str:pk>', HistoryView.as_view(), name = 'history'),

]