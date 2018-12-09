_____NavBar________
Instead of pure text Navbar, I use as many icons as possible.
After compare different icon method(inline SVG, icon sprite sheet, icon fonts), I choose the inline SVG at last.
Advantages: Easy to use, only one line for each icon; More freedom, I can use icons from different libraries, or even modify some of them and use my own version.

_______User Account________

User could update information and avatar image.

________Journal  Forum(Vibe)  Station_________
Journals and reports(comments,posts) are Paginated, so the interface is more clean and controlled.
I learned pagination and the routes for build a forum and the basic database from this series of Youtube videos by
Corey Schafer, it was really helpful:
https://youtu.be/MwZwr5Tvyxo

User can update or delete the report, journal, station they created. User_id is used for checking whether this user is the creator.
However, for station it is a little bit different, since the "update" and "delete" button is shown on the makers' info windows.
I cannot use session within JavaScript, so I send loggedIn and user_id information through flask template.

________User Public Profile, Station Public Profile______________

It would be useful if user can see other users' comments(reports), or all the events/journals of a station, so I created public profile for both
user and station, using similar templates as journal.html and forum.html.


________Database____________
Use relation database SQLAlchemy. 
Images are stored by name, which is a hex(for safe file name)
I used a lot of url_for to get the image path.


______MAP _______
The first technique issue is transferring data from python to JavaScript.
Google Map API initialize before DOM is ready for jQuery. So the jQuery's way of querying data
from database is not possible when the data is needed at initializing Google Map.
After serval tries, I endup choosing to use Jinja within JavaScript to jsonify data passed by flask template. I don't know
if there is better way to do it. At least this works, though the grammer is very wired(not recongnized by Text Editor).

The most difficult part in Map is to show information in different layers. 
1. Click the station marker, user will see a legend of this station through an infowindow.
On this infowindow there are three buttons link to other functions(update, delete, more info)
By default, Google Map API will remember the last clicked infowindow, so when there are two infowindows shown
on the map, if you click A, then hit the delete button on B's infowindow, then it is A that is deleted Instead of B.
To solve this problem, instead of setting different modals for each station, I choose to set the same shared modal for them.
When buiding the buttons on the infowindow, I attached a data attribute "data-station" to it. 
So when the modal is shown, it knows the button that triggered this event, through the data attribute,
the modal can figure out which station has triggered this event.

2. Click Calendar date, events will popup. 
The tech issue is the sequence of several related events. To achieve this, when calendar is being clicked, a global variable has to be called and changed to record which date
is clicked. This data has to be used when setting the infowindow open function. However, Google Map's Infowindow API do not provide information about whether the window is open or closed (Several related method are not documented),
so after each click, we have to clean the opened infowindows and then call new windows. I came up with using the same global variable, clean according to its current value, then change value,
and open new series of infowindows.

3. Calendar indicates which dates have events. 
This will enable more user-friendly interface. To achieve this, a JS set("eventDays") of date strings is created when initializing
the Calendar, so each time a calendar day cell is created, it will check if this date is in the 'eventDays', if so, it will add a speical
class to the attributes for later CSS manipulation.  

4. Map of differnt cities
To achieve rendering maps for three cities, I use extension of map template, which is already an extension of layout. 


