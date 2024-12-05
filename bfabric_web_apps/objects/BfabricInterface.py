from bfabric import Bfabric
import requests
import json
import datetime
import bfabric
from bfabric import BfabricAuth
from bfabric import BfabricClientConfig
from dash import html
import dash_bootstrap_components as dbc
from bfabric_web_apps.objects.Logger_object import Logger


VALIDATION_URL = "https://fgcz-bfabric.uzh.ch/bfabric/rest/token/validate?token="
HOST = "fgcz-bfabric.uzh.ch"


class BfabricInterface( Bfabric ): 

    def __init__(self): 
        pass

    def token_to_data(self, token): 
        if not token:
            return None

        validation_url = VALIDATION_URL + token
        res = requests.get(validation_url, headers={"Host": HOST})
        
        if res.status_code != 200:
            res = requests.get(validation_url)
        
            if res.status_code != 200:
                return None
        try:
            master_data = json.loads(res.text)
        except:
            return None
        
        if True: 

            userinfo = json.loads(res.text)
            expiry_time = userinfo['expiryDateTime']
            current_time = datetime.datetime.now()
            five_minutes_later = current_time + datetime.timedelta(minutes=5)

            # Comparing the parsed expiry time with the five minutes later time

            if not five_minutes_later <= datetime.datetime.strptime(expiry_time, "%Y-%m-%d %H:%M:%S"):
                return "EXPIRED"
            
            environment_dict = {"Production":"https://fgcz-bfabric.uzh.ch/bfabric","Test":"https://fgcz-bfabric-test.uzh.ch/bfabric"}
            
            token_data = dict(
                environment = userinfo['environment'],
                user_data = userinfo['user'],
                token_expires = expiry_time,
                entity_id_data = userinfo['entityId'],
                entityClass_data = userinfo['entityClassName'],
                webbase_data = environment_dict.get(userinfo['environment'], None),
                application_params_data = {},
                application_data = str(userinfo['applicationId']),
                userWsPassword = userinfo['userWsPassword'],
                jobId = userinfo['jobId']
            )

            return json.dumps(token_data)
        


    def token_response_to_bfabric(self, token_response): 

        bfabric_auth = BfabricAuth(login=token_response.get('user_data'), password=token_response.get('userWsPassword'))
        bfabric_client_config = BfabricClientConfig(base_url=token_response.get('webbase_data')) 

        bfabric_wrapper = bfabric.Bfabric(config=bfabric_client_config, auth=bfabric_auth)

        return bfabric_wrapper
    

    

    def entity_data(self, token_data: dict) -> str: 

        """
        This function takes in a token from bfabric, and returns the entity data for the token.
        Edit this function to change which data is stored in the browser for this entity.
        """

        entity_class_map = {
            "Run": "run",
            "Sample": "sample",
            "Project": "container",
            "Order": "container",
            "Container": "container",
            "Plate": "plate"
        }

        if not token_data:
            return None

        wrapper = self.token_response_to_bfabric(token_data)
        entity_class = token_data.get('entityClass_data', None)
        endpoint = entity_class_map.get(entity_class, None)
        entity_id = token_data.get('entity_id_data', None)
        jobId = token_data.get('jobId', None)
        username = token_data.get("user_data", "None")
        environment= token_data.get("environment", "None")


        if wrapper and entity_class and endpoint and entity_id and jobId:

            L = Logger(
                jobid = jobId,
                username= username,
                environment= environment
            ) 
            
            # Log the read operation directly using Logger L
            entity_data_dict = L.logthis(
                api_call=wrapper.read,
                endpoint=endpoint,
                obj={"id": entity_id},
                max_results=None,
                params = None,
                flush_logs = True
            )[0]
            
            if entity_data_dict:
                json_data = json.dumps({
                    "createdby": entity_data_dict.get("createdby"),
                    "created": entity_data_dict.get("created"),
                    "modified": entity_data_dict.get("modified"),
                })
                return json_data
            else:
                L.log_operation(
                    operation= "entity_data",
                    message= "Entity data retrieval failed or returned None.",
                    params=None,
                    flush_logs=True
                )
                print("entity_data_dict is empty or None")
                return None
            
        else:
            print("Invalid input or entity information")
            return None

