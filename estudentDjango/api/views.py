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
    #response={'course_name':"",'course_code':""}

    student = Student.objects.get(enrollment_number=enrollment_id)
    #enrollment = Enrollment.objects.get(student=student)
    courses = []
    for i in  student.get_all_classes():
        courses=courses+[i]

    print courses
    response = serializers.serialize("json",  courses, relations=('program',))


    return HttpResponse(response,mimetype="application/json")


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
