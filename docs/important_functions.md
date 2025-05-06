# B-Fabric Web Apps Functions

This section provides an in-depth explanation of the **core functions** used in **bfabric\_web\_apps**. These functions are responsible for **authentication, layout management, logging, API interactions, bug reporting** and more.

---
## 1. Application Initialization

### create_app()

The `create_app()` function initializes a **Dash app instance** with pre-configured settings suitable for use with B-Fabric, including responsive design and Bootstrap-based styling. This function simplifies starting a new Dash app by applying common configurations.

If you want to explore the implementation of the `create_app()` function in more detail, check out the [source code on GitHub](https://github.com/GWCustom/bfabric-web-apps/blob/main/bfabric_web_apps/utils/app_init.py).

```python
app = create_app()
```
#### Returns:
A Dash app instance with support for dynamic callbacks and responsive design.

---

#### Return type:
`dash.Dash`

---

#### Example Usage

```python
from bfabric_web_apps import create_app

# Create an instance of the Dash app using the create_app function.
app = create_app()
```
---

### Understanding the app Object in Dash  
The `app` object is an instance of the `Dash` class from the [`dash`](https://dash.plotly.com/) library. It serves as the central object of a Dash application, managing the layout, callbacks, and overall app configuration. The `Dash()` class is used to create an instance of a Dash application. It initializes the app, providing the structure to define its layout and interactivity. The `Dash()` class serves as the foundation for building Dash applications, allowing developers to add components like HTML elements, interactive controls, and graphs.

For more details on defining layouts in Dash, refer to the [Dash Layout Documentation](https://dash.plotly.com/layout#dash-layout).

---

## 2. UI and Layout Management

### get_static_layout()

The `get_static_layout()` function combines various **UI components** into a structured Dash layout with pre-defined tabs for **Main**, **Documentation**, and **Report a Bug**. This layout ensures a consistent look and feel across B-Fabric applications, while allowing customization of the main content and documentation.

If you want to explore the implementation of the `get_static_layout()` function in more detail, check out the [source code on GitHub](https://github.com/GWCustom/bfabric-web-apps/blob/main/bfabric_web_apps/layouts/layouts.py#L4).


```python
app.layout = get_static_layout(app_title, main_content, documentation_content)
```

#### Args:
1. **base_title** (*str*, optional): The title displayed in the browser tab. Defaults to `None`.
2. **main_content** (*Dash HTML Component*, optional): The main content displayed in the "Main" tab. Defaults to `None`.
3. **documentation_content** (*Dash HTML Component*, optional): The static documentation displayed under the "Documentation" tab. Defaults to `None`.

---

#### Returns:
A Dash layout containing the specified content along with static tabs for **Main**, **Documentation**, and **Report a Bug**.

---

#### Return type:
`dash.html.Div`

---

#### Example Usage
```python
# Import the 'html' module from Dash
from dash import html

sidebar = html.Div([...])  # Custom sidebar content
content = html.Div([...])  # Main app content
documentation = html.Div([...])  # Documentation content

# Set the layout of the app
app.layout = get_static_layout("My App", sidebar, documentation)
```

For detailed guidance on implementing and structuring layouts, please refer to the official [Dash documentation](https://dash.plotly.com/layout).

---

## 3. Authentication & Token Handling

### Overview

The B-Fabric authentication flow is designed to be straightforward and seamless for users of the `bfabric_web_app` library. While the underlying processes are abstracted, the following provides an overview of how the authentication and token handling works.

![Authentication Token Flow](_images/Authentication_Token_Flow.png)

#### Steps Explained:

1. **Token Sent to FGCZ Application Server**  
   When a user clicks a link in B-Fabric, they are redirected to the web application's page. The authentication token is included as a parameter in the URL.  
   Example URL:  
   `https://some.webapp/param1?token=xyabcdefg1234561234234234asdf`

2. **Token Validation**  
   The web application sends the token to a dedicated REST endpoint hosted on `fgcz-bfabric.uzh.ch`.

3. **Token Decryption**  
   If the token is valid, B-Fabric responds with a JSON payload containing essential authentication details, such as the username, web service password, and entity class information.

4. **Authenticated API Calls**  
    Now that the web application has authenticated the user, it can use the username and web service password obtained from the token auth endpoint to authenticate subsequent calls to the B-Fabric web service.

---

### process_url_and_token()

The `process_url_and_token()` function processes URL parameters to extract and validate authentication tokens, retrieve related entity data, and prepare page content for B-Fabric applications.

If you want to explore the implementation of the `process_url_and_token()` function in more detail, check out the [source code on GitHub](https://github.com/GWCustom/bfabric-web-apps/blob/main/bfabric_web_apps/utils/callbacks.py#L8).

```python
process_url_and_token(url_params)
```

#### Args:
1. **url_params** (*str*):  
   The URL parameters containing the token (e.g., `"?token=abc123"`).

---

#### Processing Steps:

1. **Check for `url_params`**:  
   - If `url_params` is empty or `None`, the function immediately returns `None` for the token, token data, entity data, app data, session details, `None` for the job link, and a default `" "` for the page title.

2. **Extract the token**:  
   - Splits the `url_params` string to find the segment after `token=`.
   - This extracted string is treated as the token.

3. **Validate the token**:  
   - Calls `BfabricInterface.token_to_data(token)` to validate the token.  
   - If the token is expired (`"EXPIRED"`), returns `None` for the token, token data, entity data, app_data, session details, job link, and a default `" "` for the page title.  
   - If the token is invalid or not found, the function also returns `None` values for these fields and uses `" "` for the page title.

4. **Retrieve entity data and app data**:  
   - On successful token validation, loads the token data (`tdata`) from JSON.  
   - Calls `BfabricInterface.entity_data(tdata)` to fetch entity details and parses it into `entity_data`.  
   - Calls `BfabricInterface.app_data(tdata)` to fetch app-related information and parses it into `app_data`.

5. **Generate page title**:  
   - Constructs a string based on the entity class, entity name, and environment.  
   - Falls back to `"Bfabric App Interface"` if key fields are missing.

6. **Construct job link**:  
   - Extracts the `jobId` from the token data (`tdata`).  
   - Checks the environment (test or production) and constructs the corresponding B-Fabric job URL with `jobId`.  
   - If no `jobId` is present, `job_link` defaults to `None`.

7. **Compose session details**:  
   - Builds a list of Dash HTML components containing summary information about the entity, token details, and app metadata.  
   - Includes environment, job ID, user name, session expiration time, and the current timestamp.

---

#### Returns:
The function returns a 7-element tuple, which varies depending on whether authentication succeeds or fails.

1. **Authenticated Case**:
   - **Returns**:
     1. **token** (*str*): The extracted token string.
     2. **token_data** (*dict*): A dictionary containing valid user and environment data.
     3. **entity_data** (*dict*): Details about the current entity (e.g., name, class).
     4. **app_data** (*dict*): Information about the related application (e.g., name, description).
     5. **page_title** (*str*): A dynamically generated string based on token and entity data.
     6. **session_details** (*list*): A list of Dash HTML components summarizing the session.
     7. **job_link** (*str*): Dynamically generated link to the job page (if `jobId` is provided).
   - **Return Type**:  
     *(str, dict, dict, dict, str, list, str)*

2. **Authentication Fails**:
   - **Returns**:
     1. **token**: `None`
     2. **token_data**: `None`
     3. **entity_data**: `None`
     4. **app_data**: `None`
     5. **page_title** (*str*): Defaults to `" "`.
     6. **session_details**: `None`
     7. **job_link**: `None`
   - **Return Type**:  
     *(None, None, None, None, str, None, None)*

---

#### Example Usage - Callback Integration
This function is typically used within a Dash callback to manage authentication. As a reference, you can check out how this function is used in [`generic_bfabric.py`](https://github.com/GWCustom/bfabric-web-app-template/blob/main/generic_bfabric.py#L44).

```python
@app.callback(
    [
        Output('token', 'data'),                # Store authentication token.
        Output('token_data', 'data'),           # Store token metadata.
        Output('entity', 'data'),               # Store entity data.
        Output('app_data', 'data'),               # Store app data.
        Output('page-title', 'children'),       # Update page title.
        Output('session-details', 'children'),  # Update session details.
        Output('dynamic-link', 'href')  # Directly update the button!
    ],
    [Input('url', 'search')]                    # Extract token from URL parameters.
)
def generic_process_url_and_token(url_params):
    return process_url_and_token(url_params)
```

---

## 4. Logging

### Overview

Logging in B-Fabric is crucial for tracking user actions, API calls, and errors. Logs are stored in B-Fabric's job history, ensuring transparency, accountability, and effective debugging.

---

### Accessing Logs in B-Fabric  

1. Open the **Job** menu item (see screenshot).  
2. Use filters or search by **Job ID** to find the relevant job.  
3. Click on the **Job ID** to open the job details.  
4. In the job details view, click on the **Log** entry to access all recorded logs for that job.  

![Screenshot showing where to find logs in B-Fabric](_images/Logger_page.png)  

If the web application is based on the provided **[templates](usage.md)**, there is an additional way to find the logs.

#### Through Web Applications
If the web applications are built using the provided **[templates](usage.md)**, a shortcut to logs is available:  
1. In the application, locate the **button in the top-right corner** (see screenshot).  
2. Clicking this button will **directly open the corresponding logs** for the job.  


![Screenshot of the log button in web apps](_images/View_Logs.png)  

---

### Initializing a Logger Instance  

A logger instance is essential for tracking user actions, API calls, and errors within B-Fabric. This process ensures accountability and simplifies debugging by maintaining detailed logs of system events.

---

#### get_logger()

The `get_logger()` function extracts logging-related information from `token_data` and initializes a **Logger instance** for managing and storing logs in B-Fabric.

If you want to explore the implementation of the `get_logger()` function in more detail, check out the [source code on GitHub](https://github.com/GWCustom/bfabric-web-apps/blob/main/bfabric_web_apps/utils/get_logger.py).

```python
L = get_logger(token_data)
```

##### Args:  
1. **token_data** (*dict*): A dictionary containing token information. This is required to associate logs with the corresponding user or session in B-Fabric.

##### Returns:  
A logger instance for managing and creating logs.

#### Return Type:: 
`bfabric_web_apps.Logger.Logger`

##### Example

```python
# Check if token data is available
if token_data:
    # Initialize the logger instance
    L = get_logger(token_data)
    
    # Use logger instance to log a simple user action
    L.log_operation("User Login", "User logged in successfully.")
```

---

### Creating Logs: Manual and Automatic Methods  

Logging in B-Fabric enables tracking of system events through two key methods: **manual logging** with `log_operation()` and **automatic logging** with `logthis()`.  

- **Use `log_operation()`** when you need to manually record specific user actions or system events, such as data submissions or logins.
- **Use `logthis()`** when making API calls to automatically log execution details, including function names, input parameters, execution time, and results. This simplifies API monitoring by capturing all relevant context without additional manual logging.  

---

#### log_operation()

The `log_operation()` function allows manual logging of user actions, storing these logs in **B-Fabric's job history**. It is commonly used for tracking specific events, such as data submissions or user logins.

If you want to explore the implementation of the `log_operation()` function in more detail, check out the [source code on GitHub](https://github.com/GWCustom/bfabric-web-apps/blob/main/bfabric_web_apps/objects/Logger.py#L69).


```python
L.log_operation(operation, message, params, flush_logs)
```

##### Args:  
1. **operation** (*str*): A short event label describing the action (e.g., `"Login"`, `"Update Sample"`).  
2. **message** (*str*): A detailed description of the event.  
3. **params** (*dict*, optional): Additional metadata related to the event. Defaults to `{}`.  
4. **flush_logs** (*bool*): Controls whether logs are immediately sent to the backend. Defaults to `True`.   
   - If `True`: The log entry is appended to the local log storage and immediately flushed to the backend using the `flush_logs()` method. This ensures that the log is recorded in real time.  
   - If `False`: The log entry is stored locally and will remain in the local cache until the next time the `flush_logs()` method is explicitly called. This can be useful for batching multiple log entries to minimize backend calls.

---

##### Returns:  
- `None`

---

##### Example

```python
# Check if token data is available
if token_data:
    # Initialize the logger instance
    L = get_logger(token_data)
    # Log a file upload action
    L.log_operation(
        operation ="FileUpload", 
        message = "User uploaded a CSV file",
        params = {"filename": "data.csv"},
        flush_logs = False #The log entry is stored locally
    )
```

---

#### logthis()

The `logthis()` function automatically wraps an API call, logging essential details such as the function name, input parameters, execution time, and return values. This method simplifies logging for API interactions while capturing all necessary context.

If you want to explore the implementation of the `logthis()` function in more detail, check out the [source code on GitHub](https://github.com/GWCustom/bfabric-web-apps/blob/main/bfabric_web_apps/objects/Logger.py#L117).

```python
result = L.logthis(api_call, args, obj, flush_logs, kwargs)
```

##### Args:  
1. **api_call** (*function*): The API function to execute. Example API calls could be `read` or `save`, depending on whether data needs to be retrieved or stored.
2. **endpoint** (*str*): The endpoint to read from, e.g. "sample".
3. **obj** (*dict*) A dictionary containing the query, for every field multiple possible values can be provided, the final query requires the condition for each field to be met
4. **flush_logs** (*bool*): Controls whether logs are immediately sent to the backend. Defaults to `True`.   
   - If `True`: The log entry is appended to the local log storage and immediately flushed to the backend using the `flush_logs()` method. This ensures that the log is recorded in real time.  
   - If `False`: The log entry is stored locally and will remain in the local cache until the next time the `flush_logs()` method is explicitly called. This can be useful for batching multiple log entries to minimize backend calls.
5. **kwargs**: These are keyword arguments passed directly to the API call. For example, `max_results` can be used to specify a cap on the number of results to query. This example applies specifically to a `read` API call. If provided as an integer, the number of results will be limited to the specified value. If set to `None`, the code will load all available pages. The function will continue fetching data page by page until either the maximum number of results is reached or all pages have been retrieved.

---

##### Returns:  
- The result of the API call.

---

##### Return Type:  
- `any`

---

##### Example

```python
lane_samples = L.logthis(
    api_call = wapper.read,
    endpoint="rununitlane",
    obj={"id": [str(elt["id"]) for elt in lane_data.get("rununitlane", [])]},
    flush_logs = False #The log entry is stored locally
    max_results=None, #Keyword arguments to pass to the API call (kwargs)
)
```

---


### flush_logs()

The `flush_logs()` function is used to send all accumulated log entries to the backend at once and clear the local cache. This function is particularly useful when multiple logging operations have been performed with `flush_logs=False`, allowing logs to be batched and sent in a single request instead of logging each action individually. If no logs are stored, calling this function has no effect.

If you want to explore the implementation of the `flush_logs()` function in more detail, check out the [source code on GitHub](https://github.com/GWCustom/bfabric-web-apps/blob/main/bfabric_web_apps/objects/Logger.py#L103).

```python
L.flush_logs()
```

##### Args:  
- None

---

##### Returns:  
- None

---

##### Behavior:  
- If there are **pending logs** saved locally, they are flushed with a **single API call** to the backend, reducing the number of individual requests.
- After a successful flush, the local log storage is cleared.
- If no logs are pending, the function does nothing and exits immediately.

---

##### Example

```python
# Initialize the logger instance
L = get_logger(token_data)

# Log multiple API calls without flushing immediately
entity_data_list = L.logthis(
    api_call=wrapper.read,
    endpoint=endpoint,
    obj={"id": entity_id},
    max_results=None,
    flush_logs=False # Store log locally
)

lane_samples = L.logthis(
    api_call=wrapper.read,
    endpoint="rununitlane",
    obj={"id": [str(elt["id"]) for elt in lane_data.get("rununitlane", [])]},
    max_results=None,
    flush_logs=False # Store log locally
)

# Flush all stored logs at once
L.flush_logs()
```

---

# 5. B-Fabric Wrapper

This chapter provides detailed documentation on obtaining and using the **B-Fabric Wrapper**, a crucial component in the B-Fabric application environment, designed for seamless interactions with the B-Fabric API.

---

## Overview

The B-Fabric Wrapper is an authenticated object providing a convenient and secure way to perform API calls to B-Fabric, such as reading data or saving resources. It encapsulates authentication credentials and configurations needed to interact with the B-Fabric system.

The wrapper must be initialized by validating an authentication token before it can be retrieved and used for subsequent operations.

---

## Wrapper Initialization

The wrapper initialization is handled internally by the system upon successful token validation. Users do not need to manually initialize the wrapper but must ensure that the authentication token has been validated first.

---

## Retrieving the B-Fabric Wrapper

### `get_wrapper()`

The `get_wrapper()` method returns the initialized B-Fabric wrapper. This method ensures that the wrapper is correctly configured and ready to use after token validation.

If the wrapper has not been initialized (due to the absence of prior token validation), the method will raise an error.

#### Method Definition

```python
def get_wrapper(self):
    if self._wrapper is None:
        raise RuntimeError("Bfabric wrapper is not initialized. Token validation must run first.")
    return self._wrapper
```

---

### Exception Handling

* **RuntimeError:** If the wrapper is requested before token validation, indicating that the wrapper has not yet been initialized.

---

### Usage Example

Here's how you can easily obtain and utilize the B-Fabric wrapper:

#### Importing the B-Fabric Interface

```python
from bfabric_web_apps.objects.BfabricInterface import bfabric_interface
```

#### Getting the Wrapper

```python
# Retrieve the B-Fabric wrapper after successful token validation
wrapper = bfabric_interface.get_wrapper()
```

### Important Considerations

* The wrapper object is **essential** for interacting with the B-Fabric API, and operations such as data queries (`read`) and submissions (`save`) rely on this wrapper.
* Always ensure the wrapper is initialized by validating the authentication token beforehand. The token validation process happens automatically when using the provided B-Fabric workflow (`process_url_and_token`).

---


#### Example:

```python
from bfabric_web_apps.utils.callbacks import process_url_and_token
from bfabric_web_apps.objects.BfabricInterface import bfabric_interface

# Validate token first (internally initializes wrapper)
token, token_data, _, _, _, _, _ = process_url_and_token(url_params)

# Get the wrapper object
wrapper = bfabric_interface.get_wrapper()

# Example API call using the wrapper
results = wrapper.read("sample", {"id": "1234"})
```

---

### Practical Usage Tips

* Always handle potential exceptions by using try-except blocks when retrieving the wrapper, especially in scenarios where token validation status may be uncertain.

---








## 6. B-Fabric Power User Access

### Power User Overview
- **Username**: **gfeeder**
- **Purpose**: The power user account is used to perform elevated operations in the B-Fabric system, such as reading or modifying restricted data. Ensure that this access is used responsibly and within the bounds of the system's usage policies.

---

### get_power_user_wrapper()

Initializes and returns an **authenticated wrapper** for interacting with the **B-Fabric API**. This wrapper is specifically configured for **Power User** access, allowing privileged operations within the system. The default **Power User** login is **`gfeeder`**.

This function uses the environment information provided in `token_data` to determine the appropriate configuration for initializing the `Bfabric` instance. It reads the configuration from a predefined path (`CONFIG_FILE_PATH`) and applies the environment settings.

If you want to explore the implementation of the `get_power_user_wrapper()` function in more detail, check out the [source code on GitHub](https://github.com/GWCustom/bfabric-web-apps/blob/main/bfabric_web_apps/utils/get_power_user_wrapper.py).

```python
power_user_wrapper = get_power_user_wrapper(token_data)

```
---
#### Args: 
1. **token_data** (*dict*): A dictionary containing token-related information.  
   - The `"environment"` key specifies the environment configuration (e.g., production or testing).  
   - If the `"environment"` key is not provided, it defaults to `"None"`.

---

#### Returns:
- A `Bfabric` instance, authenticated and configured for the specified environment.

---
##### Return Type:  
- `bfabric_web_apps.bfabric_web_apps.Bfabric`

---

#### Example Usage

```python
# Initialize the power user wrapper
power_user_wrapper = get_power_user_wrapper(token_data)
```

---
## 7. Bug Reports

### Overview

The bug-report functionality within the `bfabric-web-apps` Python library utilizes the Unix command-line utility `mail` to send emails from a running application. 

When the `send_bug_report` function is invoked, **token details, session details, and entity details** are sent as input parameters from the browser cache. These details are aggregated into a `mail_string`, which is then sent to the **bug-report email address** via a system call to the Unix command-line utility `mail`.

**“Mail”** must therefore be active and running on the deployed system, and accessible to the application process for the bug-report functionality to work. 

The default choice of bug-report mail address is **"gwtools@fgcz.system"** which is an OTRS queue, which is only accessible from within FGCZ server hardware. This is adaptable for your own use-case.

---

#### Modifying the Bug-Report Email Address

By default, bug reports are sent to `gwtools@fgcz.system`, but you can customize this to fit your organization's needs. The bug-report email address can be modified as follows:

```python
bfabric_web_apps.BUG_REPORT_EMAIL_ADDRESS = "my_email@my_domain.com" 
```

This change ensures that bug reports are redirected to your preferred email address instead of the default FGCZ system queue.

For further details on modifying global variables, refer to [Chapter 7: Dynamic Variable Configuration](#dynamic-variable-configuration).

---

### submit_bug_report()

Submits bug reports by collecting the user-provided bug description, along with token and entity data, and then emails these details to the **bug-report email address** configured in `bfabric_web_apps.BUG_REPORT_EMAIL_ADDRESS`. By default, this address is `gwtools@fgcz.system`, but it can be customized as needed.

If you want to explore the implementation of the `submit_bug_report()` function in more detail, check out the [source code on GitHub](https://github.com/GWCustom/bfabric-web-apps/blob/main/bfabric_web_apps/utils/callbacks.py#L92).

```python
submit_bug_report(n_clicks, bug_description, token, entity_data)
```

#### Args:
1. **n\_clicks** (int): Number of times the submit button has been clicked.
2. **bug\_description** (str): Description of the bug provided by the user.
3. **token** (str): Authentication token.
4. **entity\_data** (dict): Data related to the current entity.

#### Returns:
- **tuple**: Two boolean values indicating whether the submission succeeded or failed.  
  - **is\_open\_success** (bool): True if bug report submission was successful.  
  - **is\_open\_failure** (bool): True if bug report submission failed.

#### Example

As a reference, you can check out how this function is used in [`generic_bfabric.py`](https://github.com/GWCustom/bfabric-web-app-template/blob/main/generic_bfabric.py#L73).

```python
@app.callback(
    [
        Output("alert-fade-bug-success", "is_open"),  # Show success alert.
        Output("alert-fade-bug-fail", "is_open")      # Show failure alert.
    ],
    [Input("submit-bug-report", "n_clicks")],         # Detect button clicks.
    [
        State("bug-description", "value"),            # Bug description input.
        State("token", "data"),                       # Authentication token.
        State("entity", "data")                       # Entity metadata.
    ],
    prevent_initial_call=True
)
def generic_handle_bug_report(n_clicks, bug_description, token, entity_data):
    return submit_bug_report(n_clicks, bug_description, token, entity_data)
```

---
# 8. Remote Creation of Web Applications

## Overview

The `create_web_app()` function allows users to remotely create a new web application by providing necessary inputs such as **name, URL, description, and technology type**. This function eliminates the need to manually open B-Fabric, enabling application creation directly from the terminal.

---

## create_web_app()

The `create_web_app()` function prompts the user for **input parameters** required for creating a web application, validates these inputs, and then submits them to B-Fabric's API.

If you want to explore the implementation of the `create_web_app()` function in more detail, check out the [source code on GitHub](https://github.com/GWCustom/bfabric-web-apps/blob/14-auto-registration-of-apps-in-b-fabric/bfabric_web_apps/utils/create_app_in_bfabric.py).

```python
create_web_app()
```

### Input Parameters:
These are the variables used to create the web application. Some require user input, while others have default values.

| Parameter        | Input/Default  | Description |
|-----------------|---------------|-------------|
| **system**      | User Input     | The system where the web app will be created (`TEST` or `PROD`). |
| **technologyid** | User Input     | The ID corresponding to the chosen application type. Must be selected from available options. |
| **name**        | User Input     | The name of the web application. |
| **weburl**      | User Input     | The URL of the web application. |
| **description** | User Input     | A brief description of the web application. |
| **type**        | Default (`WebApp`) | Defines the application type. Always set to `WebApp`. |
| **supervisorid**| Default (`2446`)  | The ID of the supervisor managing the application. |
| **enabled**     | Default (`True`)  | Specifies whether the application is active. |
| **valid**       | Default (`True`)  | Indicates whether the application is valid. |
| **hidden**      | Default (`False`) | Determines whether the application is hidden. |

---

## Example Usage

```python
from bfabric_web_apps import create_web_app

# Run the function to create a new web application
create_web_app()
```

### Steps to Fill Out the Inputs:
1. **Select the System**:
   - Type `TEST` for the test system or `PROD` for the production system.
   - If an invalid input is entered, the function will prompt again.

2. **Choose the Application Type**:
   - Available technologies for **TEST**:
     - 1: Genomics / Transcriptomics
     - 2: Proteomics
     - 4: Metabolomics / Biophysics
     - 6: General
     - 10: New Tech
   - Available technologies for **PRODUCTION**:
     - 1: Genomics / Transcriptomics
     - 2: Proteomics
     - 4: Metabolomics / Biophysics
     - 6: General
     - 10: Bioinformatics
   - Select the number corresponding to your application type.

3. **Provide Additional Information**:
   - Enter the **Application Name**.
   - Provide the **Web URL** where the application is hosted.
   - Enter a **short description** of the web application.

Once all inputs are provided, the function submits the data to B-Fabric and confirms successful creation.

# 9. Main Job Execution (run\_main\_job)

---

## Overview

The `run_main_job` function provides a generalized approach to executing pipeline tasks. It orchestrates critical operations including file handling, command execution, resource management, attachment handling, and automatic charging in B-Fabric. This function extensively logs operations to ensure transparency, facilitate debugging, and maintain accountability.

---

### Function Signature

```python
run_main_job(
    files_as_byte_strings: dict, 
    bash_commands: list[str], 
    resource_paths: dict,
    attachment_paths: dict, 
    token: str,
    service_id: int = 0,
    charge: list[int] = [],
)
```

---

### Arguments Explained

* **files\_as\_byte\_strings** (`dict`):

  * Used when the `run_main_job` function is executed on an external server (e.g., via Redis queue). It maps destination file paths to their file contents represented as byte strings, enabling file transfer and subsequent use within the pipeline execution.

* **bash\_commands** (`list[str]`):

  * List of bash commands executed sequentially.

* **resource\_paths** (`dict`):

  * Maps local file paths or directories to B-Fabric container IDs.

* **attachment\_paths** (`dict`):

  * Maps file paths (logs, reports) to their filenames for attachment as links in B-Fabric.

* **token** (`str`):

  * Authentication token from B-Fabric.

* **service\_id** (`int`, optional):

  * B-Fabric service ID to charge against. Defaults to `0` (no charging).

* **charge** (`list[int]`, optional):

  * List of B-Fabric container IDs to charge for the service. Defaults to empty (no charging).

---

### Function Steps & Behavior

#### Step 1: Saving Files

* Saves provided byte string files to specified server locations.
* Logs each file operation (success or failure).

#### Step 2: Bash Command Execution

* Executes provided bash commands sequentially.
* Logs detailed output and errors from each command.

#### Step 3: Creating Workunits

* Creates workunits in B-Fabric based on container IDs.
* Logs created workunit IDs or errors.

#### Step 4: Resource Registration

* Registers server files as resources associated with created workunits.
* Logs each successful resource registration or failure.

#### Step 5: Attachment as Links

* Copies files to remote storage (FGCZ storage).
* Creates B-Fabric links to attached files.
* Logs success or failures of each file attachment.

#### Step 6: Automatic Charging

* Automatically charges specified containers for provided services.
* Logs charges and handles cases without provided service IDs.

---

### Return Value

* **None**
* All activities are logged for debugging and traceability.

---

### Example Usage (Callback Integration)

To effectively use the `run_main_job` function, you must prepare appropriate arguments as follows:

1. **Prepare files as byte strings**: When executing remotely (via Redis queue), read the necessary files and encode them as byte strings:

```python
files_as_byte_strings = {}
files_to_send = ["./pipeline_samplesheet.csv", "./NFC_DMX.config"]

for file_path in files_to_send:
    with open(file_path, "rb") as file:
        files_as_byte_strings[file_path] = file.read()
```

2. **Construct bash commands**:

```python
bash_commands = [
    "rm -rf /path/to/workdir",
    "nextflow run nf-core/pipeline -profile docker --input ./pipeline_samplesheet.csv --outdir /output/dir"
]
```

3. **Define resource paths**:

```python
resource_paths = {"/output/results/": container_id}
```

4. **Specify attachment paths**:

```python
attachment_paths = {"/output/results/report.html": "report.html"}
```

5. **Queue the job execution**:

```python
from rq import Queue
from redis import Redis

redis_queue = Queue(queue, connection=Redis())
redis_queue.enqueue(run_main_job, kwargs={
    "files_as_byte_strings": files_as_byte_strings,
    "bash_commands": bash_commands,
    "resource_paths": resource_paths,
    "attachment_paths": attachment_paths,
    "token": url_params,
    "charge": [container_id],
    "service_id": service_id
})
```

---

### Best Practices

* Ensure the provided file paths and commands are thoroughly tested before integration.
* Utilize extensive logging to monitor and debug job execution.
* Handle all exceptions gracefully and log meaningful messages.
* Regularly monitor B-Fabric logs for operations initiated via this function.

---
