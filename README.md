# Expenses Tracker App

## Overview

The Expenses Tracker App is a Django-based web application that allows users to manage and track their income and expenses. Built with PostgreSQL as the backend database, the app is Dockerized and deployed on Google Cloud for maximum scalability and efficiency.

## Features

- User Authentication and Registration
- Customizable Profile and Settings
- Transaction Management (Income/Expenses)
- Transaction Categorization
- Dashboard Analytics
- Date Range Filters
- Password Management

## Technologies

- Django
- PostgreSQL
- Docker
- Google Cloud

## Models

### Category

Fields:

- `category_type`: Type of the category (Income/Expense)
- `name`: Name of the category
- `parent_category`: Optional parent category

### Transaction

Fields:

- `amount`: Amount of the transaction
- `transaction_type`: Type of the transaction (Income/Expense)
- `category`: Category of the transaction
- `description`: Optional description
- `date`: Date of the transaction
- `user`: User who owns the transaction

## Key Views

- `HomeView`: Welcome page displaying the current date.
- `LoginInterfaceView`: Custom login view.
- `LogoutInterfaceView`: Custom logout view.
- `SignupView`: User registration with email validation.
- `ProfileView`: User profile management.
- `AuthorizedView`: Restricted access view.
- `ChangeEmailView`: View for changing email.
- `ChangePasswordView`: View for changing the password.

For Transaction Management:
- `TransactionsListView`: View for listing transactions with optional date range filter.
- `TransactionsCreateView`: View for creating a new transaction.
- `TransactionsUpdateView`: View for updating an existing transaction.
- `TransactionsDeleteView`: View for deleting a transaction.
- `DashboardView`: View for dashboard analytics.

## Installation and Deployment

### Requirements

- Python 3.x
- Docker
- Google Cloud account

### Local Development

Clone the repository:

```bash
git clone https://github.com/artyom-vetlugin/DjangoBudgetTracker.git
```

Run Docker Compose:

```bash
docker-compose up --build
```

Your app should now be running at `http://localhost:8000`.

### Deployment to Google Cloud

Follow the Google Cloud documentation for deploying a Dockerized app.

---
