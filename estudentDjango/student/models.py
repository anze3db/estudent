from django.contrib.auth.models import get_hexdigest
from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator 
from django.utils.encoding import force_unicode
from codelist.models import *

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
    
    GENDER = (
        ('M', _('male')),
        ('F', _('female')),
    )
    
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER)
    birth_date = models.DateField(_("date of birth"))
    birth_country = models.ForeignKey("codelist.Country", related_name="birth_country", verbose_name = _("country of birth"))
    birth_place = models.CharField(_("place of birth"), max_length=255)
    birth_region = models.ForeignKey("codelist.Region", related_name="region", verbose_name=_("region of birth"))
    
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


    def get_all_classes(self):
        allClass=[]
        #course={}
        enroll = Enrollment.objects.filter(student=self)
        for e in enroll:
            #course["enrollment"]=e
            #course["courses"]=e.get_courses()
            allClass= allClass+[e.get_courses()]

        return allClass

    def get_current_exam_dates(self):
        courses = self.get_current_classes()
        return list(ExamDate.objects.filter(course__in=courses))




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
    study_year = models.PositiveIntegerField(_("study year"))
    class_year  = models.PositiveIntegerField(_("class year")) #letnik
    ENROL_CHOICES = (
        ('V1', 'Prvi vpis v letnik'),
        ('V2', 'Ponavljanje letnika'),
        ('V3', 'Nadaljevanje letnika'),
        ('AB', 'Absolvent')
    )
    enrol_type = models.CharField(_("enrollment type"), max_length=2, choices=ENROL_CHOICES, default='V1')
    courses = models.ManyToManyField("codelist.Course", null=True, blank=True)
    modules      = models.ManyToManyField("Module", null=True, blank=True)
    regular       = models.BooleanField(_("regural"), default=True)
    
    def __unicode__(self):
        return u'%d %s %s %d (%d)' % (self.student.enrollment_number, self.student.name, self.student.surname, self.study_year, self.class_year)
    
    def format_year(self):
        return u'%d/%d' % (self.study_year, self.study_year+1)

    


    def get_courses(self):
        courses =[]
        modules=Module.objects.get(enrollment=self)
        allInProgram=Curriculum.objects.filter(program=self.program)
        mandatory=allInProgram.filter(mandatory=1)
        for selectiveCourse in  Course.objects.filter(enrollment__student=self.student):
            courses=courses+[selectiveCourse.course_code]
        for man in mandatory:
            courses=courses+[man.course_id]
        for mod in Curriculum.objects.filter(module=modules): #todo check if module is null
            courses=courses+[mod.course_id]

        allCourses=[]
        for i in Course.objects.all():
            for j in courses:
                if i.course_code==j:
                    allCourses=allCourses+[i]

        return allCourses

    class Meta:
        verbose_name_plural = _("enrollments")
        verbose_name = _("enrollment")
        ordering = ['program', 'study_year', 'class_year']
        unique_together = ('student', 'study_year', 'program', 'class_year')


class ExamDate(models.Model):
    """
    tabela izpitni roki
    """
    course = models.ForeignKey("codelist.Course", related_name=("course"), verbose_name = _("course"))
    instructors = models.ForeignKey("codelist.GroupInstructors", verbose_name=_("group of instructors"), null=True, blank=True)
    study_year = models.PositiveIntegerField(_("study year"),db_index=True)
    location    = models.CharField(_("location"),max_length=7)
    date = models.DateField(_("date"))
    nr_SignUp   = models.PositiveIntegerField(_("nr of Sign up"))
    total_points = models.PositiveIntegerField(_("total points"))
    min_pos = models.PositiveIntegerField(_("minimal points"))
    students =models.ManyToManyField(Enrollment, through='ExamSignUp')


    
    def __unicode__(self):
        return force_unicode(str(self.date) + ' ' + str(self.course))

    class Meta:
        verbose_name_plural = _("exam dates")
        verbose_name = _("exam date")


    def already_signedUp(self, student):
        return bool(ExamSignUp.objects.filter(examdate__course__in=codelist.Course.objects.filter(examdate__examsignup__enrollment__student=student)))


class ExamSignUp(models.Model):
    enroll = models.ForeignKey('Enrollment')
    examDate = models.ForeignKey('ExamDate')
    VP = models.BooleanField(_("VP"))

    RESULTS = (
                ('NR', 'Ni rezultatov'),
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
    result_exam = models.CharField(_("results exam"), max_length=2, choices=RESULTS, default='NR')
    result_practice = models.CharField(_("results practice"), max_length=2, choices=RESULTS, default='NR')
    points  = models.PositiveIntegerField(_("points"),null=True, blank=True)
    paidfor = models.CharField(_("paid for"),max_length=2, choices=(('Y', 'Yes'), ('N', 'No')), default='Y')
    valid = models.CharField(_("valid"),max_length=2, choices=(('Y', 'Yes'), ('N', 'No')), default='Y')

    def __unicode__(self):
        return force_unicode(str(self.examDate) + ' ' + str(self.enroll) + ' (' + str(self.result_exam) + ')')
    
    class Meta:
        verbose_name_plural = _("exam signups")
        verbose_name = _("exam signup")
        

class Module(models.Model):
    module_code = models.CharField(_("module code"), max_length=6, primary_key=True, unique=True)
    descriptor = models.CharField(_("module name"), max_length=255)
    

    def __unicode__(self):
        return self.descriptor

    class Meta:
        verbose_name = _("module")
        verbose_name_plural = _("modules")
    



class Curriculum(models.Model):
    course = models.ForeignKey("codelist.Course")
    program = models.ForeignKey("codelist.StudyProgram")
    class_year  = models.PositiveIntegerField(_("class year"),null =True, blank=True)
    mandatory = models.BooleanField(_("mandatory"))
    valid = models.BooleanField(_("valid"),default=True)
    module = models.ForeignKey("Module", null=True, blank=True)
    only_exam   = models.BooleanField()

    @staticmethod
    def getNonMandatory(program, year):
        return Curriculum.objects.filter(program=program, class_year = year, mandatory = 0)



    def __unicode__(self):
        return u'%s   ( obvezni: %s)' % (  self.course, 'DA' if self.mandatory else 'NE')
        #return u'%s %s (letnik:%d,  obvezni:%s, aktiven:%s)' % (self.course, self.program, self.class_year,  'DA' if self.mandatory else 'NE', 'DA' if self.valid else 'NE')

    class Meta:
        verbose_name = _("curriculum course")
        verbose_name_plural = _("curriculum")
        ordering = ['program']


#class StudentsGroup(models.Model):
#    name = models.CharField(_("student group name"), max_length=255)
#    student = models.ManyToManyField("Student", null=True, blank=True)
#    canSignUp= models.BooleanField(default=True)
#
#    def __unicode__(self):
#        return str(self.name)
#
#    class Meta:
#        verbose_name = _("students group")
#        verbose_name_plural = _("students groups")

