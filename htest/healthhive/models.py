from django.db import models

# Create your models here.
class ActiveIngredient (models.Model):
	drug_code = models.IntegerField(default=0)
	active_ingredient_code = models.IntegerField(default=0)
	ingredient = models.CharField(max_length=240)
	ingredient_supplied_ind = models.CharField(max_length=1)
	strength = models.CharField(max_length=20)
	strength_unit = models.CharField(max_length=40)
	strength_type = models.CharField(max_length=40)
	dosage_value = models.CharField(max_length=20)
	base = models.CharField(max_length=1)
	dosage_unit = models.CharField(max_length=20)
	notes = models.CharField(max_length=2000)

