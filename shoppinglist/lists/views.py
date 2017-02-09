from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render
from django.forms import inlineformset_factory, modelformset_factory, TextInput, HiddenInput
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from django.forms.formsets import DELETION_FIELD_NAME

from oauth2client.contrib.django_util import decorators
from oauth2client import client

from .models import List, Item
from .forms import ListCreateForm


class MyListView(ListView):
    """
    The /mylists/ root. Lists lists I own.
    """
    model = List
    template_name = 'lists/mylists.html'
    context_object_name = 'mylists'

    @method_decorator(decorators.oauth_required())
    def dispatch(self,request,*args,**kwargs):
        return super(MyListView,self).dispatch(request,*args,**kwargs)

    def get_queryset(self):
        return List.objects.filter(owner = self.request.oauth.credentials.id_token['email'])

class ListCreate(SuccessMessageMixin, CreateView):
	template_name = 'lists/create_form.html'
	form_class = ListCreateForm
	success_message = "List Created. Now you can add some items."

	@method_decorator(decorators.oauth_required())
	def dispatch(self,request,*args,**kwargs):
		return super(ListCreate,self).dispatch(request,*args,**kwargs)

	def form_valid(self, form):
		form.instance.owner = self.request.oauth.credentials.id_token['email']
		return super(ListCreate, self).form_valid(form)

class ListDelete(DeleteView):
	model = List
	success_url = reverse_lazy('lists:mylists')
	success_message = "Your list deleted successfully."

	@method_decorator(decorators.oauth_required())
	def dispatch(self,request,*args,**kwargs):
		current_user = request.oauth.credentials.id_token['email']
		parentList = self.get_object()
		if current_user != parentList.owner and not request.user.is_superuser: 
			raise PermissionDenied

		return super(ListDelete,self).dispatch(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(ListDelete, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		context['items'] = Item.objects.filter( parentList = self.get_object() )
		return context

	## TODO: CHECK OWNERSHIP

	def delete(self, request, *args, **kwargs):
		"""
		Work around as SuccessMessageMixin does not work with DeleteView
		"""	
		messages.success(self.request, self.success_message)
		return super(ListDelete, self).delete(request, *args, **kwargs)

@decorators.oauth_required
def editListView(request, pk):
	"""
	Create / process form to edit all items in list.
	"""
	# Get current user and list object to check ownship
	current_user = request.oauth.credentials.id_token['email']
	parentList = List.objects.get(pk=pk)
	if current_user != parentList.owner and not request.user.is_superuser: 
		raise PermissionDenied

	# Generate formset for the parent list, so we can edit the list name
	ListFormSet = modelformset_factory(
		List, 
		fields=("name",),
		extra=0,
		widgets={
    		'name': TextInput(attrs={'class': 'form-control form-title form-inactive', 'required': True}),
    		}
		)

	itemCount = Item.objects.filter(parentList = parentList).count()
	if itemCount > 0:
		extraItemField = 0
	else:
		extraItemField = 1 

	# Generate the formset of list member items, so we can edit the shopping list
	ItemInlineFormSet = inlineformset_factory(
		List, 
		Item, 
		fields=("name", "parentList"), 
		extra=extraItemField, # Extra items will be added through JS
		widgets={
    		'name': TextInput(attrs={'class': 'form-control form-inactive', 'required': True}),
    		}
    	)
	# if POST generate form data and save if valid
	if request.method == 'POST':
		item_formset = ItemInlineFormSet( request.POST, instance=parentList )
		list_formset = ListFormSet( request.POST, queryset= List.objects.filter(pk=pk) )
		if item_formset.is_valid() and list_formset.is_valid():
			### TODO: TRANSACTIONS
			item_formset.save()
			list_formset.save()
			# Redirect to list page.
			return HttpResponseRedirect(reverse('lists:edit', kwargs={'pk':pk}))
		else:
			## TODO Handle error by empty fields
			messages.error(request, formset.errors)
			return HttpResponseRedirect(reverse('lists:edit', kwargs={'pk':pk}))
	# if a GET (or any other method) create a blank form
	else:
		# Limit list items to only include parent list members (not from any old list)
		item_formset = ItemInlineFormSet( instance=parentList )
		# Limit list item to one. We only want to edit the title of the current list
		list_formset = ListFormSet( queryset= List.objects.filter(pk=pk) )
		return render(request, 'lists/item_form.html', {
			'item_formset': item_formset, 
			'list_formset': list_formset, 
			'mylist': parentList}) # Is parentList necessary (if all the work is done by the form )



            