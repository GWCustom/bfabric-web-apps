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
    <img src="logo.png" alt="Logo" width="80" height="50.6">
  </a>

<h3 align="center">B-Fabric Web Apps</h3>

  <p align="center">
    A web-based platform for developing and integrating satellite applications around the B-Fabric Laboratory Information Management System (LIMS).
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
  - [Quickstart](#Quickstart)
    - [Basic Usage Example](#Basic-Usage-Example)
  - [Built With](#built-with)
- [What Is B-Fabric?](#what-is-bfabric)
- [What Is B-FabricPy?](#what-is-bfabricpy)
- [What Is Dash?](#what-is-dash)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)




## About The Project

The `bfabric-web-app` is a Python library published on PyPI, designed to simplify the creation of web applications that interact with B-Fabric. It abstracts much of the complexity involved in connecting with the B-Fabric API, enabling developers to focus on building custom functionality. B-Fabric Web Apps are modular satellite applications designed to extend the functionality of the B-Fabric Laboratory Information Management System (LIMS). These web apps facilitate seamless integration, data visualization, and advanced functionalities for managing scientific experiments and data.

Key Features:
- **Dynamic Integration**: Build applications that integrate directly with B-Fabric via its API.
- **Custom Dashboards**: Create custom dashboards for visualizing and managing data.
- **Streamlined Workflows**: Simplify and enhance workflows for researchers and lab managers.


### Quickstart

You can install the `bfabric-web-app` module via pip:

```sh
pip install bfabric-web-apps
```

To see how the `bfabric-web-app` library is used, refer to the [`bfabric-web-app-template`](https://github.com/GWCustom/bfabric-web-app-template) repository. This template app demonstrates:
- Setting up a project with `bfabric-web-app`.
- Using Dash to create visual dashboards.
- Interacting with the B-Fabric LIMS using the Python library.

#### Basic Usage Example

After installation, you can create a simple Dash-based web application using `bfabric-web-app` like this:

```python
from bfabric_web_app import BfabricApp
import dash
from dash import html

# Initialize the B-Fabric app
app = BfabricApp(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Welcome to B-Fabric Web App"),
    html.P("This is a simple example demonstrating the usage of bfabric-web-app.")
])

# Run the application
if __name__ == "__main__":
    app.run_server(debug=True)
```

This example initializes a basic web application that integrates with B-Fabric, displaying a simple dashboard.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python.js]][Python-url]
* [![Dash][Dash.js]][Dash-url]
* [![Plotly][Plotly.js]][Plotly-url]
* [![Flask][Flask.js]][Flask-url]

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

Contributions are welcome and encouraged! Here's how you can help:

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
5. Submit a pull request.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## License

Distributed under the MIT License. See `LICENSE` for more details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contact

GWC GmbH - [GitHub](https://github.com/GWCustom) - [LinkedIn](https://www.linkedin.com/company/gwc-gmbh/posts/?feedView=all)

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
