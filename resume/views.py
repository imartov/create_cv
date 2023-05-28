from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotAllowed, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import *

from .forms import (
    CreateCVPositionForm,
    CreateCVContactForm,
    CreateCVSkillForm,
    CreateCVPersonalDataForm,
    CreateCVWorkExperienceForm,
    CreateCVReferencesForm,
)

from my_feedback.forms import FeedBackForm
import resume.forms
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.forms.models import modelformset_factory


menu = {
    'create_cv': 'Create CV'
}

def main_page(request):
    ''' Рендерит главную страницу '''

    form = FeedBackForm
    username = request.user.username

    # количество посещений
    # num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits'] = num_visits + 1

    context = {
        'menu': menu,
        'title': 'Main page',
        'form': form,
        'username': username}
    
    return render(request, 'resume/main_page.html', context=context)


@login_required(login_url='/users/login/')
def create_cv_position(request):
    ''' ренедрит форму для внесения позиции '''

    username = request.user.username
    
    if request.method == 'POST':
        position_form = resume.forms.CreateCVPositionForm(request.POST)
        if position_form.is_valid():
            position_form = position_form.save(commit=False)
            position_form.created_by = request.user
            position_form.save()
            return redirect('resume:create_cv_personal_data', username)

    position_form = CreateCVPositionForm()
    context = {
        'position_form': position_form,
        'username': username}

    return render(request, "resume/create_cv_position.html", context)


def update_position(request, pos_id):
    position = get_object_or_404(Position, id=pos_id)
    position_form = CreateCVPositionForm()

    if request.method == 'POST':
        if position_form.is_valid():
            position_form.save()

    context = {
        'position': position,
        'position_form': position_form
    }

    return render(request, 'resume/partials/position_form.html', context)


def detail_position(request, pos_id):
    position = get_object_or_404(Position, id=pos_id)

    context = {
        'position': position
    }

    return render(request, 'resume/partials/position_detail.html', context)


@login_required(login_url='/users/login/')
def create_cv_personal_data(request, username):
    ''' Получает поля из всех моделей для формы / создания резюме '''

    username = request.user.username
    last_pos = Position.objects.all().last()
    
    if request.method == 'POST':
        pers_form = resume.forms.CreateCVPersonalDataForm(request.POST)
        if pers_form.is_valid():
            pers_form = pers_form.save(commit=False)
            pers_form.pos = last_pos
            pers_form.save()
            # TODO: удалить дубликаты
            return redirect('resume:create_cv_contacts', pk=last_pos.id)

    pers_form = resume.forms.CreateCVPersonalDataForm()
    context = {
        'pers_form': pers_form}

    return render(request, "resume/create_cv_personal_data.html", context)


@login_required(login_url='/users/login/')
def create_cv_contacts(request, pk):
    ''' functions for working with models.Contacts '''

    position = Position.objects.get(id=pk)
    contacts = Contacts.objects.filter(pos=position)
    form = CreateCVContactForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            contact = form.save(commit=False)
            contact.pos = position
            contact.save()
            pk = contact.pk
            return redirect("resume:detail-contact", pk) # here i do redirect
        else:
            return render(request, "resume/partials/contact_form.html", context={
                "form": form
            })

    context = {
        "form": form,
        "position": position,
        "contacts": contacts,
        'title': 'Add contacts'
    }

    return render(request, "resume/create_cv_contacts.html", context)


@login_required(login_url='/users/login/')
def update_contact(request, pk):
    contact = Contacts.objects.get(id=pk)
    form = CreateCVContactForm(request.POST or None, instance=contact)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("resume:detail-contact", pk=contact.id)

    context = {
        "form": form,
        "contact": contact
    }

    return render(request, "resume/partials/contact_form.html", context)


@login_required(login_url='/users/login/')
def delete_contact(request, pk):
    contact = get_object_or_404(Contacts, id=pk)

    if request.method == "POST":
        contact.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


@login_required(login_url='/users/login/')
def detail_contact(request, pk):
    ''' view for rendering added Contact to DB and displaying it on 'resume/create_cv_contact.html' template '''

    contact = get_object_or_404(Contacts, pk=pk)
    context = {
        "contact": contact
    }
    return render(request, "resume/partials/contact_detail.html", context)


@login_required(login_url='/users/login/')
def create_contact_form(request, pk):
    form = CreateCVContactForm()
    position = {"id": pk}
    context = {
        "form": form,
        "position": position,
    }
    return render(request, "resume/partials/contact_form.html", context)



''' views for working with Skills object during creating CV using forms '''

@login_required(login_url='/users/login/')
def create_cv_skills(request, pk):
    ''' main views for displaying form for to add skills to CV and redirect to HTMX template '''

    position = Position.objects.get(id=pk)
    skills = Skills.objects.filter(pos=position)
    form = CreateCVSkillForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            skill = form.save(commit=False)
            skill.pos = position
            skill.save()
            pk = skill.pk
            return redirect("resume:detail-skill", pk)
        else:
            return render(request, "resume/partials/skill_form.html", context={
                "form": form
            })

    context = {
        "form": form,
        "position": position,
        "skills": skills,
        'title': 'Add skills'
    }

    return render(request, "resume/create_cv_skills.html", context)


@login_required(login_url='/users/login/')
def create_skill_form(request, pk):
    ''' view for rendering form of instnce of Skills object for adding skills during creating CV '''

    form = CreateCVSkillForm()
    position = {"id": pk}
    context = {
        "form": form,
        "position": position,
    }
    return render(request, "resume/partials/skill_form.html", context)


@login_required(login_url='/users/login/')
def detail_skill(request, pk):
    ''' view for rendering added skill to DB and displaying it on 'resume/create_cv_skills.html' template '''

    skill = get_object_or_404(Skills, pk=pk)
    context = {
        "skill": skill
    }
    return render(request, "resume/partials/skill_detail.html", context)


@login_required(login_url='/users/login/')
def update_skill(request, pk):
    ''' view for updating added skill '''

    skill = Skills.objects.get(id=pk)
    form = CreateCVSkillForm(request.POST or None, instance=skill)
    position = {'id': skill.pos_id}
    print(position)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("resume:detail-skill", pk=skill.id)

    context = {
        "form": form,
        "skill": skill,
        'position': position
    }

    return render(request, "resume/partials/skill_form.html", context)


@login_required(login_url='/users/login/')
def delete_skill(request, pk):
    ''' view for delete instance of Skills object '''

    skill = get_object_or_404(Skills, id=pk)

    if request.method == "POST":
        skill.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )




''' views for working with WorkExperience object during creating CV using forms '''

@login_required(login_url='/users/login/')
def create_cv_workexp(request, pk):
    ''' main views for displaying form for to add WorkExperience to CV and redirect to HTMX template '''

    position = Position.objects.get(id=pk)
    workexps = WorkExperience.objects.filter(pos=position)
    form = CreateCVWorkExperienceForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            workexp = form.save(commit=False)
            workexp.pos = position
            workexp.save()
            pk = workexp.pk
            return redirect("resume:detail-workexp", pk=pk)
        else:
            return render(request, "resume/partials/workexp_form.html", context={
                "form": form,
                'position': position
            })

    context = {
        "form": form,
        "position": position,
        "workexps": workexps,
        'title': 'Add company'
    }

    return render(request, "resume/create_cv_workexp.html", context)


@login_required(login_url='/users/login/')
def create_workexp_form(request, pk):
    ''' view for rendering form of WorkExperience object for adding instnce during creating CV '''

    form = CreateCVWorkExperienceForm()
    position = {"id": pk}
    context = {
        "form": form,
        "position": position,
    }
    return render(request, "resume/partials/workexp_form.html", context)


@login_required(login_url='/users/login/')
def detail_workexp(request, pk):
    ''' view for rendering added WorkExperience to DB and displaying it on 'resume/create_cv_workexp.html' template '''

    workexp = get_object_or_404(WorkExperience, pk=pk)
    context = {
        "workexp": workexp,
        'pk': pk
    }
    return render(request, "resume/partials/workexp_detail.html", context)


@login_required(login_url='/users/login/')
def update_workexp(request, pk):
    ''' view for updating added WorkExperience '''

    workexp = WorkExperience.objects.get(id=pk)
    form = CreateCVWorkExperienceForm(request.POST or None, instance=workexp)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("resume:detail-workexp", pk=workexp.id)

    context = {
        "form": form,
        "workexp": workexp
    }

    return render(request, "resume/partials/workexp_form.html", context)


@login_required(login_url='/users/login/')
def delete_workexp(request, pk):
    ''' view for delete instance of WorkExperience object '''

    workexp = get_object_or_404(WorkExperience, id=pk)

    if request.method == "POST":
        workexp.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )



''' views for working with References object during creating CV using forms '''

@login_required(login_url='/users/login/')
def create_cv_references(request, pk):
    ''' main views for displaying form for to add Reference to CV and redirect to HTMX template '''

    position = Position.objects.get(id=pk)
    references = References.objects.filter(pos=position)
    form = CreateCVReferencesForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            reference = form.save(commit=False)
            reference.pos = position
            reference.save()
            pk = reference.pk
            return redirect("resume:detail-reference", pk=pk)
        else:
            return render(request, "resume/partials/reference_form.html", context={
                "form": form,
                'position': position
            })

    context = {
        "form": form,
        "position": position,
        "references": references,
        'title': 'References'
    }

    return render(request, "resume/create_cv_references.html", context)


@login_required(login_url='/users/login/')
def create_reference_form(request, pk):
    ''' view for rendering form of References object for adding instnce during creating CV '''

    form = CreateCVReferencesForm()
    position = {"id": pk}
    context = {
        "form": form,
        "position": position,
    }
    return render(request, "resume/partials/reference_form.html", context)


@login_required(login_url='/users/login/')
def detail_reference(request, pk):
    ''' view for rendering added References to DB and displaying it on 'resume/create_cv_references.html' template '''

    reference = get_object_or_404(References, pk=pk)
    context = {
        "reference": reference,
        'pk': pk
    }
    return render(request, "resume/partials/reference_detail.html", context)


@login_required(login_url='/users/login/')
def update_reference(request, pk):
    ''' view for updating added References '''

    reference = References.objects.get(id=pk)
    form = CreateCVReferencesForm(request.POST or None, instance=reference)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("resume:detail-reference", pk=reference.id)

    context = {
        "form": form,
        "reference": reference
    }

    return render(request, "resume/partials/reference_form.html", context)


@login_required(login_url='/users/login/')
def delete_reference(request, pk):
    ''' view for delete instance of References object '''

    reference = get_object_or_404(References, id=pk)

    if request.method == "POST":
        reference.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )



def get_all_cv(request):
    all_cv = Position.objects.filter(created_by_id=request.user.id)
    context = {
        'all_cv': all_cv
    }

    return render(request, 'resume/all_cv.html', context)


def get_detail_cv(request, pos_id):
    position = get_object_or_404(Position, pk=pos_id)
    pers_datas = PersonalData.objects.filter(pos_id=pos_id)
    contacts = Contacts.objects.filter(pos_id=pos_id)
    skills = Skills.objects.filter(pos_id=pos_id)
    work_exps = WorkExperience.objects.filter(pos_id=pos_id)
    try:
        summary = Summary.objects.get(pos_id=pos_id)
    except Exception as ex:
        summary = None
    references = References.objects.filter(pos_id=pos_id)

    context = {
        'position': position,
        'pers_data': pers_datas,
        'contacts': contacts,
        'skills': skills,
        'work_exps': work_exps,
        'summary': summary,
        'references': references
    }

    return render(request, 'resume/detail_cv.html', context)
    