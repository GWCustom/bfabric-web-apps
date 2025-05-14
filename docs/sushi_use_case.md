# Sushi Use Case

This chapter presents a practical example of how B-Fabric datasets can be used to drive Sushi-based workflows through a Dash web interface, using the `bfabric_web_apps` library and the SushiRunner application.

---

## Overview

This chapter demonstrates how the `bfabric_web_apps` library can be used to build modular, Dash-based web interfaces for launching [Sushi](https://github.com/uzh/sushi) applications. The SushiRunner app connects B-Fabric datasets with the [SushiFabric](https://github.com/uzh/sushi_fabric) command-line interface and the [WorkflowManager](https://github.com/uzh/workflow_manager), enabling structured job submission without requiring users to manually prepare TSV inputs or scripts.

SushiRunner serves as a **proof-of-concept** application that allows authenticated B-Fabric users to submit predefined Sushi jobs using a form-based web interface.

For source code and a quickstart guide, visit:
[GWCustom/SushiRunner](https://github.com/GWCustom/SushiRunner)

---

### What is Sushi?

[Sushi](https://github.com/uzh/sushi) is a Ruby-based framework for developing and executing bioinformatics workflows. It enables reproducible and modular pipelines by abstracting input/output definitions and runtime parameters. Sushi apps can be executed locally or on computing clusters using [SushiFabric](https://github.com/uzh/sushi_fabric) and managed via [WorkflowManager](https://github.com/uzh/workflow_manager).

Sushi is used extensively within the [FGCZ](https://fgcz-bfabric.uzh.ch/bfabric/) infrastructure and integrates well with B-Fabric through standardized dataset and parameter input files.

---

## SushiRunner Use Case

SushiRunner demonstrates how a B-Fabric-aware Dash application can be built to configure, validate, and launch Sushi applications.

The app is implemented using the `bfabric_web_apps` library and follows a template-based structure with reusable layout components. Users interact with a dynamic web form that collects job-specific parameters and generates the required `dataset.tsv` and `parameters.tsv` files before triggering execution via `sushi_fabric`.

Although this use case specifically showcases SushiRunner, many of its patterns (authentication, dataset loading, parameter forms, and result registration) are reusable in other workflow UIs.

---

### Sushi Workflow

The typical workflow in SushiRunner consists of the following steps:

1. **Launch from B-Fabric**
   The user opens the app via a dataset-specific link from B-Fabric.

2. **Load Dataset Metadata**
   The app automatically retrieves and parses metadata via the B-Fabric API.

3. **Configure Parameters**
   Users select the Sushi app to run and define input parameters (e.g., RAM, CPU, paired-end, QC options).

4. **Generate Input Files**
   The app creates the required `dataset.tsv` and `parameters.tsv` files for Sushi.

5. **Submit Job via `sushi_fabric`**
   Sushi is invoked using the appropriate app class and configuration.

6. **Monitor Execution**
   Jobs are executed and tracked using WorkflowManager. Status updates and logs are available via the FGCZ monitoring tools.

7. **Register Workunits and Outputs**
   Completed job information is registered back into B-Fabric for traceability.

---

### App Structure

SushiRunner apps are organized as modular Dash apps, one per Sushi tool (e.g., FastQC, MultiQC, Trimgalore). The architecture includes:

* **Dataset Integration**
  Retrieves and parses metadata from B-Fabric, typically used to generate the `dataset.tsv`.

* **Dynamic Parameter Form**
  A form-based UI dynamically updates available fields based on the selected Sushi app. Generic options (RAM, cores, partition) and app-specific parameters (e.g., `paired`, `showNativeReports`) are supported.

* **Job Submission Logic**
  Once confirmed, the app generates input files and submits the job using `sushi_fabric`, without relying on Redis queues.

* **Charging and Logging**
  Optional integration with the B-Fabric charge system and automatic workunit creation via the library's configuration.

---

### Supported Applications

Each Sushi app is handled by a separate module within SushiRunner. Example:

* **FastQC App**

  * Input: FASTQ files
  * Parameters: cores, RAM, paired-end toggle, etc.
  * Submission: Uses `FastqcApp` class in `sushi_fabric`
  * Visual output registered as attachments in B-Fabric

The SushiRunner architecture supports extending to additional Sushi apps with minimal duplication.

---

### Expected Output

Once submitted, the following outputs are produced:

* **Sushi Output Directory**
  Results are stored in a structured folder on the compute cluster, according to Sushi conventions.

* **Workunit Registration**
  Each job is logged in B-Fabric with metadata linking the execution and inputs.

* **Report Attachments**
  Reports such as HTML QC summaries can be linked back to the dataset entity.

---

By abstracting the complexity of TSV generation and `sushi_fabric` CLI usage, SushiRunner simplifies the execution of Sushi workflows through a user-friendly, form-based Dash interface — directly integrated with the B-Fabric system.
