from flask import Flask, render_template, request
from mysql.connector import Error
import joblib
import mysql.connector
import random

app = Flask(__name__)

# Load the trained machine learning model
model = joblib.load('CES_RANDOM_FOREST_MODEL.pkl')

# connect to MySQL server
try:
    conn = mysql.connector.connect(
        host="127.0.0.2",
        port=3306,
        user="root",
        password="1q2w3e4r",
        database="ces_database"
    )
    if conn.is_connected():
        print('Connected to MySQL database')
except Error as e:
    print(f"Error: {e}")


@app.route('/', methods=['GET', 'POST'])
def predict_branch():
    prediction_result = None
    schools= []
    sorted_results = []  # ตัวแปรสำหรับเก็บข้อมูลจากฐานข้อมูล
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, schoolname, schooltype, provinceid, regionname FROM schools")
        school_rows = cursor.fetchall()
        for row in school_rows:
            schools.append({"id": row[0], "schoolname": row[1], "schooltype": row[2], "provinceid": row[3], "regionname": row[4]})
        cursor.close()
    except Error as e:
        print(f"Error reading data from schools table: {e}")

    if request.method == 'POST':
        school_id = int(request.form.get('selectedSchoolId'))
        selected_school = next((item for item in schools if item['id'] == school_id), None)
        S_RANK = selected_school['schooltype']
        P_ID = selected_school['provinceid']
        R_ID = selected_school['regionname']
        FEE_NAME = 2
        S_PARENT = int(request.form.get('S_PARENT', ))
        GPA = float(request.form.get('GPA', 1))
        if GPA >= 1.00 and GPA < 1.50:
            GPA = 1
        elif GPA >= 1.50 and GPA < 2.00:
            GPA = 1.5
        elif GPA >= 2.00 and GPA < 2.50:
            GPA_MATCH = 2
        elif GPA >= 2.50 and GPA < 3.00:
            GPA = 2.5
        elif GPA >= 3.00 and GPA < 3.50:
            GPA = 3
        elif GPA >= 3.50 and GPA < 4.00:
            GPA = 3.5
        elif GPA == 4:
            GPA = 4

        GPA_MATCH = float(request.form.get('GPA_MATCH', 1))
        if GPA_MATCH >= 1.00 and GPA_MATCH < 1.50:
            GPA_MATCH = 1
        elif GPA_MATCH >= 1.50 and GPA_MATCH < 2.00:
            GPA_MATCH = 1.5
        elif GPA_MATCH >= 2.00 and GPA_MATCH < 2.50:
            GPA_MATCH = 2
        elif GPA_MATCH >= 2.50 and GPA_MATCH < 3.00:
            GPA_MATCH = 2.5
        elif GPA_MATCH >= 3.00 and GPA_MATCH < 3.50:
            GPA_MATCH = 3
        elif GPA_MATCH >= 3.50 and GPA_MATCH < 4.00:
            GPA_MATCH = 3.5
        elif GPA_MATCH == 4:
            GPA_MATCH = 4
        
        GPA_SCI = float(request.form.get('GPA_SCI', 1))
        if GPA_SCI >= 1.00 and GPA_SCI < 1.50:
            GPA_SCI = 1
        elif GPA_SCI >= 1.50 and GPA_SCI < 2.00:
            GPA = 1.5
        elif GPA >= 2.00 and GPA_SCI < 2.50:
            GPA_SCI = 2
        elif GPA_SCI >= 2.50 and GPA_SCI < 3.00:
            GPA_SCI = 2.5
        elif GPA_SCI >= 3.00 and GPA_SCI < 3.50:
            GPA_SCI = 3
        elif GPA_SCI >= 3.50 and GPA_SCI < 4.00:
            GPA_SCI = 3.5
        elif GPA_SCI == 4:
            GPA_SCI = 4


        # Prepare the input data for prediction
        new_data = [[S_RANK, P_ID, R_ID, FEE_NAME, S_PARENT, GPA, GPA_MATCH, GPA_SCI]]

        # Perform prediction
        predicted_label = model.predict(new_data)[0]

        # Map the numeric label to its corresponding string representation
        mapping = {0: 'นิเทศศาสตร์ดิจิทัล (DCA)', 
                   1: 'ดิจิทัลคอนเทนต์และสื่อ (DCM)', 
                   2: 'อินเทอร์แอคทีฟ มัลติมีเดีย แอนิเมชันและเกม (IMAG)', 
                   3: 'เทคโนโลยีสารสนเทศและนวัตกรรมดิจิทัล (ITD)', 
                   4: 'นวัตกรรมสารสนเทศทางการเเพทย์ (IMI)'}
        predicted_branch = mapping[predicted_label]
        
        
        # Calculate the percentage for each branch
        probabilities = model.predict_proba(new_data)[0]
        percentage_results = {mapping[i]: f'{prob:.1%}' for i, prob in enumerate(probabilities)}

        # เรียงลำดับ percentage_results จากน้อยไปมากตามค่าเปอร์เซ็นต์
        sorted_results = sorted(percentage_results.items(), key=lambda x: float(x[1].strip('%')), reverse=True)

        # Set the prediction result to be displayed on the website
        prediction_result = ""

# Loop through each branch and its percentage
    for i, (branch, percentage) in enumerate(sorted_results):
        if i == 0:  # If it's the first element, it has the highest percentage
            prediction_result += f"{branch}: {percentage}"
        else:
            prediction_result += f"{branch}: {percentage}"
    # Loop through each branch and its percentage and construct prediction_result with HTML line breaks
    prediction_result = "<br>".join(f"{branch}: {percentage}" for branch, percentage in sorted_results)
    
    # Render the webpage with the prediction results and province information
    return render_template('index.html', prediction_result=prediction_result, schools=schools)

if __name__ == '__main__':
    app.run(debug=True)
