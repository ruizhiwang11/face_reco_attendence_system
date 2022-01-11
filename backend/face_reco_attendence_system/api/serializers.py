from django.db import models
from django.db.models.base import Model
from rest_framework import serializers
from .models import (Student, StudentImage)

class StudentBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class StudentSingleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentImage
        fields = ['image']
        
class StudentDetailsSerializer(serializers.ModelSerializer):
    studentimage_set=StudentSingleImageSerializer(many=True)
    class Meta:
        model = Student
        fields = ['matric_number','name','studentimage_set']

class StudentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentImage
        fields = "__all__"

class UpdateStudentImageSerializer(serializers.ModelSerializer):
    matric_number = serializers.CharField(validators=[])
    class Meta:
        model = Student
        fields = ['matric_number']

class DeleteStudentSerializer(serializers.ModelSerializer):
    matric_number = serializers.CharField(validators=[])
    class Meta:
        model = Student
        fields = ['matric_number']
