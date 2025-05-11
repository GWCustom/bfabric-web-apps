# RNA-seq Use Case

```{note}
**Use Case in Progress**  
This use case is still under construction. Please check back later to learn how to use `bfabric_web_apps` to build beautiful and functional applications quickly within the B-Fabric ecosystem.
```

```{comment}


This use case showcases how the RNA-seq application is architected using the `bfabric_web_apps` library to run the NF-Core RNA-seq pipeline through a scalable and modular Dash-based interface.

---

## Overview

The RNA-seq app is a **proof-of-concept application** for transcriptomic analysis within the B-Fabric ecosystem. It demonstrates how to combine B-Fabric metadata, a user-friendly Dash interface, and NF-Core RNA-seq pipelines in a single web application.

The app is built using the `bfabric_web_apps` library and follows the `redis_index.py` template, enabling asynchronous job execution via a Redis queue system.

---

## App Structure

The RNA-seq app is organized into three main components:

1. **B-Fabric Integration**
   Internal logic handles all interactions with the B-Fabric API. It fetches project and dataset metadata, extracts relevant information, and generates sample sheet files used as pipeline input.

2. **User Interface**
   The Dash-based UI collects key input parameters such as CPU, RAM, FASTA, GTF files, and an email address. It also includes a **Charge Switch** to associate run costs with a B-Fabric container. Sample metadata is visualized in a table where users can review and edit records before submission.

3. **Main Job Execution**
   When the user confirms submission, the app:

   * Converts files to byte streams.
   * Builds the appropriate bash command to run the Nextflow-based NF-Core RNA-seq pipeline.
   * Enqueues the job to Redis for remote execution.
   * Registers output files and reports back into B-Fabric via the API.

This modular design supports rapid development and easy adaptation to other Nextflow pipelines.

---

## Server Architecture

The RNA-seq app follows a **three-tier architecture** that decouples the web interface, job scheduling, and job execution:

* A **Web App Server** hosts the Dash UI, processes input from users, fetches B-Fabric metadata, and enqueues jobs via Redis.
* A **Compute Server** listens to Redis, runs the actual Nextflow jobs using `run_main_job()`, and stores output locally.
* The **B-Fabric System** provides metadata access and receives resource links and attachments once processing is complete.

### RNA-seq Architecture Diagram

![RNA-seq Architecture Diagram](_images/use_case_architecture.png)

This architecture allows for **asynchronous**, **scalable**, and **user-friendly** execution of complex workflows integrated with B-Fabric.

---


## Step-by-Step Workflow

1. **Launch the App**
   The user opens the RNA-seq web app via a B-Fabric launch link containing a valid session token.

2. **Authentication and Token Validation**
   The app extracts the token, validates it using B-Fabric’s REST API, and fetches:

   * Token metadata
   * Application metadata
   * Dataset/entity metadata

3. **Configure Run Parameters**
   The user enters details like:

   * Job name and comment
   * Email address
   * Number of CPUs and RAM allocation
   * FASTA and GTF reference files
   * Queue selection (`light` or `heavy`)
   * Toggle charge switch (on/off)

4. **Review Sample Metadata**
   A DataTable renders the B-Fabric dataset. Users can inspect and review the detected sample names and file associations.

5. **Submit the Pipeline Job**
   After clicking the submit button, a modal asks for final confirmation.

6. **Run the Job via Redis Queue**
   On confirmation:

   * A sample sheet CSV is generated and saved
   * Associated files are converted to byte strings
   * Bash commands for pipeline execution are prepared
   * Output/attachment/resource paths are configured
   * The job is enqueued using Redis (`q(queue).enqueue(...)`)

7. **Charge Project (Optional)**
   If the Charge Switch is enabled, the selected container is charged using the `create_charge()` function before pipeline execution.

---

## Expected Output

Once the job is completed, users can expect the following:

* **Output Directory on Compute Server**:
  A directory structure containing all pipeline outputs, logs, and reports. Named based on timestamp, e.g., `/STORAGE/OUTPUT_rnaseq_2025-05-06_10-32-00`

* **Registered B-Fabric Resources**:
  The output directory and key attachments (e.g., MultiQC reports, Qualimap reports, DESeq2 plots) are linked back to the originating dataset entity in B-Fabric.

* **Accessible QC Reports**:
  HTML reports and plots are attached to the dataset for downstream inspection or publication.

* **Workunit Creation**:
  The application logs workunits for job tracking and reproducibility within the B-Fabric platform.

---

By following this structured approach, users can run RNA-seq pipelines reproducibly, monitor job progress, and trace results directly within B-Fabric—all from an interactive and simplified Dash web interface.
```