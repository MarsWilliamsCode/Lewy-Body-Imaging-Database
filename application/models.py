from django.db import models

class Patient(models.Model):
    patient_id = models.CharField(primary_key=True, max_length=50)
    age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=2, blank=True, null=True)
    diagnosis = models.CharField(max_length=25)
    disease_stage = models.CharField(max_length=10, blank=True, null=True)
    enrollment_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.patient_id)

class Scan(models.Model):
    scan_id = models.CharField(primary_key=True, max_length=50)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    scan_type = models.CharField(max_length=25)
    scan_date = models.DateField(blank=True, null=True)
    scan_location = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return str(self.scan_id)

    def get_patient(self):
        return Patient.objects.get(patient_id=self.patient_id)

class Image(models.Model):
    image_id = models.CharField(primary_key=True, max_length=50)
    scan_id = models.ForeignKey(Scan, on_delete=models.CASCADE)
    image_type = models.CharField(max_length=25, default='PNG')
    image_file = models.ImageField(blank=True, null=True)

    def __str__(self):
        return str(self.image_id)
