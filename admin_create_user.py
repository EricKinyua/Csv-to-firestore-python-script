import firebase_admin
from firebase_admin import credentials, firestore
import csv
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate('doctors.json')
app = firebase_admin.initialize_app(cred)

# Initiate firestore
store = firestore.client()

# Spreadsheet
file_path = 'practitioners.csv'

 # Define identifiers
regNumberIdentifier = 'REGISTRATION NUMBER'
regStatusIdentifier  = 'RETENTION STATUS'
regDateIdentifier  = 'REGISTRATION DATE'
fullNameIdentifier  = 'FULLNAME'
titleIdentifier  = 'TITLE'
qualificationsIdentifier  = 'Qualifications'
disciplineIdentifier  = 'Discipline'
specialityIdentifier  = 'Specialty'
sub_specialityIdentifier  = 'Sub_Speciality'
addressIdentifier  = 'Address'
codeIdentifier  = 'CODE'
officeNumberIdentifier  = 'OFFICE NUMBER '
personalNumberIdentifier  = 'PERSONAL NUMBER'
countyIdentifier  = 'COUNTY '

def sort_and_create(line):
    registration_number = line[regNumberIdentifier]
    registration_status = line[regStatusIdentifier ]
    registration_date = line[regDateIdentifier ]
    fullName = line[fullNameIdentifier]
    title = line[titleIdentifier]
    qualifications = line[qualificationsIdentifier]
    discipline = line[disciplineIdentifier]
    speciality = line[specialityIdentifier]
    sub_speciality = line[sub_specialityIdentifier]
    address = line[addressIdentifier]
    code = line[codeIdentifier]
    officeNumber = line[officeNumberIdentifier]
    personalNumber = line[personalNumberIdentifier]
    county = line[countyIdentifier]

    # Name Split
    title = fullName.split(' ')[0]
    firstName = fullName.split(' ')[1]
    otherNames = ' '.join(fullName.split(' ')[2::])

    if otherNames == 'MAINA WAMBUI':
        user = {
            'designation': 'Practitioner',
            'email': None,
            'title': title,
            'firstName': firstName,
            'lastName': otherNames,
            'userStatus': registration_status,
            'uid': None,
            'registeredOn': datetime.now(),
            'practitionerDiscipline': discipline,
            'dob': None,
            'gender': None,
            'mpdbRegDate': None,
            'mpdbRegNumber': registration_number,
            'userAddress': {
                'poBox': address,
                'location': county,
            },
            'userContact': {
                'officeNumber': officeNumber,
                'personalNumber': personalNumber,
            },
            'practitionerSpeciality': speciality,
            'practitionerSubSpeciality': sub_speciality,
            'qualifications': qualifications,
        }
        store.collection('incoming_users').document().set(user)

with open(file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter = ',')
    for line in csv_reader:
        sort_and_create(line=line)