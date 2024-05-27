from flask import Flask,render_template, request 
import blinkitInit as bk


app = Flask(__name__,template_folder="templates") 

@app.route("/") 
def hello(): 
	return render_template('index.html') 

@app.route('/pincode_post', methods=['POST']) 
def pincode_post(): 
	data = request.form.get('pin') 
	p=str(data) 
	bk.pinin(p)
	result = f"your data is {p}" 
	return result 

@app.route('/searchbar', methods=['POST'])
def searchbar():
	search = request.form.get('searchterm') 
	s=str(search) 
	bk.blinkSearch(s)
	result = f"your data is {s}" 
	return result 

if __name__ == '__main__': 
	app.run(debug=True) 
