from flask import*
app = Flask(__name__)
@app.route('/')
def a():
    return("hellow MANISH")


item = 1000

@app.route('/data', methods=['GET'])

def data():
    return jsonify(item)

@app.route('/predict')
def predict():
    return({ '1':"welcome "})

@app.route('/hello/')
@app.route('/hello/<username>')
def hello(username=None):
    return render_template("hellow.html",username=username)

#url building

@app.route('/admin')
def admin():
    return 'admin'


@app.route('/librarion')
def librarion():
    return 'librarion'


@app.route('/student')
def student():
    return 'student'


@app.route('/user/<name>')
def user(name):
    if name == 'admin':
        return redirect(url_for('admin'))
    
    if name == 'librarion':
        return redirect(url_for('librarion'))
    
    if name =='student':
        return redirect(url_for('student'))
    
    


     
if __name__ == '__main__':
   app.run(debug = True)
 