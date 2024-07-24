from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
uri = "mongodb+srv://jkrkumar1801:Iamjk1801@bloodbank.e4gksgq.mongodb.net/?appName=BloodBank"
client = MongoClient(uri)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client['plasma_donation']
recipient_collection = db['recipients']
donor_collection = db['donors']

@app.route('/')
def index():
    return render_template('index.html')      # index - home page

# Admin credentials
@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')   # admin log in page

@app.route('/adminreg')
def adminreg():
    return render_template('adminreg.html')  # admin sign up page

@app.route('/recipregistration')
def recipregistration():
    return render_template('recipregistration.html')   # recipient signup page

@app.route('/recipientlogin')
def recipientlogin():
    return render_template('reclogin.html')      # recipient login page

@app.route('/recipientrec', methods=['POST', 'GET'])
def recipientrec():
    if request.method == 'POST':
        recipient = {
            "fname": request.form['fname'],
            "lname": request.form['lname'],
            "dob": request.form['dob'],
            "email": request.form['email'],
            "mnumb": request.form['mnumb'],
            "gender": request.form['gender'],
            "address": request.form['address'],
            "password": request.form['password'],
            "pin": request.form['pin']
        }

        if recipient_collection.find_one({"fname": recipient["fname"]}):
            return render_template('reclogin.html', msg="Your account already exists, please try to log in")
        else:
            recipient_collection.insert_one(recipient)
            return render_template('reclogin.html', msg="Account has been created successfully")
    return render_template('reclogin.html', msg="Error occurred during registration")

@app.route('/donregistration')
def donregistration():
    return render_template('donregistration.html')   # donor signup page

@app.route('/donarlogin')
def donarlogin():
    return render_template('donlogin.html')      # donor login page

@app.route('/donrec', methods=['POST', 'GET'])
def donrec():
    if request.method == 'POST':
        donor = {
            "fname": request.form['fname'],
            "lname": request.form['lname'],
            "dob": request.form['dob'],
            "email": request.form['email'],
            "mnumb": request.form['mnumb'],
            "gender": request.form['gender'],
            "address": request.form['address'],
            "pin": request.form['pin']
        }

        if donor_collection.find_one({"fname": donor["fname"]}):
            return render_template('donlogin.html', msg="Your account already exists, please try to log in")
        else:
            donor_collection.insert_one(donor)
            return render_template('donlogin.html', msg="Account has been created successfully")
    return render_template('donlogin.html', msg="Error occurred during registration")

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/donar')
def donar():
    return render_template('donar.html')

@app.route('/giveplasma', methods=['POST', 'GET'])
def giveplasma():
    if request.method == 'POST':
        donor = {
            "name": request.form['name'],
            "age": request.form['age'],
            "gender": request.form['gender'],
            "mnumb": request.form['mnumb'],
            "email": request.form['email'],
            "city": request.form['city'],
            "address": request.form['address'],
            "bloodgroup": request.form['bloodgroup'],
            "issue": request.form['issue'],
            "lastbd": request.form['lastbd'],
            "slot": request.form['slot']
        }

        if donor_collection.find_one({"name": donor["name"]}):
            return render_template('donlogin.html', msg="You are already a member, please log in using your details")
        else:
            donor_collection.insert_one(donor)
            return render_template('donar.html', msg="Your request for donation is successfully submitted")
    return render_template('donar.html', msg="Error occurred during registration")

@app.route('/plasmadon')
def plasmadon():
    donors = list(donor_collection.find())
    return render_template("plasmadon.html", donors=donors)

@app.route('/delete/<name>')
def delete(name):
    result = donor_collection.delete_one({"name": escape(name)})
    if result.deleted_count > 0:
        donors = list(donor_collection.find())
        return render_template("plasmadon.html", donors=donors, msg="Delete successful")
    return render_template("plasmadon.html", msg="Delete unsuccessful")

@app.route('/mail')
def mail():
    return render_template('mail.html')

@app.route('/recipient')
def recipient():
    return render_template('recipient.html')

@app.route('/takeplasma', methods=['POST', 'GET'])
def takeplasma():
    if request.method == 'POST':
        recipient = {
            "name": request.form['name'],
            "age": request.form['age'],
            "gender": request.form['gender'],
            "mnumb": request.form['mnumb'],
            "proof": request.form['proof'],
            "address": request.form['address'],
            "plasma": request.form['plasma']
        }

        if recipient_collection.find_one({"name": recipient["name"]}):
            return render_template('reclogin.html', msg="You are already a member, please log in using your details")
        else:
            recipient_collection.insert_one(recipient)
            return render_template('recipient.html', msg="Registration successful for Plasma request")
    return render_template('recipient.html', msg="Error occurred during registration")

@app.route('/plasmareq')
def plasmareq():
    recipients = list(recipient_collection.find())
    return render_template("plasmareq.html", recipients=recipients)

@app.route('/delete/<name>')
def deleted(name):
    result = recipient_collection.delete_one({"name": escape(name)})
    if result.deleted_count > 0:
        recipients = list(recipient_collection.find())
        return render_template("plasmareq.html", recipients=recipients, msg="Delete successful")
    return render_template("plasmareq.html", msg="Delete unsuccessful")

if __name__ == "__main__":
    app.run(debug=True)
