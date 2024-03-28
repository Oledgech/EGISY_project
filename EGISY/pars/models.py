from django.db import models
class Projects(models.Model):
    name = models.TextField(null=True)
    registration_number = models.CharField(max_length=100,null=True)
    executor=models.CharField(max_length=400,null=True)
    okogu=models.TextField(null=True)
    customer=models.CharField(max_length=200,null=True)
    budget_type=models.CharField(max_length=400,null=True)
    nioktr_types=models.CharField(max_length=400,null=True)
    priority_directions=models.TextField(null=True)
    priority_directions_dop=models.TextField(null=True)
    critical_technologies=models.TextField(null=True)
    critical_technologies_dop=models.TextField(null=True)
    scientific_technology_prioritie=models.TextField(null=True)
    annotation=models.TextField(null=True)
    start_date=models.DateField(null=True)
    end_date= models.DateField(null=True)
    coexecutors=models.TextField(null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Проект'
        verbose_name_plural = 'Проекты'


