from django.contrib import admin

# Register your models here.
from .models import File   # 这个需要我们自己导入相应的模型类（数据表）

admin.site.register([File])

class FileAdmin(admin.ModelAdmin):
    list_display = ['fileID','file_name','file_image','team,','father','file_creator','data']