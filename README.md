#  Shopping List Project

An example shopping list application for a Google Apprenticeship in Digital Innovation application by Joe Halloran. 

## Project Brief: Option 2 - App Engine

Build a simple webapp, using google app engine that provides users with an ability to keep track of a shopping list

Should be written in Python, Go, or Java.
* User must be able to add, delete and edit an item to the shopping list
* User must be able to view their whole shopping list
* User must be able to delete their whole shopping list (in addition to deleting individual items)
* Each user must be able to login with their Google account and their shopping list must persist between their logins

## Dependencies

* Django
* [oauth2client](https://github.com/google/oauth2client)
* Twitter Bootstrap
* jQuery
* (plus others python packages - see [requirements.txt](https://github.com/joehalloran/shoppinglist_project/blob/master/shoppinglist/requirements.txt))

### Why Django?
1. **It is Python**
(see brief above)
2. **Learn more Django:** I have been learning Django in my spare time so I wanted to continue and extend this learning. This project allowed me to show you want I know (OOP, SQL, etc…) and learn some things I don't:
  * **Complex model relationships:**
Django apps I’ve made so far have had very simple flat structures. This project required a hierarchical relationship between shopping list and list items.
  * **Google Open Authenticatication:**
This is new to me. I wanted to try and implement this.

3. **Test Driven Development:**
I want to practice the discipline of TDD. I like the Test -> Code -> Test cycle. I can see, if done well, it reduces the risk of new features breaking existing code.
4. **Complex forms:**
(see [Challenges faced in this project](https://github.com/joehalloran/shoppinglist_project#the-edit-list-form) section)

## Project structure:

### [shoppinglist.lists](https://github.com/joehalloran/shoppinglist_project/tree/master/shoppinglist/lists):
The workhorse of the entire application. It handles all list and item functionality.
* **views.py:** _This is the [most significant file](https://github.com/joehalloran/shoppinglist_project/blob/master/shoppinglist/lists/views.py) in the project. It contains most server side functionality._
* static/lists/lists.js: Custom js to create friendly UI.
* forms.py: Meta data for 'create list' form.
* models.py: Lists and Items.
* Various unit tests.
* urls.py: URL routing.


### [shoppinglist.config](https://github.com/joehalloran/shoppinglist_project/tree/master/shoppinglist/config):
Django settings files and base urls.py

### [shoppinglist.core](https://github.com/joehalloran/shoppinglist_project/tree/master/shoppinglist/core):
Contains:
* Project wide static files (css, js, etc...)
* Abstract models for other apps.
* Logout view

### [shoppinglist.static](https://github.com/joehalloran/shoppinglist_project/tree/master/shoppinglist/static):
Destination for Django collectstatic. See [Notes on deployment](https://github.com/joehalloran/shoppinglist_project#notes-on-deployment) below.

### [shoppinglist.templates](https://github.com/joehalloran/shoppinglist_project/tree/master/shoppinglist/templates):
Contains HTML.

## Challenges faced in this project

### Complex forms - the 'edit list' form:
The shopping list edit form required using [Django Formsets](https://docs.djangoproject.com/en/1.10/topics/forms/formsets/) to create a single form that allows users to edit the list items. This resulted in a [complex function](https://github.com/joehalloran/shoppinglist_project/blob/master/shoppinglist/lists/views.py#L96) that probably should be refactored. It also required creating the appropriate [javascript](https://github.com/joehalloran/shoppinglist_project/blob/master/shoppinglist/lists/static/lists/lists.js) to:
  * Switch between edit / view mode.
  * Delete items in a user friendly way.
  * Add infinite items to the list. Special attention had to be paid to the Django [ManagementForm](https://docs.djangoproject.com/en/1.10/topics/forms/formsets/#understanding-the-managementform) data.

### oAuth:
I had not done this before and was keen to implement this myself instead of using a third party Django app (e.g. [Django Social Auth](https://github.com/omab/django-social-auth)). After some tinkering and experimenting with [oauth2client](https://github.com/google/oauth2client) and ways to add [shopping lists to their ‘owners’](https://github.com/joehalloran/shoppinglist_project/blob/master/shoppinglist/lists/views.py#L60), I pleased to say this feature is working.

*(A bit presumptuous)*
I fear I have found some errors in [Google’s documentation](https://developers.google.com/api-client-library/python/guide/django). For example, the [FlowField](https://developers.google.com/api-client-library/python/guide/django#flows) method no longer exists in [oauth2client package](https://github.com/google/oauth2client). However, I defer to the wisdom of Google and expect I am probably wrong.

### Test Driven Development:
I found it hard to write tests on unfamiliar code (e.g. oAuth), as it is tricky to prempt exactly how the code would work (and therefore what to test). I was unable to ‘spoof’ Google authentication in tests, and therefore unable to write tests effectively.


## Potential improvements:

### Integrate Google authentication with django user model:
This would reduce the need for additional oauth2client.decorators on [views.py](https://github.com/joehalloran/shoppinglist_project/blob/master/shoppinglist/lists/views.py), it would also tidy up the link between lists and their owners (using the Django User model foreign key relationship). This would also resolve difficulties in testing. It would would be much easier to spoof a logged in user, employing built in Django functionality.

### Use Ajax to submit list forms without full POST request:
Submitting forms by AJAX would make the user experience much cleaner.

### UI:
The UI and site design could be much improved.

## Notes on development

Config.settings.dev requires [cloud sql proxy](https://cloud.google.com/sql/docs/sql-proxy) to connect to a remote Google SQL mysql database.

This may require stopping mysql service on development machine (if already listening on 127.0.0.1:3306).

```
sudo /etc/init.d/mysql stop
```

And to connect cloud_sql_server:

```
cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
```

See [GAE notes](https://cloud.google.com/python/django/flexible-environment) for full explanation:

## Notes on deployment:

This app uses The GAE Flexible Environment to allow use of Python packages not in the Standard Environment.

Here is the [GAE deployment guide](https://cloud.google.com/python/django/flexible-environment) used for as a basis this app.

### app.yaml:
The app.yaml is not included in this repository for security reasons. It contains sensititve environmental variables (e.g. Django SECRET_KEY, etc…)

### Static files:
Static files are served by GAE a storage bucket. To deploy:
```
python manage.py collectstatic
```
```
gsutil rsync -R static/ gs://<your-gcs-bucket>/static
```
### CORS configuration:
Bootstrap font face files, served with static files, were initially blocked by CORS. To resolve a custom CORS config was applied to the static files storage bucket. Note the [cors-config.json](https://github.com/joehalloran/shoppinglist_project/blob/master/shoppinglist/cors-config.json) in this repository.

To get current settings:
```
gsutil cors get gs://<bucket-name>
```
To set:
```
gsutil cors set cors-config.json gs://<bucket-name>
```

Notes:
* https://cloud.google.com/storage/docs/cross-origin
* https://cloud.google.com/storage/docs/gsutil/commands/cors
