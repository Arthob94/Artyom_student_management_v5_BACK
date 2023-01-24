import json

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MY_FILE= 'my_student_list.json'

def load_data():
    with open(MY_FILE) as f:    #open file for reading
        return json.load(f) 

@app.route('/student', methods=['POST'])
def create_student():
    data = request.get_json()   #request data as dict
    existing_data_array = load_data()   # 
    existing_data_array.append(data)
    with open(MY_FILE, 'w') as f:
        f.write(json.dumps(existing_data_array))  # json.dumps converts to a string and f.write writes the string into a file.

    return data

@ app.route('/student', methods=['GET'])
@ app.route('/student/<string:student_email>', methods=['GET'])
def read_worker(student_email=""):
    json_data = load_data()
    if (student_email == ""):
        return json_data
    else:
        for x in json_data:
            if x['semail'] == student_email:
                return [x]
        return [{
            "semail": "No such email",
            "sname": "",
            "gmathematics": "",
            "gcomputers": "",
            "genglish": ""
        }]

@app.route('/student/<string:student_email>', methods=['PUT'])
def update_worker(student_email):
    json_data = load_data()
    input_data = request.get_json()   
    student_found = False
    for student in json_data:
        if (student_email == student['semail']):
            student_found = True
            student.update(input_data)
            break
    if not student_found: 
        return {"msg": "no such student "}
    with open(MY_FILE, 'w') as f:
        f.write(json.dumps(json_data))

    
    return input_data

@app.route('/student/<string:student_email>', methods=['DELETE'])
def delete_student(student_email):
    json_data = load_data()
    student_found = False
    for i, student in enumerate(json_data):
        if (student_email == student['semail']):
            student_found = True
            del json_data[i]
            break
    if not student_found: 
        return {"msg": "no such student"}
    with open(MY_FILE, 'w') as f:
        f.write(json.dumps(json_data))
    return {"msg": "student with email {} deleted".format(student_email)}

    





if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)