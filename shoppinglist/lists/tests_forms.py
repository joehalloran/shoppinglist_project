from django.test import TestCase
from django.urls import reverse

from .models import List, Item

# forms test
class ListsFormsTest(TestCase):

	def setUp(self):
		"""
		Setup script: Create some example lists and items to test views.
		"""
		List.objects.create(
			name="First List", 
			owner="Joe Bloggs")
		p = List.objects.get(name="First List")
		Item.objects.create(
			name="Beef", 
			parentList=p)

	def test_formset_delete(self):
		parentList = List.objects.get(name="First List")
		item = Item.objects.get(name="Beef")
		form_data = {
			'item_set-TOTAL_FORMS': '1', 
            'item_set-INITIAL_FORMS': '0',
            'item_set-0-id': str(item.pk),
            'item_set-0-parentList': str(parentList.pk),
            'item_set-0-name': 'Beef',
            'item_set-0-DELETE': 'on',
			}
		response = self.client.post(reverse('lists:edit', kwargs={'pk':parentList.pk}), data=data, follow=True )
		self.assertEqual(Item.objects.count(), 0)
		

	def test_formset_rename(self):

		parentList = List.objects.get(name="First List")
		item = Item.objects.get(name="Beef")

		data = {
			'item_set-TOTAL_FORMS': '1', 
            'item_set-INITIAL_FORMS': '0',
            'item_set-0-id': str(item.pk),
            'item_set-0-parentList': str(parentList.pk),
            'item_set-0-name': 'Lamb',
            'item_set-0-DELETE': 'off',
			}
		response = self.client.post(reverse('lists:edit', kwargs={'pk':parentList.pk}), data=data, follow=True )
		newItem = Item.objects.get(id=item.pk)
		self.assertEqual(newItem.name, 'Lamb')
		
