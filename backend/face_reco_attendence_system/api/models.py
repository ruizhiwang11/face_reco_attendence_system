from django.db import models


class Student(models.Model):
    matric_number = models.CharField(
        max_length=10, unique=True, default="U1111111A")
    name = models.CharField(max_length=30)


class StudentImage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    image = models.FileField(blank=False, unique=True,
                             null=False, upload_to="student")

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.image
            self.image = None
            super(StudentImage, self).save(*args, **kwargs)
            self.image = saved_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super(StudentImage, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()

    def __str__(self):
        return "{} : {}".format(self.student.matric_number, self.student.name, self.image.name)
