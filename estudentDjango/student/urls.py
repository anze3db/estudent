from django.conf.urls.defaults import patterns, include
from django.conf import settings

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
    (r'^ExamGrades/$', 'student.views.exam_grades_index'),
    (r'^ExamGrades/(?P<exam_Id>\d+)/$', 'student.views.exam_grades_view'),
	(r'^ClassList/$', 'student.views.class_list'),    
	(r'^ExamSignUp/$', 'student.views.exam_sign_up_index'),
    (r'^ExamSignUp/(?P<student_Id>\d+)/signUp/$', 'student.views.exam_sign_up'),
    (r'^ExamSignUp/(?P<student_Id>\d+)/confirm/(?P<exam_Id>\d+)/(?P<enroll_Id>\d+)/$', 'student.views.sign_up_confirm'),
    (r'^ExamSignUp/(?P<student_Id>\d+)/success/(?P<exam_Id>\d+)/$', 'student.views.sign_up_success'),
    (r'^ExamSignUp/(?P<student_Id>\d+)/signOut/$', 'student.views.exam_sign_out'),
	(r'^StudentIndex/$', 'student.views.student_index'),
    (r'^StudentIndex/(?P<student_Id>\d+)/(?P<display>\d+)/$', 'student.views.student_index_list'),
    #(r'^index/$', 'api.views.index'),

    #(r'^admin/student/ExamGrades/$', 'student.views.exam_grades_view'),

)
