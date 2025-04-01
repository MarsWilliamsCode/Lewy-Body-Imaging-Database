from django.db import models

class Patient(models.Model):
    patient_id = models.IntegerField(primary_key=True)
    age = models.IntegerField()
    sex = models.CharField(max_length=2)
    diagnosis = models.CharField(max_length=25)
    disease_stage = models.CharField(max_length=5, blank=True, null=True)
    enrollment_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.patient_id)

class Scan(models.Model):
    scan_id = models.IntegerField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    scan_type = models.CharField(max_length=25)
    scan_date = models.DateField()
    scan_location = models.CharField(max_length=25, blank=True, null=True)
    storage_path = models.CharField(max_length=90)

    def __str__(self):
        return str(self.scan_id)

class Image(models.Model):
    image_id = models.IntegerField(primary_key=True)
    scan_id = models.ForeignKey(Scan, on_delete=models.CASCADE)
    image_type = models.CharField(max_length=25)

    def __str__(self):
        return str(self.image_id)

class Annotation(models.Model):
    annotation_id = models.IntegerField(primary_key=True)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    label = models.CharField(max_length=25)

    def __str__(self):
        return str(self.annotation_id)