# Libros

## About The Project

Libros is a feature-rich online bookstore web application built with the Django framework. It provides a platform for users to browse, search, and manage a collection of books. The project is fully containerized using Docker and includes a comprehensive user management system, advanced search capabilities, and performance optimizations through caching.

## Features

*   **User Authentication:** Secure user registration with email verification, login, and logout functionalities.
*   **Password Management:** Robust password reset flow via email.
*   **User Profiles:** Customizable user profiles with options to update personal information and profile pictures.
*   **Book Management:** Create, view, and manage books, including details like title, description, price, and cover image.
*   **Advanced Search & Filtering:** A powerful search engine to find books by title, description, or tags. Results can be further filtered by price range and rating.
*   **Tagging System:** `django-taggit` integration for easy categorization and discovery of books.
*   **Dynamic Homepage:** An infinite-scrolling homepage powered by HTMX for a seamless browsing experience.
*   **Performance Caching:** Utilizes Redis to cache frequently accessed data, such as the homepage and book detail pages, significantly reducing database load and improving response times.
*   **Containerized Environment:** Docker and Docker Compose are used for consistent development and easy deployment.
*   **Data Seeding:** A custom management command is available to populate the database with fake book data for testing and demonstration.

## Technology Stack

*   **Backend:** Python, Django
*   **Database:** PostgreSQL
*   **Caching:** Redis
*   **Frontend:** HTML, Bootstrap 5, CSS, JavaScript, HTMX
*   **Containerization:** Docker, Docker Compose

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

*   Git
*   Docker
*   Docker Compose

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kotoninja/libros.git
    cd libros
    ```

2.  **Create the environment file:**
    Duplicate the `.env.dist` file and rename it to `.env`.
    ```bash
    cp .env.dist .env
    ```

3.  **Configure environment variables:**
    Open the `.env` file and update the variables. A `SECRET_KEY` can be generated using Django's `get_random_secret_key()` function.
    ```
    SECRET_KEY=your_strong_secret_key
    POSTGRES_USER=your_db_user
    POSTGRES_PASSWORD=your_db_password
    POSTGRES_DB=your_db_name
    EMAIL_HOST_USER=your_email@example.com
    EMAIL_HOST_PASSWORD=your_email_app_password
    ```

4.  **Build and run the containers:**
    ```bash
    docker compose up --build
    ```
    The application server will be accessible at `http://localhost:8000`.

5.  **Apply database migrations:**
    In a new terminal, run the following command to set up the database schema:
    ```bash
    docker compose exec server python manage.py migrate
    ```

6.  **Create a superuser (optional):**
    To access the Django admin panel, create a superuser:
    ```bash
    docker compose exec server python manage.py createsuperuser
    ```

7.  **Populate the database with sample data (optional):**
    Use the custom management command to add sample books to the library. Replace `<amount>` with the number of books you want to create.
    ```bash
    docker compose exec server python manage.py closepoll <amount>
    ```
    For example, to add 50 books:
    ```bash
    docker compose exec server python manage.py closepoll 50
    ```

## Project Structure

The project is organized into three main Django applications:

*   **`core`**: Contains the main project settings, root URL configuration, global static files, and base templates.
*   **`library`**: Handles all functionalities related to books. This includes models for books, views for listing, detail, creation, and searching, as well as templates and a management command for data seeding.
*   **`user`**: Manages user authentication and profiles. It includes forms for login and registration, views for handling user sessions, password resets, email activation, and user settings pages.