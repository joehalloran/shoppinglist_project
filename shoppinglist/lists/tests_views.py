from django.test import TestCase
from django.urls import reverse

from .models import List, Item

class ListsViewsTest(TestCase):

	def setUp(self):
		"""
		Setup script: Create some example lists and items to test views.
		"""

		List.objects.create(
			name="First List", 
			owner="joe@example.com")
		p = List.objects.get(name="First List")
		for i in range(10):
			Item.objects.create(
				name="Item " + str(i), 
				parentList=p)
		List.objects.create(
			name="Second List", 
			owner="jane@example.com")
		q = List.objects.get(name="Second List")
		for i in range(10,20):
			Item.objects.create(
				name="Item " + str(i), 
				parentList=q)

	def test_mylists_view(self):
		"""
		Test mylists view returns lists.
		"""
		url = reverse('lists:mylists')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "First List")
		self.assertNotContains(response, "Second List")

	def test_lists_edit_view(self):
		"""
		Test mylists edit view returns list, list items, and a save but.
		"""
		l= List.objects.get(name="First List")
		url = reverse('lists:edit', args=[l.id])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "First List")
		self.assertContains(response, "Item 0")
		self.assertContains(response, "Item 9")
		self.assertContains(response, "Save")

	def test_lists_edit_view_does_not_contain_items_from_other_lists(self):
		"""
		Test mylist edit view does include items in other lists.
		"""
		l= List.objects.get(name="First List")
		url = reverse('lists:edit', args=[l.id])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, "Second List")
		self.assertNotContains(response, "Item 10")
		self.assertNotContains(response, "Item 19")
