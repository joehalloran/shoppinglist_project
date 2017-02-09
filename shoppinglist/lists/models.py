from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible

from core.models import TimeStampedModel

@python_2_unicode_compatible  # only if you need to support Python 2
class List(TimeStampedModel):

	name = models.CharField(max_length=200)
	owner = models.EmailField()
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('lists:edit', args=[str(self.id)])

@python_2_unicode_compatible  # only if you need to support Python 2
class Item(TimeStampedModel):

	name = models.CharField(max_length=200)
	parentList = models.ForeignKey(
        'List',
        on_delete=models.CASCADE,
    )
	
	def __str__(self):
		return self.name