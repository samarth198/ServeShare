from django.urls import path
from . import views
app_name = 'jobs'

urlpatterns = [
    path('post-job',views.post_job,name='post_job'),
    path('new-jobs',views.jobs,name='new_jobs'),
    path('<int:job_id>',views.job_desc,name='details'),
    # url pattern for approving and disaaproving applicant
    path('job/<int:job_id>/approve/<int:user_id>/', views.approve_applicant, name='approve_applicant'),
    path('job/<int:job_id>/disapprove/<int:user_id>/', views.disapprove_applicant, name='disapprove_applicant'),
]

