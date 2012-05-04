# Create your views here.
from django.http import HttpResponse
from failedloginblocker.models import FailedAttempt
from student.models import Student, Enrollment
from codelist.models import  StudyProgram
import json

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
    response={'student_name':"",'courses':"", "nekikarje":"zbrisi"}       
    
    student = Student.authStudent(student_id, request.GET['password'])       
    response["student_name"] = student.name
    
    
    
    enroll = Enrollment.objects.filter(student=student).order_by('program', 'study_year', 'class_year')
    for v in enroll:
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
    
    
    
    