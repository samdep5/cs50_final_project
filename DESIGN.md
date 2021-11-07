General structure (folders and languages) and requirements.txt :
To implement my website I used an assortment of python, flask, SQL, HTML, and CSS. The file requirements.txt lists all of the libraries imported for the application.
In the folder titled “static” are the images that were used as the background and icon of the website along with the styles.css file where I added custom style choices.
In the templates folder, there are the 11 pages that all make up the website and are used for different paths. Then there is also the helpers.py folder and application.py
folders that have the Python code for the web server.

SQLite database plants.db:
For storing the data from entries in the website, a SQLite database was used called plants.db that consisted of the tables users, plant, and journal. The user table stores
the integer primary key id, text-type username, text-type hash of the entered password, and text timezone that corresponds to a timezone in the pytz library. The plant table
stores the integer primary key id, the integer user_id that matches the id in the user table, thus linking a plant to a specific user, frequency integer for the frequency of
watering in days, and date-type field startdate that allows the user to set the date of the plant’s first watering. The journal table features an integer primary key id, a
text field title for the title of the journal entry, a text field entry for the body of the journal entry, a user_id that corresponds to the id in the users table that connects
a journal entry to a user, and a date field date that sets the current date considering the set time zone.

helpers.py and apology.html:
In the helpers.py folder, the function login_required() is defined, which is used throughout the application.py paths to ensure a user is signed when accessing all pages besides
the register (register.html) and login (login.html) pages. This means that a user has access to only their plants and can not see other user’s information. This file helpers.py
also defines apology(), which returns the customized error page apology.html. The function ensures that special characters do not alter the error message and renders the
apology.html page. The apology.html page features an image of some potted plants that is displayed along with an error message and code that changes depending on the parameters
entered in the apology() function. For example, apology(‘username is taken’) would take you from the current webpage to a page with the ‘username is taken’ message, errorcode,
and image are displayed, allowing the user to see why the website denied their request and how to fix the request.

layout.html:
The file layout.html is fairly integral to the website because the other html pages that make up the website begin by “extending” layout.html and including the file’s code at the
top of the page. This sets up the view of the webpage and links the styles.css file, bootstrap documentation, and web icon to each file to be displayed on each page of the website.
It also sets up a customized title for each page and creates a navigation bar with the Register and Login elements if the user is not logged in and the Add Plant, Delete Plant, Edit
Plant, and Plant Journal elements on the left and Logout on the right. The navigation bar allows the user to easily move between different pages of the website to access different
features. Layout.html also displays alerts at the top of the page if the flash() function is called in the pathway, giving users confirmation that their actions were recorded.

login (login.html and login() in application.py):
When a user first loads the webpage, they are taken to the rendered login.html page via a GET request that routes through the login() function in application.py. Login.html consists
of two inputs of type text that a user can enter a username and password into. When they hit the submit button, the submission occurs via a POST request. With the POST request, in the
login() function any previous user is forgotten, the username and password input values are checked to make sure they aren’t empty, and the username and password are compared against
the users saved in the users table to check for an existing user with the same password hash. Once validated, the user will be logged in and taken to the plant.html homepage.

register (register.html and register() in application.py):
To register for an account, a person must click on the register button in the navigation bar on the login page, which will take them to register.html via a GET request where there are
text fields to enter their username, password and password confirmation and a drop down menu (used to prevent errors that would likely occur in a text entry) to select their time zone
(each entry corresponds to a timezone in the pytz library). A user would fill out the data and submit it via POST. Then, after ensuring the entries are not empty, the password and
confirmation password components match, and the username is not taken, the username, hashed password, and pytz timezone text value are saved in the users table. The user is now logged
in and redirected to the plant.html page (the home page).

plant (plant.html and plant() in application.py)
After a user is logged in, they are taken to the plant.html page via a GET request. In the plant.html page, an if condition is established where a message According to the Jinja if
statement in the plant.html page, if no plants have been entered the page should read “Whoops, looks like you don't have any plants added!” so that it isn’t empty. When there are plants
corresponding to the particular user, the next watering date for a plant is calculated (considering timezone) accordingly:
- If the start date occurs after the current date (current date - start date is negative) the start date is the next watering day
- If the current date - start date divided by frequency has no remainder, the current day is the watering day
- If current date - the start date is greater than the frequency, the next watering date is calculated by subtracting the remainder when current date - start date is divided by the
  frequency
- If the current date - start date is less than the frequency, the next watering date is the current date plus the frequency minus (current date - start date)
Calculating it this way allowed for the consideration of timezone. Based on these conditions, the next watering date is calculated and appended to the dictionary of a single plant's
attributes within the list of all of the user’s plants. Then, in the plant.html page a for loop (which was used for efficiency) loops through the plants list of each plant and its
attributes and displays the name and next watering time of the plant.

addplant (addplant.html and addplant() in application.py):
To add a plant, a person must click on the Add Plant button in the navigation bar once logged in, which will take them to addplant.html via a GET request where there is a text field
to enter the plant name, a number field to enter the watering frequency as a positive integer (using this form type with a min of 1 prevents decimal or negative entries), and the start
date as a date (using a date form type ensures the date format will be correct and the popup calendar is user-friendly). A user would fill out the data and submit it via POST. Then,
after ensuring the entries are not empty, the plant name is not a copy for the user, the user’s id, plant name, watering frequency and start date are saved in the users table. The user
is now redirected to the plant.html page (the home page) where their newly added plant is listed.

editplant (editplant.html and editplant() in application.py):
To edit a plant, a person must click on the Edit Plant button in the navigation bar once logged in which will take them to editplant.html via a GET request. If there are no plants logged
by the user, the page will display “There aren’t any plants to edit yet!” which prevents users from filling out blank forms. If there are plants, the page displays a drop down to choose
which of the user’s plants will be edited (which is created using a for loop in Jinja), followed by the same type of forms that were in the addplant.html. A user would fill out the data
and submit it via POST. Then, after ensuring a plant was selected, and at least one field is changed, each form is checked for input and the table updated accordingly. I used a counter
to determine if at least one field is changed and prevented repetitively checking for each form being empty. The user is now redirected to the plant.html page (the home page) where their
newly updated plant is listed.

deleteplant (deleteplant.html and deleteplant() in application.py):
To delete a plant, a person must click on the Delete Plant button in the navigation bar once logged in which will take them to deleteplant.html via a GET request. If there are no plants
logged by the user, the page will display “There aren’t any plants to delete yet!” which prevents users from interacting with blank forms. If there are plants, the page displays a drop
down to choose which of the user’s plants will be deleted (which is created using a for loop in Jinja). A user would select the desired plant and submit it with the button via POST. Then,
after ensuring a plant was selected, the plant is deleted from the plant table. The user is now redirected to the plant.html page (the home page) where their deleted plant is no longer
listed.

journal (journal.html, journalentry.html, deletejournal.html and journal(), journalentry(), deletejournal() in application.py):
To access the journal, a user must click on the Plant Journal button in the navigation tab. Using a Jinja if statement, if there are no journal entries the page will say “No entries yet!”
However, if there are journal entries they will be displayed in a collapsible accordion of entries that list the entry date (which was determined using the datetime and pytz libraries to
ensure timezone sensitivity) followed by the title that  the text entry is collapsible into. With this structure, a user can see the title and date of their entries and locate desired
entries more easily. On this journal.html page are also two buttons: a New entry button that takes the user to journalentry.html and a Delete entry button that takes the user to
deletejournal.html.

When the New entry button is pressed, the user is taken to a page where they can enter a title in a text input and a larger text area element that allows for the user to type more for
their notes. When the user submits this via the Add Entry button and requests via POST, it is checked that the title and entry fields have input, the current date considering the
timezone is calculated, and then a journal entry with the current date, entry input, and title input is added to the journal database and the user is redirected to journal.html where
their entry is displayed.

When the Delete entry button is pressed and deletejournal.html requested via GET, the user is taken to a page where the date and title of each data entry is displayed in a dropdown form
for the user to select. The user can select the entry they wish to delete and submit the button, requesting via POST. It is ensured that an entry was selected, and, if so, the entry is
deleted from the journal table. The user is redirected to journal.html where their deleted entry is no longer displayed.

styles.css and general style:
For style, I relied a lot on the form and button formatting from bootstrap under the “form-group” and “form-control” and “btn btn-success” classes respectively. I also used the
accordion style from bootstrap for the journal entries to make it as easy to navigate and read as possible. I also used an override for some of bootstraps colors or styles to fit the
plant aesthetic; for example, I made sure that the form entries glowed green when selected instead of blue. I also set an image of some plant leaves as the background of my website to
make it more pleasing than a simple white background.









