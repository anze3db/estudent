from codelist.models import *
from django.conf.urls.defaults import *
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

class CountryAdmin(admin.ModelAdmin):

    UPDATE_URL = 'http://www.stat.si/klasje/tabela.aspx?CVN=3888'
    model = Country
    
    list_display = ('descriptor',)
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

class StudyProgramAdmin(admin.ModelAdmin):
    model = StudyProgram
    
    list_display = ('descriptor',)
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

class PostAdmin(admin.ModelAdmin):
    model = Post
    
    list_display = ('descriptor',)
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

class RegionAdmin(admin.ModelAdmin):
    model = Region
    
    list_display = ('descriptor',)
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

class FacultyAdmin(admin.ModelAdmin):
    model = Faculty
    
    list_display = ('descriptor',)
    ordering = ('descriptor',)
    search_fields = ('descriptor',)
    
    def admin_update_faculty(self, request):
        Faculty.updateAll()
        messages.success(request, _("Faculty added successfully"))
        
        return redirect('/codelist/faculty')
    
    def get_urls(self):
        urls= super(FacultyAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'update',
                self.admin_site.admin_view(self.admin_update_faculty),
                name='admin_update_faculty',
                ),
        )
        return my_urls + urls
     
admin.site.register(Faculty, FacultyAdmin)
        
class CourseAdmin(admin.ModelAdmin):
    model= Course1
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    
    
admin.site.register(Course1, CourseAdmin)


class InstructorAdmin(admin.ModelAdmin):
    model= Instructor
    
    list_display = ('name','surname',)
    ordering = ('name','surname',)
    search_fields = ('name','surname',)
    
admin.site.register(Instructor, InstructorAdmin)
    
