# jolin-chan.github.io
Read Me - SleepS50

Link to our short video: https://youtu.be/5yeTnkuiNTc 

In order to run SleepS50, you’ll first need to set up Visual Studio Code on your computer locally. To do so:

Download Visual Studio Code: https://code.visualstudio.com/
Next, you’ll want to install some languages and extensions in order to run the files that SleepS50 needs. Be sure to pay attention to whether you are downloading a MacOS or Windows application. Install the following:
Hint: You can also follow along on this tutorial hosted by Harvard’s CS50 course if you would like: https://www.youtube.com/watch?v=aDx3EiIh1TM 
Download the latest version of Python: https://www.python.org/downloads/
Download the LTS version of Node.js: https://nodejs.org/en/
Pre-install SQLite3 by downloading: https://www.sqlite.org/download.html
Hint: If using a Macbook, download the “Precompiled Binaries for Mac OS X (x86)” 
Check to see where SQLite3 was stored on the computer by running 
which sqlite3

Copy the SQLite3 to the correct directory by running the following in your terminal:
cd ~/Desktop
ls
Cp sqlite3 / “refer to what 2cii. returned in the terminal”	
sudo

Download the Flask Python Library by running the following in your terminal:
pip3 install flask
pip3 install flask_session
pip3 install lib50

From here, you should be able to download the SleepS50 zip file and import it into your codespace. To run SleepS50, 
Change into the SleepS50 directory by executing the following in your terminal:
cd final

First set up an API key. You can do this by visiting: https://iexcloud.io/cloud-login#/register/ 
Next, create an “Individual” account by entering your name, email address, and a password
Once registered, opt to create a free plan by scrolling down to “Get started for free” and clicking “Select Start plan”
Check your email inbox to follow through the steps with the confirmation email that was sent
Visit: https://iexcloud.io/cloud-login?r=https%3A%2F%2Fiexcloud.io%2Fconsole%2Ftokens#/
Under the “Token” column, copy the key that begins with pk (this key will be referenced to as the value in the next step)
Now, in your terminal window, execute:
export API_KEY=value

Be sure to exclude any spaces immediately before or after the = sign
Lastly, execute:
flask run

in your terminal and a link should appear. Click on that link and it will take you directly to the SleepS50 website. 
Once you are on the website, you can read the introduction on the first page. First, register to create an account. Once you have done that, you will automatically be taken to the login page where you can login with the username and password that you just created. From there, you will be able to see the home page. At the top, you can use the navigation bar to navigate through the different pages that the website offers. For example:
On the diary tab, you can record your sleep for the previous night by answering the prompt questions
Once you have submitted a diary entry, you can go to the analysis tab to see a breakdown of your sleep analysis and trend based on the information that you have submitted thus far
You can also view a record of all of the diary entries that you have submitted on the log page
On the resources page, you can find some resources that you can take advantage of in order to improve your sleep. You can download audio files to save onto your phone as a ringtone or you can click on topics that you are interested in to find relevant information for it
And lastly, if you ever need to, you can always change your password on the change password tab

Additional:
If you wish to view the SQL tables for SleepS50 manually in your terminal, you can do so by executing the following in your terminal window:
sqlite3 sleeps50.db


SleepS50 is comprised of 3 tables- 
a users table that stores the user’s user id, username, and password
a diary table that stores the daily diary log of each user
a tips table that stores the links to various sleep aid resources 

You can view all of the entries in any of the 3 tables by executing the following:
SELECT * FROM table_name


If you only want to view specific entries or information, you can follow the standard SQLite syntax in order to call on them