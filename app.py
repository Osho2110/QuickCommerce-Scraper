from flask import Flask,render_template, request, url_for, jsonify
import blinkit as bk
import bigbasket as bb
import dmart as dm
import threading
import webbrowser
import time
import os
import json

#Change Port Number here
SetPort=5000

app = Flask(__name__,template_folder="templates") 

def open_browser(SetPort):
	time.sleep(1)
	webbrowser.open_new(f"http://localhost:{SetPort}")

@app.route("/") 
def hello(): 
	return render_template('index.html') 

@app.route('/pincode_post', methods=['POST']) 
def pincode_post():
	data = request.form.get('pin') 
	p=str(data)
	thread_blinkp = threading.Thread(target=bk.BlinkCheckAvailability,args=(p,))
	thread_bigp = threading.Thread(target=bb.BigCheckAvailability,args=(p,))
	thread_dmp = threading.Thread(target=dm.DmartCheckAvailability,args=(p,))
	thread_blinkp.start()
	thread_bigp.start()
	thread_dmp.start()
	thread_bigp.join()
	thread_blinkp.join()
	thread_dmp.join()
	 
	return jsonify({"redirect": url_for('searchpage')})

@app.route("/searchpage")
def searchpage():
	return render_template("search.html")

@app.route("/resultpage", methods=['POST','GET'])
def resultpage():
	return render_template("list.html")


@app.route('/searchbar', methods=['POST'])
def searchbar():
	search = request.form.get('searchterm') 
	s=str(search)
	thread_blinks = threading.Thread(target=bk.blinkSearch,args=(s,))
	thread_bigs = threading.Thread(target=bb.bigSearch,args=(s,))
	thread_dms = threading.Thread(target=dm.dmartSearch,args=(s,))

	thread_blinks.start()
	thread_bigs.start()
	thread_dms.start()
	thread_blinks.join()
	thread_bigs.join()
	thread_dms.join()
	print("Search complete")

	
	combined_file = "./static/data.json"
	# Check if combined file exists
	if os.path.exists(combined_file):
		os.remove(combined_file)  # Clear existing data
	combined_data = []
	for filename in ["dmartOP.json", "output.json", "outputbig.json"]:
		with open(filename, "r" , encoding="utf-8") as infile:
			data = json.load(infile)
			if isinstance(data, list):  # Handle list or single object
				combined_data.extend(data)
			else:
				combined_data.append(data)
	data = {"data": combined_data}
	with open(combined_file, "w") as outfile:
		json.dump(data, outfile, indent=4)  # Pretty-print for readability
	return jsonify({"redirect": url_for('resultpage')})

if __name__ == '__main__': 
	threading.Thread(target=open_browser, args=(SetPort,)).start()
	app.run(debug=False, port=SetPort)