from django.urls import path
from .views import AddStudentView, DetectionView, UpdateStudentImageView, DeleteStudentView, TrainView

urlpatterns = [
    path('create-student', AddStudentView.as_view()),
    path('update-student-image', UpdateStudentImageView.as_view()),
    path('delete-student', DeleteStudentView.as_view()),
    path('train', TrainView.as_view()),
    path('detect', DetectionView.as_view())
]
