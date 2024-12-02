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
   - 5.1 [Predicting Models](#51-predicting-models)  
   - 5.2 [Predicting Values](#52-predicting-values)  
6. [Saving and Loading Models](#6-saving-and-loading-models)  
   - 6.1 [Saving Models](#61-saving-models)  
   - 6.2 [Loading Models](#62-loading-models)  
7. [Glossary](#7-glossary) 


# 1. Introduction

Welcome to the SpaceDuck linear regression application! This tool is
designed to make data analysis accessible and intuitive for users of
all experience levels. By leveraging linear regression, the
application enables users to explore relationships between variables,
build predictive models, and gain actionable insights from their data.

This application simplifies the process of creating, visualizing,
saving, and loading simple and multiple linear regression models.
Users can work with data stored in various formats such as CSV, Excel,
and SQLite, and perform tasks like data visualization and predictive
analysis. The tool is ideal for novice users and professionals seeking
an accessible solution for data-driven tasks.

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

Table 2.1: Shows the minimum system requirements.

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


Figure 2.1: Shows the main interface.

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


Figure 3.2: Shows the data to create models.

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


Figure 4.1: Shows the Modelo section interface.

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

## 5.1 Predicting Models

The model allows you to manipulate the graph view with the values of
the regression model. This function helps you apply your model’s
future values.

**To predict using the model**

1.  Select and hold (or right-click) on the generated model to open
    menu.

2.  Go to **Plot Options** \> **Grid**.

3.  Select both **Show X Grid** and **Show Y Grid**

    Grid lines will appear alongside the model.

<a href="https://imgbb.com/"><img src="https://i.ibb.co/vLK5zwq/image5.png" alt="image5" border="0"></a>


Figure 5.1: Shows the settings to enable graph grids.

## 5.2 Predicting Values

The prediction tool allows you to input values and generate values
based on your regression model. This step helps you apply your model’s
future values.

**To predict using the data**

1.  Click on the bar **Introducir número para realizar la predicción**

2.  Add the numerical value into the bar

3.  Click **Predict**

    Application will generate a prediction below the **Predict** bar

<a href="https://ibb.co/N2k6KjP"><img src="https://i.ibb.co/TMnBt8S/image6.png" alt="image6" border="0"></a>

Figure 5.2: Shows the interface for data predictions.

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

# 7. Glossary

Definition of terms used throughout the applications.

| Terms Used: | Definition: |
|----|----|
| Dependent Variable | The outcome or target variable in a regression model that the analysis aims to predict or explain, based on the independent variables. |
| Independent Variable | A variable used as input in a regression model to explain or predict the dependent variable. |
| Regression Model | A statistical method used to establish relationships between a dependent variable and one or more independent variables. |
| Dataset | A structured collection of data used for analysis or training models, typically consisting of rows |

Table 7.1: Shows the glossary of terms.
