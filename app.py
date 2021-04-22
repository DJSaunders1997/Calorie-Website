from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import DBConModule

@app.route('/')
def index():

    dave_calories = DBConModule.get_daily_total('Dave')
    meg_calories = DBConModule.get_daily_total('Dave')

    return render_template('index.html', dave_calories=dave_calories, meg_calories=meg_calories)

@app.route('/action')
def action():
    print('starting action')
    command = request.args.get('command', default ='add', type = str)
    amount = request.args.get('amount', default =0, type = int)

    if command == 'add':
        # todo call add calories
        DBConModule.add_calories('Dave', amount)
        res = DBConModule.get_daily_total('Dave')
    elif command == 'minus':
        # minus calories
        print()
    
    dave_calories = DBConModule.get_daily_total('Dave')
    meg_calories = DBConModule.get_daily_total('Meg')

    #return render_template('index.html', dave_calories=dave_calories, meg_calories=meg_calories)
    return jsonify(result=dave_calories)

@app.route('/action2')
def action2():
    print('starting action 2')
    command = request.args.get('command', default ='add', type = str)
    amount = request.args.get('amount', default =0, type = int)

    if command == 'add':
        # todo call add calories
        DBConModule.add_calories('Dave', amount)
        res = DBConModule.get_daily_total('Dave')
    elif command == 'minus':
        # minus calories
        print()
    
    dave_calories = DBConModule.get_daily_total('Dave')

    return jsonify(result=dave_calories)

@app.route('/who')
def who():
    return 'Made By Dave'