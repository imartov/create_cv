from django.urls import path
from . import views


app_name = 'resume'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('create-cv-position/', views.create_cv_position, name='create_cv_position'),
    path('<str:username>/create-cv-pers-data/', views.create_cv_personal_data, name='create_cv_personal_data'),

    # paths for working with Contacts objects
    path('create-cv-contacts/<int:pk>', views.create_cv_contacts, name='create_cv_contacts'),
    path('htmx/contact/<pk>/', views.detail_contact, name="detail-contact"),
    path('htmx/contact/<pk>/update/', views.update_contact, name="update-contact"),
    path('htmx/contact/<pk>/delete/', views.delete_contact, name="delete-contact"),
    path('htmx/create-contact-form/<int:pk>/', views.create_contact_form, name='create-contact-form'),

    # paths for working with Skills objects
    path('create-cv-skills/<int:pk>', views.create_cv_skills, name='create_cv_skills'),
    path('htmx/skill/<pk>/', views.detail_skill, name="detail-skill"),
    path('htmx/skill/<pk>/update/', views.update_skill, name="update-skill"),
    path('htmx/skill/<pk>/delete/', views.delete_skill, name="delete-skill"),
    path('htmx/create-skill-form/<int:pk>/', views.create_skill_form, name='create-skill-form'),

    # paths for working with WorWorkExperience objects during creating CV
    path('create-cv-workexp/<int:pk>/', views.create_cv_workexp, name='create_cv_workexp'),
    path('htmx/workexp/<int:pk>/', views.detail_workexp, name="detail-workexp"),
    path('htmx/workexp/<int:pk>/update/', views.update_workexp, name="update-workexp"),
    path('htmx/workexp/<int:pk>/delete/', views.delete_workexp, name="delete-workexp"),
    path('htmx/create-workexp-form/<int:pk>/', views.create_workexp_form, name='create-workexp-form'),

    # paths for working with Referncess objects during creating CV
    path('create-cv-references/<int:pk>/', views.create_cv_references, name='create_cv_references'),
    path('htmx/reference/<int:pk>/', views.detail_reference, name="detail-reference"),
    path('htmx/reference/<int:pk>/update/', views.update_reference, name="update-reference"),
    path('htmx/reference/<int:pk>/delete/', views.delete_reference, name="delete-reference"),
    path('htmx/create-reference-form/<int:pk>/', views.create_reference_form, name='create-reference-form'),
]