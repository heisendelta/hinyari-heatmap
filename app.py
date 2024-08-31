from flask import Flask, request, render_template, redirect, url_for, abort
from datetime import datetime
from jinja2 import TemplateNotFound
from werkzeug.exceptions import NotFound

app = Flask(__name__)

def render_template_fixed(template_string):
    try:
        return render_template(template_string)
    except TemplateNotFound:
        # Redirect to custom 404 page
        abort(404)
    except Exception as e:
        # Optionally log the error or handle other exceptions
        print(f"An error occurred: {e}")
        abort(404)

@app.route('/')
def index():
    return render_template_fixed(f'info/{datetime.today().strftime("%m-%d")}.html')

@app.route('/info')
def info():
    date = request.args.get('date', datetime.today().strftime("%m-%d"))
    return render_template_fixed(f'info/{date}.html')

@app.route('/region_info')
def region_info():
    region = request.args.get('region', '')
    date = request.args.get('date', datetime.today().strftime("%m-%d")) # 01-01

    if date == '':
        date = datetime.today().strftime("%m-%d")
    if len(date.split('-')) > 2:
        date = '-'.join(date.split('-')[-2:])
    if region == '':
        return redirect(url_for('info', date=date))
    
    return render_template_fixed(f'region_info/{region}_{date}.html')

@app.errorhandler(404)
def page_not_found(e):
    if isinstance(e, NotFound):
        return render_template('404.html'), 404
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
