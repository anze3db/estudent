from django.conf.urls.defaults import *
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from student.models import *

class AddressInLine(admin.TabularInline):
    model = Address
    max_num = 2
    
class PersonalInformationInLine(admin.StackedInline):
    model = PersonalInformation
    max_num = 1


class StudentAdmin(admin.ModelAdmin):
    model = Student
    search_fields = ('enrollment_number', 'name', 'surname')
    inlines = [AddressInLine, PersonalInformationInLine]


admin.site.register(Student, StudentAdmin)
admin.site.register(Address)
admin.site.register(Enrollment)
admin.site.register(ExamDate)
