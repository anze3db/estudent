# Create your views here.
import datetime
from codelist.models import Course, StudyProgram, Instructor
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import context, loader
from django.template.context import RequestContext, Context
from student.models import *
from codelist.models import Course
from django.core import serializers


def exam_grades_index(request):

    exam_dates=ExamDate.objects.all().order_by('date')
    if request.user.groups.filter(name = 'profesorji'):
        exam_dates = [e for e in exam_dates if e.instructors and e.instructors.instructor.filter(user = request.user)]
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
        prijava['tocke'] = "" if p.points == None else p.points
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
        
        prog = forms.ChoiceField(choices=programs, label="Program")
        cour = forms.ChoiceField(choices=choices, label="Izbirni predmet")
        year = forms.MultipleChoiceField(choices=[(2012, 2012), (2011, 2011), (2010, 2010)], label="Leto")
        
        
    students = []
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if 'year' in request.POST:
            students = Enrollment.objects.filter(study_year__in = request.POST.getlist('year'), courses = request.POST['cour'], program = request.POST['prog'])
            
        
    else:
        form = ClassForm()
        
    return render_to_response('admin/student/class_list.html', {'form':form, 'students': students}, RequestContext(request))


def exam_sign_up_index(request):
    student_enrolls = Student.objects.all()
    student_enrolls = "[ " + ", ".join([ '"' + str(s.pk) + '"' for s in student_enrolls]) + " ]"

    try:
        student_Id=request.POST['vpisna']
        if student_Id.isdigit():
            try:
                student = Student.objects.get(enrollment_number=student_Id)

                if 'prijava' in request.POST:
                    return HttpResponseRedirect(reverse('student.views.exam_sign_up', args=[student.enrollment_number]))
                elif 'odjava' in request.POST:
                    return HttpResponseRedirect(reverse('student.views.exam_sign_out', args=[student.enrollment_number]))
                elif Student.DoesNotExist:
                    return HttpResponseRedirect(reverse('student.views.exam_sign_out', args=[student.enrollment_number]))
            except:
                pass
                
        return render_to_response('admin/student/exam_sign_up_index.html', {
            'error_message': "Student s to vpisno stevilko ne obstaja",
            'students':student_enrolls
            }, context_instance=RequestContext(request))

    except:
        return render_to_response('admin/student/exam_sign_up_index.html', {'students':student_enrolls}, context_instance=RequestContext(request))




def exam_sign_up(request, student_Id):
    s = get_object_or_404(Student, enrollment_number=student_Id)
    student = Student.objects.get(enrollment_number=student_Id)
    enroll= Enrollment.objects.filter(student=s)

    class EnrollForm(forms.Form):
        enrolls=[]
        ePk=[]

        for enroll in Enrollment.objects.filter(student=student):
                enrolls.append((enroll.pk, enroll.__unicode__()))

        enrolments=forms.ChoiceField(choices=enrolls)

    exams=[]
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        enroll= Enrollment.objects.get(id=request.POST['enrolments'])
        classes=Course.objects.filter(curriculum__in=enroll.get_classes()  )
        exams=ExamDate.objects.filter(course__in=classes)

    else:
        form=EnrollForm()


    return render_to_response('admin/student/exam_sign_up.html', {'form':form,'Roki':exams, 'Student':student_Id, 'Vpis':enroll}, RequestContext(request))

def exam_sign_out(request, student_Id):
    s = get_object_or_404(Student, enrollment_number=student_Id)

    exist=ExamSignUp.objects.filter(examDate__in=s.get_current_exam_dates())


    return render_to_response('admin/student/exam_sign_out.html', {'Prijave':exist}, RequestContext(request))
    
    
def student_index(request):
    student_enrolls = Student.objects.all()
    student_enrolls = "[ " + ", ".join([ '"' + str(s.pk) + '"' for s in student_enrolls]) + " ]"
    
    try:
        student_Id = request.POST['vpisna']
        if student_Id.isdigit():
            try:
                student = Student.objects.get(enrollment_number=student_Id)
                if 'zadnje' in request.POST:
                    return HttpResponseRedirect(reverse('student.views.student_index_list', args=[student.enrollment_number, 1]))
                else:
                    return HttpResponseRedirect(reverse('student.views.student_index_list', args=[student.enrollment_number, 0]))


                return HttpResponseRedirect(reverse('student.views.student_index_list', args=[student.enrollment_number, 0]))
            except:
                pass
                
        return render_to_response('admin/student/student_index.html', {
            'error_message': "Student s to vpisno stevilko ne obstaja",
            'students':student_enrolls
            }, context_instance=RequestContext(request))
    except:
        return render_to_response('admin/student/student_index.html', {'students':student_enrolls}, context_instance=RequestContext(request))


def student_index_list(request, student_Id, display): #0=all, 1=last
    student = get_object_or_404(Student, enrollment_number=student_Id)

    response = []

    enrolls = Enrollment.objects.filter(student=student).order_by('program', 'study_year', 'class_year')
    prog = ""
    for enroll in enrolls:
        out={}
        out['program'] = enroll.program.descriptor
        # same program, don't repeat
        if prog != out['program']:
            out['noprogram'] = True
            prog = out['program']

        out['enrollment_type'] = enroll.enrol_type+' - '+enroll.get_enrol_type_display()
        out["redni"]=enroll.regular
        out["letnik"]=enroll.class_year
        out["study_year"]=enroll.class_year

        #out['enroll'] = enroll
        
        courses = []
        classes = enroll.get_classes()
        courses2 = Course.objects.filter(curriculum__in=classes).order_by('course_code')
        
        for p in courses2:
            try:
                course={}
                course["name"]=p.name
                course["sifra_predmeta"]=p.course_code
                course["izvajalci"]=p.predavatelji()
                signups = ExamSignUp.objects.filter(enroll=enroll).order_by('examDate__date')
                signups = filter(lambda s: s.examDate.course.name == p.name, signups)
                signups = filter(lambda s: (s.result_exam != "NR" and s.VP != True), signups)

                if len(signups) > 0:
                    fsignup = signups[0]
                    signs = []
                    for s in signups:
                        polaganje={}
                        polaganje['datum']=s.examDate.date.strftime("%d.%m.%Y")
                        polaganje['izvajalci']=s.examDate.instructors
                        cur=Curriculum.objects.get(course=p, program=enroll.program)
                        if(cur.only_exam==True):
                            polaganje['ocena']=s.result_exam
                        else:
                            polaganje['ocena']=str(s.result_exam)+"/"+ str((s.result_practice if s.result_exam > 5 else 0))
                        signs.append(polaganje)

                    if fsignup.examDate.repeat_class(student,0)>0:
                        course['odstevek_ponavljanja']=" - "+fsignup.examDate.course.nr_attempts_all(student)-fsignup.examDate.repeat_class(student,0)
                    else:
                        course['odstevek_ponavljanja']=""
                    course['polaganja_letos']=fsignup.examDate.course.nr_attempts_this_year(student)
                    course['stevilo_polaganj']=fsignup.examDate.course.nr_attempts_all(student)
                    #polaganje['stevilo_polaganj']

                if display == "1":
                        signs = signs[-1:]

                    course["signups"] = signs

                courses = courses+[course]
            except:
                raise
                pass
        out["courses"]=courses
        out["povprecje_izpitov"]=enroll.get_exam_avg()
        out["povprecje_vaj"]=enroll.get_practice_avg()
        out["povprecje"]=enroll.get_avg()       
        response = response + [out]
        
    return render_to_response('admin/student/student_index_list.html', {'student':student, 'data':response}, RequestContext(request))
    
    
    
def sign_up_confirm(request, student_Id, exam_Id, enroll_Id):
    student = get_object_or_404(Student, enrollment_number=student_Id)
    exam=ExamDate.objects.get(pk=exam_Id)
    enroll= Enrollment.objects.get(pk=enroll_Id)
    d = datetime.timedelta(days=14)


    message = {"msg":"","error":""}


    try:
        if 'prijava' in request.POST:

            error_msgs = exam.signUp_allowed(student)
            nr_all= exam.course.nr_attempts_all(student)
            nr_this=exam.course.nr_attempts_this_year(student)
            rep=exam.repeat_class(student)



            if error_msgs != None:
                message["error"]= error_msgs[0]
            elif exam.already_positive(student):
                message["error"]='Za ta predmet ze obstaja pozitivna ocena'
            elif exam.already_signedUp(student):
                message["error"]='Na ta predmet ste ze prijavljeni ali pa se ni bila vnesena ocena'
            elif nr_this>=3:
                message["error"]='Ta predmet ste letos opravljali ze 3x. Prijava ni vec mogoca'
            elif nr_all>=6:
                message["error"]='Ta predmet ste  opravljali ze 6x. Prijava ni vec mogoca'
            elif exam.date < (datetime.date.today()+ datetime.timedelta(days=3)):
                message["error"]='Rok za prijavo na izpit je potekel'
           
            elif exam.date < (ExamDate.objects.get(examsignup=exam.last_try(student)).date+d):
                message["error"]='Ni se preteklo 14 dni od zadnje prijave'

            else:

                ExamSignUp.objects.create(enroll=enroll, examDate=exam).save()
                nr_all= exam.course.nr_attempts_all(student)
                message["msg"]='Uspesna prijava na izpit '+ str(exam)+'To je vase '+str(nr_all)+'. polaganje'
            return HttpResponseRedirect(reverse('student.views.exam_success', args=(student.enrollment_number, exam_Id, )))
                #return render_to_response('admin/student/exam_sign_up_confirm.html', {'Student':student, 'rok':exam, 'msg':message['msg']}, RequestContext(request))

        elif 'nazaj' in request.POST:
            return HttpResponseRedirect(reverse('student.views.exam_sign_up', args=(student.enrollment_number, )))


    except :

        return render_to_response('admin/student/exam_sign_up_confirm.html', {'Student':student, 'rok':exam, 'msg':message}, RequestContext(request))

    #return render_to_response('admin/student/exam_sign_up_confirm.html', {'Student':student, 'rok':exam, 'msg':message['msg']}, RequestContext(request))



    return render_to_response('admin/student/exam_sign_up_confirm.html', {'Student':student, 'rok':exam}, RequestContext(request))

def sign_up_success(request, student_Id, exam_Id):
    return render_to_response('admin/student/exam_sign_up_success.html', {'Student':student_Id, 'rok':exam_Id}, RequestContext(request))

def student_personal(request, student_Id):
    student= Student.objects.get(enrollment_number = student_Id)
    enrollment = Enrollment.objects.filter(student = student_Id)
    return render_to_response('admin/student/student_personal.html', {'enrollment':enrollment,'student':student}, RequestContext(request))

