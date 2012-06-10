from codelist.models import *
from django.conf.urls.defaults import *
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django import forms

class CodelistAdmin(admin.ModelAdmin):
    
    def changelist_view(self, request, extra_context=None):
        """
        Overrides the default changelist_view, sets the default filter valid to true
        """
        if not request.GET.has_key('valid__exact'):
            q = request.GET.copy()
            q['valid__exact'] = '1'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(CodelistAdmin,self).changelist_view(request, extra_context=extra_context)   


class CountryAdmin(CodelistAdmin):
    UPDATE_URL = 'http://www.stat.si/klasje/tabela.aspx?CVN=3888'
    model = Country
    
    list_display = ('descriptor', 'valid',)
    list_filter = ('valid',)
    ordering = ('descriptor',)
    search_fields = ('descriptor',)

    def admin_update_countries(self, request):
        Country.updateAll()
            
        messages.success(request, _("Countries added successfully"))
        
        return redirect('/codelist/country')

    # override the get_urls to add a custom view:
    def get_urls(self):
        urls = super(CountryAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'update',
                self.admin_site.admin_view(self.admin_update_countries),
                name='admin_update_countries',
            ),
        )
        return my_urls + urls


admin.site.register(Country, CountryAdmin)

class StudyProgramAdmin(CodelistAdmin):
    model = StudyProgram
    
    list_display = ('descriptor', 'valid',)
    list_filter = ('valid',)
    ordering = ('descriptor',)
    search_fields = ('descriptor',)

    def admin_update_study_programs(self, request):
        StudyProgram.updateAll()
            
        messages.success(request, _("Study Programs added successfully"))
        
        return redirect('/codelist/studyprogram')

    # override the get_urls to add a custom view:
    def get_urls(self):
        urls = super(StudyProgramAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'update',
                self.admin_site.admin_view(self.admin_update_study_programs),
                name='admin_update_study_programs',
            ),
        )
        return my_urls + urls


admin.site.register(StudyProgram, StudyProgramAdmin)

class PostAdmin(CodelistAdmin):
    model = Post
    
    list_display = ('descriptor', 'valid',)
    list_filter = ('valid',)
    ordering = ('descriptor',)
    search_fields = ('descriptor',)

    def admin_update_posts(self, request):
        Post.updateAll()
            
        messages.success(request, _("Post added successfully"))
        
        return redirect('/codelist/post')

    # override the get_urls to add a custom view:
    def get_urls(self):
        urls = super(PostAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'update',
                self.admin_site.admin_view(self.admin_update_posts),
                name='admin_update_posts',
            ),
        )
        return my_urls + urls


admin.site.register(Post, PostAdmin)

class RegionAdmin(CodelistAdmin):
    model = Region
    
    list_display = ('descriptor', 'valid',)
    list_filter = ('valid',)
    ordering = ('descriptor',)
    search_fields = ('descriptor',)
    
    def admin_update_regions(self, request):
        Region.updateAll()
        
        messages.success(request, _("Region added successfully"))
        
        return redirect('/codelist/region')
    
    def get_urls(self):
        urls = super(RegionAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'update',
                self.admin_site.admin_view(self.admin_update_regions),
                name='admin_update_regions',
                ),
        )
        return my_urls + urls
    
admin.site.register(Region, RegionAdmin)

class FacultyAdmin(CodelistAdmin):
    model = Faculty
    
    list_display = ('descriptor', 'valid',)
    list_filter = ('valid',)
    ordering = ('descriptor',)
    search_fields = ('descriptor',)
    
    def admin_update_faculty(self, request):
        Faculty.updateAll()
        messages.success(request, _("Faculty added successfully"))
        
        return redirect('/codelist/faculty')
    
    def get_urls(self):
        urls = super(FacultyAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'update',
                self.admin_site.admin_view(self.admin_update_faculty),
                name='admin_update_faculty',
                ),
        )
        return my_urls + urls
     
admin.site.register(Faculty, FacultyAdmin)
        
class CourseAdmin(CodelistAdmin):
    model = Course
    list_display = ('course_code', 'name', 'predavatelji', 'valid',)
    list_filter = ('valid','instructors')
    ordering = ('name',)
    search_fields = ('name',)
    
    def admin_update_course(self, request):
        Course.updateAll()
        messages.success(request, _("Course added successfully"))
        
        return redirect('/codelist/course')

    def get_urls(self):
        urls = super(CourseAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'update',
                self.admin_site.admin_view(self.admin_update_course),
                name='admin_update_course',
            ),
        )
        return my_urls + urls
    
admin.site.register(Course, CourseAdmin)


class InstructorAdmin(CodelistAdmin):
    model = Instructor
    list_display = ('name', 'surname', 'valid',)
    list_filter = ('valid',)
    ordering = ('name', 'surname',)
    search_fields = ('name', 'surname',)
    
    def admin_update_instructor(self, request):
        Instructor.updateAll()
        messages.success(request, _("Instructor added successfully"))
        
        return redirect('/codelist/instructor')

    def get_urls(self):
        urls = super(InstructorAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'update',
                self.admin_site.admin_view(self.admin_update_instructor),
                name='admin_update',
            ),
        )
        return my_urls + urls
    
admin.site.register(Instructor, InstructorAdmin)

class GroupInstructorsForm(forms.ModelForm):
    class Meta:
        model = GroupInstructors
    def clean(self):
        super(GroupInstructorsForm, self).clean()
        if len(self.cleaned_data.get('instructor')) > 3:
            raise forms.ValidationError(u'Izberete lahko najvec tri izvajalce.')
        return self.cleaned_data

class GroupInstructorsAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'get1st', 'get2nd', 'get3rd')
    form = GroupInstructorsForm
    list_per_page = 10000

admin.site.register(GroupInstructors, GroupInstructorsAdmin)


class BetterUserAdmin(UserAdmin):
    """
    Add user form now has options to edit permissions and groups
    This makes it easy to add a django user to an instructor
    """
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Groups'), {'fields': ('groups',)}),
    )

admin.site.unregister(User)
admin.site.register(User, BetterUserAdmin)

