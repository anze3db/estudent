from django.conf.urls.defaults import *
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from student.models import *

admin.site.register(Student)
admin.site.register(Address)
admin.site.register(Enrollment)        
admin.site.register(ExamDate)
