
# GitHub Documentation


## Project Overview

This project is focused on developing an intuitive application that simplifies the process of creating, visualizing, and managing linear regression models. It is designed to be user-friendly, enabling data analysts, business professionals, and IT team members to work seamlessly with data from various formats like CSV, Excel, and SQLite databases. The goal is to facilitate efficient data analysis and prediction-making, even for those without advanced technical skills. The documentation will guide project members, developers, and technical writers through the application's features, setup, and use.

## Agile Development Process

The Agile development process is a flexible and collaborative approach to software development, focusing on progress and continuous improvement. For this project, the work is divided into 8 sprints, each lasting one week. This allows the team to tackle tasks regularly, prioritize objectives, and adapt to any changes during development. At the end of each sprint, the team holds a retrospective meeting on Discord to review successes, address challenges, and plan improvements for the next sprint. This approach promotes effective teamwork, open communication, and ensures consistent progress toward the project’s goals.

## What is Artificial Intelligence?

Artificial intelligence refers to the simulation of human intelligence in machines. These systems are designed to learn, reason, and solve problems, allowing them to perform tasks that typically require human cognition, such as recognizing patterns, making predictions, or understanding language.

## What is Machine Learning

Machine learning is a subset of artificial intelligence that focuses on developing algorithms and models that enable computers to learn and make decisions without being  programmed. By analyzing large amounts of data, machine learning models can identify patterns, make predictions, and improve their accuracy over time. Common applications include recommendation systems, image recognition, and predictive analytics. This project uses machine learning techniques like linear regression to analyze data and predict outcomes based on the relationships between variables.

## What is Linear Regression?

Linear regression is a statistical method used to model the relationship between a dependent variable and one or more independent variables within datasets. It helps predict outcomes by fitting a straight line or pattern to the data points, showing how changes in the independent variables are associated with changes in the dependent variable.

## Example of Linear Regression

| Temperature (°C) | Coffee Sales (# of Cups) |
|-------------------|---------------------|
| 15                | 50                  |
| 20                | 60                  |
| 25                | 80                  |
| 30                | 100                 |
###### Table 1: Coffee Sales Based on Temperature ######

Let’s say you run a small coffee shop and want to predict your daily coffee sales based on the temperature outside. Collecting data on the temperature (independent variable) and corresponding coffee sales (dependent variable) over several days allows you to use linear regression to find a relationship between the two. For example, if you record data showing that more coffee is sold on warmer days, the application can calculate a line of best fit, such as Coffee Sales = 2 × Temperature + 20. This equation allows you to predict sales for any given temperature. If the temperature is 20°C, the expected sales would be 60 cups (2 × 20 + 20). Similarly, for 35°C, sales would be 90 cups (2 × 35 + 20). Linear regression simplifies understanding how one factor, such as temperature, influences another, like coffee sales, helping you make data-driven decisions to prepare for demand. This simple scenario can provide a clear basic understanding of how linear regression can work and the applications used in this project for data representation.

## How Does This Apply to This Project?

The application allows users to import data, select variables, and create regression models that can predict outcomes based on input data. By providing a graphical interface, the project makes it easier for users to build and interpret these models without needing to write code or have an in-depth understanding of statistical analysis. This ensures that the tool is accessible and useful for a range of users who may use or support the application.

## Project-Specific Information

### Team Members and Roles
- **Product Owner**: Oversees the project’s direction, prioritizes features, and ensures alignment with user needs.
- **Scrum Master**: Facilitates Agile practices and manages sprint progress.
- **Developers**: Responsible for implementing core functionalities, such as regression model creation, data handling, and prediction features.
- **Technical Writer**: Creates user documentation, maintains the README, and provides user-facing explanations of application features.

### Responsibilities
- **Developers**: Develop and maintain application code, ensuring smooth functionality and integration of features.
- **Technical Writer**: Collaborates closely with developers to understand the application, translates technical details into user-friendly documentation, and ensures accessibility for all intended audiences.


### Localization
The localization for this project is a blend of Spanish and English. If it becomes a requirement, the documentation will be adapted to support multiple languages.

### Developer Considerations
- **Data Formats**: Ensure seamless handling of CSV, Excel, and SQLite files with proper error handling and compatibility checks.

### Technical Writer Role in GitHub
- **Contribution**: The writer will actively manage and update the project’s GitHub repository, including:
  - Writing and formatting the README.
  - Maintaining Markdown documentation for usage and developer instructions.
  - Providing clear commit messages to track documentation updates.

