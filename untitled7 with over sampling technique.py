# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11qc06h2CAENp0vAzY00dffm0HKdUjfy3

**Bank Customer Churn Prediction Using Different ML Classification Algorithm .**

In this notebook i will have to build the model which will predict the customer will churn or not on the basis of the some features.

Preferably and based on model performance, choose a model that will attach a probability to the churn to make it easier for customer service to target low hanging fruits in their efforts to prevent churn.

**import the libraries**
"""

import pandas as pd 
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

"""importing the dataset into the dataframe"""

df=pd.read_csv(r'C:\Users\gupta\Downloads\churn.csv')
df.head(5)

df.shape

"""see the above line there are 10000 rows and 14 columns are there in this dataset"""

# i will check there is any null values or not
df.isnull().sum()

"""in this dataset there is no null values."""

df.describe(include='all')

#drop these features
df.drop(axis=1,columns=['RowNumber','CustomerId','Surname'],inplace=True)

df_corr=df.corr()
df_corr

"""in this dataset there is no correlation between the other different columns

"""

'''import seaborn as sns 
sns.heatmap(data=df.corr())

labels = 'Exited', 'Retained'
sizes = [df.Exited[df['Exited']==1].count(), df.Exited[df['Exited']==0].count()]
explode = (0, 0.1)
fig1, ax1 = plt.subplots(figsize=(10, 8))
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')
plt.title("Proportion of customer churned and retained", size = 20)
plt.show()'''

"""see the above the visiualization the many customers retained as compared to exited . From the above diagram there are only 20.4% people are exited

to check the outliers we will use boxplot
"""

'''sns.boxplot(data=df['CreditScore'],orient='v')

"""in the creditscore features there are some outliers"""

sns.boxplot(data=df['EstimatedSalary'],orient='v')

sns.boxplot(data=df['Balance'])

sns.boxplot(data=df['Tenure'],orient='v')

"""from the above three graphs we will there is no outlier values

"""

sns.boxplot(data=df['Age'],orient='v')

"""in the age column there are present many outliers"""

fig, axarr = plt.subplots(2, 2, figsize=(20, 12))
sns.countplot(x='Geography', hue = 'Exited',data = df, ax=axarr[0][0])
sns.countplot(x='Gender', hue = 'Exited',data = df, ax=axarr[0][1])
sns.countplot(x='HasCrCard', hue = 'Exited',data = df, ax=axarr[1][0])
sns.countplot(x='IsActiveMember', hue = 'Exited',data = df, ax=axarr[1][1])

df['Exited'].value_counts()

import matplotlib.pyplot as plt

exited_classes=pd.value_counts(df['Exited'],sort=True)
exited_classes.plot(kind='bar',rot=0)
plt.title('customer churn distribution')
plt.xticks(range(2))
plt.xlabel('exited_classes')
plt.ylabel('Frequency')'''

''' i will have convert categorical values in the numerical  '''
df = pd.get_dummies(df
                    , columns = ["Geography"])
df.replace({'Female': 0,'Male': 1},inplace=True)
df

"""**Remove all outlier from creditscore and age features**"""

q1=df.CreditScore.quantile(0.25)
q3=df.CreditScore.quantile(0.75)
q1,q3

iqr=q3-q1
iqr

upper_limit=q3+1.5*iqr
lower_limit=q1-1.5*iqr
upper_limit,lower_limit

df1=df[(df.CreditScore>lower_limit)&(df.CreditScore<upper_limit)]
df1.sample(5)

df1.CreditScore.value_counts()

Q1=df.Age.quantile(0.25)
Q3=df.Age.quantile(0.75)
Q1,Q3

IQR=Q3-Q1
IQR

upper_bound=Q3+1.5*IQR
lower_bound=Q1-1.5*IQR
upper_bound,lower_bound

df2=df1[(df1.Age>lower_bound)&(df1.Age<upper_bound)]
df2.sample(5)

sns.boxplot(data=df2['CreditScore'],orient='v')

"""split the dataset"""

x=df2.drop(['Exited'],axis=1)
y=df2['Exited']

''' this will balanced the dataset'''
from imblearn.combine import SMOTETomek
smk=SMOTETomek(random_state=42)
X_res,y_res=smk.fit_resample(x,y)
print(X_res.shape,y_res.shape)

'''split the dataset into training and testing dataset'''
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X_res,y_res,test_size=0.2)

"""*Feature Scaling*"""

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.transform(X_test)

"""**Building the Models**

*first i will used logistic regression*
"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
logit=LogisticRegression(random_state=10)
logit.fit(X_train,y_train)

y_pred=logit.predict(X_test)

x_pred=logit.predict(X_train)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

from sklearn.metrics import accuracy_score
score=accuracy_score(y_pred,y_test)
score

from sklearn.metrics import classification_report
print(classification_report(y_test,y_pred))

accuracy_score(x_pred,y_train)

"""from this algorithm i will get 74% accuracy on testing data and almost same accuracy on training data

**KNN ALGORITHIM**
"""





from sklearn.neighbors import KNeighborsClassifier
neigh = KNeighborsClassifier(n_neighbors=3,metric='minkowski')

neigh.fit(X_train,y_train) 

ypredknn=pd.DataFrame(neigh.predict(X_test))

print('Testing data : {}'.format(accuracy_score(y_test,ypredknn)))
print(confusion_matrix(y_test,ypredknn))
print(classification_report(y_test,ypredknn))

"""**Training Accuracy**"""

xpredknn=pd.DataFrame(neigh.predict(X_train))
print(accuracy_score(y_train,xpredknn))

error_rate = []
# Will take some time
for i in range(1,40):
 
 knn = KNeighborsClassifier(n_neighbors=i)
 knn.fit(X_train,y_train)
 pred_i = knn.predict(X_test)
 error_rate.append(np.mean(pred_i != y_test))

import matplotlib.pyplot as plt
plt.figure(figsize=(10,6))
plt.plot(range(1,40),error_rate,color='blue', linestyle='dashed', marker='o',
 markerfacecolor='red', markersize=10)
plt.title('Error Rate vs. K Value')
plt.xlabel('K')
plt.ylabel('Error Rate')

"""with this very easily i will choose the value of k"""

from sklearn.neighbors import KNeighborsClassifier
knn_clf = KNeighborsClassifier(n_neighbors=15,metric='minkowski',p=2)

knn_clf.fit(X_train,y_train) 

ypred=knn_clf.predict(X_test)
print(confusion_matrix(y_test,ypred))

print(classification_report(y_test,ypred))
print('testing data {}'.format(accuracy_score(y_test,ypred)))



"""**DECISION TREE CLASSIFIER**"""

from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier( max_depth=7,random_state=0,class_weight='balanced')
classifier = classifier.fit(X_train,y_train)
pred_dc=classifier.predict(X_test)
xpred_dc=classifier.predict(X_train)
from sklearn import metrics
print( 'Testing Accuracy',metrics.accuracy_score(y_test,pred_dc))
print( 'Training Accuracy',metrics.accuracy_score(y_train,xpred_dc))

print(confusion_matrix(y_test,pred_dc))

print(classification_report(y_test,pred_dc))

classifier.predict_proba(X_test)





"""**Random Forest Classifier**"""

from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier( n_estimators=300,criterion='entropy',max_depth=12, random_state=10,class_weight='balanced')
clf.fit(X_train, y_train)
pred=clf.predict(X_test)
xpred=clf.predict(X_train)
print(confusion_matrix(y_test,pred))

print(classification_report(y_test,pred))
print(accuracy_score(y_test,pred))
print('training accuracy',accuracy_score(y_train,xpred))

y_test[:10]

pred[:100]==y_test[:100]



clf.predict([[550,1,50,5,250000,0,0,1,14000,0,1,0]])







"""**Support Vector Classifier**"""

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

clf_svc = SVC(kernel='rbf')
clf_svc.fit(X_train,y_train)
svc_pred = clf_svc.predict(X_test)
print(accuracy_score(y_test,svc_pred))

print(confusion_matrix(y_test,svc_pred))

print(classification_report(y_test,svc_pred))

y_test[:100]

svc_pred[:100]==y_test[:100]

"""**Model Pickling**"""

import pickle
pickle.dump(clf, open('churn_model.pkl','wb'))

