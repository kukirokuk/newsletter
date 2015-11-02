from django import forms

from .models import SignUp

class ContactForm(forms.Form):
	full_name = forms.CharField(required = False)
	email = forms.EmailField()
	message = forms.CharField()


		
class SignUpForm(forms.ModelForm):
    class Meta:
	model = SignUp
	fields = ['email', 'full_name']

    def clean_email(self):
	email = self.cleaned_data.get('email')
	email_base, provider = email.split("@")
	domain, extension = provider.split('.')
	if not extension == "edu":
	    raise forms.ValidationError("Pleasae use a valid .edu collage email")
	return email

    def clean_full_name(self):
	full_name = self.cleaned_data.get('full_name')
	return full_name

class SignUpVoteForm(forms.Form):
    vote = forms.ChoiceField(widget=forms.RadioSelect())
    def __init__(self, signup):
        forms.Form.__init__(self)
        self.fields['vote'].hobbies = [(c.id, c.hobby) for c in signup.hobby_set.all()]