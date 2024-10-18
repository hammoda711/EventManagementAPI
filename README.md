# EventManagementAPI


## Introduction
The **Event Management System** is a web application designed to help users create, manage, and attend events. It provides various functionalities for users, event hosts, and superusers, allowing efficient event organization and participation.

## Features
- User registration, login, and profile management.
- Host creation with capabilities to create, update, and delete events.
- Event management with capacity handling and attendee registration.
- Superuser privileges for managing users, hosts, and all events.
- Upcoming events listing for both users and hosts.
- Custom permissions based on user roles (user, host, superuser).
- Filtering, searching, and pagination for events.

## Roles and Privileges
1. **User**  
   - Can register, update, delete their account.
   - Can create a host profile if they want to host events.
   - Can register for events and view upcoming events they are attending.

2. **Host**  
   - Can create, update, delete, and manage events.
   - Can view upcoming events they are hosting.

3. **Superuser**  
   - Can delete user accounts and events.
   - Can view all users, hosts, and events in the system.

## Core Functionality
- **Event Management**: Hosts can perform CRUD operations on their events.
- **User Registration for Events**: Users can register for events, and event capacity is managed accordingly.
- **Filtering and Search**: Events can be searched and filtered based on various criteria (e.g., date, location).
- **Custom Permissions**: Role-based permissions for different functionalities ensure security and proper access control.

## Technology Stack
- **Backend**: Django, Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Authentication**: Simple JWT (JSON Web Token)
  
## Installation and Setup
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up the PostgreSQL database:
   ```
   # Example PostgreSQL setup
   CREATE DATABASE event_management_db;
   CREATE USER event_user WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE event_management_db TO event_user;
   ```
4. Apply migrations:
   ```
   python manage.py migrate
   ```
5. Run the server:
   ```
   python manage.py runserver
   ```

## API Endpoints


- **User Endpoints**:
  
  - `GET /users/` - List all users
  - `GET api/accounts/user/{username}/` - Retrieve a specific user
  - `PUT api/accounts//user/{username}/` - Update a specific user
  - `PATCH api/accounts//user/{username}/` - Partially update a specific user
  - `DELETE api/accounts/user/{username}/` - Delete a specific user

- **Host Endpoints**:
  
  - `GET api/accounts/hosts/` - List all hosts
  - `POST api/accounts/host-profile/` - Create a new host
  - `GET api/accounts/host-profile/{username}/` - Retrieve a specific host
  - `PUT api/accounts/host-profile/{username}/` - Update a specific host
  - `PATCH api/accounts/host-profile/{username}/` - Partially update a specific host
  - `DELETE api/accounts/host-profile/{username}/` - Delete a specific host

- **Authentication Endpoints**:
  
  - `POST /register/` - User registration
  - `POST /login/` - User login
  - `POST /logout/` - User logout

- **Events App Endpoints**:

- `POST api/events/create/` - Create a new event
- `DELETE api/events/{pk}/delete/` - Delete a specific event
- `GET api/events/{pk}/detail/` - Retrieve details of a specific event
- `GET api/events/upcoming/user/` - List all upcoming events for the authenticated user
- `GET api/events/upcoming/host/` - List all upcoming events for the authenticated host
- `GET api/events/all/` - List all events (only allowed for super user)
- `POST api/events/{event_id}/attend/` - Register for a specific event

## ERD

- [Entity Relationship Diagram (ERD)](event_management/docs/ERD.md)

## Contributing
Feel free to open issues or pull requests if you find any bugs or have suggestions for improvements.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

