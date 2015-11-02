from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
from .forms import ContactForm, SignUpForm
from .models import SignUp
from newsletter.forms import SignUpVoteForm

def home(request):
	title = "Sign Up now"
	form = SignUpForm(request.POST or None)
	queryset = SignUp.objects.all()
	context = { 
	  "form": form,
	  "title": title,
	  "queryset": queryset
}
	if form.is_valid():
		instance = form.save(commit=False)
		full_name = form.cleaned_data.get('full_name')
		if not full_name:
			full_name = "New full name"
		instance.full_name = full_name
		if not instance.full_name:
			instance.full_name =  "Jukline"
		instance.save()
		# print instance.email
		# print instance.full_name
		context = { 
	    	"template_title": "Thanks"
		}
	# if request.user.is_authenticated() and request.user.is_staff:
	

	return render(request, "home.html", context)

def signup(request, signup_id):
	signup = SignUp.objects.get(pk=signup_id)
	form = SignUpVoteForm(signup=signup)
	return render(request,'signup.html', {'signup': signup, "form": form})

def contact(request):
	title = 'Contact us'
	form = ContactForm(request.POST or None)
	if form.is_valid():
		form_email = form.cleaned_data.get("email")
		form_message = form.cleaned_data.get("message")
		form_full_name = form.cleaned_data.get("full_name")
		subject = 'Site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = (from_email, 'all-stick@ya.ru')
		contact_message = "%s: %s via %s"%(form_full_name, form_message, form_email)

		send_mail(subject, contact_message, from_email, [to_email], 
			fail_silently=False)

	context = {
		"form": form,
		"title": title

	}
	return render(request, "forms.html", context)
