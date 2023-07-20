from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext as _

# Create your models here.


class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()


class StudentManager(BaseUserManager):
    def create_user(self, serial_number, password=None, **extra_fields):
        if not serial_number:
            raise ValueError("The Serial Number must be set")
        user = self.model(serial_number=serial_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, serial_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(serial_number, password, **extra_fields)


class Student(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = StudentManager()

    USERNAME_FIELD = "serial_number"
    REQUIRED_FIELDS = []

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    MARITAL_CHOICES = [
        ("M", "Married"),
        ("S", "Single"),
    ]

    RESIDENCE_CHOICES = [("I", "inside"), ("O", "outside")]

    serial_number = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    date_of_birth = models.DateField(null=True)
    place_of_birth = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    living_place = models.CharField(max_length=20)
    living_city = models.CharField(max_length=20)

    arabic_first_name = models.CharField(max_length=30)
    arabic_second_name = models.CharField(max_length=30)
    arabic_third_name = models.CharField(max_length=30)
    arabic_last_name = models.CharField(max_length=30)

    marital_status = models.CharField(max_length=1, choices=MARITAL_CHOICES)

    national_number = models.CharField(max_length=15, null=True)
    phone_number = models.IntegerField(null=True)
    credit_number = models.IntegerField(null=True)
    residence = models.CharField(max_length=1, choices=RESIDENCE_CHOICES)
    family_book_number = models.CharField(max_length=15, null=True)
    family_paper_number = models.CharField(max_length=15, null=True)
    family_serial_number = models.CharField(max_length=15, null=True)
    section = models.CharField(max_length=20)
    division = models.CharField(max_length=20)

    closest_family = models.CharField(max_length=30)
    mother_name = models.CharField(max_length=30)
    mothers_job = models.CharField(max_length=30)
    other_to_call = models.CharField(max_length=30)
    phone_number_email = models.CharField(max_length=30)

    supervisor = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"[serial_number:{self.serial_number},password:{self.password},first_name:{self.first_name}]"


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, through="Enrollment")


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day_of_week = models.IntegerField()
    lecture_time = models.ForeignKey("LectureTime", on_delete=models.CASCADE)


class LectureTime(models.Model):
    LECTURE_TIMES = [
        ("09:00", "9:00 AM"),
        ("10:00", "10:00 AM"),
        ("12:00", "12:00 PM"),
        ("14:00", "2:00 PM"),
    ]
    start_time = models.CharField(max_length=5, choices=LECTURE_TIMES)
