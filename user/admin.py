from django.contrib import admin

# Register your models here.
from .models import Book, Order, UserInfo  # 这个需要我们自己导入相应的模型类（数据表）

admin.site.register([Book, Order, UserInfo])
