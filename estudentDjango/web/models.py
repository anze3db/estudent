from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.
class Country(models.Model):
	category_code = models.CharField(max_length=3)
	descriptor    = models.CharField(max_length=255)
	descriptor_english = models.CharField(max_length=255)
	
	class Meta:
		verbose_name_plural = _("countries")
		verbose_name = _("country")
		
	def __unicode__(self):
		return self.descriptor
	
	
		
