from users.models import User
from django import forms
from django.forms import ModelForm
import resume.models
import users
from django.forms.models import inlineformset_factory


class CreateCVPersonalDataForm(ModelForm):
    ''' Создает форму для персональных данных '''
    
    class Meta:
        model = resume.models.PersonalData
        fields = ('name', 'photo', )


class CreateCVPositionForm(ModelForm):
    ''' Создает форму для позиции '''
    
    class Meta:
        model = resume.models.Position
        fields = '__all__'
        exclude = ('created_by', )


class CreateCVContactForm(forms.ModelForm):
    ''' form for COntacts object '''

    class Meta:
        model = resume.models.Contacts
        fields = (
            'contact_label',
            'contact_value'
        )


class CreateCVSkillForm(forms.ModelForm):
    ''' form for Skills object '''

    class Meta:
        model = resume.models.Skills
        fields = ('skill', )


class CreateCVWorkExperienceForm(forms.ModelForm):
    ''' form for WorkExperience object '''

    class Meta:
        model = resume.models.WorkExperience
        fields = ('company',
                  'position_work',
                  'link_company',
                  'date_of_employment',
                  'date_of_dismissal',
                  'description')
        

class CreateCVReferencesForm(forms.ModelForm):
    ''' form for References object '''

    class Meta:
        model = resume.models.References
        fields = ('ref_name',
                  'ref_link')