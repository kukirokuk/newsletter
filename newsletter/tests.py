from django.test import TestCase
from django.utils import timezone
from newsletter.models import SignUp, Hobby
from django.core.urlresolvers import reverse
from newsletter.forms import SignUpVoteForm

class NewsletterModelTest(TestCase):
    def test_creating_a_new_signup_and_saving_it_to_the_database(self):
        # start by creating a new signup object 
        signup = SignUp()
        signup.email = "abc@yahoo.edu"
        signup.full_name = "Vasya"

        # check we can save it to the database
        signup.save()

        # now check we can find it in the database again
        all_signups_in_database = SignUp.objects.all()
        self.assertEquals(len(all_signups_in_database), 1)
        only_signup_in_database = all_signups_in_database[0]
        self.assertEquals(only_signup_in_database, signup)

        # and check that it's saved its two attributes: email and full_name
        self.assertEquals(only_signup_in_database.email, "abc@yahoo.edu")
        self.assertEquals(only_signup_in_database.full_name, signup.full_name)

    def test_verbose_name_for_pub_date(self):
        for field in SignUp._meta.fields:
            if field.name ==  'email':
                self.assertEquals(field.verbose_name, 'Email adress')

    def test_poll_objects_are_named_after_their_full_name(self):
        p = SignUp()
        p.full_name = 'Amerigo'
        self.assertEquals(unicode(p), 'Amerigo')

class HobbyModelTest(TestCase):

    def test_creating_some_hobbies_for_a_signup(self):
        # start by creating a new Poll object
        signup = SignUp()
        signup.email="abc@yahoo.edu"
        signup.full_name = "Amerigo"
        signup.save()

        # now create a Choice object
        hobby = Hobby()

        # link it with our Poll
        hobby.signup = signup

        # give it some text
        hobby.hobby = "Reading"

        # save it
        hobby.save()

        # try retrieving it from the database, using the signup object's reverse
        # lookup
        signup_hobbies = signup.hobby_set.all()
        self.assertEquals(signup_hobbies.count(), 1)

        # finally, check its attributes have been saved
        hobby_from_db = signup_hobbies[0]
        self.assertEquals(hobby_from_db, hobby)
        self.assertEquals(hobby_from_db.hobby, "Reading")

class HomePageViewTest(TestCase):

    def test_root_url_shows_all_signups(self):
        # set up some sigups
        signup1 = SignUp(email='fifa@yandex.edu', full_name='Filippo Insaghi')
        signup1.save()
        signup2 = SignUp(email='uefa', full_name="Cezaro Prandelli")
        signup2.save()

        response = self.client.get('/')

        # check we've used the right template
        self.assertTemplateUsed(response, 'home.html')

        # check we've passed the full names to the template
        full_names_in_context = response.context['queryset']
        self.assertEquals(list(full_names_in_context), [signup1, signup2])

        # check they are in our new subscribers section at the main page
        self.assertIn(signup1.full_name, response.content)
        self.assertIn(signup2.full_name, response.content)

        # check the page also contains the urls to individual signup pages
        signup1_url = reverse('newsletter.views.signup', args=[signup1.id,])
        self.assertIn(signup1_url, response.content)
        signup2_url = reverse('newsletter.views.signup', args=[signup2.id,])
        self.assertIn(signup2_url, response.content)

class SingleSignUpViewTest(TestCase):

    def test_page_shows_signup_title_and_no_votes_message(self):
        # set up two polls, to check the right one is displayed
        signup1 = SignUp(email='fifa@yandex.edu', full_name='Filippo Insaghi')
        signup1.save()
        signup2 = SignUp(email='uefa@yahoo.edu', full_name="Cezaro Prandelli")
        signup2.save()

        response = self.client.get('/signup/%d/' % (signup2.id, ))

        # check we've used the signup template
        self.assertTemplateUsed(response, 'signup.html')

        # check we've passed the right poll into the context
        self.assertEquals(response.context['signup'], signup2)

        # check the poll's question appears on the page
        self.assertIn(signup2.full_name, response.content)

    def test_page_shows_hobbies_using_form(self):
        # set up a signup with hobbies
        signup1 = SignUp(email='fifa@yandex.edu', full_name='Filippo Insaghi')
        signup1.save()
        hobby1 = Hobby(signup=signup1, hobby='Fishing')
        hobby1.save()
        hobby2 = Hobby(signup=signup1, hobby='Swimming')
        hobby2.save()

        response = self.client.get('/signup/%d/' % (signup1.id, ))

        # check we've passed in a form of the right type
        self.assertTrue(isinstance(response.context['form'], SignUpVoteForm))

        # and check the form is being used in the template,
        # by checking for the hobby text
        form = SignUpVoteForm(signup=signup1)
        print form.as_p()
        self.assertIn(hobby1.hobby, response.content)
        self.assertIn(hobby2.hobby, response.content)

class PollsVoteFormTest(TestCase):

    def test_form_renders_poll_choices_as_radio_inputs(self):
        # set up a signup with a couple of hobbies
        signup1 = SignUp(email='fifa@yandex.edu', full_name='Filippo Insaghi')
        signup1.save()
        hobby1 = Hobby(signup=signup1, hobby='Fishing')
        hobby1.save()
        hobby2 = Hobby(signup=signup1, hobby='Swimming')
        hobby2.save()

        # set up another poll to make sure we only see the right choices
        signup2 = SignUp(email='uefa@yahoo.edu', full_name="Cezaro Prandelli")
        signup2.save()
        hobby = Hobby(signup=signup2, hobby='Movies')
        hobby.save()

        # build a voting form for signup1
        form = SignUpVoteForm(signup=signup1)

        # check it has a single field called 'vote', which has right choices:
        self.assertEquals(form.fields.keys(), ['vote'])

        # choices are tuples in the format (choice_number, choice_text):
        self.assertEquals(form.fields['vote'].hobbies, [
            (hobby1.id, hobby1.hobby),
            (hobby2.id, hobby2.hobby),
        ])

        # check it uses radio inputs to render
        print form.as_p()
        # self.assertIn('type="radio"', form.as_p())
