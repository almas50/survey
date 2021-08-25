from django.contrib import admin
from .models import Question, Survey, Response
# Register your models here.
admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(Response)
