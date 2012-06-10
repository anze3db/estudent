from django.db import models
from django.utils.encoding import smart_unicode, force_unicode
from django.utils.translation import ugettext as _
from settings import PROJECT_PATH
from urllib import urlopen, urlencode
from django.db.transaction import commit_on_success # pohitri insert
from django.core.validators import RegexValidator 
#from student.models import ExamSignUp, Enrollment, ExamDate, Student
from django.contrib.auth.models import User
import re 
import os
import datetime


class Course(models.Model):
    num_regex = re.compile(r'^[0-9]{5}$') 
    course_code = models.CharField(_("course code"), max_length=5, primary_key=True, unique=True, validators=[RegexValidator(regex=num_regex)])
    name = models.CharField(_("course name"), max_length=255)
   # instructors = models.ManyToManyField("Instructor", related_name=("instructors"), verbose_name = _("instructors"))
    instructors   = models.ManyToManyField("GroupInstructors", null=True, blank=True)
   # def instructors_str(self): return ','.join(map(unicode, self.instructors.all()))
    # CT_JOINED = ('S', 'Skupni') # vec predavateljev istim studentom, kdorkoli razpise rok
    #CT_SPLIT = ('R', 'Razdeljeni') # studentje se razdelijo med predavatelje, vsak zase razpise rok
    #course_type = models.CharField(_("course type"), max_length=255, choices=(CT_JOINED, CT_SPLIT))
    valid = models.BooleanField(_("valid"), default=True)

    # tuki je se treba nekam dodat za kater letnik je to... pa se v enrollment
   # compulsoryfor = models.ManyToManyField("StudyProgram", related_name=("compulsoryfor"), blank=True)
   # selectivefor = models.ManyToManyField("StudyProgram", related_name=("selectivefor"), blank=True)
    program     = models.ManyToManyField("StudyProgram", through='student.Curriculum', blank= True)

    #bug v lokalizaciji - mora imeti tako ime
    def predavatelji(self):
        return ' / '.join([str(i) for i in self.instructors.all()])

    def __unicode__(self):
        return self.course_code + " " +  self.name
    
    @classmethod
    @commit_on_success
    def updateAll(cls):
        FILE = os.path.join(PROJECT_PATH, 'predmeti.csv')
        
        csv_file = open(FILE)
        csv_data = csv_file.readlines()
        csv_file.close()
        
        Course.objects.all().delete()
        GroupInstructors.objects.all().delete()
        for line in csv_data:
            if line == "" : continue
            l = line.split(';')
            if l[1][0] == "#": continue
            i = int(l[0])
            c = Course()
            c.course_code = i
            c.save()
            for ll in l[2:]:
                if ll.strip() == "": continue
                
                profsesorji = [(prof.split(",")[1].strip().capitalize(),prof.split(",")[0].strip().capitalize())for prof in ll.strip().split("/")]
                groups = GroupInstructors.objects.all()
                for prof in profsesorji:
                    instructor = Instructor.objects.filter(name=prof[0], surname=prof[1])[0]
                    groups = [g for g in groups if instructor in g.instructor.all()]
                
                if len(groups)==0:
                    g = GroupInstructors()
                    g.save()
                    for prof in profsesorji:
                        try:
                            instructor = Instructor.objects.filter(name=prof[0], surname=prof[1])[0]
                            if instructor != None: g.instructor.add(instructor)
                        except:
                            print "instruktor not found"
                    g.save()
                else:
                    g = groups[0]
                if len(g.instructor.all())>0: c.instructors.add(g)
                    
            c.course_code = i
            c.name = l[1].strip()
            c.save()

    def repeat_class(self, student, retrn=0):
        from student.models import ExamSignUp
        all_signUps = list(ExamSignUp.objects.filter(enroll__student=student, examDate__course=self))
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


    def nr_attempts_this_year(self, student):
        from student.models import ExamSignUp


        year=datetime.date.today().year
#        month_today=datetime.date.today().month
#        begin=datetime.date(year-1, 10, 1)
#        end=datetime.date(year, 9, 31)
#        if 10<=month_today<=12:
#            begin=datetime.date(year, 10, 1)
#            end=datetime.date(year+1,9, 31)

        exSig= ExamSignUp.objects.filter(enroll__student=student, VP=False, examDate__course=self)
        nr_try=0
        y=0

        for t in exSig:
            if t.examDate.date.year==year:
                nr_try=nr_try+1
                y=t.examDate.date.year


        return nr_try

    def nr_attempts_this_year_till_now(self, student,nowdate):
        from student.models import ExamSignUp

        year=datetime.date.today().year
        exSig= ExamSignUp.objects.filter(enroll__student=student, VP=False, examDate__course=self)
        nr_try=0

        for t in exSig:
            if t.examDate.date.year==year and t.examDate.date<nowdate:
                nr_try=nr_try+1


        return nr_try

    def nr_attempts_all(self, student):
        from student.models import ExamSignUp
        all_signUps = list(ExamSignUp.objects.filter(enroll__student=student, examDate__course=self))
        i=0
        for a in all_signUps:
            if a.VP==False:
                i=i+1

        return i

    def nr_attempts_all_till_now(self, student,nowdate):
        from student.models import ExamSignUp
        all_signUps = list(ExamSignUp.objects.filter(enroll__student=student, examDate__course=self))
        print all_signUps
        print "\n\n"
        i=0
        for a in all_signUps:
            if a.VP==False and a.examDate.date < nowdate:
                i=i+1
        return i    

    def nr_attempts_this_enroll(self, enroll):
        from student.models import ExamSignUp
        all_signUps = list(ExamSignUp.objects.filter(enroll=enroll, examDate__course=self))
        i=0
        for a in all_signUps:
            if a.VP==False:
                i=i+1
        return i


    def already_signedUp(self, student):
        from student.models import ExamSignUp
        all=list(ExamSignUp.objects.filter(enroll__student=student, examDate__course=self))

        if(len(all))>0:
            return True
        else:
            return False


    #TODO fix this
    def results(self, student):
        
        # enroll = Enrollment.objects.filter(student=student)        
        attempts = student.ExamSignUp.objects.filter(enroll__student__enrollment_number=student.enrollment_number).filter(examDate__course__course_code=self.course_code).order_by("examDate")
        result = []
        for a in attempts:
            if not a.result == None:
                
                res = str(a.result)
            result = result + [{ 'result': res}]
            
        return result

    @staticmethod
    def getAllInstructors(course_code):
        return Course.objects.filter(course_code=course_code)
                    
    class Meta:
        verbose_name_plural =_("courses")
        verbose_name=_("course")

# Create your models here.
class Country(models.Model):
    category_code = models.CharField(_("country code"), max_length=3,  primary_key=True, unique=True)
    descriptor = models.CharField(_("country name"), max_length=255)
    descriptor_english = models.CharField(_("country name original"), max_length=255)
    valid = models.BooleanField(_("valid"), default=True)
    
    class Meta:
        verbose_name_plural = _("countries")
        verbose_name = _("country")
        
    def __unicode__(self):
        return self.descriptor
    
    @classmethod
    @commit_on_success
    def updateAll(cls):
        UPDATE_URL = 'http://www.stat.si/klasje/tabela.aspx?CVN=3888'
        
        csv_data = urlopen(UPDATE_URL, data=urlencode(
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
            c.category_code = l[1].strip()
            c.descriptor = smart_unicode(l[2].strip(), encoding='windows-1250', strings_only=False, errors='strict')
            c.descriptor_english = l[3].strip()
            c.valid = True
            c.save()
            
class StudyProgram(models.Model):
    program_code = models.CharField(_("program code"), max_length=5, primary_key=True, unique=True)
    descriptor = models.CharField(_("program name"), max_length=255)
    valid = models.BooleanField(_("valid"), default=True)
        
    class Meta:
        verbose_name_plural = _("study programs")
        verbose_name = _("study program")
        
    def __unicode__(self):
        return force_unicode(self.program_code + " " + self.descriptor)
    
    @classmethod
    def updateAll(cls):
        UPDATE_FILE = os.path.join(PROJECT_PATH, 'programSmerIzbirnaSkupina.txt')
        
        csv_file = open(UPDATE_FILE)
        csv_data = csv_file.readlines()
        csv_file.close()
        
        # remove all the data from the table:
        StudyProgram.objects.all().delete();
        
        for line in csv_data:
            l = line.split('\t')
            c = StudyProgram()
            c.program_code = l[0].strip()
            c.descriptor = smart_unicode(l[1].strip(), encoding='windows-1250', strings_only=False, errors='strict')
            c.save()
            
class Post(models.Model):
    post_code = models.CharField(_("post code"), max_length=5, primary_key=True, unique=True)
    descriptor = models.CharField(_("post name"), max_length=255)
    valid = models.BooleanField(_("valid"), default=True)
    
    class Meta:
        verbose_name_plural = _("posts")
        verbose_name = _("post")
        
    def __unicode__(self):
        return self.post_code + " " + self.descriptor
    
    @classmethod
    @commit_on_success    
    def updateAll(cls):
        UPDATE_FILE = os.path.join(PROJECT_PATH, 'poste.txt')
        
        csv_file = open(UPDATE_FILE)
        csv_data = csv_file.readlines()
        csv_file.close()
        
        # remove all the data from the table:
        Post.objects.all().delete();
        
        for line in csv_data:
            l = line.split('\t')
            c = Post()
            c.post_code = l[0].strip()
            c.descriptor = l[1].strip()
            c.save()
            
class Region(models.Model):
    region_code = models.CharField(_("region code"), max_length=3, primary_key=True, unique=True)
    descriptor = models.CharField(_("region name"), max_length=255)
    valid = models.BooleanField(_("valid"), default=True)

    class Meta:
        verbose_name_plural = _("regions")
        verbose_name= _("region")
        
    def __unicode__(self):
        return self.descriptor
    
    @classmethod
    @commit_on_success    
    def updateAll(cls):
        UPDATE_FILE = os.path.join(PROJECT_PATH, 'obcine.txt')
        
        csv_file = open(UPDATE_FILE)
        csv_data = csv_file.readlines()
        csv_file.close()
        
        Region.objects.all().delete()
        
        for line in csv_data:
            l = line.split('\t')
            c = Region()
            c.region_code = l[0].strip()
            c.descriptor = l[1].strip()
            c.save()    

class Faculty(models.Model):
    faculty_code =  models.CharField(_("faculty code"), max_length=3, primary_key=True, unique=True)
    descriptor = models.CharField(_("faculty name"), max_length=255)
    valid = models.BooleanField(_("valid"), default=True)
    
    class Meta:
        verbose_name_plural = _("faculties")
        verbose_name= _("faculty")
        
    def __unicode__(self):
        return self.descriptor
    
    @classmethod
    def updateAll(cls):
        Faculty.objects.all().delete()                
        c = Faculty()
        c.faculty_code = "163"
        c.descriptor = "FRI"
        c.save()
            
class Instructor(models.Model):
    num_regex = re.compile(r'^63[0-9]{4}$') 
    instructor_code = models.CharField(_("instructor code"), max_length=6, primary_key=True, unique=True, validators=[RegexValidator(regex=num_regex)])
    name = models.CharField(_("name"), max_length=255)
    surname = models.CharField(_("surname"), max_length=255)
    valid = models.BooleanField(_("valid"), default=True)
  #  courses = models.ManyToManyField("Course", related_name=("courses"), verbose_name = _("courses"), blank=True)
    user = models.OneToOneField(User, null=True)
    
    def __unicode__(self):
        return self.name + ' ' + self.surname +" (" + self.instructor_code + ")"

    @classmethod
    @commit_on_success
    def updateAll(cls):
        FILE = os.path.join(PROJECT_PATH, 'profesorji.txt')
        
        csv_file = open(FILE)
        csv_data = csv_file.readlines()
        csv_file.close()
        
        Instructor.objects.all().delete()
        i=10000
        for line in csv_data:
            if line == "" : continue
            l = line.split(',')
            if len(l)<2: continue
            c = Instructor()
            c.instructor_code = "i"+str(i)
            c.name = l[1].strip().capitalize()
            c.surname = l[0].strip().capitalize()
            c.save()
            i=i+1

    class Meta:
        verbose_name_plural =_("instructors")
        verbose_name=_("instructor")


class GroupInstructors(models.Model):
    instructor = models.ManyToManyField("Instructor", null=True, blank=True)
    def __unicode__(self):
        return force_unicode(', '.join([i.surname for i in self.instructor.all()]))
    def get1st(self):
        instructor = self.instructor.all()
        return instructor[0].surname if len(instructor) >= 1 else ''
    def get2nd(self):
        instructor = self.instructor.all()
        return instructor[1].surname if len(instructor) >= 2 else ''
    def get3rd(self):
        instructor = self.instructor.all()
        return instructor[2].surname if len(instructor) >= 3 else ''
    def get_first(self):
        return self.objects.get(id=1)

    def generateName(self):
        return force_unicode(', '.join([i.surname for i in self.instructor.all()]))

    @staticmethod
    def getAllInstr(course_code):
        return GroupInstructors.objects.filter(course__course_code=course_code)

    class Meta:
        verbose_name_plural = _("groups of instructors")
        verbose_name=_("group of instructors")

