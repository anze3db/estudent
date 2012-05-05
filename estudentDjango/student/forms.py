from django.forms.models import ModelForm

class StudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        
        if instance and instance.name:
            self.fields['enrollment_number'].widget.attrs['readonly'] = True
            
        def clean_enrollment_number(self):
            return self.instance.enrollment_number