from django.db import models

# Create your models here.
class District(models.Model):
    district_name = models.CharField(max_length=100)

    def __str__(self):
        return self.district_name

class Location(models.Model):
    location_name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return f"{self.location_name} - {self.district.district_name}"
    
    class Meta:
        ordering = ['district', 'location_name']
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
    
class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.subcategory_name
    




    