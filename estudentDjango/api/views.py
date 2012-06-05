# Create your views here.
from __future__ import division
from datetime import timedelta
from django.http import HttpResponse
from django.core import serializers
from django.template.context import RequestContext
from failedloginblocker.models import FailedAttempt
from student.models import Student, Enrollment, ExamDate, ExamSignUp, Curriculum
from codelist.models import  StudyProgram, Course, GroupInstructors
from django.shortcuts import get_object_or_404, render_to_response
from student.models import *
import json
import codelist
from django.db.models import Q

def login(request):
    user = request.GET['id']
    response = {'name': "", 'surname':"", 'login': False, 'numTries':0, 'errors':""}
    fa = None
    try:
        fa = FailedAttempt.objects.order_by('-timestamp').filter(username=user)[0]
        if fa.recent_failure():
            if fa.too_many_failures():
                fa.failures += 1
                fa.save()
                response['numTries'] = fa.failures
                response['errors'] = "Too many login attempts."
                return HttpResponse(json.dumps(response), mimetype="application/json")
    except:
        fa = None
    print fa
    auth = Student.authStudent(user, request.GET['password'])
    
    if auth:
        response["name"] = auth.name
        response["surname"] = auth.surname
        response["login"] = True
    else:
        if fa is None or not fa.recent_failure() :
            fa = FailedAttempt(username=user, failures=0)
        fa.failures += 1
        fa.save()
        response['numTries'] = fa.failures
        response['errors'] = "Wrong username or password."
                
    return HttpResponse(json.dumps(response), mimetype="application/json")

def index(request):
    student_id = request.GET['id']
    student = get_object_or_404(Student, enrollment_number=student_id)
    response = []
    
    enrolls = Enrollment.objects.filter(student=student).order_by('program', 'study_year', 'class_year')
    
    prog = ""
    for enroll in enrolls:
        out={}
        out['program'] = enroll.program.descriptor
        out['enrollment_type']=enroll.enrol_type+' - '+enroll.get_enrol_type_display()
        out['redni']=enroll.regular
        out['letnik']= enroll.class_year
        out['study_year'] = enroll.study_year


        
        courses = []
        classes = enroll.get_classes()
        courses2=Course.objects.filter(curriculum__in=classes)
        #courses2 = Course.objects.filter(curriculum__in=classes).order_by('course_code')
        
        for p in courses2:
            try:
                course={}
                course["name"]=p.name
                course["sifra_predmeta"]=p.course_code
                course["predavatelj"]=p.predavatelji()
                signups = ExamSignUp.objects.filter(examDate__course__course_code=p.course_code).order_by('examDate__date')

                eno_pol=[]
                for s in signups:
                    if (s.result_exam == "NR" or s.VP == True):
                        continue
                    polaganje={}
                    polaganje['datum']=s.examDate.date.strftime("%d.%m.%Y")
                    polaganje['izvajalci']=force_unicode(s.examDate.instructors)
                    #if s.examDate.course.
                    cur=Curriculum.objects.get(course=p, program=enroll.program)
                    if(cur.only_exam==True):
                        polaganje['ocena']=s.result_exam
                    else:
                        polaganje['ocena']=str(s.result_exam)+"/"+ str((s.result_practice if s.result_exam > 5 else 0))
                    polaganje['stevilo_polaganj']=s.examDate.course.nr_attempts_all(student)
                    if s.examDate.repeat_class(student,0)>0:
                        polaganje['odstevek_ponavljanja']=s.examDate.course.nr_attempts_all(student)-s.examDate.repeat_class(student,0)
                    else:
                        polaganje['odstevek_ponavljanja']=0
                    polaganje['polaganja_letos']=s.examDate.course.nr_attempts_this_year(student)
                    #polaganje['stevilo_polaganj']
                    eno_pol.append(polaganje)

                course["polaganja"]=eno_pol
                courses = courses+[course]
            except:
                raise
        out["courses"]=courses
        out['povprecje_izpitov']=enroll.get_exam_avg()
        out['povprecje_vaj']=enroll.get_practice_avg()
        out['povprecje']=enroll.get_avg()

        response.append(out)


    return HttpResponse(json.dumps({"index":response}),mimetype="application/json")


def getStudentEnrollments(request):
    student_id = request.GET['student_id']

    response=[]


    for e in  Enrollment.objects.filter(student__enrollment_number=student_id):
        enroll={}
        enroll['key']=e.pk
        enroll['study_program']=e.program.descriptor
        enroll['study_year']=e.study_year
        enroll['class_year']=e.class_year
        print enroll
        response.append(enroll)


    return HttpResponse(json.dumps({"enrollments":response}),mimetype="application/json")


def getCoursesforEnrollment(request):
    enrollment_id = request.GET['id']
    #response={'course_name':"",'course_code':""}

    student = Student.objects.get(enrollment_number=enrollment_id)
    enrollment = Enrollment.objects.get(student=student)
    courses = []
    for i in  enrollment.get_courses():
        courses=courses+[i]


   # response = serializers.serialize("json",  courses, relations=('program',))


    return HttpResponse(courses,mimetype="application/json")

def getAllCourses(request):
    enrollment_id = request.GET['id']

    try:
        student = Student.objects.get(enrollment_number=enrollment_id)
        courses=student.get_all_classes()


        #return HttpResponse(serializers.serialize("json", courses))
        return HttpResponse(courses,mimetype="application/json")

    except:

        return HttpResponse('error: try /?id=[enrollmentNr]')



def examDates(request):
    enrollment_id = request.GET['enrollment_id']


    enrollment = Enrollment.objects.get(id = enrollment_id)
    es = ExamSignUp.objects.filter(enroll = enrollment)

    response = serializers.serialize("json", es, relations=('program',));


    return HttpResponse(response,mimetype="application/json")


def enrolemntList(request):
    student_id = request.GET['id']
    
    student = Student.objects.get(enrollment_number = student_id)
    
    enrolemtns = Enrollment.objects.filter(student = student)
    response = serializers.serialize("json", enrolemtns, relations=('program',));

        
    
    return HttpResponse(response,mimetype="application/json")


def getFilteredCoursesModules(request):
    program = request.GET['program'] if 'program' in request.GET else ''
    year = request.GET['year'] if 'year' in request.GET else ''
    modules = request.GET['modules'].split(',')
    student = request.GET['student']
    id = request.GET['id']
    
    enrollments = Enrollment.objects.filter(student = student).exclude(pk=id)
    for e in enrollments:
        pass
        #print Curriculum.getNonMandatory(e.program, e.class_year)
        #print e.courses
        #
        #print e.modules
    
    if program == '' or year == '':
        return HttpResponse(serializers.serialize("json", []))

    
    
    currs = Curriculum.getNonMandatory(program, year)
    module_courses = Curriculum.objects.filter(module__in = modules)
    # filtriramo vse predmete, ki so v izbranih coursih:
    currs = [c for c in currs if c not in module_courses]
    
    return HttpResponse(serializers.serialize("json", currs))

def getFilteredGroupInstructorsForCourses(request):
    courseID = request.GET['courseId']

    course=Course.objects.get(course_code=courseID)
    instr=Course.getAllInstructors(courseID)
    ins= GroupInstructors.getAllInstr(courseID)


    return HttpResponse(serializers.serialize("json", ins))

def getFilteredCourses(request):
    programId = request.GET['programId']

    courses = Curriculum.objects.filter(program = programId, mandatory = False)
    print courses
    return HttpResponse(serializers.serialize("json", courses))



def getAllExamDates(request):
    enrollment_id = request.GET['id']


    student = Student.objects.get(enrollment_number=enrollment_id)
    enroll = Enrollment.objects.filter(student = student)


    exams=student.get_current_exam_dates()

    return HttpResponse(serializers.serialize("json", exams))
    #return HttpResponse(exams,mimetype="application/json")




def test(request):
    """

    """
    enrollment_id = request.GET['id']
    student = Student.objects.get(enrollment_number=enrollment_id)
    #enroll = Enrollment.objects.get(pk=enrollment_id)
    #student=enroll.student
    #courses=student.get_all_classes()
    #
    # classes=Course.objects.filter(curriculum__in=courses)





    exam=ExamDate.objects.get(id=25);
    d = timedelta(days=14)

    last=exam.last_try(student)
    e=ExamDate.objects.get(examsignup=last)
    t= exam.date > (e.date + d)

    #return HttpResponse(serializers.serialize("json", student)
    return HttpResponse(exam.date,mimetype="application/json")


def addSignUp(request):
    message = {"msg":"","error":""}
    
    examDateId = int(request.GET['exam_id'])
    student_id = request.GET['student_id']
    enroll_id = request.GET['enroll_id']
    student = Student.objects.get(enrollment_number=student_id)

    exam=ExamDate.objects.get(id=examDateId);
    error_msgs = exam.signUp_allowed(student)
    nr_this=exam.course.nr_attempts_this_year(student)
    nr_all= exam.course.nr_attempts_all(student)
    d = datetime.timedelta(days=14)

    if error_msgs != None: 
        message["error"]= error_msgs[0]
    elif exam.already_positive(student):
        message["error"]='Za ta predmet ze obstaja pozitivna ocena'
    elif nr_this>=3:
        message["error"]='Ta predmet ste letos opravljali ze 3x. Prijava ni vec mogoca'
    elif nr_all>=6:
        message["error"]='Ta predmet ste  opravljali ze 6x. Prijava ni vec mogoca'
    elif exam.already_signedUp(student):
        message["error"]='Na ta predmet ste ze prijavljeni in se ni bila vnesena ocena'
    elif exam.date < (datetime.date.today()+ datetime.timedelta(days=3)):
        message["error"]='Rok za prijavo na izpit je potekel'
    elif exam.date < (ExamDate.objects.get(examsignup=exam.last_try(student)).date+d):
        message["error"]='Ni se preteklo 14 dni od zadnje prijave'

    else:
        enroll = Enrollment.objects.get(pk=enroll_id)
        ExamSignUp.objects.create(enroll=enroll, examDate=exam).save()
        message["msg"]='Uspesna prijava na izpit'+ str(exam)

    return HttpResponse(json.dumps(message),mimetype="application/json")



def removeSignUp(request):
    message = {"msg":"","error":""}
    
    examDateId = int(request.GET['exam_id'])
    student_id = request.GET['student_id']
    student = Student.objects.get(enrollment_number=student_id)

    exam=ExamDate.objects.get(id=examDateId);
    error_msgs = exam.signUp_allowed(student)
    
    if error_msgs != None: 
        message["error"]= error_msgs[0]
    elif not exam.already_signedUp(student):
        message["error"]='Na ta predmet niste prijavljeni'
    elif exam.already_positive(student):
        message["error"]='Za ta predmet ze obstaja pozitivna ocena'
    elif exam.date < (datetime.date.today()+ datetime.timedelta(days=3)):
        message["error"]='Rok za odjavo izpita je potekel'        
    else:
        enroll = list(Enrollment.objects.filter(student=student))[-1]
        examSignUp = ExamSignUp.objects.get(enroll=enroll, examDate=exam)
        examSignUp.delete()
        message["msg"]='Uspesna odjava od izpita'+ str(exam)

    return HttpResponse(json.dumps(message),mimetype="application/json")


def getEnrollmentExamDates(request):
    enrollment_id = request.GET['enroll_id']
        
    enroll = Enrollment.objects.get(pk=enrollment_id)
    classes=Course.objects.filter(curriculum__in=enroll.get_classes())
    student=enroll.student

    response=[]

    for e in ExamDate.objects.filter(course__in=classes):
        ex={}
        ex['exam_key']=e.pk
        ex['course_key']=e.course.course_code
        ex['course']=e.course.name
        ex['date']=str(e.date)
        ex['instructors']=str(e.instructors)
        ex['signedup']=e.already_thisExam(enroll.student)
        ex['all_attempts']=e.course.nr_attempts_all(student)
        ex['attempts_this_year']=e.course.nr_attempts_this_year(student)
        ex['attempts_this_enrollment']=e.course.nr_attempts_this_enroll(student)
        ex['enroll_type']=enroll.enrol_type
        ex['repeat_class_exams']=e.repeat_class(student)
        response.append(ex)

    return HttpResponse(json.dumps({"EnrollmentExamDates":response}),mimetype="application/json")



def getStudentEnrollmentsForYear(request):
    student_id = request.GET['student_id']
    year=request.GET['year']
    enroll = Enrollment.objects.filter(student__enrollment_number=student_id, study_year=year)
    return HttpResponse(serializers.serialize("json", enroll))
