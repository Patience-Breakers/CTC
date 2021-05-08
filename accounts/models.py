from django.db import models
from django.db.models import Count


class Course (models.Model):
    course_id = models.CharField(primary_key=True, max_length=100)
    course_name = models.CharField(max_length=100, null=False)
    course_image = models.ImageField(upload_to="course-images/", default="")
    desc = models.CharField(max_length=250, default="")

    class Meta:
        ordering = ['course_name']

    def _str_(self):
        return self.course_name


class Teacher (models.Model):
    teacher_id = models.AutoField(primary_key=True)
    teacher_name = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=10, null=False, default="")
    password = models.CharField(max_length=10, null=False, default="")
    teacher_image = models.ImageField(upload_to="teacher-images/", default="")
    teacher_email = models.EmailField(max_length=254, default="")
    teacher_phone = models.CharField(max_length=20, default='')
    teacher_dob = models.DateField(auto_now=False, auto_now_add=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default="")

    def _str_(self):
        return self.teacher_name


class Student (models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=10, null=False, default="")
    password = models.CharField(max_length=10, null=False, default="")
    email = models.EmailField(max_length=254, default="")
    phone_no = models.CharField(max_length=20, default='')
    image = models.ImageField(upload_to="course-images/", default="")
    dob = models.DateField(auto_now=True, auto_now_add=False)
    CATEGORY = (
        (u'U', u'Under Grad'),
        (u'P', u'Post Grad'),
        (u'H', u'High School Student'),
        (u'O', u'Others'),
    )
    stud_category = models.CharField(max_length=2, null=True,
                                     choices=CATEGORY, default='U')
    courses = models.ManyToManyField(Course)

    class Meta:
        ordering = ['name']

    def _str_(self):
        return self.name


class Lecture (models.Model):
    lec_id = models.AutoField(primary_key=True)
    lec_no = models.CharField(default="0", max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default="")
    lecture_name = models.CharField(max_length=100, default="")
    lec_date = models.DateField(auto_now=True, auto_now_add=False)
    video = models.FileField(upload_to="videos/", null=True)
    material = models.FileField(upload_to="lec_materials/", null=True)
    thumbnail = models.ImageField(upload_to="course-images/", default="")

    def _str_(self):
        return self.lec_no


class Watch_time(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default="")
    w_lect = models.ForeignKey(Lecture, on_delete=models.CASCADE, default="")
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(auto_now=True, auto_now_add=False)
    Rating = models.IntegerField(default=0)


class Todo(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default="")
    task = models.CharField(default="NULL", max_length=100)
    iscomplete = models.BooleanField(default=False)


# class Todo(models.Model):

class Logs(models.Model):
    student_id = models.IntegerField(primary_key=True)
    edit_time = models.DateField(auto_now=False, auto_now_add=False)


