from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from students.models import Student, Course, Enrollment, Lecture, LectureTime
from knox.models import AuthToken
from .serializers import (
    StudentSerializer,
    RegisterSerializer,
    StudentMainDetailsSerializer,
    StudentSecondaryDetailsSerializer,
    StudentLoginSerializer,
    CourseSerializer,
    EnrollmentSerializer,
    LectureSerializer,
    LectureTimeSerializer,
)

# rest_framework imports
from rest_framework import permissions

# knox imports
from knox.views import LoginView as KnoxLoginView


class CreateStudentView(generics.CreateAPIView):
    # Create student API view
    serializer_class = StudentSerializer


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = StudentLoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.validated_data
        _, token = AuthToken.objects.create(student)
        return Response(
            {"student": StudentSerializer(student).data, "token": token},
            status=status.HTTP_202_ACCEPTED,
        )


class ManageStudentView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated student"""

    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated student"""
        return Response(self.request.user, status=status.HTTP_200_OK)


class RegisterAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        return Response(
            {
                "student": StudentSerializer(
                    student, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(student)[1],
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST", "GET"])
def student(request):
    if request.method == "GET":
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def student_main_details(request):
    if request.method == "GET":
        students = Student.objects.all()
        serializer = StudentMainDetailsSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def student_secondary_details(request):
    if request.method == "GET":
        students = Student.objects.all()
        serializer = StudentSecondaryDetailsSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self):
        return Response(self.queryset, status=status.HTTP_200_OK)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def list(self, request, *args, **kwargs):
        enrollment_list = super().list(request, *args, **kwargs).data
        response_list = []
        for enroll in enrollment_list:
            if enroll["student"] == request.user.serial_number:
                response_list.append(enroll)
        return Response(response_list)

    def create(self, request: Request, *args, **kwargs):
        student_serial = request.data["student"]
        if student_serial == request.user.serial_number:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "You can only create an enrollment for yourself"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def delete(self, request, *args, **kwargs):
        params = request.query_params
        if params.get("student_id") == request.user.serial_number:
            self.queryset.filter(
                student=params.get("student_id"), course=params.get("course_id")
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "You can only delete an enrollment for yourself"},
            status=status.HTTP_403_FORBIDDEN,
        )


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def list(self, request: Request, *args, **kwargs):
        lectures = self.queryset.filter(course=request.query_params.get("course"))
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)


class LectureTimeViewSet(viewsets.ModelViewSet):
    queryset = LectureTime.objects.all()
    serializer_class = LectureTimeSerializer

    def get(self):
        return Response(self.queryset, status=status.HTTP_200_OK)
