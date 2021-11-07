Link to my project video: https://www.youtube.com/watch?v=c-xZ175TNhQ

Things to do before accessing the website:

It seems that, when run on Safari, the inputs with type date do not offer a popup calendar (which can occasionally cause an error), but will format correctly when run on Chrome.
This website should therefore be run on Chrome.

For my final project, I created a website to track plant information (specifically watering times) using python, Flask, HTML, and CSS. Before running my website, you must first
ensure that all of the packages listed in requirements.txt are installed, particularly the pytz package; to do this, run "pip install pytz'' in your terminal. Ensure that all of
the other packages listed are also installed. Now, unzip the project folder and make your current directory the project folder (“cd project”). Then, begin flask by typing “flask
run” into your terminal, and click on the link that is printed out to view the website.

Login, Register, plant.html, and Logout:
After following the link, you should be at a login page. Because you do not have an account yet, you must register before logging in. In the top right corner, there is a “Register”
option; click this and enter your desired username, password (which must match with the “Password (again) input), and current timezone. When the account information is satisfactory,
click the Register button. Now, you will be logged in and on the home page. Whenever on a different page of the website, clicking the “PlantMom.com” in the left of the navigation bar
will take you back to the home page. Log out anytime by clicking the “Logout” in the top right corner and can log back in by entering your registered username and password on the” Log
In” page.

Add Plant:
Because you haven't added any plants the home page will say “Whoops, looks like you don’t have any plants added!” To add some plants, click the “Add Plant” button in the top left of the
navigation bar. Enter the plant name, how often you water the plant in an integer frequency of days (for example, if you water your plant every 3 days, you’d enter 3) and the start date
of the watering schedule for this plant. After adequately filling out these fields, hit the “Add Plant” button, and you will be redirected to the homepage where the name of your plant and
the next upcoming watering date of the plant are displayed under “My Plants”.

Delete Plant:
In the navigation bar, there is also a “Delete Plant” option. If your plant dies, you can delete it from your plant list: click the “Delete Plant” button, and you will be at a page with a
drop down menu that lists all of your plants. Select the one you want to delete and click the “Delete Plant” button. You will then be redirected to the homepage where your deleted plant is
no longer listed.

Edit Plant:
You can also edit the properties of a plant with the “Edit Plant” option in the navigation bar. This will take you to a page where you select the plant you wish to edit from a drop down menu.
Then, fill out the field or fields that you want to change (name, frequency or start date) and submit the “Make changes” button. You will be redirected to the homepage where the plant has been
updated accordingly.

Plant Journal:
The Plant Journal page also allows you to leave notes about your plants; click on the “Plant Journal” button in the navigation bar to go to a page that says “No entries yet!” To add an entry,
click on the new entry button and complete the title and entry areas. Hit the “Add Entry” button, and you will be brought back to the journal page that has a collapsable list of your journal
entries. To delete an entry, click the “Delete Entry” button and then select the entry you wish to delete from the dropdown and click the delete entry submit button. You will be redirected to
the Plant Journal page where you will see your listed entries without the deleted one.



