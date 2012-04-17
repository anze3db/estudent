from django.contrib.auth.models import get_hexdigest
from django.db import models
from django.utils.translation import ugettext as _

ALGO = 'sha1'



class Student(models.Model):

    def generateEnrollment(): #@NoSelf
        """Generates a new enrollment number"""
        
        last = Student.objects.order_by('enrollment_number')
        if last.count() > 0:
            return last.get().enrollment_number + 1   
        else:
            return 
        
    enrollment_number = models.IntegerField(_("enrollment number"), primary_key=True, unique=True, default=generateEnrollment)
    name = models.CharField(_(_("name")), max_length=255)
    surname = models.CharField(_("surname"), max_length=255)
    social_security_number = models.CharField(_("social security number"), max_length=13, blank = True, null = True)
    tax_number = models.CharField(_("tax number"), max_length=8)
    email = models.EmailField(_("email"), max_length=255)
    password = models.CharField(_('password'), max_length=128, blank = True, null = True)
    
    courses = models.ManyToManyField("codelist.Course")
    program = models.OneToOneField("codelist.StudyProgram")

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
    course    = models.ManyToManyField("codelist.Course", null=True, blank=True)
    
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
    course = models.ForeignKey("codelist.Course", related_name=("course"), verbose_name = _("course"))
    instructor = models.OneToOneField("codelist.Instructor", verbose_name=_("instructor"))
    date = models.DateField();
    students = models.ManyToManyField('Student', blank=True)
    
    def __unicode__(self):
        return str(self.date) + ' ' + str(self.course)

    class Meta:
        verbose_name_plural = _("exam dates")
        verbose_name = _("exam date")
        
class ExamResult(models.Model):
    exam = models.OneToOneField('ExamDate')
    student = models.OneToOneField('Student')
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

    def __unicode__(self):
        return str(self.exam.date) + ' ' + str(self.student) + ' (' + str(self.result) + ')'
    
    class Meta:
        verbose_name_plural = _("exam results")
        verbose_name = _("exam result")




