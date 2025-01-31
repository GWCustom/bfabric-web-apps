from bfabric import Bfabric
import requests
import json
import datetime
import bfabric
from bfabric import BfabricAuth
from bfabric import BfabricClientConfig
from bfabric_web_apps.utils.get_logger import get_logger
import os
import bfabric_web_apps



VALIDATION_URL = "https://fgcz-bfabric.uzh.ch/bfabric/rest/token/validate?token="
HOST = "fgcz-bfabric.uzh.ch"


class BfabricInterface( Bfabric ):
    """
    A class to interface with the Bfabric API, providing methods to validate tokens,
    retrieve data, and send bug reports.
    """

    def __init__(self):
        """
        Initializes an instance of BfabricInterface.
        """
        pass

    def token_to_data(self, token):
        """
        Validates the given token and retrieves its associated data.

        Args:
            token (str): The token to validate.

        Returns:
            str: A JSON string containing token data if valid.
            str: "EXPIRED" if the token is expired.
            None: If the token is invalid or validation fails.
        """

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

        """
        Converts token response data into a Bfabric object for further interactions.

        Args:
            token_response (dict): The token response data.

        Returns:
            Bfabric: An authenticated Bfabric instance.
        """

        bfabric_auth = BfabricAuth(login=token_response.get('user_data'), password=token_response.get('userWsPassword'))
        bfabric_client_config = BfabricClientConfig(base_url=token_response.get('webbase_data')) 

        bfabric_wrapper = bfabric.Bfabric(config=bfabric_client_config, auth=bfabric_auth)

        return bfabric_wrapper
    

    

    def entity_data(self, token_data: dict) -> str: 
        """
        Retrieves entity data associated with the provided token.

        Args:
            token_data (dict): The token data.

        Returns:
            str: A JSON string containing entity data.
            {}: If the retrieval fails or token_data is invalid.
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
            return json.dumps({})
        
        wrapper = self.token_response_to_bfabric(token_data)
        entity_class = token_data.get('entityClass_data', None)
        endpoint = entity_class_map.get(entity_class, None)
        entity_id = token_data.get('entity_id_data', None)
        jobId = token_data.get('jobId', None)
        username = token_data.get("user_data", "None")
        environment = token_data.get("environment", "None")

        if wrapper and entity_class and endpoint and entity_id and jobId:
            L = get_logger(token_data)
            
            # Log the read operation directly using Logger L
            entity_data_dict = L.logthis(
                api_call=wrapper.read,
                endpoint=endpoint,
                obj={"id": entity_id},
                max_results=None,
                params=None,
                flush_logs=True
            )[0]
            
            if entity_data_dict:
                json_data = json.dumps({
                    "name": entity_data_dict.get("name", ""),
                    "createdby": entity_data_dict.get("createdby"),
                    "created": entity_data_dict.get("created"),
                    "modified": entity_data_dict.get("modified"),
                })
                return json_data
            else:
                L.log_operation(
                    operation="entity_data",
                    message="Entity data retrieval failed or returned None.",
                    params=None,
                    flush_logs=True
                )
                print("entity_data_dict is empty or None")
                return json.dumps({})
            
        else:
            print("Invalid input or entity information")
            return json.dumps({})
        
    
    def send_bug_report(self, token_data = None, entity_data = None, description = None):
        """
        Sends a bug report via email.

        Args:
            token_data (dict): Token data to include in the report.
            entity_data (dict): Entity data to include in the report.
            description (str): A description of the bug.

        Returns:
            bool: True if the report is sent successfully, False otherwise.
        """

        mail_string = f"""
        BUG REPORT FROM QC-UPLOADER
            \n\n
            token_data: {token_data} \n\n 
            entity_data: {entity_data} \n\n
            description: {description} \n\n
            sent_at: {datetime.datetime.now()} \n\n
        """

        mail = f"""
            echo "{mail_string}" | mail -s "Bug Report" {bfabric_web_apps.BUG_REPORT_EMAIL_ADDRESS}
        """

        print("MAIL STRING:")
        print(mail_string)

        print("MAIL:")
        print(mail)

        os.system(mail)

        return True

