from django.db import models

# Create your models here.
class Country(models.Model):
	category_code = models.CharField(max_length=3)
	descriptor    = models.CharField(max_length=255)
	descriptor_english = models.CharField(max_length=255)
	
	def __unicode__(self):
		return self.descriptor_english
