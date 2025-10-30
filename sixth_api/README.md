# 🌐 Project Overview
This repository hosts a Django application with a `Django REST Framework (DRF)` powered API for managing dogs and their breeds. The API supports CRUD
operations, dynamic data annotations, and optimized query handling. It is containerized with `Docker` for efficient deployment and uses `PostgreSQL` as
its database backend.

## 🚀 Key Features
- 🐕 **Dog Management**: Comprehensive CRUD operations for managing individual dogs, including attributes like name, age, breed, gender, and preferences
(favorite food and toy).
- 🐾 **Breed Management**: Manage dog breeds with metadata like size, friendliness, trainability, shedding, and exercise needs.
- 📊 **Dynamic Annotations**: Calculate average age of dogs per breed. Count dogs belonging to specific breeds dynamically.
- ⚡ **Optimized Query sets**: Efficient query handling with select_related and annotate for minimizing database queries.
- 🐳 **Dockerized Environment**: Simplified deployment using Docker Compose for a reproducible setup.

## 💻 Technologies Used
| [![Python](https://img.shields.io/badge/Python-%23242938?style=flat&logo=python&logoColor=%23366994&logoSize=auto&labelColor=%23ffc331)](https://www.python.org/) | [![Django](https://img.shields.io/badge/Django-%23092e20?style=flat&logo=django&logoSize=auto)](https://www.djangoproject.com/) | [![DjangoRestFramework (DRF)](https://img.shields.io/badge/Django%20REST%20Framework%20(DRF)-%237f2d2d?style=flat&logoSize=auto)](https://www.django-rest-framework.org/) | [pip-tools](https://github.com/jazzband/pip-tools) | [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%23242938?style=flat&logo=postgresql&logoColor=white&logoSize=auto&labelColor=%23336791)](https://www.postgresql.org/) | [![Docker](https://img.shields.io/badge/Docker-%232396ed?style=flat&logo=docker&logoColor=white&logoSize=auto)](https://www.docker.com/) |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------:|
|                                                          The main language used for building the project                                                          |                A high-level Python web framework that encourages rapid development and clean, pragmatic design.                 |                                                                    For building a powerful RESTful API                                                                    |          For managing Python dependencies          |                                                                    Database for dog and breed data storage                                                                    |                                          Containerizes the application and manages dependencies                                          |

## 🛠️ Setup Instructions
### 📋 Prerequisites
- `Docker` is installed on your machine.
- `.env` file is created in the root directory of the repository with your variables from the `.env.example` file.

## 🚀 Running the Application
1. Clone the repository:
```bash
git clone https://github.com/Nikilandgelo/workmate_tasks.git
```
2. Navigate to the project directory:
```bash
cd workmate_tasks
cd sixth_api
```
3. Start Services with Docker Compose:
```bash
docker-compose up -d --build
```
This will build and start the `PostgreSQL` and `Django` application containers.
4. Access services:
- `PostgreSQL`: On port `5432` of your machine.
- `Django`: On port `8000` of your machine.

## 📖 API Documentation
The **API** is documented and accessible via `Swagger UI`, powered by `drf-spectacular`. Use the following endpoint to explore the available API routes and their schemas:
- **Swagger UI** : `http://localhost:8000/api/swagger/`
- **Download Schema (YAML)**: `http://localhost:8000/api/download_schema/`
> [!NOTE]
> Ensure the server is running to access the documentation.


## 🏗️ App Architecture
- **Models**:
  - `Dog`: Includes fields such as _**name**_, _**age**_, _**breed**_ (foreign key), _**gender**_, _**color**_, _**favorite_food**_ and _**favorite_toy**_. 
  - `Breed`: Includes fields such as **_name_**, **_size_**, **_friendliness_**, **_trainability_**, **_shedding_amount_**, and **_exercise_needs_**. 
- **Serializers**:
  - `DogSerializer`: Serializes Dog objects with custom fields for breed average age and count. 
  - `BreedSerializer`: Serializes Breed objects with dynamic dog count on list of breeds.
- **Views**:
  - `DogViewSet`: Provides CRUD operations for dogs.
  - `BreedViewSet`: Provides CRUD operations for breeds.
> [!NOTE]
> Both viewsets are optimized with subquery and select_related to minimize database calls.
