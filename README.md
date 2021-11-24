# Expresso Blog Forked by *The Sad Hatters*

*The Sad Hatters*: Noakai Aronesty, Annabel Zhang  
SoftDev pd2  
K20 -- Throw Some Forking STUYLE On It  
2021-11-24

### Notes
- css folder inside static folder is cool. There aren't any other static files, but it's still a good practice
- The website works well without css, though the way in which blogs are created, in that you create a blog without creating the first entry, is strange.
- Without css, the links and texts are smaller and closer together, but usable. The logo is also enormous.
- We added our own css file and applied it to each html file for big improvements all around.

# Expresso Blog by Espresso
**Roster & Roles:**<br/>
*Daniel (Project Manager):* Managed front-end development (templating & styling) & worked on backend (routing, login & register, listing blog posts).<br/>
*Joshua:* Coded the basic functionality of the website as well as the file structure for storing blogs.<br/>
*Sophie:* Did lots of bugtesting. Wrote the about page.<br/>

### What is Expresso?
Expresso is a blogging website where you can create your own blog! Register for an account, name your blog, and you’re on your way to expressing yourself. The home menu will also display recent posts made by other people, while the Discover tab allows you to look at specific people, and what they’ve posted on their blog! Edit your posts at the click of a button and post whenever you feel like it!

### How does it work?

An SQLite Database stores 2 tables, USERS & POSTS. The USER table contains the User ID (UID), the username, the password, the blog name, and the number of posts in their blog. This allows the website to display the posts in reverse chronological order. POSTS is used to store the information about each post, although the text itself is not stored. This table stores the date and time the post was created, the UID of the user who made it, the post number in the blog, and the title of the post. The text of each post is stored in a separate folder, called blogs. This folder has a separate folder for each UID, labeled accordingly. Posts are stored as text files in these folders, keeping them from slowing the database down as the amount of posts gets larger.

## Setting up 
```bash
# Get repo
git clone https://github.com/sookiemonster/Expresso-Blog.git
cd Expresso-Blog/app
```

<b>Highly suggested to run this in a virtual environment</b>
```bash
pip install virtualenv
python3 -m venv venv
```
```bash
source ./venv/bin/Activate # Linux/macOS/Git Bash
```
```bash
.\venv\Scripts\Activate # Windows CMD
```

Install dependencies
```bash
pip install -r requirements.txt
```

Run __init__.py
```bash
python3 __init__.py
```
