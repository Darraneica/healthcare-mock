from flask import Flask, render_template, request, redirect, url_for
import csv
import pandas as pd

app = Flask(__name__)

# Helper functions to read/write CSV and Excel
def read_patients_data():
    # Read from CSV
    patients = []
    try:
        with open('patients_data.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                patients.append(row)
    except FileNotFoundError:
        pass  # File doesn't exist yet, so no data is available
    return patients

def write_patients_data(patients):
    # Write to CSV
    with open('patients_data.csv', mode='w', newline='') as file:
        fieldnames = ['id', 'name', 'birthdate', 'age', 'diagnosis', 'doctor_name', 'medicine_name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for patient in patients:
            writer.writerow(patient)
    
    # Also write to Excel
    df = pd.DataFrame(patients)
    df.to_excel('patients_data.xlsx', index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        birthdate = request.form['birthdate']
        age = request.form['age']
        diagnosis = request.form['diagnosis']
        doctor_name = request.form['doctor_name']
        medicine_name = request.form['medicine_name']

        patients = read_patients_data()
        patient_id = len(patients) + 1  # Simple patient ID generation
        new_patient = {
            'id': patient_id,
            'name': name,
            'birthdate': birthdate,
            'age': age,
            'diagnosis': diagnosis,
            'doctor_name': doctor_name,
            'medicine_name': medicine_name
        }
        patients.append(new_patient)
        write_patients_data(patients)

        return redirect(url_for('view_patients'))

    return render_template('add_patient.html')

@app.route('/view_patients')
def view_patients():
    patients = read_patients_data()
    return render_template('view_patients.html', patients=patients)

@app.route('/update_patient/<int:patient_id>', methods=['GET', 'POST'])
def update_patient(patient_id):
    patients = read_patients_data()
    patient = next((p for p in patients if p['id'] == patient_id), None)

    if request.method == 'POST':
        patient['name'] = request.form['name']
        patient['birthdate'] = request.form['birthdate']
        patient['age'] = request.form['age']
        patient['diagnosis'] = request.form['diagnosis']
        patient['doctor_name'] = request.form['doctor_name']
        patient['medicine_name'] = request.form['medicine_name']

        write_patients_data(patients)
        return redirect(url_for('view_patients'))

    return render_template('update_patient.html', patient=patient)

@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    patients = read_patients_data()
    patients = [p for p in patients if p['id'] != patient_id]
    write_patients_data(patients)
    return redirect(url_for('view_patients'))

if __name__ == '__main__':
    app.run(debug=True)
