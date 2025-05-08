from django.db import models
from django.utils import timezone

class Prescription(models.Model):
    name = models.CharField(max_length=100, default="Unknown")
    age = models.IntegerField(default=0)
    sex = models.CharField(max_length=10, default="Unknown")
    address = models.CharField(max_length=200, default="Unknown")
    mobile = models.CharField(max_length=15, default="Unknown")
    reg_no = models.CharField(max_length=50, default="Unknown")
    appointment = models.CharField(max_length=100, default="Unknown")
    date = models.DateField(default=timezone.now)

    disease = models.TextField(blank=True)
    cc = models.TextField(blank=True)
    oe = models.TextField(blank=True)
    ix = models.TextField(blank=True)

    disease_condition = models.CharField(max_length=200, blank=True)
    chief_complaint = models.TextField(blank=True)
    
    
    medicines = models.TextField(blank=True)


    blood_pressure = models.CharField(max_length=20, blank=True)
    pulse = models.CharField(max_length=20, blank=True)
    temperature = models.CharField(max_length=20, blank=True)
    heart = models.CharField(max_length=200, blank=True)
    lungs = models.CharField(max_length=200, blank=True)
    abdomen = models.CharField(max_length=200, blank=True)
    anaemia = models.CharField(max_length=100, blank=True)
    jaundice = models.CharField(max_length=100, blank=True)
    cyanosis = models.CharField(max_length=100, blank=True)
    oedema = models.CharField(max_length=100, blank=True)

    past_history = models.TextField(blank=True)
    present_history = models.TextField(blank=True)
    drug_history = models.TextField(blank=True)

    class_type = models.CharField(max_length=100, blank=True)
    ideal_weight = models.CharField(max_length=20, blank=True)
    weight = models.FloatField(blank=True, null=True)
    height_feet = models.FloatField(blank=True, null=True)
    height_inch = models.FloatField(blank=True, null=True)
    bmi = models.FloatField(blank=True, null=True)

    insulin = models.CharField(max_length=100, blank=True)
    z_score = models.CharField(max_length=100, blank=True)
    bmr = models.CharField(max_length=100, blank=True)
    edd = models.CharField(max_length=100, blank=True)
    last_visit = models.CharField(max_length=100, blank=True)
    paid_amount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.date}"
class HeaderFooter(models.Model):
    background_color = models.CharField(max_length=7, default="#FFFFFF")  # HEX value
    footer_text = models.TextField(blank=True)
    show_barcode = models.BooleanField(default=True)

    def __str__(self):
        return f"Header/Footer Settings (ID: {self.id})"


class TemplateData(models.Model):
    TEMPLATE_TYPES = [
        ('drug', 'Drug'),
        ('advice', 'Advice'),
        ('treatment', 'Treatment'),
        ('cc', 'C/C'),
        ('oe', 'O/E'),
        ('ix', 'I/X'),
    ]

    type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    content = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type}: {self.content}"

    