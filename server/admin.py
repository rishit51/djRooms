from django.contrib import admin
from .models import *
# Register your models here.
models=[Server,Category,Channel]

for i in models:
    admin.site.register(i)