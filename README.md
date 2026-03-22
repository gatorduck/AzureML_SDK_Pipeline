# Azure ML Pipeline with Python SDK v2

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Azure ML](https://img.shields.io/badge/Azure_ML-0078D4?style=flat&logo=microsoftazure&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=flat&logo=xgboost&logoColor=white)

> **TL;DR:** End-to-end ML pipeline on Azure Machine Learning using Python SDK v2 — XGBoost regression to predict blood pressure from the [UCI Diabetes dataset](https://archive.ics.uci.edu/dataset/34/diabetes).

## Overview

This repo illustrates creating a machine learning pipeline in the cloud with the Python SDK and used to develop a model to predict a patient's blood pressure given several features e.g. insulin, BMI, and many more.

This scenario solves a regression problem, in this case a continuous numeric value for blood pressure. The main purpose is primarily to guide in the creation of a pipeline using Azure Machine Learning and the Python SDK.

## Creating Machine Learning Pipelines with Python SDK v2 in Azure Machine Learning

There are many ways to create pipelines in Azure Machine Learning. This method uses a programmatic approach with the Python SDK (software development kit). This approach is ideal for developing pipelines and experimenting. For production, I recommend the CLI and the AML extension which helps create a production grade pipeline.

```mermaid
flowchart TB
    subgraph pipeline with sdkv2
    c1(data prep component) --> c2(training component)
    end
```

The files are setup to follow a sequence of steps that mimic an ML workflow starting with _p01_.


## 1 Development 

_p01_development.ipynb_

Assuming role of MLOps or ML engineer we have received a notebook that creates a ML model.

## 2 Productionalize

_p02_refactor.py_

1. We convert our notebook into a Python script (.py) as pipeline jobs require scripts. However note, that I will ultimately create two scripts, one for each component found under the components folder.

2. To make things easier to manage we create functions from our steps.

3. This method also introduces the _argparse_ package which is used to read data into the Python script or any other input such as a parameter. 


Note we have removed reference to our workspace and data file paths.

### 2a - Components with Python SDK v2

```mermaid
flowchart LR
    script:::bar --> notebook:::foobar --> component
    classDef bar stroke:#0f0
    classDef foobar stroke:#00f
```    

We create components using two approaches, with Python SDK we define the structure of our component and another example we define a component with a yaml file.

At this level, we can specify compute and environment at the component level.

We start with Python SDK v2 or the programmatic approach. 

_src/p03_data_prep.py_

We take our functions from the prep stage in our _p02_refactor.py_ script and make a few adjustments. This will become a separate independent component from our training portion of our pipeline and will be used to scale our features.

This will be the staging point for data ingestion into our pipeline, so we define two arguments. One for input which will be the data we ultimately want to use, and output which is the data that has been transformed and ready for training.

Within our _main()_ function we ultimately want to return our prepped data so we adjust our function to return data as a .csv and save it to our output argument named _--prepped_data_. 

Arguments

_--input_data_ - argument that will reference file path / file name as it is defined as uri_file

_--prepped_data_ - argument that will reference file path as it is defined as uri_folder

We will not provide the file path just yet to our data and where to store our transformed data. At this point we are creating skeletons for our pipeline.

_p03_create_data_prep_component.ipynb_

We will create the actual component using a notebook with Python SDK's _command_ function. We also take an additional step and register this component into our AML workspace.


### 2b - Components with YAML

```mermaid
flowchart LR
    yaml:::foo & script:::bar --> notebook:::foobar --> component
    classDef foo stroke:#f00
    classDef bar stroke:#0f0
    classDef foobar stroke:#00f
```    

This approach defines our component using a YAML file. 

_p04_create_register_component.ipynb_

This notebook loads the YAML file and creates a component for us (note, script is defined in the YAML file).

_p04_training.yaml_

YAML file holding component inputs, outputs, script reference, and environment. 

_src/p04_training.py_

Our actual script that is executed when running the training component. 


## 3 Create Our Pipeline

_p05_create_pipeline.ipynb_

This last notebook creates our pipeline. Because we didn't specify compute type in our components we specify the compute resource to run this pipeline. We can also define different computes per component, would make sense to use GPU or Spark Cluster for just the training component and CPU compute for data prep.

### Benefits 

- Pipeline stood up primarily with Python
- Great for experimentation and rapid development

### Drawbacks

- For production reproducibility, the CLI approach is preferred

## Project Structure

```
├── README.md
├── .gitignore
├── requirements.txt
├── config.json
├── data/
│   └── diabetes.csv
├── notebooks/
│   ├── p01_development.ipynb
│   ├── p03_create_data_prep_component.ipynb
│   ├── p04_create_register_component.ipynb
│   └── p05_create_pipeline.ipynb
└── src/
    ├── p02_refactor.py
    ├── p03_data_prep.py
    ├── p04_training.py
    └── p04_training.yaml
```

## Data Source

[UCI Diabetes Dataset](https://archive.ics.uci.edu/dataset/34/diabetes)
