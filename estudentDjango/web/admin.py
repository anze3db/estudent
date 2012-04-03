from django.conf.urls.defaults import *
from django.contrib import admin, messages
from django.shortcuts import redirect
from urllib import urlopen
from urllib import urlencode
from web.models import Country
from django.utils.encoding import smart_unicode

class CountryAdmin(admin.ModelAdmin):

    UPDATE_URL = 'http://www.stat.si/klasje/tabela.aspx?CVN=3888'
    model = Country
    
    list_display = ('descriptor',)
    ordering = ('descriptor',)
    search_fields = ('descriptor',)

    def admin_update_countries(self, request):
        
        csv_data = urlopen(self.UPDATE_URL, data=urlencode(
				{'__EVENTTARGET':'lbtnCSV',
				 '__VIEWSTATE':'/wEPDwUKMTE0NzM0NDIwOA8WAh4IRmlsZU5hbWUFDERSWkFWRV8yMDA3YRYCAgUPZBYCAgEPDxYCHgRUZXh0BUZEUlpBVkUgLSBEcsW+YXZlIGluIGRydWdhIG96ZW1samEgLSBzbG92ZW5za2kgc3RhbmRhcmQgSVNPIDMxNjYsIDIwMDdhZGRkGIb41rYrP0v4AjxvttSQlHzBYkKrRV1AnnRqhWi3Khc=',
				 '__EVENTVALIDATION':'/wEWBgLjvsyeCgL9jOOoBAKy46z3AQK9zJaBCQLs0bLrBgKM54rGBqOqwJFQsH2QbRBir2QR/GT3KuQJWO2Z+1fyMQB26Y8j'
						
				}))
        csv_data.readline()
        
        # remove all the data from the table:
        Country.objects.all().delete();
        
        for line in csv_data.readlines():
            l = line.split(';')
            c = Country()
            print l[1], str(l[2]), l[3]
            c.category_code = l[1].strip()
            c.descriptor = smart_unicode(l[2].strip(), encoding='windows-1250', strings_only=False, errors='strict')
            c.descriptor_english = l[3].strip()
            c.save()
            
        messages.success(request, "Countries added successfully")
        
        return redirect('/web/country')

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
