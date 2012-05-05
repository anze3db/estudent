from django.contrib.auth.models import get_hexdigest
from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator 
from django.utils.encoding import force_unicode

import re 

ALGO = 'sha1'



class Student(models.Model):

    def generateEnrollment(): #@NoSelf
        """Generates a new enrollment number"""
        
        last = Student.objects.order_by('-enrollment_number')
        if last.count() > 0:
            return last.filter()[0].enrollment_number + 1   
        else:
            return 63110001

    num_regex = re.compile(r'^63[0-9]{6}$')         
    enrollment_number = models.IntegerField(_("enrollment number"), primary_key=True, unique=True, default=generateEnrollment, validators=[RegexValidator(regex=num_regex)])
    name = models.CharField(_(_("name")), max_length=255)
    surname = models.CharField(_("surname"), max_length=255)
    
    ss_regex = re.compile(r'^[0-3][0-9][0-1][0-9][0-9]{3}50[0-9]{4}$')
    social_security_number = models.CharField(_("social security number"), max_length=13, blank = True, null = True, validators=[RegexValidator(regex=ss_regex)])
    #social_security_number = models.CharField(_("social security number"), max_length=13, blank = True, null = True)
    tax_number = models.CharField(_("tax number"), max_length=8)
    email = models.EmailField(_("email"), max_length=255)
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
        
    class Admin:
        js = ('/app_media/disableEnrollmentNumber.js')

    
    def __unicode__(self):
        return str(self.enrollment_number) + ' ' + self.name + ' ' + self.surname
    
    
        
class PersonalInformation(models.Model):
    # TODO: add name, surname and stuff from student that should be here
    GENDER = (
        ('M', _('male')),
        ('F', _('female')),
    )
    
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER)
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
    region = models.ForeignKey("codelist.Region", related_name=("address_region"), verbose_name=_("region"))
    post = models.ForeignKey("codelist.Post", related_name=("address_post"), verbose_name=_("post"))
    country = models.ForeignKey("codelist.Country", related_name=("address_country"), verbose_name = _("country"))
    student = models.ForeignKey("Student", related_name=("student"))
    type = models.CharField(max_length = 1, choices = ADDRESS_TYPES)
    send_address = models.BooleanField(_("send address"))
    
    class Meta:
        verbose_name_plural = _("addresses")
        verbose_name = _("address")

class Enrollment(models.Model):
    student = models.ForeignKey("Student", verbose_name=_("student"), related_name="enrollment_student")
    program = models.ForeignKey("codelist.StudyProgram",related_name="study_program", verbose_name=_("study program"))
    study_year = models.PositiveIntegerField('Study year')
    class_year  = models.PositiveIntegerField() #letnik
    ENROL_CHOICES = (
        ('V1', 'Prvi vpis v letnik'),
        ('V2', 'Ponavljanje letnika'),
        ('V3', 'Nadaljevanje letnika'),
        ('AB', 'Absolvent')
    )
    enrol_type = models.CharField(max_length=2, choices=ENROL_CHOICES, default='V1')
    courses = models.ManyToManyField("codelist.Course", null=True, blank=True)
    
    def __unicode__(self):
        return u'%d %s %s %d (%d)' % (self.student.enrollment_number, self.student.name, self.student.surname, self.study_year, self.class_year)
    
    def format_year(self):
        return u'%d/%d' % (self.study_year, self.study_year+1)

    
    class Meta:
        verbose_name_plural = _("enrollment")
        verbose_name = _("enrollment")
        ordering = ['program', 'study_year', 'class_year']
        unique_together = ('student', 'study_year', 'program', 'class_year')
        
        
class ExamDate(models.Model):
    """
    tabela izpitni roki
    """
    course = models.ForeignKey("codelist.Course", related_name=("course"), verbose_name = _("course"))
    instructor = models.ForeignKey("codelist.Instructor", verbose_name=_("instructor"))
    date = models.DateField();
    students = models.ManyToManyField('Student', blank=True)
    
    
    def __unicode__(self):
        return force_unicode(str(self.date) + ' ' + str(self.course))

    class Meta:
        verbose_name_plural = _("exam dates")
        verbose_name = _("exam date")
        
class ExamSignUp(models.Model):
    enroll = models.ForeignKey('Enrollment')
    examDate = models.ForeignKey('ExamDate')

    RESULTS = (
                ('NR', 'Ni rezultatov'),
                ('VP', 'Vrnjena prijava'),
                ('1', 'nezadostno 1'),
                ('2', 'nezadostno 2'),
                ('3', 'nezadostno 3'),
                ('4', 'nezadostno 4'),
                ('5', 'nezadostno 5'),
                ('6', 'zadostno 6'),
                ('7', 'dobro 7'),
                ('8', 'prav dobro 8'),
                ('9', 'odlicno 9'),
                ('10', 'odlicno 10'),
            )
    result = models.CharField(max_length=2, choices=RESULTS, default='NR')
    paidfor = models.CharField(max_length=2, choices=(('Y', 'Yes'), ('N', 'No')), default='Y')
    valid = models.CharField(max_length=2, choices=(('Y', 'Yes'), ('N', 'No')), default='Y')

    def __unicode__(self):
        return str(self.examDate) + ' ' + str(self.enroll) + ' (' + str(self.result) + ')'
    
    class Meta:
        verbose_name_plural = _("exam signups")
        verbose_name = _("exam signup")




