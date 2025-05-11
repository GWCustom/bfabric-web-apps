# Global Variables

B-Fabric Web Apps provide a set of **global variables** that can be customized by users to adapt the application's behavior to specific needs. These variables control aspects such as configuration file paths, email addresses for support, server settings, and the development environment state.

This chapter explains how to modify these variables and where they are stored.

---

## List of Global Variables

The following global variables can be modified in B-Fabric Web Apps:

| Variable                    | Default Value                                                     | Description                                                        |
| --------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------ |
| REDIS\_HOST                 | "localhost"                                                       | Hostname for the Redis server used by the application.             |
| REDIS\_PORT                 | 6379                                                              | Port number for the Redis server.                                  |
| CONFIG\_FILE\_PATH          | "\~/.bfabricpy.yml"                                               | Path to the configuration file used by the application.            |
| HOST                        | "127.0.0.1"                                                       | The IP address where the Dash app is hosted.                       |
| PORT                        | 8050                                                              | The port number used by the Dash server.                           |
| DEV                         | False                                                             | Indicates whether the application is running in development mode.  |
| DEBUG                       | False                                                             | Enables verbose logging for debugging purposes.                    |
| DEVELOPER\_EMAIL\_ADDRESS   | "[griffin@gwcustom.com](mailto:griffin@gwcustom.com)"             | Email address for development-related inquiries.                   |
| BUG\_REPORT\_EMAIL\_ADDRESS | "[gwtools@fgcz.system](mailto:gwtools@fgcz.system)"               | Email address for submitting bug reports.                          |
| GSTORE\_REMOTE\_PATH        | "/path/to/remote/gstore"                                          | Path to the remote gstore location (FGCZ-specific).                |
| SCRATCH\_PATH               | "/scratch/folder"                                                 | Path to the scratch directory (FGCZ-specific).                     |
| TRX\_LOGIN                  | "[trxcopy@fgcz-server.uzh.ch](mailto:trxcopy@fgcz-server.uzh.ch)" | SSH login used for transferring files (FGCZ-specific).             |
| TRX\_SSH\_KEY               | "/home/user/.ssh/your\_ssh\_key"                                  | Path to the SSH key used for secure file transfer (FGCZ-specific). |
| URL                         | "https\:/fgcz/dummy/url"                                          | Base URL for internal services or pipelines.                       |
| SERVICE\_ID                 | 0                                                                 | Service ID used for billing or internal tracking purposes. |
| DATASET\_TEMPLATE\_ID       | 0                                                                 | Dataset template ID used for dataset creation.             |

---

## How to Modify Global Variables

You can modify these global variables within your script before initializing the application.

#### Customize Redis Settings

```python
bfabric_web_apps.REDIS_HOST = "redis-server"
bfabric_web_apps.REDIS_PORT = 6380
```

#### Change the Configuration File Path

```python
bfabric_web_apps.CONFIG_FILE_PATH = "~/custom_config.yml"
```

#### Change Host and Port Settings

```python
bfabric_web_apps.HOST = "127.0.0.1"
bfabric_web_apps.PORT = 8080
```

#### Enable Development or Debug Mode

```python
bfabric_web_apps.DEV = True
bfabric_web_apps.DEBUG = True
```

#### Update Developer Email Address

```python
bfabric_web_apps.DEVELOPER_EMAIL_ADDRESS = "support@mydomain.com"
```

#### Update Bug Report Email Address

```python
bfabric_web_apps.BUG_REPORT_EMAIL_ADDRESS = "bugs@mydomain.com"
```

#### Update FGCZ-specific Settings

```python
bfabric_web_apps.GSTORE_REMOTE_PATH = "/new/gstore/path"
bfabric_web_apps.SCRATCH_PATH = "/new/scratch"
bfabric_web_apps.TRX_LOGIN = "trxcopy@new-server"
bfabric_web_apps.TRX_SSH_KEY = "/home/user/.ssh/other_key"
bfabric_web_apps.URL = "https://new.url/path"
```

#### Change the Service ID

```python
bfabric_web_apps.SERVICE_ID = 123
```

#### Change the Dataset Template ID

```python
bfabric_web_apps.DATASET_TEMPLATE_ID = 5
```