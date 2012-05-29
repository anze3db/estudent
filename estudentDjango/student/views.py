# Create your views here.
from codelist.models import Course, StudyProgram
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import context, loader
from django.template.context import RequestContext, Context
from student.models import ExamSignUp, ExamDate, Enrollment, Student


def exam_grades_index(request):

    exam_dates=ExamDate.objects.all().order_by('date')
    return render_to_response('admin/student/exam_grades_index.html', {'izpitni_roki': exam_dates,}, RequestContext(request))

#http://stackoverflow.com/questions/4148923/is-it-possible-to-create-a-custom-admin-view-without-a-model-behind-it
def exam_grades_view(request, exam_Id): #show list of all objects

    examDateId = int(exam_Id)
    exam=ExamDate.objects.get(id=examDateId)

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

def class_list(request):
    
    class ClassForm(forms.Form):
        
        choices = []
        for c in Course.objects.all():
            choices.append((c.pk, c.__unicode__()))
        
        programs = []
        for p in StudyProgram.objects.all():
            programs.append((p.pk, p.__unicode__()))
        
        prog = forms.ChoiceField(choices=programs)
        cour = forms.ChoiceField(choices=choices)
        year = forms.MultipleChoiceField(choices=[(2012, 2012), (2011, 2011), (2010, 2010)])
        
        
    students = []
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if 'year' in request.POST:
            students = Enrollment.objects.filter(study_year__in = request.POST.getlist('year'), courses = request.POST['courses'])
            
        
    else:
        form = ClassForm()
        
    return render_to_response('admin/student/class_list.html', {'form':form, 'students': students}, RequestContext(request))


def exam_sign_up_index(request):
    try:
        student_Id=request.POST['vpisna']
        if student_Id.isdigit():
            student = Student.objects.get(enrollment_number=student_Id)

            if 'prijava' in request.POST:
                return HttpResponseRedirect(reverse('student.views.exam_sign_up', args=[student.enrollment_number]))
            elif 'odjava' in request.POST:
                return HttpResponseRedirect(reverse('student.views.exam_sign_out', args=[student.enrollment_number]))
            elif Student.DoesNotExist:
                return HttpResponseRedirect(reverse('student.views.exam_sign_out', args=[student.enrollment_number]))

        else:
            return render_to_response('admin/student/exam_sign_up_index.html', {
                'error_message': "Student with this number does not exist",
                }, context_instance=RequestContext(request))


    except:
        return render_to_response('admin/student/exam_sign_up_index.html', {}, context_instance=RequestContext(request))




def exam_sign_up(request, student_Id):
    s = get_object_or_404(Student, enrollment_number=student_Id)

    return render_to_response('admin/student/exam_sign_up.html', {}, RequestContext(request))

def exam_sign_out(request, student_Id):
    s = get_object_or_404(Student, enrollment_number=student_Id)

    exist=ExamSignUp.objects.filter(examDate__in=s.get_current_exam_dates())


    return render_to_response('admin/student/exam_sign_out.html', {'Prijave':exist}, RequestContext(request))