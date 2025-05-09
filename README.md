# IBM Data Science Project: Sales Forecasting and Optimization

## Project Overview
This project aims to predict future sales for a retail business using historical sales data. The process involves data collection, cleaning, exploration, time-series forecasting model development, optimization, and deployment. The end goal is to create an accurate sales prediction model to help businesses optimize inventory, marketing, and sales strategies.

## Contributors
- **Abdallah Adel Abdallah** (21063654)
- **Abdelrahman Adel Abdelkader** (21057228)
- **Abdelrahman Badawy Ali** (21074236)
- **Asmaa Muhammad Abdelhamid** (21095177)
- **Maryam Taha Abdelaty** (21067260)
- **Muhammed Ahmed Abdelmegeed** (21063106)

**Supervised by:** Eng. Islam Adel

## Table of Contents
1. [Project Overview](#project-overview)
2. [Contributors](#contributors)
3. [Project Milestones](#project-milestones)
   - [First Milestone: Data Collection and Exploration](#first-milestone-data-collection-and-exploration)
   - [Second Milestone: Data Analysis and Visualization](#second-milestone-data-analysis-and-visualization)
   - [Third Milestone: Forecasting Model Development](#third-milestone-forecasting-model-development)
   - [Fourth Milestone: MLOps, Deployment, and Monitoring](#fourth-milestone-mlops-deployment-and-monitoring)
4. [Business Impact](#business-impact)
5. [Limitations & Future Work](#limitations--future-work)
6. [Technologies Used](#technologies-used)
7. [Conclusion](#conclusion)

## Project Milestones

### First Milestone: Data Collection and Exploration
- **Dataset Source:** Kaggle (`retail_store_inventory.csv`)
- **Dataset Size:** 73,100 rows, 15 columns
- **Key Features:**
  - Date: Daily records (January 2022)
  - Store IDs (`S001`–`S005`) & Product IDs (`P0001`–`P0020`)
  - Categories: Electronics, Clothing, Groceries, Toys, Furniture
  - Region: North, South, East, West
  - Sales metrics: Inventory Level, Units Sold, Demand Forecast
  - External factors: Weather Condition, Holiday/Promotion
- **Data Quality:** No missing values or duplicates found
- **Initial Insights:**
  - Electronics category has highest demand
  - East region shows strongest sales performance
  - Correlation analysis shows relationship between discounts, price, and sales

### Second Milestone: Data Analysis and Visualization
- **Statistical Analysis:**
  - Correlation analysis between Units Sold, Discount, and Holiday/Promotion
  - Hypothesis testing for effect of holidays on sales
  - ANOVA testing for weather condition impact
- **Key Visualizations:**
  - Monthly sales trends showing stability across 2022–2023
  - Sales distribution by weather condition (minimal impact)
  - Impact of promotions and holidays on different product categories

### Third Milestone: Forecasting Model Development
| Model               | Train R² | Test R² | MAE  | RMSE |
|---------------------|----------|---------|------|------|
| Linear Regression   | 0.9937   | 0.9937  | 7.47 | 8.65 |
| Decision Tree       | 1.0000   | 0.9871  | 10.12| 12.39|
| K-Nearest Neighbors | 0.9608   | 0.9430  | 21.00| 26.06|

- **Selected Model:** Linear Regression
  - Best performance across all metrics
  - No overfitting (consistent train/test scores)
  - Highly interpretable results

### Fourth Milestone: MLOps, Deployment, and Monitoring
- **MLOps Implementation:**
  - Used MLflow for experiment tracking and model versioning
  - Created centralized tracking server for experiment management
- **Model Deployment:**
  - Implemented interactive Streamlit web application
  - Supports both real-time and batch predictions
- **Monitoring System:**
  - Continuous tracking of model performance
  - Alerts for model drift detection
  - Dashboard reporting for stakeholders

## Business Impact
- **Inventory Optimization:** Reduced stockouts and overstocking
- **Cost Efficiency:** Quantified promotion ROI (10% discount drives ~15-unit sales increase)
- **Data-Driven Decisions:** Achieved 99.37% accuracy for sales forecasting

## Limitations & Future Work
- **Data Limitations:** 11-day dataset restricts analysis of long-term seasonality
- **Model Enhancements:** Explore Prophet or XGBoost with larger datasets
- **Operational Improvements:** Implement A/B testing and user feedback loops

## Technologies Used
- Python (data analysis and modeling)
- MLflow (experiment tracking)
- Streamlit (deployment)
- Statistical analysis libraries (e.g., pandas, scikit-learn)

## Conclusion
This project successfully delivered a robust framework for predicting sales, achieving **99.37% accuracy** with minimal error (RMSE = 8.65). The implemented MLOps pipeline ensures reproducibility, collaboration, and seamless model updates, positioning the business to make inventory decisions with high prediction accuracy and adapt dynamically to market changes.
