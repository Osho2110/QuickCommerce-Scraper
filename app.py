from flask import Flask,render_template, request 
import blinkitInit as bk


def sendpin(info):
	bk.pinin(info)

app = Flask(__name__,template_folder="templates") 

@app.route("/") 
def hello(): 
	return render_template('index.html') 

@app.route('/process', methods=['POST']) 
def process(): 
	data = request.form.get('data') 
	x=str(data) 
	sendpin(x)
	result = f"your data is {x}" 
	return result 

if __name__ == '__main__': 
	app.run(debug=True) 
