from django.conf.urls import include, url
from django.urls import path

from . import views
from Powerapp.views import *


app_name = "Powerapp"

urlpatterns=[
    path('addmodule/', CreateModule.as_view(),name='addmodule' ),
    path('deletemodule/<str:pk>/', DeleteModule.as_view(), name='deletemodule'),
    path('updatemodule/<str:pk>', UpdateModule.as_view(), name='updatemodule' ),
    path('detailmodule/<str:pk>', DetailModule.as_view(), name='detailmodule' ),
    path('listmodule', ListModules.as_view(), name = 'listmodules'),
    path('listmodule', ListModules.as_view(), name = 'home')
]