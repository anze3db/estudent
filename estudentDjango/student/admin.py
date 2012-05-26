from django.conf.urls.defaults import *
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from student.models import *
from student.forms import StudentForm

class AddressInLine(admin.TabularInline):
    model = Address
    max_num = 2
    raw_id_fields = ("country","region","post")
    
class PhoneInLine(admin.TabularInline):
    model = Phone
    max_num = 2
    
class StudentAdmin(admin.ModelAdmin):
    model = Student
    search_fields = ('enrollment_number', 'name', 'surname')
    inlines = [PhoneInLine, AddressInLine]
    form = StudentForm
    raw_id_fields = ("birth_country","birth_region")


class EnrollmentAdmin(admin.ModelAdmin):
    model = Enrollment
    search_fields = ('student__name','student__surname', 'student__enrollment_number')
    raw_id_fields = ("student","program")
    list_filter = ('study_year', 'class_year', 'modules', 'program', 'courses', 'enrol_type', 'regular');
    

class CurriculumAdmin(admin.ModelAdmin):
    model = Curriculum
    list_filter = ('mandatory', 'class_year', 'module', 'program');

    search_fields = ('course',)





class ModuleAdmin(admin.ModelAdmin):
    model = Module
    #list_filter = ('curriculum__course', 'mandatory');
    
    
admin.site.register(Student, StudentAdmin)
admin.site.register(Address)
admin.site.register(Enrollment, EnrollmentAdmin)        
admin.site.register(ExamDate)
admin.site.register(ExamSignUp)
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(Module, ModuleAdmin)

