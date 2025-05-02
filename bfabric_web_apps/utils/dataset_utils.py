
def is_numeric(value):
    try:
        float(value)  # or int(value) if you only want integers
        return True
    except ValueError:
        return False


def dataset_to_dictionary(dataset): 

    """
    Convert B-Fabric API Dataset Response 
    to a dictionary. The dictionary will have the attribute names as keys and the field values as lists, 
    so that it can be easily converted to a pandas dataframe.

    Args: 
        dataset (dict): B-Fabric API Dataset Response

    Returns:
        dict: A dictionary where the keys are the attribute names and the values are lists of field values, ready to become a pandas dataframe.
    """

    # Check if the dataset is empty
    if not dataset:
        return {}

    attributes = dataset.get("attribute", []) 
    items = [elt.get("field") for elt in dataset.get("item", [])]

    position_map = {str(elt.get("position")): elt.get("name") for elt in attributes} # Create a mapping of attribute positions to names
    df_dict = {elt : [] for elt in position_map.values()} # Create a dictionary to hold the dataframe data

    for item in items: 
        for field in item: 
            attribute_position = field.get("attributeposition")
            df_dict[position_map.get(attribute_position)].append(field.get("value")) # Append the field value to the corresponding attribute name in the dictionary
                
    # Create a dataframe from the dictionary
    return df_dict


def dictionary_to_dataset(dictionary, dataset_name, containerid, dataset_template_id=0, linked_workunit_id=0): 
    
    """
    Convert a dictionary to a B-Fabric API Dataset

    Args: 
        dictionary (dict): A dictionary where the keys are the attribute names and the values are lists of field values.

    Returns:
        dict: A B-Fabric API Dataset ready to be sent to the API.
    """

    if not isinstance(dictionary, dict):
        raise ValueError("Input must be a dictionary.")
    
    if not isinstance(dataset_name, str):
        raise ValueError("Dataset name must be a string.")
    
    if not is_numeric(containerid):
        raise ValueError("Container ID must be a numeric string or integer.")
    
    if not isinstance(dataset_template_id, int):
        raise ValueError("Dataset template ID must be an integer.")
    
    if not isinstance(linked_workunit_id, int):
        raise ValueError("Linked workunit ID must be an integer.")

    # Check if the dictionary is empty
    if not dictionary:
        return {}

    # Create a list of attributes
    attributes = [{"name": name, "position": str(i+1)} for i, name in enumerate(dictionary.keys())]

    # Create a list of items
    items = []
    for i in range(len(next(iter(dictionary.values())))):  # Get the length of the first value list
        item = [{"attributeposition": str(j+1), "value": dictionary[name][i]} for j, name in enumerate(dictionary.keys())]
        items.append({"field": item, "position": str(i+1)})

    to_return = {"attribute": attributes, "item": items, "name": dataset_name, "containerid": containerid}

    if dataset_template_id:
        # Add the dataset template ID to the dataset
        to_return["datasettemplateid"] = dataset_template_id

    if linked_workunit_id:
        # Add the linked workunit ID to the dataset
        to_return["workunitid"] = linked_workunit_id

    return to_return