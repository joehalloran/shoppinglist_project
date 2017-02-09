from django.http import HttpResponseRedirect
from django.urls import reverse

from oauth2client.contrib.django_util import decorators

@decorators.oauth_required
def logout(request):
    if request.oauth.has_credentials():
    	response = HttpResponseRedirect(reverse('home'))
    	response.delete_cookie('sessionid')
    	return response


            