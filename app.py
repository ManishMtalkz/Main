from flask import*
app = Flask(__name__)
@app.route('/')
def a():
    return("hellow")

@app.route('/predict')
def predict():
    return({ '1':"welcome "})

@app.route('/hello/')
@app.route('/hello/<username>')
def hello(username=None):
    return render_template("hellow.html",username=username)
















     
if __name__ == '__main__':
   app.run(debug = True)
 