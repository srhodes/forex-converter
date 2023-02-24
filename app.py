from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickenzarecool12345"
debug = DebugToolbarExtension(app)

# code function get_exchange_rate here found online

def get_exchange_rate(from_currency, to_currency):
    url = f"https://api.exchangerate.host/latest?base={from_currency}&symbols={to_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rate = data["rates"].get(to_currency)
        if rate:
            return rate
    return None

@app.route('/hello')
def say_hello():
    return "Hello World"

# chatgpd code mix-in with my code

@app.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        from_currency = request.from['from_currency']
        to_currency = request.from['to_currency']
        amount = request.form['amount']
        try:
            amount= float(amount)
        except ValueError:
            return render_template('index.html', error="Invalid amount")

        rate =get_exchange_rate(from_currency, to_currency)
        if not rate:
            return render_template('home.html', error="Invalid currency code")

        converted_amount = round(amount * rate, 2)
        return render_template('home.html', converted_amount=f"{to_currency} {converted_amount}")  
              
    return render_template('home.html')

@app.route('/result')
def result():
    return render_template('result.html')