from django.conf.urls.defaults import patterns, include
from django.conf import settings

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
    (r'^ExamGrades/$', 'student.views.exam_grades_index'),
    (r'^ExamGrades/(?P<exam_Id>\d+)/$', 'student.views.exam_grades_view'),
    #(r'^index/$', 'api.views.index'),

    #(r'^admin/student/ExamGrades/$', 'student.views.exam_grades_view'),

)