from django.conf.urls import url, include

from student import views

urlpatterns = [
    url(r'^register/$', views.Register.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^task/$', views.TaskAssign.as_view()),
    url(r'^update_task/$', views.UpdateStatus.as_view()),
    url(r'^approve_task/$', views.ApproveTask.as_view()),
    url(r'update_profile/$', views.UpdateProfile.as_view()),
    url(r'^delete_task/(?P<task_id>[0-9]+)/$', views.TaskAssign.as_view(),name='delete_task'),
    url(r'^task_list/$', views.TaskList.as_view()),
]