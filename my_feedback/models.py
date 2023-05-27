from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FeedBack(BaseModel):
    name = models.CharField(max_length=255, blank=True, verbose_name='Title')
    email = models.EmailField(blank=True, verbose_name='Email')

    def __str__(self):
        return self.name
