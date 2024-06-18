from flask import Flask, request, jsonify, render_template
import pyodbc

app = Flask(__name__)

# MSSQL connection details
server = 'JEFFREY'
database = 'EksamensProjekt_DB'
username = 'Oechsner'
password = '1234'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Connect to MSSQL
cnxn = pyodbc.connect(connection_string)
cursor = cnxn.cursor()

@app.route('/')
def home():
    return render_template('index_mssql.html')

@app.route('/insert', methods=['POST'])
def insert():
    data = request.json
    columns = ', '.join(data.keys())
    values = ', '.join(f"'{v}'" for v in data.values())
    query = f"INSERT INTO Cities_Climate_Risk_and_Vulnerability_Assessments_2023 ({columns}) VALUES ({values})"
    cursor.execute(query)
    cnxn.commit()
    return jsonify(message="Document Inserted"), 201

@app.route('/retrieve', methods=['GET'])
def retrieve():
    cursor.execute("SELECT TOP 10 * FROM Cities_Climate_Risk_and_Vulnerability_Assessments_2023")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in rows]
    return jsonify(result), 200

@app.route('/update', methods=['POST'])
def update():
    query_data = request.json.get('query')
    update_data = request.json.get('update')
    set_clause = ', '.join(f"{k}='{v}'" for k, v in update_data.items())
    where_clause = ' AND '.join(f"{k}='{v}'" for k, v in query_data.items())
    query = f"UPDATE Cities_Climate_Risk_and_Vulnerability_Assessments_2023 SET {set_clause} WHERE {where_clause}"
    cursor.execute(query)
    cnxn.commit()
    return jsonify(message="Document Updated"), 200

@app.route('/delete', methods=['POST'])
def delete():
    query_data = request.json
    where_clause = ' AND '.join(f"{k}='{v}'" for k, v in query_data.items())
    query = f"DELETE FROM Cities_Climate_Risk_and_Vulnerability_Assessments_2023 WHERE {where_clause}"
    cursor.execute(query)
    cnxn.commit()
    return jsonify(message="Document Deleted"), 200

@app.route('/aggregate', methods=['GET'])
def aggregate():
    query = "SELECT Country, COUNT(*) as total FROM Cities_Climate_Risk_and_Vulnerability_Assessments_2023 GROUP BY Country"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in rows]
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
