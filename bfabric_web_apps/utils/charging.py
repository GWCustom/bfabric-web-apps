
from bfabric_web_apps.utils.get_logger import get_logger
from bfabric_web_apps.utils.get_power_user_wrapper import get_power_user_wrapper

def create_charge(token_data, container_id, service_id):
    """
    Create a charge in B-Fabric.
    
    Args:
        token_data (dict): Authentication token data.
        container_id (int): Container ID (Order ID).
        service_id (int): Service ID.
    
    Returns:
        list[dict]: List of charge data.
    """
    
    # Get a logger and an api wrapper
    L = get_logger(token_data)
    wrapper = get_power_user_wrapper(token_data)

    # Get the user ID from the token data to assign a charger
    usr_id = wrapper.read("user", {"login": token_data.get("user_data")})[0]['id']

    charge_data = {
        "serviceid": service_id,
        "containerid": container_id,
        "chargerid": usr_id
    }

    # Create and log the charge
    charge = L.logthis(
        api_call=wrapper.save,
        endpoint="charge",
        obj=charge_data,
        params=None,
        flush_logs=True
    )

    return charge
