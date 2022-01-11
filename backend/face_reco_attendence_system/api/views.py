import PIL
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Student, StudentImage
from .serializers import StudentImageSerializer, StudentBasicSerializer, StudentDetailsSerializer, UpdateStudentImageSerializer, DeleteStudentSerializer
from PIL import Image
import numpy as np
import cv2
from .trainer import Trainer


class AddStudentView(APIView):

    def post(self, request, *args, **kwargs):
        student_serializer = StudentBasicSerializer(data=self.request.data)
        if student_serializer.is_valid():
            student = student_serializer.save()
            print(student)
            for image in self.request.FILES.getlist('images'):
                student_image = StudentImageSerializer(
                    data={
                        'student': student.id,
                        'name': student.name,
                        'image': image
                    }
                )
                if student_image.is_valid():
                    student_image.save()
                else:
                    return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(StudentDetailsSerializer(student).data, status=status.HTTP_201_CREATED)
        else:
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateStudentImageView(APIView):

    def patch(self, request, *args, **kwargs):
        update_student_image_serializer = UpdateStudentImageSerializer(
            data=request.data)
        if update_student_image_serializer.is_valid():
            matric_number = update_student_image_serializer.data.get(
                'matric_number')
            queryset = Student.objects.filter(matric_number=matric_number)

            if not queryset.exists():
                return Response({'msg': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

            student = queryset[0]
            for image in self.request.FILES.getlist('images'):
                student_image = StudentImageSerializer(
                    data={
                        'student': student.id,
                        'name': student.name,
                        'image': image
                    }
                )
                if student_image.is_valid():
                    student_image.save()
                else:
                    print(update_student_image_serializer.errors)
                    return Response(update_student_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(StudentDetailsSerializer(student).data, status=status.HTTP_200_OK)
        else:
            print(update_student_image_serializer.errors)

            return Response(update_student_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteStudentView(APIView):

    def delete(self, request, *args, **kwargs):
        delete_student_serializer = DeleteStudentSerializer(data=request.data)
        if delete_student_serializer.is_valid():
            matric_number = delete_student_serializer.data.get('matric_number')
            queryset_student = Student.objects.filter(
                matric_number=matric_number)

            if not queryset_student.exists():
                return Response({'msg': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
            student_object = queryset_student[0]
            queryset_images = StudentImage.objects.filter(
                student=student_object)
            for image in queryset_images:
                image.delete()
            student_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(delete_student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrainView(APIView):

    def __init__(self):
        self.detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def get_images_and_labels(self):
        face_samples = []
        ids = []
        all_students = Student.objects.all()
        for student in all_students:
            all_images_set = StudentImage.objects.filter(student=student)
            for image in all_images_set:
                PIL_image = Image.open(image.image.path).convert('L')
                image_numpy = np.array(PIL_image, 'uint8')
                id = student.id
                faces = self.detector.detectMultiScale(image_numpy)
                for(x, y, w, h) in faces:
                    face_samples.append(image_numpy[y:y+h, x:x+w])
                    ids.append(id)
        return face_samples, ids

    def get(self, request, *args, **kwargs):

        try:
            trainer = Trainer()
            faces, ids = self.get_images_and_labels()
            trainer.train(faces, ids)
            return Response({'msg': f'{len(ids)} faces trained'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': e.with_traceback} ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
