from django.conf.urls.defaults import *
from django.contrib import admin, messages
from django.contrib.admin.options import csrf_protect_m
from django.core.context_processors import request
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from student.forms import StudentForm
from student.models import *

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
    
    
    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        self.list_display = ['action_checkbox', '__str__','_vpisna','_ime', '_priimek',]
        if 'study_year' not in request.GET:
            self.list_display.append('study_year')
        if 'class_year' not in request.GET:
            self.list_display.append('class_year')
        if 'program' not in request.GET:
            self.list_display.append('program')
        if 'enrol_type__exact' not in request.GET:
            self.list_display.append('enrol_type')
        if 'regular__exact' not in request.GET:
            self.list_display.append('regular')
            
        return admin.ModelAdmin.changelist_view(self, request, extra_context=extra_context)
    
    model = Enrollment
    search_fields = ('student__name','student__surname', 'student__enrollment_number')
    raw_id_fields = ("student","program")
    list_filter = ('study_year', 'class_year', 'modules', 'program', 'courses', 'enrol_type', 'regular');
    #list_display_links = ('id', )

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

