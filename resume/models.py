from django.db import models
from django.urls import reverse
from users.models import User


class Position(models.Model):
    position_name = models.CharField(max_length=255, blank=True, verbose_name='Position')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user by', blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_create']

    def __str__(self):
        return self.position_name


class PersonalData(models.Model):
    pos = models.ForeignKey('Position', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Position')
    first_name = models.CharField(max_length=50, blank=True, verbose_name='First name')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Last name')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("person", kwargs={"pk": self.pk})
    

class Contacts(models.Model):
    pos = models.ForeignKey('Position', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Position')
    contact_label = models.CharField(max_length=100, blank=True, verbose_name='Contact label')
    contact_value = models.CharField(max_length=255, blank=True, verbose_name='Contact value')

    def __str__(self):
        return self.contact_label


class Skills(models.Model):
    pos = models.ForeignKey('Position', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Position')
    skill = models.CharField(max_length=20, blank=True, verbose_name='Skill')

    def __str__(self):
        return self.skill
    
    def get_absolute_url(self):
        return reverse("skill", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = []


class WorkExperience(models.Model):
    pos = models.ForeignKey('Position', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Position Relative')
    company = models.CharField(max_length=50, verbose_name='Company', blank=True)
    position_work = models.CharField(max_length=50, verbose_name='Position', blank=True)
    link_company = models.URLField(verbose_name="Company's link", blank=True)
    date_of_employment = models.DateField(blank=True, verbose_name='Date of employment')
    date_of_dismissal = models.DateField(blank=True, verbose_name='Date of dismissal')
    description = models.TextField(blank=True, verbose_name='Description')

    def __str__(self):
        return self.company

    class Meta:
        ordering = ["-date_of_employment"]


class Summary(models.Model):
    pos = models.ForeignKey('Position', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Position')
    summary = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.summary[:10]


class References(models.Model):
    pos = models.ForeignKey('Position', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Position')
    ref_name = models.CharField(max_length=50, blank=True, verbose_name="References name")
    ref_link = models.URLField(verbose_name="Link", blank=True)

    def __str__(self):
        return self.ref_name
    
    def get_absolute_url(self):
        return reverse("referenc", kwargs={"pk": self.pk})
