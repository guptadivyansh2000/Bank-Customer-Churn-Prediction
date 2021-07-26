# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 12:31:15 2021

@author: gupta
"""
import pywebio
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask , send_from_directory
from sklearn.preprocessing import StandardScaler
from pywebio.input import *
from pywebio.output import *
import pickle 
from argparse import ArgumentParser
import nest_asyncio
nest_asyncio.apply()
scaler=StandardScaler()
model=pickle.load(open('churn_model_undersampling.pkl','rb'))
app=Flask(__name__)


def predict():
    CreditScore=input("Enter the credit score",type=FLOAT)
    Age=input("Enter the Age",type=NUMBER)
    Tenure=input("enter the tenure",type=NUMBER)
    Balance=input("enter the balance present in your account",type=FLOAT)
    NumOfProducts=input('no of products',type=NUMBER)
    HasCrCard=input("you have credit card yes 1 or no 0",type=NUMBER)
    IsActiveMember=input('is active member ',type=NUMBER)
    EstimatedSalary=input("Enter the Salary",type=FLOAT)
    
    Gender=select('are you a male or female',['Female','Male'])
    if (Gender=='Male'):
        Gender=1
    else:
        Gender=0
        
    Geography=select("choose ur location",['Geography_France','Geography_Germany','Geography_Spain'])
    if (Geography=='Geography_France'):
        Geography_France=1
        Geography_Germany=0
        Geography_Spain=0
        
    elif (Geography=='Geography_Germany'):
        Geography_France=0
        Geography_Germany=1
        Geography_Spain=0
    else:
        Geography_France=0
        Geography_Germany=0
        Geography_Spain=1
        
        
    #scaler=StandardScaler()
    scaler.fit_transform([CreditScore,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,Gender,Geography])
    prediction=model.predict([[CreditScore,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,Gender,Geography]])
    
    
    output=round(prediction[0])   
    if (prediction==1):
        put_text('customer will churn')
        
    else:
        put_text('customer will not churn')
        
app.add_url_rule('/tools','webio_view',webio_view(predict),methods=['GET','POST','OPTIONS'])

'''if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(predict, port=args.port)'''
    
 
if __name__ == '__main__' :
     pywebio.start_server(predict,port=80)       
        
        
        
        
        
        