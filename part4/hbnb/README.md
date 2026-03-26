# **HBNB-Project** : Project Setup and Package Initialization:

## **Description:**
This part of the HBnB project focuses on setting up a modular and scalable architecture.
Configuring the layer structure Presentation, business logic, and persistence of the Hbnb project.
Creating the necessary folders, packages, and files.
Initialization of the facade pattern for communication between layers. Implementation of in-memory storage to manage the storage and validation of objects.

---

## **Structure Directory and file:**

### Directory:

* **hbnb/** : root directory

* **app/** : directory contains the core application code.

* **app/api/** : subdirectory houses the API endpoints, organized by version (v1/).

* **app/models/** : subdirectory contains the business logic classes (e.g., user.py, place.py).

* **app/services/** : subdirectory is where the Facade pattern is implemented, managing the interaction between layers.

* **app/persistence/** : subdirectory is where the in-memory repository is implemented.

### File:

* **run.py** : is the entry point for running the Flask application.

* **config.py** : will be used for configuring environment variables and application settings.

* **requirements.txt** : will list all the Python packages needed for the project.

---

## **Business Logic Layer:**
### Description:

This layer contains the main entities of the system.
Each class validates its own data.
The relationship between entities are defined here.
The layer is independent of the API.

#### Class descriptions:

* **BaseModel:**

Centralises common attributes.
Uses UUID to guarantee uniqueness.
Automatically manages timestamps.
Avoids code duplication.(DRY, "Don't Repeat Yourself")
* **User:**

Represents a user of the system.
Validates the data format.
email uniqueness handled by the Facade.
can own multple Places.
Can write multiple Reviews.
* **Review:**

Represents an available property.
Validates geographical coordinates.
Ensures that the owner is a valid user.
May contain multiple reviews.
May be associeted with multiple amenities.
* **Place:**

Represents a review of a Place.
Associates a User with a Place.
Guarantee a valid rating (1-5).
* **Amenity:**

Represents a feature of a property.
E.g: Wi-Fi, Parking.
Can be associated with several Places.

---
## **Models and Relationships:**
**1. User (1) ────< Place (N):**
* A user may own multiple places.
* A place has only one user (owner).
* One-to-many.

**2. Place (1) ────< Review (N):**
* A Place can have multiple Reviews.
* A Review belongs to only one Place.
* One-to-many.

**3.User (1) ────< Review (N):**
* A user can write multiple reviews.
* A review is written by a single user.
* One-to-many.

**4.Place (N) ────< Amenity (N):**
* A Place can have multiple Amenities.
* An Amenity can belong to multiple Places.
* Many-to-many.
---
## **API / V1:**
### Description:
The API layer represents the Presentation Layer of the application.
It exposes RESTful endpoints using Flask-RESTX and handles:

* HTTP requests and responses.
* Input validation.
* JSON serialization.
* Status codes (200, 201, 400, 404).
* Error handling.

The API does not contain business logic.

It communicates with the Business Logic layer exclusively through the Facade.

All endpoints are versioned under:
* **/api/v1/**
---
## **Facade:**
### Description:
### The HBnBFacade acts as an intermediary between:
* The API layer.
* The Business Logic layer.
* The Persistence layer.
### It centralizes application logic and ensures:
* Validation of relationships between entities.
* Coordination between repositories.
* Data integrity.
* Separation of concerns.

The Facade prevents the API from directly accessing repositories or models, improving maintainability and scalability.

### It implements operations such as:
* Creating users and places.
* Retrieving data.
* Updating entities.
* Validating ownership and relationships.
---
## **Repository:**
### Description:
The Repository layer handles data storage and retrieval.
### The project currently uses an InMemoryRepository, which:
* Stores objects in a Python dictionary.
* Provides CRUD operations (Create, Read, Update, Delete).
* Abstracts data access from business logic.

This abstraction allows the storage mechanism to be replaced later (e.g., database integration) without modifying the Business Logic layer.

### The Repository ensures:
* Encapsulation of data access.
* Reusability.
* Clean separation between logic and persistence.
---
## **Unit test:**
### Description:
The project includes automated unit tests to ensure the reliability, stability, and correctness of each layer of the application.

### **The tests validate:**
* Business rules inside models (data validation, constraints).
* Facade logic and entity coordination.
* API endpoints behavior (status codes, validation, error handling).
* Repository CRUD operations.

Unit tests help detect regressions early and guarantee that future modifications do not break existing functionality.

### **Test Coverage Includes:**
### Model Tests:

* Field validation (required fields).
* Boundary conditions (e.g., max length for names).
* Email format validation.
* Rating and coordinate constraints.
* Exception handling (ValueError).

### API Tests:

* Successful resource creation (201).
* Retrieval of single and multiple resources (200).
* Validation errors (400).
* Not found errors (404).
* Boundary value testing.
* Data integrity checks.

### Facade & Repository Tests:

* Entity creation and update logic.
* Relationship validation.
* In-memory storage behavior.

### Running all tests:
* **"python3 -m unittest discover unittests"**

---
## **Installation:**

### Installing dependencies using:

* **"pip install -r requirements.txt"**
---

## **Running the Application:**

### Start the application with:
* **"python run.py"**

### The application will run on:

* **http://127.0.0.1:5000/**

---
## **Testing the API with curl:**
## Examples:
### **1.Create a User:**
* curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}'

### **2.Create a Place:**
* curl -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{
  "title": "Cozy Apartment",
  "description": "Nice place to stay",
  "price": 100.0,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "owner_id": "USER_ID",
  "amenities": []
}'

### **3.Get all Places:**
* curl http://127.0.0.1:5000/api/v1/places/

### **4.Get place by ID:**
* curl http://127.0.0.1:5000/api/v1/places/PLACE_ID

### **5.Update a Place:**
* curl -X PUT http://127.0.0.1:5000/api/v1/places/PLACE_ID \
-H "Content-Type: application/json" \
-d '{
  "title": "Luxury Condo",
  "price": 250.0
}'

### **6.Error Handling Example:**
* curl -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{
  "title": "Test",
  "price": 100,
  "latitude": 40,
  "longitude": 2,
  "owner_id": "INVALID_ID",
  "amenities": []
}'
---
## **Authors:**

### Team:

* Mila **AUDU**: https://github.com/Milaa-au
* Pawnee **DEFIZE**: https://github.com/Pawnee33
