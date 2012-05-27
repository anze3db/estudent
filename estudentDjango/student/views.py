# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import context
from django.template.context import RequestContext
from student.models import ExamSignUp, ExamDate


class ExamGrades(object):
    model = ExamSignUp
    i=1



#http://stackoverflow.com/questions/4148923/is-it-possible-to-create-a-custom-admin-view-without-a-model-behind-it
def exam_grades_view(request): #show list of all objects
    examDateId = int(request.GET['examId'])
    exam=ExamDate.objects.get(id=examDateId);

    prijave = ExamSignUp.objects.filter(examDate=exam)


    result = []
    for p in prijave:
        prijava = {}
        prijava['priimek'] = p.enroll.student.surname
        prijava['ime'] = p.enroll.student.name
        prijava['leto'] = str(p.enroll.study_year) + "/" + str(p.enroll.study_year + 1)
        prijava['vpisna_st'] = p.enroll.student.enrollment_number
        result = result + [prijava]


    return render_to_response('admin/student/exam_grades.html', {'izpitnirok': exam, 'prijave':result}, RequestContext(request))
