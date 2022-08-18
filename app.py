import json
from urllib import request
from flask import Flask,Response,request
import pathlib
import pandas as pd
from werkzeug.utils import secure_filename
import pdfplumber
from collections import Counter

companies=['CHOLA','HDFC','FGI','ICICI','NIA','RSA','SBI']

app=Flask(__name__)


def policy_type_return(fileName):
    file_ext=pathlib.Path(fileName).suffix
    return  file_ext=='.pdf'
        

          

@app.route("/company",methods=["POST"])
def get_company():
    policy=request.files["fileName"]
    fileName=policy.filename
    if not policy_type_return(fileName):
        return Response (
            response=json.dumps({"message":"Not a pdf file"}),
            status=200,
            mimetype="appication/json"
        )
             
    count=dict()
    with pdfplumber.open(fileName) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
            policy=text
            word=''
            # print(policy.count('CHOLA'))
    for letter in policy:
        if letter!=' ':
            word+=letter
        if letter==' ':
            word=word.upper()
            print(word)
            for company in companies:
                if company in word:
                    if company in count:
                        count[company]+=1
                    else:
                        count[company]=1
            word=''
                    
    max_count=0
    company_policy=''
    for company in companies:
        if company in count and count[company]>max_count:
            max_count=count[company]
            company_policy=company      
    print(company_policy,max_count)     
    return Response(
            response=json.dumps({"message":company_policy}),
            status=200,
            mimetype="appication/json"
            
        )   
        
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80,debug=True)