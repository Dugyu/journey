What have you not done for your project yet?
The profile page should include links to recent events journal in this station.



Create Journal Function I feel this is really hard...If I want to allow user to add styles, images, links, etc... Option 1: Rich Text content, use Rich Text Editor API, store text and image data as Blob. Option 2: Separate text and images, store images by their name, and later use url_for to call them.

Either is difficult if I want user has ability to edit their posts later.

What problems, if any, have you encountered?
Add overlay content. I want the calendar node overlay on the map.
Rich text editor, how to store rich text content in database, specifically in Sqlite3. Text? String(for image)? Blobs?

What have you done for your project so far?
Completed environments setup in VS Code(Python, Flask, SQLAlchemy, Sqlite3).
Completed Website navbar and templates with use of a lot of SVG icons, built a basic database.
Completed User login logout with Ajax, profile page, update username, email, profile image
Completed Report and Forum part, user could add comment to city and it will be shown in Vibe(forum) with their avatars, from the latest to the oldest, with pagination. User can update and delete their comments. User can click 1 user and see all the comments of this specific user.
Completed 90% of Map part. Now a Customized Style Google Map is shown in /Map/city, user could select which city they want to render through a dropdown menu, and user could submit Stations(title, location, timeinfo, basic info, image)， which will then be rendered on the map as customized markers and infowindows. 

Completed Populate comments on the map (as small and low opacity markers) according to their geolocation. (So before post comments, the browser will ask users to allow using their locations. It could also have a customzize location input, so user could hide their real location if they want)

Completed Station introduction(profile) page, shown as a Modal once user clicked link in the marker's info window.

Calendar and events journal. Plan to build a calendar(On the Map Page) through html and css. Show events on calender.Click on a specific date of Calendar, those stations that host events on that dates will have popups on the Map.