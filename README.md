# **Classroom-Manager REST API Flask Project** 🏫

## Project Overview 📝
The Classroom-Manager project is designed as a robust educational resource management system, featuring:

- **Purpose**: Facilitate the management of educational resources within academic institutions, such as classrooms, departments, and user accounts.
- **Core Feature**: High-quality _RESTful API_ that allows for efficient management of user records, classes, and classroom bookings.
- **Target Audience**: Ideally suited for schools and universities looking to digitize and streamline their resource allocation and scheduling processes.
- **API Functionality**: Provides a scalable and secure interface for developers to integrate and extend functionalities seamlessly.
- **Technology Stack**: Utilizes modern technologies including `Flask` for the backend, `SQLAlchemy` for ORM, and `PostgreSQL` as the database.

## How to Run the Application 🔧
To get the application up and running, follow these steps:
1. **Setup with Docker**:
  - Clone the repository to your local machine.
  - Navigate to the backend directory of the project.
  - Use Docker Compose to build and run the containers:
    ```bash
    docker-compose up -d
    ```

2. **Running the Application**:
  - Access the backend services via [localhost:6200/docs](http://localhost:6200/docs) where you can interact with the API through its Swagger documentation.

## How to Stop the Application 🔌
To stop and remove the application containers, use the following Docker Compose commands:
- **Stopping the application**:
  ```bash
  docker-compose stop
  ```

- **Removing the application**:
  ```bash
  docker-compose down
  ```

## Architecture 🔍
The backend architecture of Classroom-Manager is designed around a clean separation of concerns, promoting maintainability and scalability:
- **Presentation Layer** (`/routes`): Manages API endpoints, serving as the interface that receives requests and sends responses.
- **Business Logic Layer** (`/services`): Processes data, applying business rules and handling operations like user authentication, resource management, etc.
- **Data Access Layer** (`/repositories` & `/models`): Responsible for database interactions, ensuring data integrity and providing an abstraction layer over direct database manipulations.

## Key Directories 📍
- **`/migrations`**: Contains database migration scripts.
- **`/src`**: The heart of the application where the main logic resides.
  - **`/app`**: The core application folder.
    - **`/repositories`**: Contains code interacting with the database.
    - **`/models`**: Defines the data models.
    - **`/orm`**: Object-relational mapping setup.
    - **`/serializations`**: Code for serializing and deserializing data.
    - **`/routes`**: Defines the endpoints of the API.
    - **`/services`**: Business logic of the application.

## Technologies 🌐
- **`Flask`**: A lightweight framework for building web applications in `Python`.
- **`SQLAlchemy`**: An ORM tool for database operations, enhancing code maintainability and security.
- **`JWT` Libraries**: Handling authentication using JSON Web Tokens.
- **`Docker`**: Containerization of the application ensuring consistent environments.
- **`PostgreSQL`**: The primary relational database used for storing all application data.

## API Capabilities 💡
- **User Management**: Register, authenticate, update, and manage user profiles.
- **Department Management**: Create, update, delete, and retrieve departments within an organization.
- **Building Management**: Handle operations related to building resources including CRUD operations.
- **Classroom Management**: Manage classrooms, including scheduling and booking functionalities.
- **Request Management**: Handle booking requests for classrooms, managing approvals and rejections.

## Database Interaction 🗃
The application uses `PostgreSQL` as its database. 
The **ORM** (Object-Relational Mapping) provided by `SQLAlchemy` abstracts the SQL layer, offering a high-level interface for database operations. 
The **repository pattern** further encapsulates the logic needed to access data sources, ensuring that the business logic is not dependent on database specifics.

## Docker Configuration 🐳
The application runs in Docker containers. The `docker-compose.yml` file orchestrates multiple services:
- **Flask Application Container**: Hosts the `Flask` application.
- **PostgreSQL Container**: Manages the database service, isolated from the application logic.
