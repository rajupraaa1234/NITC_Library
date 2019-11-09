from django.contrib import admin
from . models import Post, Profile,Book,Admin,Notice,IssueBook
# Register your models here.
admin.site.register(Post) 
admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Admin)
admin.site.register(Notice)
admin.site.register(IssueBook)