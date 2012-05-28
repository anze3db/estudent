# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import context, loader
from django.template.context import RequestContext, Context
from student.models import ExamSignUp, ExamDate


def exam_grades_index(request):

    exam_dates=ExamDate.objects.all().order_by('date')
    output = list(exam_dates)
    #latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    #output = ', '.join([p.question for p in latest_poll_list])
    t = loader.get_template('admin/student/exam_grades_index.html')
    c = Context({
        'izpitni_roki': exam_dates,
        })

    return HttpResponse(t.render(c))


    #return render_to_response('admin/student/exam_grades_index.html', {}, RequestContext(request))




#http://stackoverflow.com/questions/4148923/is-it-possible-to-create-a-custom-admin-view-without-a-model-behind-it
def exam_grades_view(request, exam_Id): #show list of all objects

    examDateId = int(exam_Id)
    exam=ExamDate.objects.get(id=examDateId);

    prijave = ExamSignUp.objects.filter(examDate=exam)


    result = []
    for p in prijave:
        prijava = {}
        prijava['priimek'] = p.enroll.student.surname
        prijava['ime'] = p.enroll.student.name
        prijava['leto'] = str(p.enroll.study_year) + "/" + str(p.enroll.study_year + 1)
        prijava['vpisna_st'] = p.enroll.student.enrollment_number
        prijava['opcije']= p.RESULTS
        prijava['tocke']=p.points
        prijava['ocena_izpita'] = p.result_exam
        prijava['ocena_vaj']=p.result_practice




        result = result + [prijava]


    return render_to_response('admin/student/exam_grades.html', {'izpitnirok': exam, 'prijave':result}, RequestContext(request))
