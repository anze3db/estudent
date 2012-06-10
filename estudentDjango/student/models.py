from __future__ import division
from itertools import chain
from django.contrib.auth.models import get_hexdigest
from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator 
from django.utils.encoding import force_unicode
from codelist.models import *


import re
import string
from django.core.exceptions import ValidationError


ALGO = 'sha1'



class Student(models.Model):

    def generateEnrollment(): #@NoSelf
        """Generates a new enrollment number"""
        
        last = Student.objects.order_by('-enrollment_number')
        if last.count() > 0:
            return last.filter()[0].enrollment_number + 1   
        else:
            return 63110001
        
    def validate_name(value): #@NoSelf
        if re.search(r'[\d\s_]', value):
            raise ValidationError(u'Polje lahko vsebuje samo znake abecede.')
        if re.search(r'[^\w]', value, re.UNICODE) != None:
            raise ValidationError(u'Polje lahko vsebuje samo znake abecede.')

    num_regex = re.compile(r'^63[0-9]{6}$')    
    name_regex = re.compile("[^\W\d_]+", re.UNICODE)
    enrollment_number = models.IntegerField(_("enrollment number"), primary_key=True, unique=True, default=generateEnrollment, validators=[RegexValidator(regex=num_regex)])
    name = models.CharField(_(_("name")), max_length=255, validators=[validate_name])
    surname = models.CharField(_("surname"), max_length=255, validators=[validate_name])
    
    ss_regex = re.compile(r'^[0-3][0-9][0-1][0-9][0-9]{3}50[0-9]{4}$|^[0-3][0-9][0-1][0-9]0{9}$')
    social_security_number = models.CharField(_("social security number"), max_length=13, validators=[RegexValidator(regex=ss_regex)])
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
        enroll = Enrollment.objects.filter(student=self)
        for e in enroll:
            allClass.append(e.get_classes())

        return allClass

    def get_all_classes_clean(self):
        courses = self.get_all_classes()

        return Course.objects.filter(curriculum__in=courses)


    def get_current_exam_dates(self):
        courses = self.get_all_classes()
        classes=Course.objects.filter(curriculum__in=courses)

        return ExamDate.objects.filter(course__in=classes)


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

    def __unicode__(self):
        return u'%s, %s, %s' % (self.street, self.post, self.country)

class Phone(models.Model):
    
    
    TELEPHONE_TYPES = (
        ('H', _('home number')),
        ('W', _('work number')),
        ('M', _('mobile number')),
    )
    
    num_regex = re.compile(r'^[\d +\-()/]*$') 
    type = models.CharField(max_length = 1, choices = TELEPHONE_TYPES)
    number = models.CharField(max_length = 255, validators=[RegexValidator(regex=num_regex)])
    student = models.ForeignKey("Student", related_name=("student_phone"))

    def __unicode__(self):
        return self.number

class Enrollment(models.Model):
    
    def check_if_grade(self):
        pass
    
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
    regular       = models.BooleanField(_("regular"), default=True)
    
    def _id(self):
        return u'<a href="/student/enrollment/%s/">%s</a>' % (self.id, self.id,)
    def _vpisna(self):
        return self.student.enrollment_number
    def _ime(self):
        return self.student.name
    def _priimek(self):
        return self.student.surname
    
    
    def __unicode__(self):
        return u'%d %s %s %d (%d)' % (self.student.enrollment_number, self.student.name, self.student.surname, self.study_year, self.class_year)
    
    def format_year(self):
        return u'%d/%d' % (self.study_year, self.study_year+1)



    def get_classes(self):

        
        modules=Module.objects.filter(enrollment=self)
        allInProgram=Curriculum.objects.filter(program=self.program)
        selectiveCourse =  Course.objects.filter(enrollment=self)

        mandatory=allInProgram.filter(mandatory=1)
        mod = Curriculum.objects.filter(module__in=modules) #todo check if module is null
        select=Curriculum.objects.filter(course__in=selectiveCourse)

        result_list = list(chain(select,mandatory,mod))

        return result_list

    def get_exam_avg(self):
        avg=0
        i=0
        classes=self.get_classes()
        courses=Course.objects.filter(curriculum__in=classes)
        exams=ExamSignUp.objects.filter(enroll=self, examDate__course__in=courses)
        for e in exams:
            if e.is_positive():
                avg= avg+int(e.result_exam)
                i=i+1

        if i!=0:
            return float(avg/i)
        else:
            return avg

    def get_practice_avg(self):
        avg=0
        i=0
        classes=self.get_classes()
        courses=Course.objects.filter(curriculum__in=classes)
        exams=ExamSignUp.objects.filter(enroll=self, examDate__course__in=courses)
        for e in exams:
            if e.is_positive():
                avg= avg+int(e.result_practice)
                i=i+1

        if i!=0:
            return float(avg/i)
        else:
            return avg

    def get_avg(self):
        avg=0
        i=0
        classes=self.get_classes()
        courses=Course.objects.filter(curriculum__in=classes)
        exams=ExamSignUp.objects.filter(enroll=self, examDate__course__in=courses)
        for e in exams:
            if e.is_positive():
                avg= avg+int(e.result_practice)
                i=i+1
                avg= avg+int(e.result_exam)
                i=i+1

        if i!=0:
            return float(avg/i)
        else:
            return avg




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
    study_year = models.PositiveIntegerField(_("study year"),db_index=True, default=2011)
    location    = models.CharField(_("location"),max_length=7)
    date = models.DateField(_("date"))
    nr_SignUp   = models.PositiveIntegerField(_("nr of Sign up"))
    total_points = models.PositiveIntegerField(_("total points"))
    min_pos = models.PositiveIntegerField(_("minimal points"))
    students =models.ManyToManyField(Enrollment, through='ExamSignUp')


    
    def __unicode__(self):
        return force_unicode(self.date.strftime("%d.%m.%Y") + ' ' + str(self.course))

    class Meta:
        verbose_name_plural = _("exam dates")
        verbose_name = _("exam date")

    def year(self):
        self.date.year

    def repeat_class(self, student, retrn=0):
        all_signUps = list(ExamSignUp.objects.filter(enroll__student=student, examDate__course=self.course))
        all=len(all_signUps)
        rep=0

        for x in all_signUps:
            type=x.enroll.enrol_type
            if type == 'V2':
                rep=rep+1

        ost=all-rep
        if retrn == 0:
            return rep
        else:
            return (all, rep)

    def already_thisExam(self, student):
        flag=False

        for c in Course.objects.filter(course__examsignup__enroll__student=student):
            if(c==self.course):
                ex=ExamSignUp.objects.filter(enroll__student=student, examDate__course=c)
                for e in ex:
                    if e.examDate==self: flag=True
        return flag


    def already_signedUp(self, student):
        #if fals, Ok to signUp
        flag=False

        for c in Course.objects.filter(course__examsignup__enroll__student=student):
            if(c==self.course):
                flag=True
                ex=ExamSignUp.objects.filter(enroll__student=student, examDate__course=c)
                for e in ex:
                    if(e.result_exam=='NR'): flag=True
                    #elif (len(list(ExamSignUp.object.filter(examDate=self)))!=0): flag=True
                    elif (int(e.result_exam)<=5): flag=False
                for e in ex:
                    if e.examDate==self: flag=True

        return flag

    def already_positive(self, student):
        all=list(ExamSignUp.objects.filter(enroll__student=student, examDate__course=self.course))

        for a in all:
            if not a.VP and a.is_positive():
                return True
        return False

    def last_try(self, student):
        all=len(list(ExamSignUp.objects.filter(enroll__student=student, examDate__course=self.course).order_by('-examDate__date')))
        last=ExamSignUp.objects.filter(enroll__student=student, examDate__course=self.course).order_by('-examDate__date')
        if all>1:
            last=list(ExamSignUp.objects.filter(enroll__student=student, examDate__course=self.course).order_by('-examDate__date'))[0]

        return last

    def signUp_allowed(self, student):
        errors = []

        enroll=list(Enrollment.objects.filter(student=student))[-1]
        signUp_thisYear=ExamSignUp.objects.filter(enroll=enroll, examDate__course=self.course, VP=False)
        signUps=list(signUp_thisYear)


        #preveri to solsko leto
        if len(signUps)>3:
            errors.append("Presegli ste dovoljeno stevilo prijav v tem solskem letu (3)")
            return errors

        #preveri vse prijave
        all_signUps = list(ExamSignUp.objects.filter(enroll__student=student, examDate__course=self.course))
        max=6

        for x in all_signUps:
            type=x.enroll.enrol_type
            if type != 'V1' and type !='AB':
                max=max+3
            if x.VP: max=max+1

        if len(all_signUps)>6:
            errors.append("Presegli ste dovoljeno stevilo prijav  (6)")
            return errors



        if len(errors) != 0: return errors

        return None # no error


    #doesn't probably work: see student/admin.py ExamDate for something similar.
    def exam_on_date_exist(self):
        exams=ExamDate.objects.filter(course=self.course)
        for e in exams:
            if e.instructors==self.instructors & e.date==self.date:
                return True
            else:
                return False



    @classmethod
    @commit_on_success
    def updateAll(cls):
        from random import random
        from random import shuffle
        print "update cur"
        FILE = os.path.join(PROJECT_PATH, 'predmetnik.csv')
        
        csv_file = open(FILE)
        csv_data = csv_file.readlines()
        csv_file.close()
        dnevi = range(1,27)
        for line in csv_data:
            line = line.strip()
            try:
                l = re.compile(",", re.UNICODE).split(line)
                
                course = Course.objects.filter(name=l[4])[0]
                zimski = l[5] == "zimski"
                for instructorGroup in course.instructors.all():
                    for leto in range(2008,2013):
                        i=0
                        shuffle(dnevi)
                        steviloprijav = int(random()*3+1)*50
                        for mesec in [2 if zimski else 6 , 8, 9]:
                            i += 1
                            dan = dnevi[i]
                            datum = datetime.date(leto,mesec,dan)
    
                            ucilnica = "P"+str(int(random()*random()*20+1))
                            vsetTocke = 100
                            meja = 50 + (0 if random() < 0.5 else 10)
                            
                            ed = ExamDate()
                            ed.date = datum
                            ed.instructors = instructorGroup
                            ed.course = course
                            ed.location = ucilnica
                            ed.nr_SignUp = steviloprijav
                            ed.total_points = vsetTocke
                            ed.min_pos = meja
                            ed.save()
                            print datum, zimski,instructorGroup,course
                        
                        
            except BaseException as e:
                print e



class ExamSignUp(models.Model):
    enroll = models.ForeignKey('Enrollment')
    examDate = models.ForeignKey('ExamDate')
    VP = models.BooleanField(_("VP"), default=False)

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

    def is_positive(self):
        if self.result_exam=='NR':
            return False
        if int(self.result_exam)>5:
            return True
        else:
            return False


    #keeeel meeeee
    def student_index_view_examDate(self):
        return force_unicode(str(self.examDate.date.strftime("%d.%m.%Y")))
    def student_index_view_result(self):
        return force_unicode(str(self.result_exam)+"/"+str(self.result_practice));

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
        return u'%s   (%s)' % (self.course, 'Obvezni' if self.mandatory else 'Izbirni')
        #return u'%s %s (letnik:%d,  obvezni:%s, aktiven:%s)' % (self.course, self.program, self.class_year,  'DA' if self.mandatory else 'NE', 'DA' if self.valid else 'NE')

    class Meta:
        verbose_name = _("curriculum course")
        verbose_name_plural = _("curriculum")
        ordering = ['program']
        

    @classmethod
    @commit_on_success
    def updateAll(cls):
        print "update cur"
        FILE = os.path.join(PROJECT_PATH, 'predmetnik.csv')
        
        csv_file = open(FILE)
        csv_data = csv_file.readlines()
        csv_file.close()
        
        Curriculum.objects.all().delete()
        Module.objects.all().delete()
        i=10000
        for line in csv_data:
            i += 1
            line = line.strip()
            try:
                l = re.compile(",", re.UNICODE).split(line)
                program = StudyProgram.objects.get(program_code=l[0])
                letnik = int(l[1])
                mandatory = l[2] == "obvezni"
                valid = True
                if l[3] != "":
                    modules = Module.objects.filter(descriptor=l[3])
                    if len(modules)==0:
                        module = Module()
                        module.module_code = "m"+str(i)
                        module.descriptor = l[3]
                        module.save()
                    else:
                        module = modules[0]
                
                course = Course.objects.filter(name=l[4])[0]
                
                c = Curriculum()
                c.class_year = letnik
                c.course = course
                if not mandatory and l[3] != "":
                    c.module = module
                c.mandatory = mandatory
                c.valid = valid
                c.program = program
                c.save()
                 
                
            except BaseException as e:
                print e






