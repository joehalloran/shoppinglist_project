from django.test import TestCase
from django.urls import reverse

from lists.models import List, Item

class ListsViewsTest(TestCase):
	
	def test_lists_home_view(self):
		"""
		Test the home view opens and contains the correct text.
		"""
		url = reverse('home')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "list")
		

