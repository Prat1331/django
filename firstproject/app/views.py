from django.shortcuts import render
import numpy as np
import pickle as pkl

# Create your views here.
def index(request):
    return render(request, "index.html")

def loadFile(filename):
    file = open(filename, "rb")
    obj = pkl.load(file)
    file.close()
    return obj

def predict(request):
    model = loadFile("model.pkl")
    minmax = loadFile("minmax.pkl")
    age = int(request.GET['age'])
    gender = request.GET['gender']
    body_pain = int(request.GET['body_pain'])
    fever = int(request.GET['fever'])
    runny_nose = int(request.GET['runny_nose'])
    breathing = int(request.GET['breathing'])
    nasal = int(request.GET['nasal'])
    sore = int(request.GET['sore'])
    severity = request.GET['severity']
    contact = request.GET['contact']

    if gender == "female":
        female = 1
        male = 0
        trans = 0
    elif gender == "male":
        female = 0
        male = 1
        trans = 0
    else:
        female = 0
        male = 0
        trans = 1
        
    if severity == "mild":
        mild = 1
        moderate = 0
        severe = 0
    elif severity == "moderate":
        mild = 0
        moderate = 1
        severe = 0
    else:
        mild = 0
        moderate = 0
        severe = 1
        
    if contact == "no":
        no = 1
        yes = 0
        not_known = 0
    elif contact == "yes":
        no = 0
        yes = 1
        not_known = 0
    else:
        no = 0
        yes = 0
        not_known = 1
        
    data = np.array([[age, body_pain, fever, runny_nose, breathing, nasal, sore, 
            female, male, trans, mild, moderate, severe,
            no, not_known, yes]])
    
    print(data)
    
    test_data = minmax.transform(data)
    prediction = model.predict(test_data)

    if prediction[0] == 0:
        msg = "Not Infected"
    else:
        msg = "Infected"

    return render(request, "predict.html", 
                  {"prediction" : msg})