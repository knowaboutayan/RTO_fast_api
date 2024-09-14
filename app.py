from error_response import api_err
from fastapi import FastAPI
from typing import Optional
from config import config
from pydantic import BaseModel
import random
from services import emailSending
import datetime
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://rto-managemet-system.vercel.app"],  # Or use ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

 
@app.get('/')
def index():
    return "THANKS FOR USING API BY CREATIONOLOGY"

@app.get('/vehicle_details')
def get_vehicle_details(vehicle_id:str = None):
    QUERY =  "SELECT * FROM vehicle_details" + (f" where vehicle_id = '{vehicle_id.upper()}'" if (vehicle_id is not None) else "")
    response = config.query_runner(sql_query=QUERY)
    if response == 1:
        return api_err.server_error
    if len(response)==0:
        return api_err.no_data_found
    
    formated_response = { 'status':200, 'data':[{'vehicle_id':row[0],'owner_id':row[1],'license_plate_no':row[2],'model':row[3]} for row in response]}
    # formated_response = json.dumps(formated_response)
    return formated_response

    
@app.get('/owner_details')
def get_owner_details(owner_id:str = None):
    QUERY =  "SELECT * FROM owner_details" + (f" where owner_id = '{owner_id.upper()}'" if (owner_id is not None) else "")
    response = config.query_runner(sql_query=QUERY)
    if response == 1:
        return api_err.server_error
    if len(response)==0:
        return api_err.no_data_found
    
    formated_response ={ 'status':200, 'data':[{'owner_id':row[0],'owner_name':row[1],'owner_email':row[2]} for row in response]}
    # formated_response = json.dumps(formated_response)
    return formated_response

@app.get('/challan_details')
def get_challan_details(challan_id:str =None):
    QUERY =  "SELECT * FROM challan_details" + (f" where challan_id = '{challan_id.upper()}'" if (challan_id is not None) else "")
    response = config.query_runner(sql_query=QUERY)
    if response == 1:
        return api_err.server_error
    if len(response)==0:
        return api_err.no_data_found
    
    formated_response ={ 'status':200, 'data':[{'challan_id':row[0],'license_plate_no':row[1],'violance_date':row[2],'violation':row[3],'amount':row[4],'violetion_time':row[5]} for row in response]}
    # formated_response = json.dumps(formated_response)
    return formated_response

class Owner_details(BaseModel):
    owner_id:str
    name:str
    email:str
    
@app.post('/add/owner_details')
async def add_owner_details(owner_details:Owner_details):
    QUERY = f"INSERT INTO owner_details VALUES('{owner_details.owner_id.upper()}','{owner_details.name.upper()}','{owner_details.email.lower()}');commit;"
    response = config.query_runner(sql_query=QUERY)
    if response == 1:
        return api_err.server_error
    if len(response)==0:
        return api_err.no_data_found
    
    formated_response ={ 'status':200, 'text':"Added successul"}
    # formated_response = json.dumps(formated_response)
    return formated_response

class Vehicle_details(BaseModel):
    vehicle_id: str
    name:str
    owner_id: str
    license_plate_no:str
    model: str
    email:str

@app.post('/add/vehicle_details')
async def add_vehicle(vehicle_details:Vehicle_details):
    with open('html_email/welcome.html') as file:
        body = file.read()
        body = body.replace("{{OWNER_NAME}}",vehicle_details.name.title())
        body = body.replace("{{OWNER_ID}}",vehicle_details.owner_id.upper())
        body = body.replace("{{VEHICLE_ID}}",vehicle_details.vehicle_id.upper())
        body = body.replace("{{VEHICLE_MODEL}}",vehicle_details.model.upper())
        body = body.replace("{{MODEL_NUMBER}}",vehicle_details.model.upper())
        body = body.replace("{{LICENSE_PLATE_NUMBER}}",vehicle_details.license_plate_no.upper())
    
    
    
    response = emailSending.send_email(receiver_email=[vehicle_details.email],subject=f"Registration Successful for {vehicle_details.license_plate_no.upper()}",body=body,body_type='html')
    
    if response==1:
        return api_err.server_error
   
    QUERY = f"INSERT INTO vehicle_details VALUES('{vehicle_details.vehicle_id.upper()}','{vehicle_details.owner_id.upper()}','{vehicle_details.license_plate_no.upper()}','{vehicle_details.model.upper()}');commit;"
    response = config.query_runner(sql_query=QUERY)
    if response == 1:
        return api_err.server_error
    if len(response)==0:
        return api_err.no_data_found
    
    formated_response ={ 'status':200, 'text':"Added successul"}
    # formated_response = json.dumps(formated_response)
    return formated_response

class Challan_details(BaseModel):
    name:str
    model:str
    challan_id:str
    license_plate_no:str
    violation:str
    amount:str
    violetion_time:str
    email:str
    
    
@app.post('/add/challan_details')
async def add_challan_details(challan_details:Challan_details):
    QUERY = f"""
    INSERT INTO challan_details 
    VALUES(
        '{challan_details.challan_id}',
        '{challan_details.license_plate_no}',
        DATE_FORMAT(CURDATE(), '%Y-%m-%d'),
        '{challan_details.violation}',
        '{challan_details.amount}',
        CURRENT_TIMESTAMP
    );
"""

    with open('html_email/challan.html') as file:
        body = file.read()
        body = body.replace("{{CHALLAN_NUMBER}}",challan_details.challan_id.upper())
        body = body.replace("{{DATE_TIME}}",f"{datetime.datetime.now()}")
        body = body.replace("{{VEHICLE_NUMBER}}",challan_details.license_plate_no.upper())
        body = body.replace("{{MODEL_NUMBER}}",challan_details.model.upper())
        body = body.replace("{{OWNER_NAME}}",challan_details.name.upper())
        body = body.replace("{{VIOLATION}}",challan_details.violation)
        body = body.replace("{{FINE_AMOUNT}}",challan_details.amount)
    
    response = emailSending.send_email(receiver_email=[challan_details.email],subject=f"E-CHALLAN for {challan_details.challan_id}",body=body,body_type='html')
    
    if response==1:
        return api_err.server_error
    
    response = config.query_runner(sql_query=QUERY)
    if response == 1:
        return api_err.server_error
    if len(response)==0:
        return api_err.no_data_found
    
    formated_response ={ 'status':200, 'text':"Added successul"}
    # formated_response = json.dumps(formated_response)
    return formated_response

class Otp(BaseModel):
    email:str
@app.post('/verification/otp')
async def otp_send(otp:Otp):
    OTP = random.randint(1000,9999)
    with open('html_email/OTP_verification.html') as file:
        body = file.read()
        body=body.replace('{{OTP}}',str(OTP))
        
    emailSending.send_email(receiver_email = [otp.email],body=body,body_type='html',subject="OTP verification")
    
    formated_response = {'status':200,'otp':OTP}
    return formated_response

class Update_owner_details(BaseModel):
    owner_id:str
    name:str
    email:str
    
@app.put('/update/owner_details')
async def updateOwner_details(update_owner_details:Update_owner_details):
    QUERY = f"UPDATE owner_details SET name = '{update_owner_details.name}',email='{update_owner_details.email}' WHERE owner_id = '{update_owner_details.owner_id}'"
    response = config.query_runner(sql_query=QUERY) 
    if(response==1):
        return api_err.update_unsuccessful
    return api_err.update_successful

class Update_vehicle_details(BaseModel):
    vehicle_id:str
    owner_id:str
    

@app.put('/update/vehicle_details')
async def updateOwner_details(update_vehicle_details:Update_vehicle_details):
    QUERY = f"UPDATE vehicle_details SET owner_id = '{update_vehicle_details.owner_id.upper()}' WHERE vehicle_id = '{update_vehicle_details.vehicle_id.upper()}'"
    response = config.query_runner(sql_query=QUERY) 
    if(response==1):
        return api_err.update_unsuccessful
    return api_err.update_successful

@app.delete('/delete/owner_details')
async def deleteOwner_details(owner_id:str):
    QUERY = f"DELETE FROM owner_details where owner_id = '{owner_id}'"
    response = config.query_runner(sql_query=QUERY) 
    if(response==1):
        return api_err.delete_unsuccessful
    return api_err.delete_successful
    
@app.delete('/delete/vehicle_details')
async def deleteOwner_details(vehicle_id:str):
    QUERY = f"DELETE FROM vehicle_details where vehicle_id = '{vehicle_id}'"
    response = config.query_runner(sql_query=QUERY) 
    if(response==1):
        return api_err.delete_unsuccessful
    return api_err.delete_successful

