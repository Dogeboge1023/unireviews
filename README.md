# UniReviews - Unfiltered Student Reviews
## My First Work
#### Video Demo:  <https://youtu.be/C-5DR0mDu2s?si=HV9g7EDduqoFbTfj>
#### Description: University review website where students can review their universities, so other people read those reviews to choose which university they want apply to.

 Due to how the university application system works in my country (Georgia), this project could be very beneficial to many people in my country. Often, people don't know which university is right for them, so they are confused which university to pick. So my Website could be helpful to such people.
## Why It was made:
While trying to search for ideas, I was watching old CS50 fair videos where Harvard and Yale students were presenting their projects. I also watched several final projects from the Gallery of Final Projects. While trying to find an idea, I saw several videos with reviews of the website. I thought it would be interesting to make a review/rating website. But I wanted something that would be useful to people and also useful to me.

So for context, firstly, I am a freshman at Tbilisi, Georgia's Business and Technology University," and while I was trying to choose which university, It was a very frustrating experience to me since I really didn't know the opinion of the students from those universities that I was considering and had no friends who I could ask for a reliable opinion. So in the end, I just had to read old Facebook posts and just go by teachers and friends opinions, which I really didn't trust. In the end, I fairly like the university I chose, but with this website, I want to make this research part easier and less confusing or stressful for people who will be choosing their university in the future. 

## How It's Made:
**Tech used:** HTML 52.4%, Python 23.1%, CSS 20.3%, JavaScript 4.2%, SQL Database, Bootstrap <br>

Before starting this project, I had to make a finance assignment for CS50, where I learned how to use Python in a flask web application, which makes websites more interactive and interesting. This experience really helped me make this project. So from this experience, I wanted to make a flask website that I could stylize more and perform some other functions. Now I will discuss each file, my difficulties, and its design.

### <b>app.py:</b>
This is the file where all the logic is. At first, I deleted all the unnecessary parts from finance app.py, which I intended just for copying import statements and register logic that I wrote myself.

At first, I started making changes to the registration page. The biggest thing I changed there is probably JavaScript added, which dynamically checks if password and password confirmation are matching, if password is at least 8 characters, and if username is inputted. As you know, most of the websites now have an 8-character minimum on passwords since passwords with fewer characters might be unsafe, and it is better to use longer or more complex passwords. Also, I added a select form to choose which university student you are, which will play a crucial role on the index page. All of this is inserted into the SQL database.

Then we have review submission logic that isn't that interesting since it just inserts the review into the SQL table. It inserts values like which university they reviewed, the time they submitted the review, their user ID and post ID, as well as the rating of the university.

The index page logic is much more interesting. Since we captured during the registration at the university that the user is a student, now we can check if they are a student of the university they reviewed. This might be very beneficial to a lot of people because, of course, reviews coming From someone who is not a student at the university they are reviewing won't be very reliable.

Also, using Python, I made it so that it only shows the date of the submission rather than the exact time, including hours, minutes and seconds, which are not really necessary.

And the last feature I implemented was changing passwords. It's pretty simple due to check_password_hash from werkzeug.security. Also, I debated if people should be able to change their universities, since it might lead to misleading information since they can just avoid having "not a student of this university", so I chose that it would be better if they had to email support (me) to change their university. In my opinion, it might lead to fewer spam and trolling-type reviews.

### <b>unireviews.db:</b>
One of the most important files is unireviews.db. This is the place where all the data is saved, including  reviews, titles, ratings, passwords (of course hashed), and much more.

for reviews I had to create new table including many columns like: title, Univeristy, date, review, rating, student or not.
### <b>styles.css:</b>
This file stylizes the whole website, and I had a lot of fun stylizing each pixel of the website. Fonts, transparency and so on. Thanks to the Hype4.academy glassphormism generator, Google Fonts, and Bootstrap, I was able to make my website prettier. Also, using CSS it helped some textareas and other elements fit more on mobile.

## Lessons Learned:
While doing this project, I was using git to make commits and uploading it to GitHub. Since git and GitHub is such big part of software development.

Also, with this project, I learned many CSS tricks while researching interesting things to add to my website.

As well as whole CS50 course led to this project and my understanding that I really like working with software and computers. Thanks to David J. Malan
## Screenshots:
![homepagedesktop](https://github.com/Dogeboge1023/unireviews/assets/82914110/27b63842-ca9f-4d25-83b0-cbf7786ba714)
![reviewdesktop](https://github.com/Dogeboge1023/unireviews/assets/82914110/72ff39c3-f968-408c-9c5b-af9623ce6bb1)
![homepagephone](https://github.com/Dogeboge1023/unireviews/assets/82914110/6758e8ec-614b-4dcd-9f6d-f0fa6d9b5ab7)
![reviewphone](https://github.com/Dogeboge1023/unireviews/assets/82914110/78e5f649-cc62-4173-bdc7-35b9092e49d6)
## Stuff used:
**Glassmorphism CSS Generator:** https://hype4.academy/tools/glassmorphism-generator


**Google fonts and icons:** https://fonts.google.com/

**Bootstrap:** https://getbootstrap.com/

## This was CS50!



