from rest_framework import serializers
from rest_framework.validators import ValidationError
from students.models import Student, Course, Enrollment, Lecture, LectureTime
from django.contrib.auth import authenticate


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "code", "teacher", "students")


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ("id", "student", "course", "date_enrolled")


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ("id", "course", "day_of_week", "lecture_time")


class LectureTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureTime
        fields = ("id", "start_time")


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

    def to_representation(self, instance):
        # Call the superclass method to get the default representation
        representation = super().to_representation(instance)

        # Remove the fields you want to exclude from the response
        representation.pop("groups", None)
        representation.pop("user_permissions", None)
        representation.pop("last_login", None)
        representation.pop("is_superuser", None)
        representation.pop("is_active", None)
        representation.pop("is_staff", None)
        # Return the modified representation
        return representation


class StudentMainDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

    def to_representation(self, instance):
        # Call the superclass method to get the default representation
        representation = super().to_representation(instance)

        # Remove the fields you want to exclude from the response
        representation.pop("groups", None)
        representation.pop("user_permissions", None)
        representation.pop("last_login", None)
        representation.pop("is_superuser", None)
        representation.pop("is_active", None)
        representation.pop("is_staff", None)
        representation.pop("closest_family", None)
        representation.pop("mother_name", None)
        representation.pop("mothers_job", None)
        representation.pop("other_to_call", None)
        representation.pop("phone_number_email", None)
        representation.pop("supervisor", None)

        # Return the modified representation
        return representation


class StudentSecondaryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

    def to_representation(self, instance):
        # Call the superclass method to get the default representation
        representation = super().to_representation(instance)

        # Remove the fields you want to exclude from the response
        representation.pop("groups", None)
        representation.pop("user_permissions", None)
        representation.pop("last_login", None)
        representation.pop("is_superuser", None)
        representation.pop("is_active", None)
        representation.pop("is_staff", None)

        representation.pop("serial_number", None)
        representation.pop("first_name", None)
        representation.pop("last_name", None)
        representation.pop("gender", None)
        representation.pop("email", None)
        representation.pop("date_of_birth", None)

        representation.pop("place_of_birth", None)
        representation.pop("country", None)
        representation.pop("living_place", None)
        representation.pop("living_city", None)
        representation.pop("arabic_first_name", None)
        representation.pop("arabic_second_name", None)

        representation.pop("arabic_third_name", None)
        representation.pop("arabic_last_name", None)
        representation.pop("marital_status", None)
        representation.pop("national_number", None)
        representation.pop("phone_number", None)
        representation.pop("credit_number", None)

        representation.pop("residence", None)
        representation.pop("section", None)
        representation.pop("division", None)
        # Return the modified representation
        return representation


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        serial_exist = Student.objects.filter(
            serial_number=attrs["serial_number"]
        ).exists()
        if serial_exist:
            raise ValidationError("serial number already exists")
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        student = super().create(validated_data)
        student.set_password(password)
        student.save()
        return student


class StudentLoginSerializer(serializers.Serializer):
    serial_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        student = authenticate(
            serial_number=data["serial_number"], password=data["password"]
        )
        if student and student.is_active:
            return student
        raise serializers.ValidationError("Incorrect Credentials")
