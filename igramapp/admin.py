from django.contrib import admin
from igramapp.models import Comments,Post,MyUser
# Register your models here.
admin.site.register(Comments)
admin.site.register(Post)
admin.site.register(MyUser)