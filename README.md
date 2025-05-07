# Mapping Subjective Social Status Through Data and Models

This project explores how children from different regions perceive their social status, and whether these perceptions can be predicted using material and social indicators. Using survey data from four countries, we apply exploratory data analysis, clustering, and machine learning models to uncover patterns in self-reported social standing.

## Table of Contents

- [Introduction](#introduction)
- [Data](#data)
- [Exploratory Analysis](#exploratory-analysis)
- [Clustering](#clustering)
- [Machine Learning Models](#machine-learning-models)
- [Dashboard](#dashboard)



## Introduction

Subjective social status which is how people perceive their position in the social hierarchy, can be powerful measure of health and wellbeing. In this project, we examine whether children’s perceptions of their social status, measured by their placement on a 10-step "stairs" ladder, can be predicted based on demographic information and access to material goods.

## Data 

We used survey data from children from 4 different regions that measure their self-reported social status and access to various resources. We created a new variable called 'material_index' by averaging the four different resource variables: `Qhouse`, `Qfood`, `Qmoney`, and `Qthings`.


## Exploratory Analysis

We analyzed how perceived social status varied across regions, with specific focus on India, Argentina, and two rural areas in Ecuador—Cross Cutucú and Upano Valley. We found that children in Cross Cutucú generally reported higher scores across all well-being indicators, likely reflecting the role of local community networks. Results indicated that in India, access to money and personal items had the strongest positive correlations with higher social status, whereas in Argentina, access to food showed the strongest association. 

## Clustering

We used k-means clustering to group children based on numeric survey responses. Using an elbow plot, we identified four clusters corresponding to combinations of age and perceived social status. While the clusters were somewhat intuitive, they did not reveal the unexpected subgroupings we hoped for, likely due to the smaller data size. 

## Machine Learning Models

We trained a random forest regression model to predict `stairs` using age, sex, country, and `material_index`. The model achieved:

- **Mean Squared Error (MSE):** 6.92  
- **R-squared:** 0.10  
- **% Variance Explained (training):** 8.76%

These results indicate the model struggled to capture meaningful patterns in the data. Feature importance plots showed `material_index` was the most important predictor by MSE, while `age` contributed most to tree purity. Other variables like `sex` and `country` were less relevant.

## Dashboard
We created an interactive dashboard using Streamlit to help users explore the data. It includes:

Filters to select country and age range

A table showing filtered data

A comparison of linear regression and random forest model results

A tool to test predictions based on different inputs

A world map showing average ladder scores by country

A local map highlighting regions in Ecuador







