from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
import api

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
		        {'document_root': settings.STATIC_DOC_ROOT}),
	(r'^api/', include('api.urls')),
    (r'', include(admin.site.urls)),
    (r'^admin/student/ExamGrades/$', 'student.views.exam_grades_view'),

    # Examples:
    # url(r'^$', 'estudentDjango.views.home', name='home'),
    # url(r'^estudentDjango/', include('estudentDjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
