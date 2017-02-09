from django.test import TestCase

from .models import List, Item

# models test
class ListModelsTest(TestCase):

	def setUp(self):
		"""
		Setup: Create a list with one item as member.
		"""
		List.objects.create(
			name="First List", 
			owner="Joe Bloggs")
		p = List.objects.get(name="First List")
		Item.objects.create(
			name="First Item", 
			parentList=p)

	def test_list_creation(self):
		"""
		Test list is a List and correct name is returned.
		"""
		p = List.objects.get(name="First List")
		self.assertTrue(isinstance(p, List))
		self.assertEqual(p.__unicode__(), "{}".format(p.name))

	def test_item_creation(self):
		"""
		Test item is an Item and correct name is returned.
		"""
		p = Item.objects.get(name="First Item")
		self.assertTrue(isinstance(p, Item))
		self.assertEqual(p.__unicode__(), "{}".format(p.name))