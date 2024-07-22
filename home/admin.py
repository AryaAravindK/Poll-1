from django.contrib import admin
from .models import Poll,MCQ,Descriptive,UserInfo,Response

# Register your models here.

admin.site.register(Poll)
admin.site.register(MCQ)
admin.site.register(Descriptive)
admin.site.register(UserInfo)
admin.site.register(Response)
