from collections import namedtuple
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

SignUpinfo = namedtuple('SignUpinfo', ['email', 'full_name', 'hobbies'])
Person_1 = SignUpinfo(
    email="person_1@gmail.edu",
    full_name="Petro Shchur",
    hobbies=[
        'Fishing',
        'Skating',
        'Coocking',
    ],
)
Person_2 = SignUpinfo(
    email="person_2@gmail.edu",
    full_name="Mykola Firman",
    hobbies=[
        'Smoking',
        'Swimming',
        'Painting',
    ],
)

class SignUpTest(LiveServerTestCase):
    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def DONTtest_can_create_new_poll_via_admin_site(self):
        # Gertrude opens her web browser, and goes to the admin page
        self.browser.get(self.live_server_url + '/admin/')

        # She sees the familiar 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # She types in her username and passwords and hits return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('sashok')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('222')
        password_field.send_keys(Keys.RETURN)

        # her username and password are accepted, and she is taken to
        # the Site Administration page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)


        #She now sees a couple of hyperlinks that says "Sign ups"
        signups_links = self.browser.find_elements_by_link_text('Sign ups')
        self.assertEquals(len(signups_links), 1)

        # She click at this link
        signups_links[0].click()

        #She is taken to the singnups listing page, which shows she has no singups yes
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 sign ups', body.text)

        # She sees a link to 'add ' a new signup, so she clicks it
        new_signup_link = self.browser.find_elements_by_link_text('Add sign up')
        new_signup_link[0].click()

        # She sees some input fields for "Email" and "Full name"
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Email adress:', body.text)
        self.assertIn('Full name:', body.text)

        # She types in an her email and her full name
        full_name_field = self.browser.find_element_by_name('email')
        full_name_field.send_keys("absssx@usc.edu")
        email_field = self.browser.find_element_by_name('full_name')
        email_field.send_keys("Amerigo Vespucci")

        # She sees she can enter Hobbies for the Sign up.  She adds three
        hobby_1 = self.browser.find_element_by_name('hobby_set-0-hobby')
        hobby_1.send_keys('Basketball')
        hobby_2 = self.browser.find_element_by_name('hobby_set-1-hobby')
        hobby_2.send_keys('Music')
        hobby_3 = self.browser.find_element_by_name('hobby_set-2-hobby')
        hobby_3.send_keys('Science fiction')

        # Gertrude clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()

        #She is returned to the "signups" listing, where she can see her new sing up
        new_signup_link = self.browser.find_elements_by_link_text("Amerigo Vespucci")
        self.assertEquals(len(new_signup_link), 1)

    def _setup_signups_via_admin(self):
        # Gertrude logs into the admin site
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('sashok')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('222')
        password_field.send_keys(Keys.RETURN)

        # She has a number of signups to be done.  For each one, she:
        for signup_info in [Person_1, Person_2]:
            # Follows the link to the Signup app, and adds a new signup
            self.browser.find_elements_by_link_text('Sign ups')[0].click()
            self.browser.find_element_by_link_text('Add sign up').click()

            # Enters its name, and uses the 'today' and 'now' buttons to set
            # the publish date
            email_field = self.browser.find_element_by_name('email')
            email_field.send_keys(signup_info.email)
            full_name_field = self.browser.find_element_by_name('full_name')
            full_name_field.send_keys(signup_info.full_name)

            # Sees she can enter hobbies for the Sigup on this same page,
            # so she does
            for i, hobby_text in enumerate(signup_info.hobbies):
                hobby_field = self.browser.find_element_by_name('hobby_set-%d-hobby' % i)
                hobby_field.send_keys(hobby_text)

            # Saves her new signup
            save_button = self.browser.find_element_by_css_selector("input[value='Save']")
            save_button.click()

            # Is returned to the "Sign up" listing, where she can see her
            # new sig up, listed as a clickable link by its name
            new_signup_links = self.browser.find_elements_by_link_text(
                    signup_info.full_name
            )
            self.assertEquals(len(new_signup_links), 1)

            # She goes back to the root of the admin site
            self.browser.get(self.live_server_url + '/admin/')

        # She logs out of the admin site
        self.browser.find_element_by_link_text('Log out').click()


    def test_voting_on_a_new_poll(self):
        # First, Gertrude the administrator logs into the admin site and
        # creates a couple of new Polls, and their response choices
        # self._setup_signups_via_admin()

        # Now, Herbert the regular user goes to the homepage of the site. He
        # sees a signup form
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Email adress*', body.text)
        self.assertIn('Full name', body.text)

        # He types in his email and his full name and if sign up form will dissaper 
        # then he is signuped succesfully
        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys('herbi@yandex.edu')
        full_name_field = self.browser.find_element_by_name('full_name')
        full_name_field.send_keys('Herbert')
        save_button = self.browser.find_element_by_css_selector("input[value='SignUp']")
        save_button.click()


        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Email adress*', body.text)
        self.assertNotIn('Full name', body.text)
        
        #He checks the video at the main page
        self.browser.find_element_by_tag_name('iframe').click()
        self.browser.implicitly_wait(3)
        
        # Now, Herbert the regular user goes to the homepage of the site. He
        # sees a list of new subscribers.
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Our new subscribers', body.text)
        self.browser.find_element_by_link_text('Herbert').click()

        # He is taken to a signup page
        main_heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(main_heading.text, 'Our recent subscribers')

        # He also sees a form, which offers him several choices.
        # There are three options with radio buttons
        choice_inputs = self.browser.find_elements_by_css_selector(
                "input[type='radio']"
        )
        self.assertEquals(len(choice_inputs), 3)

        # The buttons have labels to explain them
        choice_labels = self.browser.find_elements_by_tag_name('label')
        choices_text = [c.text for c in choice_labels]
        self.assertEquals(choices_text, [
            'Very awesome',
            'Quite awesome',
            'Moderately awesome',
        ])
        # He decided to select "very awesome", which is answer #1
        chosen = self.browser.find_element_by_css_selector(
                "input[value='1']"
        )
        chosen.click()

        # Herbert clicks 'submit'
        self.browser.find_element_by_css_selector(
                "input[type='submit']"
            ).click()

        # The page refreshes, and he sees that his choice
        # has updated the results.  they now say
        # "100 %: very awesome".
        self.fail('TODO')

        # The page also says "1 votes"

        # Satisfied, he goes back to sleep