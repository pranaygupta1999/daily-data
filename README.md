# Daily-data-Fetch
As a part of Internship assignment for the company Machstatz

## Link
[Heroku Link](https://flask-daily-data.herokuapp.com/) - https://flask-daily-data.herokuapp.com/

## API Consumed
https://assignment-machstatz.herokuapp.com/excel


## Usage
There are 2 routes available
* **GET** */total?day=\<date>* : API with query string where day is the querystring.
For that particular day, it sums all the Length, Weight, Quantity, and return an JSON 

    Eg. total?day=31-06-2020
* **GET** */excelreport* : Creates an excel file using the API provided,It  segregate day wise data in different sheet in a single excel file.Each sheet have Column Name as DateTime, Length, Weight, Quantity
This excel sheet is returned when this API is queried.
