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

<h3 align="center">Bfabric Web Apps</h3>

  <p align="center">
    A web-based platform for developing and integrating satellite applications around the Bfabric Laboratory Information Management System (LIMS).
    <br />
    <a href="https://pypi.org/project/bfabric-web-apps/"><strong>Explore the documentation »</strong></a>
    <br />
    <br />
    <a href="https://github.com/GWCustom/bfabric-web-apps">View Demo</a>
    ·
    <a href="https://github.com/GWCustom/bfabric-web-apps/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/GWCustom/bfabric-web-apps/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#example-and-template-reference">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


## About The Project

Bfabric Web Apps are modular satellite applications designed to extend the functionality of the Bfabric Laboratory Information Management System (LIMS). These web apps facilitate seamless integration, data visualization, and advanced functionalities for managing scientific experiments and data.

Key Features:
- **Dynamic Integration**: Build applications that integrate directly with Bfabric via its API.
- **Data Validation**: Ensure high data integrity through advanced error-checking mechanisms.
- **Custom Dashboards**: Create custom dashboards for visualizing and managing data.
- **Streamlined Workflows**: Simplify and enhance workflows for researchers and lab managers.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* [![Python][Python.js]][Python-url]
* [![Dash][Dash.js]][Dash-url]
* [![Plotly][Plotly.js]][Plotly-url]
* [![Flask][Flask.js]][Flask-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## What Is Bfabric?

Bfabric is a Laboratory Information Management System (LIMS) used for managing scientific experiments and their associated data in laboratories. It provides a platform for tracking samples, analyzing results, and organizing workflows efficiently. 

For more details, visit the [Bfabric official website](https://www.fgcz.ch/the-center/infrastructure-and-tools/bfabric).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## What Is BfabricPy?

BfabricPy is a Python library that provides a programmatic interface to interact with the Bfabric API. It allows developers to integrate Bfabric functionalities into custom Python applications. This library simplifies tasks like querying samples, uploading results, and interacting with the LIMS programmatically.

BfabricPy is a dependency of this project and is fetched directly from its GitHub repository during installation.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## What Is Dash?

Dash is a Python framework for building interactive web applications. It combines the power of Plotly for data visualization and Flask for backend support, making it ideal for scientific and analytical dashboards.

For more details, visit the [Dash official documentation](https://dash.plotly.com/).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## What Is This Library?

The `bfabric-web-app` is a Python library published on PyPI, designed to simplify the creation of web applications that interact with Bfabric. It abstracts much of the complexity involved in connecting with the Bfabric API, enabling developers to focus on building custom functionality.

### Linking to the Template App

To see how the `bfabric-web-app` library is used, refer to the [`bfabric-web-app-template`](https://github.com/GWCustom/bfabric-web-app-template) repository. This template app demonstrates:
- Setting up a project with `bfabric-web-app`.
- Using Dash to create visual dashboards.
- Interacting with the Bfabric LIMS using the Python library.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

To get a local copy of the project up and running, follow these steps:

### Prerequisites

Before getting started, ensure you have the following installed on your system:

- **Python 3.9 or higher**: The project is compatible with Python 3.9+.
- **Pip package manager**: For managing Python dependencies.
- **Git**: Required to clone the repository and fetch the `bfabric` dependency.
- **Environment Configuration**: Ensure you have access to the Bfabric API and can configure your `.env` file with the necessary API key.

The project relies on several Python libraries (e.g., Dash, Plotly, Flask, and others), which will be installed automatically via the `requirements.txt` file.


### Example and Template Reference

The `bfabric-web-app` is a Python library published on PyPI, designed to simplify the development of web applications that interact with the Bfabric Laboratory Information Management System (LIMS). Instead of directly installing this repository, you can use the library in your Python projects.

To get started with the `bfabric-web-app`, refer to the [`bfabric-web-app-template`](https://github.com/GWCustom/bfabric-web-app-template) repository. This template provides a fully functional example of how to build a web app using the library.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage

Bfabric Web Apps provide a user-friendly interface for managing and validating scientific data. Here are some key use cases:

1. **Data Upload and Validation**:
   - Ensure data integrity before uploading to Bfabric.
   - Flag missing or incorrect data fields with detailed user warnings.

2. **Custom Dashboards**:
   - Generate dynamic dashboards for data visualization and analysis.

3. **Error Alerts**:
   - Notify users of potential data inconsistencies during data import or export.

_For detailed examples and usage guides, refer to the [Documentation](https://github.com/GWCustom/bfabric-web-apps/docs)._

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

Project Repository: [https://github.com/GWCustom/bfabric-web-apps](https://github.com/GWCustom/bfabric-web-apps)

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
