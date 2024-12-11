from db import DBConn
from visualiser import Graphs
from waitress import serve
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user


# config
app = Flask(__name__)
app.config.update(
    DEBUG=False,
    SECRET_KEY="CHANGE_ME"
)

# flask login config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Creating user model
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.username = "admin"   #Change this
        self.password = "admin"   #Change this

    def __repr__(self):
        return "User"


# creating an admin user
admin_user = User(1)


# defining local sqlite databases
datastore = DBConn()


@app.before_request
def create_db_connection():

    global datastore
    datastore.connect()
    datastore.create_table()


@app.teardown_request
def teardown_db_connection(exception):

    global datastore
    if not datastore.conn is None:
        datastore.disconnect()


@login_manager.user_loader
def load_user(id):
    return User(id)


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "admin":
            user = admin_user
            login_user(user)
            flash(f'Welcome {username}!', 'success')
            return redirect(url_for("home"))
        else:
            return render_template('loginpage.html', error="Wrong username or password")
    return render_template('loginpage.html')


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match", "error")
        
        # try:
        #     # user_mgmt.create_user(username, password)
        #     flash("User created successfully!", "success")
        #     return redirect(url_for("login"))
        # except:
        #     return render_template("registerpage.html", error="Username already exists")
    
    else:

        return render_template("registerpage.html")


@app.route('/home')
@login_required
def home():

    with datastore.conn:
        entries = datastore.read_db()
    return render_template('home.html', entries=entries)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/insert', methods=['POST'])
@login_required
def insert():
    if request.method == "POST":
        given_date = request.form.get("date")
        axis_amount = request.form.get("axis")
        shares_amount = request.form.get("shares")
        pension_amount = request.form.get("pension")
        lisa_amount = request.form.get("lisa")
        total_value = int(axis_amount) + int(pension_amount) + int(shares_amount) + int(lisa_amount)

        with datastore.conn:
            datastore.add_record(
                date=given_date,
                axis=axis_amount,
                shares=shares_amount,
                pension=pension_amount,
                lisa=lisa_amount,
                total=total_value
            )

        flash("Data Added Successfully")

        return redirect(url_for('home'))


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':

        edit_id = request.form.get('id')
        new_axis = request.form['axis']
        new_shares = request.form['shares']
        new_pension = request.form['pension']
        new_lisa = request.form['lisa']

        with datastore.conn:
            datastore.edit_record(
                row_id=int(edit_id),
                axis=int(new_axis),
                shares=int(new_shares),
                pension=int(new_pension),
                lisa=int(new_lisa)
            )

        flash("Data Updated Successfully")

        return redirect(url_for('home'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
@login_required
def delete(id):

    del_id = int(id)
    with datastore.conn:
        datastore.del_record(row_id=del_id)

    flash("Data Deleted Successfully")

    return redirect(url_for('home'))


@app.route('/graphs')
@login_required
def graphs():

    with datastore.conn:
        graph_viz = Graphs(datastore)

    try:
        line_chart = graph_viz.line_graph()
        progress_chart = graph_viz.progress_graph()
        stacked_chart = graph_viz.stacked_graph()
        treemap = graph_viz.treemap_plot()

        return render_template('graphs.html',
                            line_chart=line_chart,
                            progress_chart=progress_chart,
                            stacked_chart=stacked_chart,
                            treemap=treemap)
    except Exception as err:
        flash("Unable to generate graphs, check if data has been added", "error")
        return redirect(url_for("home"))


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5100)