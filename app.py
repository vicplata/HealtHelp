 #!/usr/bin/env python3


 ###    HealtHelp
 ###
 ###    Creator: Victor Plata
 ###    RowdyHacks2020
 ###    Twilio
 ###
 ###
 ###
 ###
 ###
 ###


from flask import Flask, send_file, jsonify, request
import simplejson as json
import csv
import hashlib
import requests





###
###
### Get the number of daily and total cases in the US, using APIs
###
###
def getStats():
    r = requests.get('http://corona-api.com/countries/us')
    dat = r.json()
    todayConfirmed = dat['data']['today']['confirmed']
    todayDeaths = dat['data']['today']['deaths']
    totalConfirmed = dat['data']['latest_data']['confirmed']
    totalDeaths = dat['data']['latest_data']['deaths']
    totalRec = dat['data']['latest_data']['recovered']
    return('Today in the US there where {} Confirmed Cases, {} Deaths, There are {} Total Confirmed Cases, {} Total deaths and {} Total recovered'.format(todayConfirmed, todayDeaths, totalConfirmed, totalDeaths, totalRec))



app = Flask(__name__)

###
###
###Class patient.
###param name, lastname, date o birth, status, passwd(hashed), list of users
###
###
class Patient:
    def __init__(self, fName, lName, dob, status, passwd, listOfUsers):
        self.fName = fName
        self.lName = lName
        self.dob = dob
        self.status = status
        self.passwd = passwd
        self.listOfUsers = listOfUsers
    ###
    ###
    ###Checcks for user verification and returns the patients info
    ###
    ###
    def printPatientInfo(self, allowName, passwd):
        p = passwd
        passwd = passwd.encode('utf-8')
        passwd = hashlib.sha256(passwd).hexdigest()                         #Password is hashed sha256
        if allowName.lower() in self.listOfUsers.lower():
            if passwd == self.passwd:
                ret = 'The patient {} {}, is {}'.format(self.fName, self.lName, self.status)
            else:
                ret = 'The secure code is incorrect, please verify it'
        else:
            ret = "Your name is not in the patient's allowed users list"

        return ret



###
###
###get the patient from the data base
###
###
def getPatient(patient_first_name, user_first_name, entered_passwd):
    fileName = 'db.csv'
    with open(fileName, 'r') as NN:
        reader = csv.reader(NN)
        for firstName, lastName, dob, status, passwd, listOfUsers in reader:
            if firstName.lower() == patient_first_name.lower():
                patient = Patient(firstName, lastName, dob, status, passwd, listOfUsers)
                messageR = patient.printPatientInfo(user_first_name, entered_passwd)
                return messageR
            else:
                messageR = "I could not find a patient with that name"
        return messageR

###
###
###Check symptoms and give a recomendation
###
###
def getSyn(fever, cough, breathing):
    if breathing == 'Yes':
        return 'Please try to contact your doctor.'
    elif cough == 'Yes' or fever == 'Yes':
        return 'Please self-quarantine, and do not self medicate'
    return 'You are okay! But be aware if any symptoms start showing up!'


@app.route('/')
def home():
    return getStats()

###
###
###Process request from Twilio to get stats
###
###
@app.route('/stats', methods=['POST'])
def collectStats():
    message = getStats()
    return jsonify(actions=[{'say': {'speech': message}},{'say': {'speech': 'Thank you for using HealtHelp'}}])


###
###
###Process request from Twilio to collect patient info
###
###
@app.route('/collect',  methods=['POST'])
def collect():
    memory = json.loads(request.form.get('Memory'))

    answers = memory['twilio']['collected_data']['collect_patients_info']['answers']

    patient_first_name = answers['patient_first_name']['answer']
    user_first_name = answers['user_first_name']['answer']
    entered_passwd = answers['secure_code']['answer']

    message = getPatient(patient_first_name, user_first_name, entered_passwd)

    return jsonify(actions=[{'say': {'speech': message}},{'say': {'speech': 'Thank you for using HealtHelp'}}])

###
###
###Process request from Twilio to check symptoms
###
###
@app.route('/collectsyn',  methods=['POST'])
def collectsyn():
     memory = json.loads(request.form.get('Memory'))

     answers = memory['twilio']['collected_data']['collect_patients_syn']['answers']

     fever = answers['fever']['answer']
     cough = answers['cough']['answer']
     breathing = answers['breathing']['answer']

     message = getSyn(fever, cough, breathing)

     return jsonify(actions=[{'say': {'speech': message}},{'say': {'speech': 'Thank you for using HealtHelp'}}])



if __name__ == "__main__":
    app.run(debug=True)
