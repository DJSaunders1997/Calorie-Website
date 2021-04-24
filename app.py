from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import datetime
today = datetime.datetime.today().strftime("%Y-%m-%d")

import DBConModule

@app.route('/')
@app.route('/<date>')
#default date will be today
def index(date=today):

    #convert date from string to datetime
    date = datetime.datetime.strptime(date, "%Y-%m-%d")

    #print(date.strftime("%Y-%m-%d"))

    dave_calories = DBConModule.get_daily_total('Dave')
    meg_calories = DBConModule.get_daily_total('Meg')

    #pass through date object to html so we can increment the day there.
    #will convert to string before showing it.
    return render_template('index.html', date=date, dave_calories=dave_calories, meg_calories=meg_calories, datetime=datetime)

# Changed from Messy Action to just an add rout
# Default will be me and 0 calories
@app.route('/add/<person>/<amount>')
def add(person='Dave', amount='0'):
    
    # Cast amount to int before adding
    DBConModule.add_calories(person, int(amount))
    res = DBConModule.get_daily_total(person)

    return jsonify(result=res)


@app.route('/who')
def who():
    return 'Made By Dave'


if __name__ == "__main__":
    #app.run(host="0.0.0.0", port="5000")
    app.run()