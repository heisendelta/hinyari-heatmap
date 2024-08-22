from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(f'info/{datetime.today().strftime("%m-%d")}')

@app.route('/info')
def info():
    date = request.args.get('date', datetime.today().strftime("%m-%d"))
    return render_template(f'info/{date}.html')

@app.route('/region_info')
def region_info():
    region = request.args.get('region', '')
    date = request.args.get('date', datetime.today().strftime("%m-%d")) # 01-01

    if date == '':
        date = '01-01'
    if len(date.split('-')) > 2:
        date = '-'.join(date.split('-')[-2:])
    if region == '':
        return redirect(url_for('info', date=date))
    
    return render_template(f'region_info/{region}_{date}.html')

if __name__ == '__main__':
    app.run(debug=True)
