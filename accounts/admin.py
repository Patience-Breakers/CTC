from django.contrib import admin
from accounts.models import Student, Teacher, Course, Lecture, Watch_time, Todo, Logs
# Register your models here.

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Watch_time)
admin.site.register(Todo)
admin.site.register(Logs)
