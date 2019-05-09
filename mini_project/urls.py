"""mini_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from mini import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('student_register/',views.student_register,name="student_register"),
    path('worker_register/',views.worker_register,name="worker_register"),
    path('student_home/',views.shome,name="shome"),
    path('worker_home/',views.whome,name="whome"),
    url(r'^handle/(?P<problem_id>[0-9]+)/$',views.handle,name="handle"),
    path('pass/',views.pass_pro,name="pass"),
    path('image/',views.image,name="image"),
    path('detect/',views.detect,name="detect"),
    path('confirm/',views.confirm,name="confirm"),
    path('confirm1/',views.confirm1,name="confirm"),
    path('report/',views.report,name="report"),
    path('profile/',views.profile,name="profile"),
    path('worker_profile/',views.worker_profile,name="worker_profile"),
    path('',views.admin,name="admin"),
    path('block/',views.block,name="block"),
    path('block_id/',views.block_id,name="block_id"),
    path('rem/',views.rem,name="rem"),
    path('rem_id/',views.rem_id,name="rem_id"),
    path('unblock/',views.unblock,name="block"),
    path('unblock_id/',views.unblock_id,name="unblock_id"),
    path('edit/',views.edit,name="edit"),
    path('s_change/',views.s_change,name="s_change"),
    path('unblock_id/',views.unblock_id,name="unblock_id"),
    path('pro/',views.pro,name="pro"),
    path('user_table/',views.user_table,name="user_table"),
    path('worker_table/',views.worker_table,name="worker_table"),
    path('garbage_table/',views.garbage_table,name="garbage_table"),
    path('civil_table/',views.civil_table,name="civil_table"),
    path('all_problem_table/',views.all_problem_table,name="all_problem_table"),
    path('completed_table/',views.completed_table,name="completed_table"),





    #path('admint_home/',views.ahome,name="ahome"),

]
