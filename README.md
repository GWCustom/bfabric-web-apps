<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/GWCustom/bfabric-web-apps">
    <img src="https://drive.google.com/uc?export=view&id=1_RekqDx9tOY-4ziZLn7cG9sozMXIhrfE" alt="Logo" width="80" height="50.6">
  </a>

<h3 align="center">B-Fabric Web Apps</h3>

  <p align="center">
    A Python-based library designed for the development and integration of satellite applications with the B-Fabric Laboratory Information Management System (LIMS).
    <br />
    <a href="https://pypi.org/project/bfabric-web-apps/"><strong>Explore the documentation »</strong></a>
    <br />
    <br />
    <a href="https://github.com/GWCustom/bfabric-web-app-template">View Demo</a>
    ·
    <a href="https://github.com/GWCustom/bfabric-web-apps/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/GWCustom/bfabric-web-apps/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
## Table of Contents

- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Quickstart](#Quickstart)
  - [Basic Usage Example](#Basic-Usage-Example)
- [What Is B-Fabric?](#what-is-bfabric)
- [What Is B-FabricPy?](#what-is-bfabricpy)
- [What Is Dash?](#what-is-dash)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)




## About The Project

The `bfabric_web_apps` is a Python library designed to simplify the creation of web applications that interact with B-Fabric. By providing built-in functions, it significantly reduces repetitive code and streamlines development. B-Fabric Web Apps are modular satellite applications that extend the functionality of the B-Fabric Laboratory Information Management System (LIMS).

###Key Features:

Simplified B-Fabric Integration
- **Token Management** – Securely handle authentication tokens for API access.  
- **Entity Data Handling** – Retrieve, modify, and update B-Fabric entities dynamically.  
- **Authentication** – Built-in token-based authentication for seamless user access.  
- **Logger** – Integrated logging for API calls, events, and errors.  
- **Dash Resource Management** – Optimize data handling to minimize API calls.

Boilerplate Dash Components & Callbacks
- Predefined layouts, UI components, and callback structures to accelerate development.  
- Reusable patterns for efficient and consistent app design.

Custom Dashboards
- Easily build interactive dashboards using Dash and Plotly to visualize and manage data.

### Built With

* [![Python][Python.js]][Python-url]
* [![Dash][Dash.js]][Dash-url]
* [![Plotly][Plotly.js]][Plotly-url]
* [![Flask][Flask.js]][Flask-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Quickstart

You can install the `bfabric_web_apps` module via pip:

```sh
pip install bfabric_web_apps
```

To see how the `bfabric_web_apps` library is used, refer to the [`bfabric-web-app-template`](https://github.com/GWCustom/bfabric-web-app-template) repository. This template app demonstrates:
- Setting up a project with `bfabric_web_apps`.
- Using Dash to create visual dashboards.
- Interacting with the B-Fabric LIMS using the Python library.

#### Basic Usage Example

After installation, you can create a simple Dash-based web application using `bfabric_web_apps` like this:

```python
from bfabric_web_apps import create_app, load_config, get_static_layout
from dash import html

# Initialize the Dash application
app = create_app()

# Load configuration (if needed)
config = load_config("./PARAMS.py")

# Define application title
app_title = "My B-Fabric App"

# Define the main layout content
app_specific_layout = html.Div([
    html.H1("Welcome to My B-Fabric App"),
    html.P("This is a quickstart example using bfabric_web_apps.")
])

# Optionally define documentation content
documentation_content = [
    html.H2("Documentation"),
    html.P("Describe your app's features here.")
]

# Set up the application layout
app.layout = get_static_layout(
    app_title,  # Title shown in the browser tab
    app_specific_layout,  # Main application content
    documentation_content  # Documentation section
)

# Run the application
if __name__ == "__main__":
    app.run_server(debug=False, port=config["PORT"], host=config["HOST"])

```

This example sets up a minimal web application using bfabric_web_apps, providing a structured layout with configurable content.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## What Is B-Fabric?

B-Fabric is a Laboratory Information Management System (LIMS) used for managing scientific experiments and their associated data in laboratories. It provides a platform for tracking samples, analyzing results, and organizing workflows efficiently. 

For more details, visit the [B-Fabric official website](https://fgcz-bfabric.uzh.ch/bfabric/).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## What Is BfabricPy?

BfabricPy is a Python library that provides a programmatic interface to interact with the [Bfabric SOAP WebService](https://fgcz-bfabric.uzh.ch/wiki/tiki-index.php?page=Webservices). It allows developers to integrate B-Fabric functionalities into custom Python applications. This library simplifies tasks like querying samples, uploading results, and interacting with the LIMS programmatically.

BfabricPy is a dependency of this project and is fetched directly from its GitHub repository during installation.

For more details, visit the [bfabricPy official Git repository](https://github.com/fgcz/bfabricPy/tree/main) or the library's [official documentation](https://fgcz.github.io/bfabricPy).
<p align="right">(<a href="#readme-top">back to top</a>)</p>


## What Is Dash?

Dash is a Python framework for building interactive web applications. It combines the power of Plotly for data visualization and Flask for backend support, making it ideal for scientific and analytical dashboards.

For more details, visit the [Dash official documentation](https://dash.plotly.com/).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Roadmap

See the [open issues](https://github.com/GWCustom/bfabric-web-apps/issues) for a full list of planned features and known issues.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the repository.
2. Create a new branch:
   ```sh
   git checkout -b feature/YourFeature
   ```
3. Make your changes and commit them:
   ```sh
   git commit -m "Add feature: YourFeature"
   ```
4. Push to your branch:
   ```sh
   git push origin feature/YourFeature
   ```
5. Open a Pull Request.

### Top contributors:

<a href="https://github.com/GWCustom/bfabric-web-apps/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=GWCustom/bfabric-web-apps" alt="Top contributors" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/GWCustom/bfabric-web-apps/blob/main/LICENSE) for more details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contact

GWC GmbH - [GitHub](https://github.com/GWCustom) - [LinkedIn](https://www.linkedin.com/company/gwc-gmbh/posts/?feedView=all)  
Griffin White - [GitHub](https://github.com/grawfin) - [LinkedIn](https://www.linkedin.com/in/griffin-white-3aa20918a/)  
Marc Zuber - [GitHub](https://github.com/MarcZuberGWC) - [LinkedIn](https://www.linkedin.com/in/marc-zuber-1161b3305/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Acknowledgments

- [Plotly Dash](https://dash.plotly.com/)
- [Flask Framework](https://flask.palletsprojects.com/)
- [Python.org](https://www.python.org/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/GWCustom/bfabric-web-apps.svg?style=for-the-badge
[contributors-url]: https://github.com/GWCustom/bfabric-web-apps/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/GWCustom/bfabric-web-apps.svg?style=for-the-badge
[forks-url]: https://github.com/GWCustom/bfabric-web-apps/network/members
[stars-shield]: https://img.shields.io/github/stars/GWCustom/bfabric-web-apps.svg?style=for-the-badge
[stars-url]: https://github.com/GWCustom/bfabric-web-apps/stargazers
[issues-shield]: https://img.shields.io/github/issues/GWCustom/bfabric-web-apps.svg?style=for-the-badge
[issues-url]: https://github.com/GWCustom/bfabric-web-apps/issues
[license-shield]: https://img.shields.io/github/license/GWCustom/bfabric-web-apps.svg?style=for-the-badge
[license-url]: https://github.com/GWCustom/bfabric-web-apps/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/company/gwc-gmbh/posts/?feedView=all
[product-screenshot]: images/screenshot.png
[Python.js]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Dash.js]: https://img.shields.io/badge/dash-20232A?style=for-the-badge&logo=dash&logoColor=61DAFB
[Dash-url]: https://dash.plotly.com/
[Plotly.js]: https://img.shields.io/badge/plotly-563D7C?style=for-the-badge&logo=plotly&logoColor=white
[Plotly-url]: https://plotly.com/
[Flask.js]: https://img.shields.io/badge/flask-0769AD?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/stable/
