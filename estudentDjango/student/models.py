from django.contrib.auth.models import get_hexdigest
from django.db import models
from django.utils.translation import ugettext as _

ALGO = 'sha1'

class Student(models.Model):
    enrollment_number = models.IntegerField(_("enrollment number"))
    name = models.CharField(_(_("name")), max_length=255)
    surname = models.CharField(_("surname"), max_length=255)
    social_security_number = models.CharField(_("social security number"), max_length=13, blank = True, null = True)
    tax_number = models.CharField(_("tax number"), max_length=8)
    password = models.CharField(_('password'), max_length=128, blank = True, null = True)
    
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

    def __unicode__(self):
        return str(self.enrollment_number)
        
class PersonalInformation(models.Model):
    GENDER = (
        ('1', _('male')),
        ('2', _('female')),
    )
    
    gender = models.IntegerField(_("gender"), choices=GENDER)
    birth_date = models.DateField(_("date of birth"))
    birth_country = models.ForeignKey("codelist.Country", related_name="birth_country", verbose_name = _("country of birth"))
    birth_place = models.CharField(_("place of birth"), max_length=255)
    birth_region = models.ForeignKey("codelist.Region", related_name="region", verbose_name=_("region of birth"))
    #nationality = models.
    student = models.ForeignKey("Student", related_name=("personal_student"))

class Address(models.Model):
    
    ADDRESS_TYPES = (
        ('P', _('permanent address')),
        ('T', _('temporary address')),
    )
    street = models.CharField(_("street"), max_length=255)
    country = models.ForeignKey("codelist.Country", related_name=("country"), verbose_name = _("country"))
    student = models.ForeignKey("Student", related_name=("student"))
    type = models.CharField(max_length = 1, choices = ADDRESS_TYPES)
    
    class Meta:
        verbose_name_plural = _("addresses")
        verbose_name = _("address")

class Enrollment(models.Model):
    student = models.ForeignKey("Student", verbose_name=_("student"))
    program = models.ForeignKey("codelist.StudyProgram", verbose_name=_("study program"))
    
    class Meta:
        verbose_name_plural = _("enrollment")
        verbose_name = _("enrollment")
        
class ExamDate(models.Model):
    course = models.ForeignKey("codelist.Course", related_name=("course"), verbose_name = _("course"))
    instructor = models.OneToOneField("codelist.Instructor", verbose_name=_("instructor"))
    date = models.DateField();
    
    def __unicode__(self):
        return str(self.date) + ' ' + str(self.course)

    class Meta:
        verbose_name_plural = _("exam dates")
        verbose_name = _("exam date")
        

