from django.db import models
class Projects(models.Model):
    name = models.CharField(max_length=250)
    registration_number = models.IntegerField()
    executor=models.CharField(max_length=100)
    okogu=models.CharField(max_length=100)
    customer=models.CharField(max_length=100)
    budget_type=models.CharField(max_length=100)
    nioktr_types=models.CharField(max_length=100)
    priority_directions=models.CharField(max_length=200)
    priority_directions_dop=models.CharField(max_length=200)
    critical_technologies=models.CharField(max_length=200)
    critical_technologies_dop=models.CharField(max_length=200)
    scientific_technology_prioritie=models.CharField(max_length=200)
    annotation=models.CharField(max_length=400)
    start_date=models.DateField()
    end_date= models.DateField()
    coexecutors=models.CharField(max_length=100)

