from django.contrib.auth.models import get_hexdigest
from django.db import models
from django.utils.translation import ugettext as _

ALGO = 'sha1'

class Student(models.Model):
    enrollment_number = models.IntegerField(_("enrollment number"))
    name = models.CharField(_(_("name")), max_length=255)
    surname = models.CharField(_("surname"), max_length=255)
    social_security_number = models.CharField(_("social security number"), max_length=13)
    tax_number = models.CharField(_("tax number"), max_length=8)
    address = models.OneToOneField("Address", related_name=("address"), verbose_name=_('address'))
    temp_address = models.OneToOneField("Address", related_name=("temp_address"), verbose_name=_('temporary address'))
    
    password = models.CharField(_('password'), max_length=128)
    
    
    def save(self, *args, **kwargs):
        self.password = get_hexdigest(ALGO, "sssalt", self.password)
        super(Student, self).save(*args, **kwargs)
    
    @staticmethod
    def authStudent(enrollment_number, password):
        try:
            return Student.objects.get(enrollment_number=enrollment_number, password=get_hexdigest(ALGO, "sssalt", password))
        except:
            return None
    
    class Meta:
        verbose_name_plural = _("students")
        verbose_name = _("student")
    
class Address(models.Model):
    street = models.CharField(_("street"), max_length=255)
    country = models.ForeignKey("codelist.Country", related_name=("country"), verbose_name = _("country"))
    
    class Meta:
        verbose_name_plural = _("addresses")
        verbose_name = _("address")

class Enrollment(models.Model):
    student = models.OneToOneField("Student", verbose_name=_("student"))
    program = models.OneToOneField("codelist.StudyProgram", verbose_name=_("study program"))
    class Meta:
        verbose_name_plural = _("enrollment")
        verbose_name = _("enrollment")