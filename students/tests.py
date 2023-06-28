from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Student
from .serializers import StudentSerializer

class StudentListTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_student(self):
        url = reverse('student-list')
        data = {
            'first_name': 'Scarlett',
            'last_name': 'Evans',
            'grade': 8,
            'email': 'scarlett@example.com',
            'date_of_birth': '2010-05-01',
            'phone': '+11111111111',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        student = Student.objects.get(pk=response.data['id'])
        serializer = StudentSerializer(student)
        self.assertEqual(response.data, serializer.data)

    def test_get_students(self):
        url = reverse('student-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        students = Student.objects.all().order_by('id')
        serializer = StudentSerializer(students, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_student_invalid_data(self):
        url = reverse('student-list')
        data = {
            'first_name': 'Scarlett',
            'last_name': 'Evans',
            'grade': 'Eighth',  # Invalid grade value
            'email': 'scarlett@example.com',
            'date_of_birth': '2010-05-01',
            'phone': '+11111111111',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_students_empty_list(self):
        Student.objects.all().delete()  # Delete all existing students
        url = reverse('student-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

class StudentDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = Student.objects.create(
            first_name='Scarlett',
            last_name='Evans',
            grade=8,
            email='scarlett@example.com',
            date_of_birth='2010-05-01',
            phone='+11111111111',
        )

    def test_get_student(self):
        url = reverse('student-detail', args=[self.student.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = StudentSerializer(self.student)
        self.assertEqual(response.data, serializer.data)

    def test_patch_student(self):
        url = reverse('student-detail', args=[self.student.pk])
        data = {
            'grade': 9,
            'phone': '+11111111000',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        serializer = StudentSerializer(self.student)
        self.assertEqual(response.data, serializer.data)

    def test_get_nonexistent_student(self):
        url = reverse('student-detail', args=[1000])  # Nonexistent student ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_nonexistent_student(self):
        url = reverse('student-detail', args=[1000])  # Nonexistent student ID
        data = {
            'grade': 9,
            'phone': '+11111111000',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)