from error_response import api_err
from fastapi import FastAPI
from typing import Optional
from config import config

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Or use ["*"] to allow all origins
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




