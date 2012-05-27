from django.conf.urls.defaults import patterns, include
from django.conf import settings

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
					
	(r'^login/$', 'api.views.login'),
	(r'^index/$', 'api.views.index'),
	(r'^examDates/$', 'api.views.examDates'),
	(r'^enrolemntList/$', 'api.views.enrolemntList'),
    (r'^examSignUp/$', 'api.views.examSignUp'),
    (r'^getCourses/$', 'api.views.getCoursesforEnrollment'),
    (r'^getAllCourses/$', 'api.views.getAllCourses'),
    (r'^getFilteredCoursesModules/$', 'api.views.getFilteredCoursesModules'),
    (r'^getFilteredGroupInstructorsForCourses/$', 'api.views.getFilteredGroupInstructorsForCourses'),
    (r'^getAllExamDates/$', 'api.views.getAllExamDates'),
    (r'^test/$', 'api.views.test'),
    (r'^addSignUp/$', 'api.views.addSignUp'),
    # Examples:
    # url(r'^$', 'estudentDjango.views.home', name='home'),
    # url(r'^estudentDjango/', include('estudentDjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
