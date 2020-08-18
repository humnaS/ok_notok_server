import numpy as np
import pandas as pd
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from sklearn import preprocessing
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import sklearn
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
import random 

df=pd.DataFrame()
data=pd.DataFrame()
my_df=pd.DataFrame()
dic=dict()
name_col=['Message Size', 'Incoming Header lines Count', 'Sender-IP','Number of complaints (BCL)', 'Inbox']

def get_file(my_file):
    global df
   
    try:
        print("hello from get file")
        file_rec = my_file
      
       
        df = pd.read_csv(file_rec.stream,delimiter=";")
        
        hold_data()
        
        retJson = {"status":200,"msg":"ok"}
        return True
    except Exception as e:
 
        try:
            file_rec = request.files['file']

            df = pd.read_excel(file_rec.stream)
      
          
            retJson = {"status":200,"msg":"ok"}
            return True
        except Exception as e:
            try:
                
                file_rec = my_file
            
            
                df = pd.read_csv(file_rec.stream)
                
                hold_data()
                print(df.head())
                retJson = {"status":200,"msg":"ok"}
                return True
                            
                
            except Exception as e:
                retJson = {"status":301,"msg":"This file format is not supported"}
            return False


def list_contains(List1, List2):
    count=0
    # Iterate in the 1st list 
    for m in List1: 
  
        # Iterate in the 2nd list 
        for n in List2: 
    
            # if there is a match
            if m == n: 
                count=count+1
                  
                  
    return count

def hold_data():
    global data
    #print("hello from hold")
    data=df.copy()
    
    #print(data.head())
    return data

def chk_col(df):
    global my_df
    my_df=df.copy()
    cols=my_df.columns
    cols=list(cols)
    
    check =  any(item in name_col for item in cols)
    print(check)
    if check ==True:
        count=list_contains(name_col,cols)
        print(count)
        if count==5:
            print("hello from inside")
            my_df=my_df[['Message Size', 'Incoming Header lines Count', 'Sender-IP','Number of complaints (BCL)', 'Inbox']]
            my_df.dropna(inplace=True)
            my_df=my_df.drop("Sender-IP",axis=1)
            my_df["cat"] = my_df["Inbox"].replace({"Yes": 1, "NO": 0,"YES":1,"No":0})
            X=my_df.drop(["Inbox","cat"],axis=1)
            y=my_df["cat"]
             
            print(type(y))
            return True,X,y
    else:
        
        return False,None,None
        
def chcking():
    try:
        global a
        global msgs
        global count
        chk,X,y=chk_col(data)
        print(chk)
        if chk== True:
            count=0
            print(X.head())
            print(y)
            a=Train_model(X,y)
            
            msgs=func_improve(X,y)
            
            find_model()
            
            return{"status":"200","List":msgs}
        else:
            return{"error":"your data shape is not correct"}
        
    except Exception as e:
        
        dic2={"error":"your data shape is not correct","msg":str(e)}
        return dic2


def Train_model(X,y):
    global dic
    print("Hllo from training")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
    model_decision = tree.DecisionTreeClassifier()
    model_decision.fit(X_train, y_train)
    y_pred_d= model_decision.predict(X_test)
    accuracy=accuracy_score(y_test, y_pred_d)

    ####################################
    
    model_svm = LinearSVC()
    model_svm.fit(X_train, y_train)
    y_pred_svm = model_svm.predict(X_test)

    accuracy2=accuracy_score(y_test, y_pred_svm)

    ##########################################
    # model_rdm = RandomForestClassifier(n_estimators = 10, criterion = 'entropy') 
							
    # model_rdm.fit(X_train, y_train) 
    # y_pred_rdm = model_rdm.predict(X_test)

    #accuracy3=accuracy_score(y_test, y_pred_rdm)
    dic={accuracy:model_decision,accuracy2:model_svm}
    
    my_list=[accuracy,accuracy2]
    print(my_list)
    my_list.sort(reverse=True)
    my_model=dic[my_list[0]]
    print(my_model)
    return my_list[0]

def func_improve(X,y):
    z=X["Number of complaints (BCL)"][0]
    y_arr=X["Incoming Header lines Count"].unique()
    y_list=y_arr.tolist()
    print(y_list)
    msg_size=X["Message Size"].unique()
    msg_list=msg_size.tolist()
    model=find_model()
    list_num=[]
    for num in y_list:
        for msgs in msg_list:
            pred=model.predict([[msgs,num,z]])
            if pred==1:
                #print(msgs,num)
                list_num.append([msgs,num])
    return list_num



def find_model():
    model=dic[a]
    return model

def count_num():
    count=random.randint(0,50)
    return count

def prediction(msg,msg1,msg2):
    try:
        model=find_model()
       
        pred=model.predict([[msg,msg1,msg2]])
        if pred==1:
            return{"Result":"Yes"}
        elif pred==0:
            count=count_num()
            return{"Result":"No","Message Size":msgs[count][0],"Incoming Header lines Count":msgs[count][1]}
    except Exception as e:
        dic2={"error":"your data shape is not correct","msg":str(e)}
        return dic2
    
    
   