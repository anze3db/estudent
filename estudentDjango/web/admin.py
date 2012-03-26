from django.conf.urls.defaults import *
from django.contrib import admin, messages
from django.shortcuts import redirect
from urllib import urlopen
from urllib import urlencode
from web.models import Country

class CountryAdmin(admin.ModelAdmin):

    UPDATE_URL = 'http://www.stat.si/klasje/tabela.aspx?CVN=3888'
    model = Country

    def admin_update_countries(self, request):
        
        messages.error(request, "The message")
        csv_data = urlopen(self.UPDATE_URL, data=urlencode(
				{'__EVENTTARGET':'lbtnCSV',
				 '__VIEWSTATE':'/wEPDwUKMTE0NzM0NDIwOA8WAh4IRmlsZU5hbWUFDERSWkFWRV8yMDA3YRYCAgUPZBYCAgEPDxYCHgRUZXh0BUZEUlpBVkUgLSBEcsW+YXZlIGluIGRydWdhIG96ZW1samEgLSBzbG92ZW5za2kgc3RhbmRhcmQgSVNPIDMxNjYsIDIwMDdhZGRkGIb41rYrP0v4AjxvttSQlHzBYkKrRV1AnnRqhWi3Khc=',
				 '__EVENTVALIDATION':'/wEWBgLjvsyeCgL9jOOoBAKy46z3AQK9zJaBCQLs0bLrBgKM54rGBqOqwJFQsH2QbRBir2QR/GT3KuQJWO2Z+1fyMQB26Y8j'
						
				}))
        csv_data.readline()
        for line in csv_data.readlines():
            l = line.split(';')
            c = Country()
            #print l[1], str(l[2]), l[3]
            c.category_code = l[1]
            #c.descriptor = l[2]
            c.descriptor_english = l[3]
            c.save()
        
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
