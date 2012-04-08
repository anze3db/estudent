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
