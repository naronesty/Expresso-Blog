from flask import Flask, render_template, request, session, redirect
import os, sqlite3

# DEFINE CONSTANTS
USER_TABLE = "USERS"
DB_FILE = "users.db"

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/", methods=["GET"])
def home():
    if (session['username']):
        return render_template("home.html") # Render home if user is logged in
    return render_template("login.html") # Render login page if not logged in

@app.route("/my_blog", methods=["GET"])
def user_blog():
    # Retrieve & render user's blog if they are logged in
    if (session['username']): 
        files = []
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        get_UID = "SELECT UID FROM %s WHERE USERNAME = %s" % (USER_TABLE, session['username'])
        c.execute(get_UID)
        uid = c.fetchone()

        get_last_post_num = "SELECT LAST_POST_NUM FROM %s WHERE id = %s" % (USER_TABLE, uid)
        c.execute(get_last_post_num)
        last_post_num = c.fetchone()

        for post_num in range(last_post_num, -1, -1): # Descend from the last post to 0
            post = open("./blogs/%s/%s.txt".format(uid, post_num))
            files.append(post.read())

        return render_template("home.html", blogs=files)
    else:
        return redirect("/")
    
@app.route("/auth", methods=["GET", "POST"])
def auth():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    client_username = request.form['username']
    client_password = request.form['password']

    c.execute("SELECT * FROM %s WHERE username=? AND password=?", (USER_TABLE, client_username, client_password))
    user = c.fetchone()

    if user != None:
        session['username'] = user[1]
        db.close()
        return redirect("/")
    db.close()
    return render_template("error.html", msg=1)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/new_entry", methods=["POST", "GET"])
def new_entry():
    if request.method == "POST":
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        get_UID = "SELECT UID FROM %s WHERE USERNAME = %s" % (USER_TABLE, session['username'])
        c.execute(get_UID)
        uid = c.fetchone()

        get_last_post_num = "SELECT LAST_POST_NUM FROM %s WHERE id = %s" % (USER_TABLE, uid)
        c.execute(get_last_post_num)
        last_post_num = c.fetchone()

        new_post_route = "./blogs/%s/%s.txt" % (uid, last_post_num)
        file = open(new_post_route, "w")

        c.execute("UPDATE %s SET LAST_POST_NUM=LAST_POST_NUM+1 WHERE UID=%s" % (USER_TABLE, uid))
        file.write(request.form['new_entry'])
        file.close()
        db.commit()
        db.close()
        return redirect("/my_blog")
    else:
        return render_template("new_entry.html")


@app.route("/register", methods=["GET", "POST"])
def make():
    if request.method == "POST":
        client_username = request.form['username']
        client_password = request.form['password']

        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        make_user_table = """CREATE TABLE IF NOT EXISTS %s(
            UID INTEGER PRIMARY KEY NOT NULL,
            USERNAME TEXT NOT NULL,
            PASSWORD TEXT NOT NULL,
            BLOG_NAME TEXT
            LAST_POST_NUM INTEGER, 
            UNIQUE (USERNAME));""" % (USER_TABLE)
            
        c.execute(make_user_table)

        # list_users = 

        try:
            # Add user credentials to database
            c.execute("INSERT INTO USERS(USERNAME, PASSWORD) VALUES(?, ?)", 
                (client_username, client_password))
            
            # Select newly created user
            c.execute("SELECT * FROM USER WHERE USERNAME=? AND PASSWORD=?", 
                (client_username, client_password))

            new_user = c.fetchone()
            os.mkdir("./blogs/%s" % (new_user[0])) # Create a blog directory to store new user's files
        except sqlite3.IntegrityError:
            return render_template("register.html", taken=True)
        db.commit()
        db.close()
        return redirect("/")
    else:
        return render_template("register.html", taken=False)

@app.route("/edit/<int:post_num>", methods=["GET", "POST"])
def edit(post_num):
    if (session['username']):
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        get_UID = "SELECT UID FROM %s WHERE USERNAME = %s" % (USER_TABLE, session['username'])
        c.execute(get_UID)
        uid = c.fetchone()

        get_last_post_num = "SELECT LAST_POST_NUM FROM %s WHERE id = %s" % (USER_TABLE, uid)
        c.execute(get_last_post_num)
        last_post_num = c.fetchone()

        if request.method == "POST":
            file = open("./blogs/%s/%s.txt".format(uid, post_num), "w")
            file.write(request.form['edit'])
            return redirect('/')
        else:
            file = open("./blogs/%s/%s.txt" % (uid, post_num), "r")
            return render_template("edit.html", text=file.read(), index=post_num)
    else:
        redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run()
