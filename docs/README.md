# SpaceDucks

# Table of Contents  

1. [Introduction](#1-introduction)  
2. [Getting Started](#2-getting-started)  
   - 2.1 [System Requirements](#21-system-requirements)  
   - 2.2 [User Interface](#22-user-interface)  
3. [Creating Linear Regression Models](#3-creating-linear-regression-models)  
   - 3.1 [Loading and Using Data](#31-loading-and-using-data)  
   - 3.2 [Creating a Model](#32-creating-a-model)  
4. [Linear Regression Models Visualization](#4-linear-regression-models-visualization)  
   - 4.1 [Visualizing Models](#41-visualizing-models)  
   - 4.2 [Creating a Description](#42-creating-a-description)  
5. [Predicting Models and Values](#5-predicting-models-and-values)  
   - 5.1 [Predicting Values](#52-predicting-values)  
6. [Saving and Loading Models](#6-saving-and-loading-models)  
   - 6.1 [Saving Models](#61-saving-models)  
   - 6.2 [Loading Models](#62-loading-models)
7. [Download and Execution Guide](#7-download-and-execution-guide)
   - [7.1 Downloading the Latest Release](#71-downloading-the-latest-release)
   - [7.2 Executing the Application](#72-executing-the-application)
8. [Glossary](#8-glossary) 


# 1. Introduction

Welcome to the SpaceDucks linear regression application! This tool makes data analysis accessible and intuitive all experience levels. By leveraging linear regression, the application enables users to explore relationships between variables, build predictive models, and gain insights from their data.

This application simplifies creating, visualizing, saving, and loading simple and multiple linear regression models. Users can work with data stored in various formats such as CSV, Excel, and SQLite, and perform tasks like data visualization and predictive analysis. The tool is ideal for novice users and professionals seeking an accessible solution for data-driven tasks.

 **Key features of the application include:**

- A user-friendly interface.

- The ability to create and visualize simple and multiple linear
  regression models.

- Support for saving and loading models for reuse.

- An integrated prediction tool.



# 2. Getting Started

This section will guide you through the initial setup required to use
the linear regression application. While the tool is simple, you will
need a python environment and specific system requirements, as shown
in Table 2.1 to run the application locally. This ensures
compatibility and provides the necessary framework for the application
to function seamlessly. By following the system requirements, you’ll
be ready to load data, build models, and begin analysis.

## 2.1 System Requirements 

Ensure your system meets the necessary minimum requirements to run the
application. This includes a Python environment and specific libraries
for seamless functionality.

| **Requirements** | **Details** |
|----|----|
| **Device Compatibility** | Windows OS |
| **Processor** | Intel i5 or Equivalent |
| **RAM** | 8GB or Higher |
| **Disc Space** | 2GB or Higher |
| **Data Software** | CSV, Excel, or SQLite files (e.g., Microsoft Excel) |

Table 2.1: The minimum system requirements to use the application.

## 2.2 User Interface

The application’s interface is designed with simplicity in mind,
making it accessible even for novice users. It features a top bar,
which acts as the control panel for core functions such as uploading
data, creating models, and managing saved files as shown in Figure
2.1. This intuitive layout ensures that users can focus on their
analysis without being overwhelmed by technical details.

| **UI Terms**         | **Definitions** |
|----------------------|-----------------|
| **Añadir archivos**  | Add File        |
| **Añadir modelo**    | Add Model       |
| **Eliminar archive** | Delete File     |
| **Siguiente**        | Next/Confirm    |
| **Datos**            | Data            |
| **Procesado**        | Processing      |
| **Modelo**           | Model           |
| **Predecir**         | Predict         |

Table 2.2: Shows the UI terms translated to English.

The main menu consists of basic functions that allow you to interact
with the application to create, visualize and model linear regression
when given data. Opening the application, you are greeted with options
to continue.

 <a href="https://ibb.co/bm9xCD8"><img src="https://i.ibb.co/H480b3k/image1.png" alt="image1" border="0"></a>


Figure 2.1: The main interface of the application.

# 3. Creating Linear Regression Models

Creating linear regression models is a core feature of this
application, enabling users to analyze relationships between variables
and make predictions. With an intuitive interface, users can select
relevant variables after loading their data and seamlessly generate
both simple and multiple linear regression models.

## 3.1 Loading and Using Data

Before creating a regression model, you need to upload and prepare
your dataset. This step ensures that the data is properly formatted
and ready for use.

<a href="https://imgbb.com/"><img src="https://i.ibb.co/ZfF5q3n/image2.png" alt="image2" border="0"></a>


Figure 3.1: Shows the file location.
 **To add a data sheet to the interface**

1.  Click **Añadir archivos**.

    File directory opens.

2.  Navigate to file location.

3.  Select the file (CSV, Excel, or SQLite formats are supported).

    The file destination address will appear under the **Añadir
    archivos** bar and will be displayed there as shown in Figure 3.1.

## 3.2 Creating a Model 

 After loading your data, define the dependent and independent
variables to generate the regression model. This process establishes
the relationship between variables and forms the basis for
predictions.
>
**To create a model**

1.  Load the dataset following the steps in **3.1**.

2.  Choose the dependent variable (Y-axis) under **Columna de entrada**.

    After you select, the variable will be displayed.

3.  Choose the independent variable (X-axis) under **Columna de
    objetivo**.

    After you select, the variable will be displayed.

4.  Click **Procesar** to process the data.

    A pop-up notification will appear, indicating the data has been
    processed.

5.  Click **Siguiente** to generate the regression model.

    If steps were followed correctly, you will be directed Modelo
    section of the application with a model created.

6.  Select **OK.**

<a href="https://ibb.co/5nCpwXQ"><img src="https://i.ibb.co/b2YwDj4/image3.png" alt="image3" border="0"></a>


Figure 3.2: The dataset and variables to create models.

# 4. Linear Regression Models Visualization

Visualization is a powerful way to analyze the regression model you’ve
created. By generating graphs, you can identify patterns, trends, and
relationships between variables. This section explains how to interact
with the visualization features and gain deeper understanding from
data created.

## 4.1 Visualizing Models

The visualization feature displays a regression graph that helps you
analyze the relationships in your data. You can interact with the
graph to explore trends and patterns in greater detail.

**To visualizing models**

- Click and drag the graph to move and adjust the view.

- Use the scroll wheel to zoom in or out.

<a href="https://ibb.co/FVXXmJC"><img src="https://i.ibb.co/Srcc50G/image4.png" alt="image4" border="0"></a>


Figure 4.1: The Model section interface.

## 4.2 Creating a Description

By adding a detailed description, you can better understand the
functionality and application of the model, ensuring its effective use
for analysis and predictions.

**To create a description**

1.  Click the text box labeled **Escribe aquí la descripción del modelo
    (opcional)**.

    You will be able to type within the text box.

2.  Type your description for the model.

3.  Click **Guardar Modelo** to save.

    The description you created for the model will be attached to the
    model when saved.

# 5. Predicting Models and Values

The prediction feature enables you to apply your regression model to
new data, offering insights that support data decision making. Once
the model is created, you can input numerical values to generate
predictions, making the application a practical tool for real-world
scenarios. Whether you’re forecasting sales, analyzing trends, or
predicting outcomes, the intuitive prediction feature ensures you can
confidently derive actionable results.

## 5.1 Predicting Values

The prediction tool allows you to input values and generate values
based on your regression model. This step helps you apply your model’s
future values.

**To predict using the data**

1.  Click on the bar **Introducir número para realizar la predicción**

2.  Add the numerical value into the bar

3.  Click **Predict**

    Application will generate a prediction below the **Predict** bar

<a href="https://ibb.co/N2k6KjP"><img src="https://i.ibb.co/TMnBt8S/image6.png" alt="image6" border="0"></a>

Figure 5.1: The interface for data predictions.

# 6. Saving and Loading Models

The ability to save and load regression models is a key feature of the
application, ensuring that your work is preserved and reusable. Saving
a model allows you to continue your progress later or share it with
others; while loading a model ensures you can revisit and refine your
work without starting from scratch.

## 6.1 Savings Models

Save your regression model to preserve your work and enable reuse.
This feature ensures that your progress remains accessible for future
tasks.

**To save a model**

1.  Go to **Modelo** section of the application.

2.  Click **Guardar** **Modelo**

    File Directory opens.

3.  Open the file destination to save the model to.

4.  Click **Save**

    Model is saved to the destination set.

## 6.2 Loading Models

Load previously saved models to continue progress or make predictions.
This feature allows you to pick up where you left off without
rebuilding the model.
>
**To load a model**

1.  Click **Añadir modelo**.

    File Directory opens.

2.  Navigate to the saved model's location.

3.  Open the model file to load it into the application.

    File address will appear, and the model will load, refer to Figure
    3.1
    
# 7. Download and Execution Guide

This section explains how to download the latest version of the application and execute it on your local system. Follow the steps below to set up and start using SpaceDucks efficiently.

## 7.1 Downloading the Latest Release

To ensure you have the latest features and updates, always download the most recent version of the application.

**Steps to Download the Application**  
1. **Visit the Repository**  
   Go to the official SpaceDucks GitHub repository:  
   [https://github.com/SpaceDucksApp](https://github.com/SpaceDucksApp).  

2. **Locate the Latest Release**  
   On the repository homepage, click on the **Releases** section or scroll down to find the latest release.  

3. **Download the Source Code**    
   To download the **source code**, click on the **Source Code (zip)** link.  

4. **Save the File**  
   Save the file in a location where you can easily access it, such as your desktop or a dedicated folder.  

---

## 7.2 Executing the Application

After downloading, follow these steps to execute the application on your system.

### For Source Code

1. **Extract the Files**  
   If you downloaded the source code as a `.zip` file, extract it using tools like WinRAR or the built-in archive manager.  

2. **Install Dependencies**  
   Open a terminal or command prompt in the extracted folder and run the following command to install the required libraries:  
   ```bash
   pip install -r requirements.txt
   ```  

3. **Run the Application**  
   Execute the following command in the terminal to start the application:  
   ```bash
   python main.py
   ```  

4. **Start Using SpaceDucks**  
   Once the application is running, the interface will open, and you can begin creating and visualizing linear regression models.  

---

By following these steps, you can download and start using SpaceDucks efficiently.

# 8. Glossary

Definition of terms used throughout the applications.

| Terms Used: | Definition: |
|----|----|
| Dependent Variable | The outcome or target variable in a regression model that the analysis aims to predict or explain, based on the independent variables. |
| Independent Variable | A variable used as input in a regression model to explain or predict the dependent variable. |
| Regression Model | A statistical method used to establish relationships between a dependent variable and one or more independent variables. |
| Dataset | A structured collection of data used for analysis or training models, typically consisting of rows |

Table 8.1: The glossary of terms used in the application.
