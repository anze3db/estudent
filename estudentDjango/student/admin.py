from django.conf.urls.defaults import *
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from student.models import *

class AddressInLine(admin.TabularInline):
    model = Address
    max_num = 2
    raw_id_fields = ("country","region","post")
    
class PersonalInformationInLine(admin.StackedInline):
    model = PersonalInformation
    max_num = 1
    raw_id_fields = ("birth_country","birth_region")


class StudentAdmin(admin.ModelAdmin):
    model = Student
    search_fields = ('enrollment_number', 'name', 'surname')
    inlines = [AddressInLine, PersonalInformationInLine]


class EnrollmentAdmin(admin.ModelAdmin):
    raw_id_fields = ("student","program")
    

        

admin.site.register(Student, StudentAdmin)
admin.site.register(Address)
admin.site.register(Enrollment, EnrollmentAdmin)        
admin.site.register(ExamDate)
admin.site.register(ExamSignUp)
