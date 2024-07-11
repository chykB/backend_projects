# User Authentication & Organisation API

## Overview

This Django-based REST API provides user authentication and organization management functionality. It allows users to register, login, create and manage organizations, and add users to organizations.

## Features

- Custom user model with email-based authentication
- JWT-based authentication
- User registration and login
- Organization creation and management
- Adding users to organizations
- Protected routes for authenticated users

## Technologies Used

- Django 4.2
- Django REST Framework 3.14
- PostgreSQL 12
- Simple JWT for token-based authentication

## Prerequisites

- Python 3.12
- PostgreSQL 12
- pip (Python package manager)

## Installation

1. Clone the repository:
    ```git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name ```

2. Create a virtual environment and activate it:
    ```
        python -m venv venv
        source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. Install the required packages:
    ```
        pip install -r requirements.txt
    ```

4. Set up your PostgreSQL database and update the `DATABASES` configuration in `settings.py` with your database credentials.

5. Apply migrations:
    ```
        python manage.py makemigrations
        python manage.py migrate
    ```
6. Create a superuser (optional):
```
    python manage.py createsuperuser
```
7. Run the development server:
```
    python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

- `POST /auth/register/`: Register a new user and create a default organization
- `POST /auth/login/`: Log in a user
- `GET /api/users/<user_id>/`: Get user details (protected)
- `GET /api/organisations/`: List user's organizations (protected)
- `GET /api/organisations/<org_id>/`: Get single organization details (protected)
- `POST /api/organisations/create`: Create a new organization (protected)
- `POST /api/organisations/<org_id>/users/`: Add a user to an organization (protected)

For detailed API documentation, refer to the [API Documentation](API_DOCUMENTATION.md) file.

## Testing

Run the test suite using:
```
    python manage.py test
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Blessing Malik - malikchika86@gmail.com

Project Link: [https://github.com/chykB/backend_projects/tree/main/user](https://github.com/chykB/backend_projects/tree/main/user)
