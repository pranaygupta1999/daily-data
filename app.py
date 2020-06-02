from flask import Flask, request, send_file, render_template
import database

dataUrl:str  = 'https://assignment-machstatz.herokuapp.com/excel'

app = Flask(__name__)
@app.route('/')
def home():
    return render_template("home.html")
@app.route('/total')
def getTotal():
    date_string = request.args.get("day")
    return database.read(date_string)

@app.route('/excelreport/')
def get_excel():
    try:
        return send_excel_file()
    except Exception as e:
	    return str(e)
    


def send_excel_file():
   return send_file( database.get_excel_file(), mimetype="application/vnd.ms-excel", as_attachment=True ,attachment_filename="excelreport.xls" , )

if __name__ == "__main__":
    print("Loading database")
    database.load_data()
    print("Starting server")
    app.run('0.0.0.0')
    