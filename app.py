from flask import Flask,render_template, request 
import blinkit as bk
import bigbasket as bb
import threading

app = Flask(__name__,template_folder="templates") 

@app.route("/") 
def hello(): 
	return render_template('index.html') 

@app.route('/pincode_post', methods=['POST']) 
def pincode_post():
	global thread_a, thread_b
	data = request.form.get('pin') 
	p=str(data)
	thread_a = threading.Thread(target=bk.BlinkCheckAvailability,args=(p,))
	thread_b = threading.Thread(target=bb.BigCheckAvailability,args=(p,))
	thread_a.start()
	thread_b.start()
	result = f"your data is {p}" 
	return result 

@app.route('/searchbar', methods=['POST'])
def searchbar():
	global thread_a, thread_b, thread_c, thread_d
	search = request.form.get('searchterm') 
	s=str(search)
	thread_c = threading.Thread(target=bk.blinkSearch,args=(s,))
	thread_d = threading.Thread(target=bb.bigSearch,args=(s,))
	thread_c.start()
	thread_d.start()
	result = f"your data is {s}" 
	return result 

if __name__ == '__main__': 
	app.run(debug=True)