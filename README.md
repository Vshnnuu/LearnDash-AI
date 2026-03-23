# LearnDash
### An AI-Powered Learner Retention Dashboard

**LearnDash** is an AI-powered Dashboard that uses an end-to-end machine learning system for predicting learner churn/unsubscription risk for an online education platform and recommends retention strategies.  
The project combines a predictive model, a decision agent, and a simulated CRM workflow inside an interactive dashboard.

---

## Overview

Online learning platforms often lose learners due to inactivity, low engagement, billing issues, or unresolved support problems.

LearnDash's system predicts churn probability and generates targeted interventions such as:

- retention discount offers
- personalized course recommendations
- proactive support outreach
- re-engagement email campaigns

The goal is to demonstrate how ML predictions can integrate with operational decision workflows.

---

## System Architecture

```
User Input (Dashboard)
        ↓
Churn Prediction Model
        ↓
Risk Classification
        ↓
Retention Decision Agent
        ↓
Intervention Strategy
        ↓
CRM Workflow Simulation
```

---

## Major pipeline features

**Preprocessing**

- Missing value imputation
- Feature scaling for numeric features
- One-hot encoding for categorical features

Implemented using `scikit-learn` pipelines and `ColumnTransformer`.

## Retention Decision Agent

A rule-based agent analyzes learner signals and model output to determine:

**Churn Drivers**
- long inactivity
- low learning activity
- payment failures
- unresolved support issues
- low engagement

**Retention Strategies**
- discount offers
- reactivation campaigns
- course recommendations
- proactive support outreach

The agent prioritizes actions based on signal severity.

## CRM Simulation Layer

To mimic real operational workflows, the system simulates CRM actions such as:
```
[COMPLETED] Discount offer created — OFF-1042
[QUEUED] Email campaign queued — EML-2208
[OPEN] Support follow-up task created — SUP-3314
[QUEUED] Learning recommendation workflow queued — LRN-5586
```
This demonstrates how predictive systems connect with marketing and customer success tools in production environments.

## Interactive Dashboard

The system includes a **Gradio dashboard** where users can:

- input learner attributes
- simulate engagement behavior
- predict churn probability
- view recommended retention actions
- see simulated CRM task execution

Inputs are grouped into tabs such as:

- Learner Profile  
- Subscription Details  
- Learning Activity  
- Engagement Signals  
- Billing & Marketing  

## Running the Project

Public link for testing: 


### 1. Create environment (for setting up locally)
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the model
```bash
python -m src.train
```

### 4. Launch the dashboard
```bash
python app.py
```

The interface will start at:

```
http://127.0.0.1:7860
```

## Tech Stack

- Python
- scikit-learn
- XGBoost
- Pandas
- Gradio
- Joblib


