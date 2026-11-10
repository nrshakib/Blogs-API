# Blog API

A RESTful Blog API built with Django and Django REST Framework. This project is part of my hands-on learning journey with Django
REST Framework, focusing on API development, authentication, permissions, serializers, and database-backed CRUD operations.

## Tech Stack

-   **Python** -- programming language
-   **Django** -- web framework
-   **Django REST Framework (DRF)** -- REST API development
-   **PostgreSQL** -- relational database
-   **djangorestframework-simplejwt** -- JWT authentication
-   **python-dotenv** -- environment variable management
-   **Postman** -- API testing

## Project Structure

The project currently contains two main apps:

-   `accounts` -- custom user model, user registration, and
    login/authentication
-   `posts` -- blog post model, serializers, views, permissions, and
    post endpoints

## Implemented Features

### 1. Custom User Model

-   Created a custom user model by extending Django's `AbstractUser`.
-   Uses email as the model's `USERNAME_FIELD`.
-   Email is unique.
-   Configured Django admin to work with the custom user model.

### 2. User Registration

-   User registration endpoint.
-   Passwords are securely hashed using Django's `set_password()`.
-   Password is write-only in the registration serializer.
-   Registration endpoint is publicly accessible.

### 3. JWT Authentication

-   Integrated SimpleJWT.
-   Login supports either **username or email** through a single `user` request field.
-   Generates access and refresh tokens after successful authentication.
-   Customized login response to include a success message, status text, user information, and tokens.
-   Customized authentication error messages for invalid username/email and invalid password.
-   JWT authentication is configured for protected API endpoints.

Example login request:

``` json
{
  "user": "username_or_email",
  "password": "your_password"
}
```

Example successful response structure:

``` json
{
  "message": "Login Successful",
  "status_text": "success",
  "data": {
    "username": "your_username",
    "email": "your_email"
  },
  "tokens": {
    "access": "access_token",
    "refresh": "refresh_token"
  }
}
```

### 4. Blog Posts

-   Create, list, retrieve, update, and delete blog posts.
-   Posts have a title, slug, content, author, status, creation timestamp, and update timestamp.
-   Slugs are generated automatically from post titles.
-   Post status supports `draft` and `published`.
-   The authenticated user is automatically assigned as the author when creating a post.
-   Retrieve, update, and delete endpoints accept either a post ID or slug.

### 5. Permissions and Post Visibility

-   Only authenticated users can access protected post endpoints.
-   Only the post author can update or delete their own post.
-   Read-only access is allowed for other users on published posts.
-   Users can access their own draft posts.
-   Other users cannot access unpublished drafts.

### 6. Filtering, Searching, and Ordering

The post listing endpoint supports:

-   Filtering posts by status.
-   Searching post title and content.
-   Ordering posts by creation date and title.

### 7. API Design

-   Used `GenericAPIView` with DRF mixins for post operations.
-   Used custom response structures for relevant endpoints.
-   Used serializer validation and `perform_create()` to handle author assignment.

## Configuration

The project uses environment variables for sensitive and environment-specific settings.

Create a `.env` file in the project root and provide the values required by your settings, for example:

``` env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

Do not commit your real `.env` file, secret key, database password, or other credentials to version control.

## Running Locally

1.  Clone the repository:

    ``` bash
    git clone <https://github.com/nrshakib/Blogs-API>
    cd <Blogs-API>
    ```

2.  Create and activate a virtual environment:

    ``` bash
    py -m venv venv
    venv\Scripts\activate
    ```

3.  Install dependencies:

    ``` bash
    pip install -r requirements.txt
    ```

4.  Configure your `.env` file.

5.  Apply database migrations:

    ``` bash
    py manage.py migrate
    ```

6.  Create a superuser if needed:

    ``` bash
    py manage.py createsuperuser
    ```

7.  Start the development server:

    ``` bash
    py manage.py runserver
    ```

The API will be available at `http://127.0.0.1:8000/`. The exact endpoint paths depend on the project's URL configuration.

## Planned / Future Improvements

The following are potential next steps and are not yet claimed as implemented:

-   Refresh-token and logout endpoints, including refresh-token blacklisting.
-   Automated API tests using DRF's testing tools.
-   Pagination for post listing.
-   More advanced filtering and query optimization.
-   Additional user profile and account-management endpoints.
-   Password change and password reset flows.
-   Email verification.
-   API documentation with OpenAPI/Swagger.
-   Production deployment, environment hardening, and logging.

## Learning Goals

This project is helping me practice:

-   Building REST APIs with Django REST Framework.
-   Working with custom user models.
-   Understanding serializers and validation.
-   Using `GenericAPIView` and mixins.
-   Implementing object-level permissions.
-   Managing authentication with JWT.
-   Working with PostgreSQL and environment variables.
-   Designing consistent API responses.

## Notes

This is a learning project and is being developed incrementally.
Features listed under **Planned / Future Improvements** are not part of the current implementation yet.
