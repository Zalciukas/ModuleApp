from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import Module

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        exclude = ['user']
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
            'registration_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h4>Basic Information</h4>'),
            Row(
                Column('s', css_class='form-group col-md-3 mb-3'),
                Column('am', css_class='form-group col-md-9 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('subject_name_lithuanian', css_class='form-group col-md-6 mb-3'),
                Column('subject_name_english', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('language', css_class='form-group col-md-4 mb-3'),
                Column('selection_type', css_class='form-group col-md-4 mb-3'),
                Column('assessment_form', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            'study_part',
            
            HTML('<hr><h4>Credits & Hours</h4>'),
            Row(
                Column('planned_credits', css_class='form-group col-md-4 mb-3'),
                Column('hours', css_class='form-group col-md-4 mb-3'),
                Column('credits_received', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            
            HTML('<hr><h4>Assessment</h4>'),
            Row(
                Column('original_grade', css_class='form-group col-md-4 mb-3'),
                Column('grade', css_class='form-group col-md-4 mb-3'),
                Column('level_achieved', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            'original_credits',
            
            HTML('<hr><h4>Additional Information</h4>'),
            Row(
                Column('exam_date', css_class='form-group col-md-6 mb-3'),
                Column('registration_date', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'teacher',
            
            HTML('<hr>'),
            Submit('submit', 'Save Module', css_class='btn btn-primary btn-lg')
        )