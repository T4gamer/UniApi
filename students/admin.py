from django.contrib import admin
from .models import Student , Course , Teacher , Lecture ,Enrollment ,LectureTime
# Register your models here.


admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Lecture)
admin.site.register(LectureTime)
admin.site.register(Enrollment)