from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pymysql
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import os

global uname
global X_train, X_test, y_train, y_test, X, Y, dataset, rf_flood, rf_loc, scaler, le
communicate = []

dataset = pd.read_csv("Dataset/FloodPrediction.csv")
le = LabelEncoder()
dataset['Location'] = pd.Series(le.fit_transform(dataset['Location'].astype(str)))#encode all str columns to numeric
dataset.fillna(0, inplace = True)

location = dataset['Location'].values.ravel()
flood = dataset['Flood?']

dataset.drop(['Sl', 'Location', 'Flood?'], axis = 1,inplace=True)

X = dataset.values

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, location, test_size = 0.2)
X_train1, X_test1, y_train1, y_test1 = train_test_split(X, flood, test_size = 0.2)

rf_loc = RandomForestClassifier()
rf_loc.fit(X_train, y_train)

rf_flood = RandomForestClassifier()
rf_flood.fit(X_train1, y_train1)
predict = rf_flood.predict(X_test1)
p = precision_score(y_test1, predict,average='macro') * 100
r = recall_score(y_test1, predict,average='macro') * 100
f = f1_score(y_test1, predict,average='macro') * 100
a = accuracy_score(y_test1,predict)*100

def PredictAction(request):
    if request.method == 'POST':
        global rf_flood, rf_loc, scaler, le
        myfile = request.FILES['t1'].read()
        fname = request.FILES['t1'].name
        if os.path.exists("DisasterApp/static/"+fname):
            os.remove("DisasterApp/static/"+fname)
        with open("DisasterApp/static/"+fname, "wb") as file:
            file.write(myfile)
        file.close()
        test_data = pd.read_csv("DisasterApp/static/"+fname)
        test_data.fillna(0, inplace = True)
        test = test_data.values
        test_data = scaler.transform(test)
        flood = rf_flood.predict(test_data)
        loc = rf_loc.predict(test_data)
        loc = le.inverse_transform(loc)
        output='<table border=1 align=center width=100%><tr><th><font size="" color="black">Test Data</th><th><font size="" color="black">Disaster Next Possible Predicted Location</th></tr>'
        for i in range(len(loc)):
            if flood[i] == 1:
                output+='<tr><td><font size="" color="black">'+str(test[i])+'</td><td><font size="" color="black">'+loc[i]+'</td></tr>'
        context= {'data':output}
        return render(request, 'ViewResult.html', context)   

def Guidelines(request):
    if request.method == 'GET':
       return render(request, 'Guidelines.html', {})        

def Predict(request):
    if request.method == 'GET':
       return render(request, 'Predict.html', {})

def Communication(request):
    if request.method == 'GET':
       return render(request, 'Communication.html', {})

def CommunicationAction(request):
    if request.method == 'POST':
        global uname, communicate
        query = request.POST.get('t1', False)
        communicate.append(uname+" : "+query)
        context= {'data':"Your query posted! Reply can be view in View Communications Link"}
        return render(request, 'Communication.html', context)

def ViewCommunication(request):
    if request.method == 'GET':
        global uname, communicate
        data = ""
        for i in range(len(communicate)):
            data += communicate[i]+"\n"
        output = '<table align="center" width="80">'
        output += '<tr><td><td><textarea name="t1" cols="80" rows="20">'+data+'</textarea></td></tr>'
        context= {'data':output}
        return render(request, 'ViewResult.html', context)

def TrainML(request):
    if request.method == 'GET':
        global p, r, f, a
        output='<table border=1 align=center width=100%><tr><th><font size="" color="black">Algorithm Name</th><th><font size="" color="black">Accuracy</th><th>'
        output += '<font size="" color="black">Precision</th><th><font size="" color="black">Recall</th><th><font size="" color="black">FSCORE</th></tr>'
        output+='</tr>'
        algorithms = ['Random Forest']
        output+='<td><font size="" color="black">'+algorithms[0]+'</td><td><font size="" color="black">'+str(a)+'</td>'
        output+='<td><font size="" color="black">'+str(p)+'</td><td><font size="" color="black">'+str(r)+'</td><td><font size="" color="black">'+str(f)+'</td></tr>'
        output+= "</table></br></br></br>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)        

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def LoadDataset(request):
    if request.method == 'GET':
       return render(request, 'LoadDataset.html', {})

def RegisterAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'disaster',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    status = "Username already exists"
                    break
        if status == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'disaster',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register(username,password,contact_no,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = "Signup completed<br/>You can login with "+username
        context= {'data': status}
        return render(request, 'Register.html', context)    

def UserLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'disaster',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username, password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    uname = username
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'UserLogin.html', context)                 

def LoadDatasetAction(request):
    if request.method == 'POST':
        myfile = request.FILES['t1'].read()
        fname = request.FILES['t1'].name
        if os.path.exists("DisasterApp/static/"+fname):
            os.remove("DisasterApp/static/"+fname)
        with open("DisasterApp/static/"+fname, "wb") as file:
            file.write(myfile)
        file.close()
        dataset = pd.read_csv("DisasterApp/static/"+fname, nrows=100)
        columns = dataset.columns
        dataset = dataset.values
        output='<table border=1 align=center width=100%><tr>'
        for i in range(len(columns)):
            output += '<th><font size="" color="black">'+columns[i]+'</th>'
        output += '</tr>'
        for i in range(len(dataset)):
            output += '<tr>'
            for j in range(len(dataset[i])):
                output += '<td><font size="" color="black">'+str(dataset[i,j])+'</td>'
            output += '</tr>'
        output+= "</table></br></br></br></br>"
        #print(output)
        context= {'data':output}
        return render(request, 'ViewResult.html', context)    







        
