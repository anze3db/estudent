# Create your views here.
from django.http import HttpResponse
from django.core import serializers
from failedloginblocker.models import FailedAttempt
from student.models import Student, Enrollment, ExamDate, ExamSignUp, Curriculum
from codelist.models import  StudyProgram, Course, GroupInstructors
from student.models import *
import json
import codelist

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
    response={'student_name':"",'study_program':"",'courses':""}       
    
    student = Student.authStudent(student_id, request.GET['password'])       
    response["student_name"] = student.name
    
    
    
    enroll = Enrollment.objects.filter(student=student).order_by('program', 'study_year', 'class_year')
    for v in enroll:
        response["study_program"]=v.program.descriptor
        courses = []
        
        for p in v.courses.order_by('course_code'):
            course={}
            course["name"]=p.name
            ocene = p.results(student)
            
            for o in ocene:
                course['result'] = o['result']
            courses = courses+[course]
        response["courses"]=courses
        
 
    
    return HttpResponse(json.dumps(response),mimetype="application/json")


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


        return HttpResponse(serializers.serialize("json", courses))
        #return HttpResponse(courses,mimetype="application/json")

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


def examSignUp(request):
    student = request.GET['id']
    course = request.GET['courseId']

    response = {''}

    return HttpResponse(response,mimetype="application/json")

def getFilteredCoursesModules(request):
    program = request.GET['program'] if 'program' in request.GET else ''
    year = request.GET['year'] if 'year' in request.GET else ''
    
    if program == '' or year == '':
        return HttpResponse(serializers.serialize("json", []))
    
    currs = Curriculum.getNonMandatory(program, year)
    return HttpResponse(serializers.serialize("json", currs))

def getFilteredGroupInstructorsForCourses(request):
    courseID = request.GET['courseId']

    course=Course.objects.get(course_code=courseID)
    instr=Course.getAllInstructors(courseID)
    ins= GroupInstructors.getAllInstr(courseID)


    return HttpResponse(serializers.serialize("json", ins))



def getAllExamDates(request):
    enrollment_id = request.GET['id']


    student = Student.objects.get(enrollment_number=enrollment_id)
    enroll = Enrollment.objects.filter(student = student)


    exams=student.get_current_exam_dates()

    return HttpResponse(serializers.serialize("json", exams))
    #return HttpResponse(exams,mimetype="application/json")




def test(request):
    enrollment_id = request.GET['id']
    student = Student.objects.get(enrollment_number=enrollment_id)
    exam=ExamDate.objects.get(id=2);

    #test=exam.already_signedUp(student)
    test=exam.signUp_allowed(student)


    return HttpResponse(test,mimetype="application/json")


def addSignUp(request):

    examDateId = int(request.GET['examId'])
    enrollment_id = request.GET['id']
    student = Student.objects.get(enrollment_number=enrollment_id)

    exam=ExamDate.objects.get(id=examDateId);

    error_msgs = exam.signUp_allowed(student)
    if error_msgs != None: return HttpResponse('{"error": "' + error_msgs[0] + '"}')

    if exam.already_signedUp(student):return HttpResponse('{"error": "Na ta predmet ste ze prijavljeni, ali se ni bila vnesena ocena"}')
    if exam.already_positive(student):return  HttpResponse('{"error": "Za ta predmet ze obstaja pozitivna ocena"}')

    enroll = list(Enrollment.objects.filter(student=student))[-1]
    ExamSignUp.objects.create(enroll=enroll, examDate=exam).save()

    return HttpResponse('Uspesna prijava na izpit'+ str(exam),mimetype="application/json")