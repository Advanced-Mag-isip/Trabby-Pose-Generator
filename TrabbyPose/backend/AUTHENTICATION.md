# Authentication API Documentation

## Overview

The Trabby Pose Generator backend implements a role-based authentication system with two user types:

- **Admin**: Can create and manage user accounts
- **User**: Can log in and use the application after admin creates their account

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

This creates the necessary database tables including the User model with authentication fields.

### 3. Seed the Admin User

```bash
python manage.py seed
```

This creates:
- **Admin Account**:
  - Username: `admin`
  - Password: `admin123`
  - Email: `admin@trabby.local`

- **Regular Test Users** (optional):
  - `user1` - `user5` with password `password123`

## Authentication Endpoints

All endpoints are prefixed with `/api/auth/`

### 1. Login

**Endpoint**: `POST /api/auth/login/`

**Description**: Authenticate user and start a session.

**Request Body**:
```json
{
  "user_name": "admin",
  "password": "admin123"
}
```

**Response** (200 OK):
```json
{
  "user": {
    "user_id": 1,
    "first_name": "Admin",
    "last_name": "User",
    "user_name": "admin",
    "email_address": "admin@trabby.local",
    "is_permitted": 1,
    "is_admin": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "message": "Login successful"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid username or password
- `401 Unauthorized`: Account is not active

**Usage Example**:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"user_name": "admin", "password": "admin123"}' \
  -c cookies.txt
```

---

### 2. Logout

**Endpoint**: `POST /api/auth/logout/`

**Description**: End user session and clear authentication.

**Requirements**: User must be authenticated (session cookie required)

**Response** (200 OK):
```json
{
  "message": "Logout successful"
}
```

**Usage Example**:
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

---

### 3. Get Current User Profile

**Endpoint**: `GET /api/auth/profile/`

**Description**: Retrieve the authenticated user's profile information.

**Requirements**: User must be authenticated

**Response** (200 OK):
```json
{
  "user": {
    "user_id": 1,
    "first_name": "Admin",
    "last_name": "User",
    "user_name": "admin",
    "email_address": "admin@trabby.local",
    "is_permitted": 1,
    "is_admin": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

**Usage Example**:
```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

---

### 4. Register / Create User

**Endpoint**: `POST /api/auth/register/`

**Description**: Create a new user account.

- **First user**: Created without authentication (automatically becomes admin)
- **Subsequent users**: Requires authenticated admin user

**Request Body**:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "user_name": "johndoe",
  "email_address": "john@example.com",
  "password": "SecurePassword123!",
  "confirm_password": "SecurePassword123!",
  "is_permitted": 1
}
```

**Response** (201 Created):
```json
{
  "user": {
    "user_id": 2,
    "first_name": "John",
    "last_name": "Doe",
    "user_name": "johndoe",
    "email_address": "john@example.com",
    "is_permitted": 1,
    "is_admin": false,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  },
  "message": "User created successfully"
}
```

**Error Responses**:
- `400 Bad Request`: Username already taken
- `400 Bad Request`: Email already registered
- `400 Bad Request`: Passwords do not match
- `403 Forbidden`: User is not an admin (after first user created)

**Usage Example** (Admin creates user):
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "user_name": "johndoe",
    "email_address": "john@example.com",
    "password": "SecurePassword123!",
    "confirm_password": "SecurePassword123!",
    "is_permitted": 1
  }'
```

---

### 5. List All Users

**Endpoint**: `GET /api/auth/users/`

**Description**: Get a list of all users in the system.

**Requirements**: Authenticated admin user only

**Response** (200 OK):
```json
{
  "users": [
    {
      "user_id": 1,
      "first_name": "Admin",
      "last_name": "User",
      "user_name": "admin",
      "email_address": "admin@trabby.local",
      "is_permitted": 1,
      "is_admin": true,
      "created_at": "2024-01-01T00:00:00Z"
    },
    {
      "user_id": 2,
      "first_name": "John",
      "last_name": "Doe",
      "user_name": "johndoe",
      "email_address": "john@example.com",
      "is_permitted": 1,
      "is_admin": false,
      "created_at": "2024-01-01T12:00:00Z"
    }
  ],
  "count": 2
}
```

**Error Responses**:
- `403 Forbidden`: User is not an admin

**Usage Example**:
```bash
curl -X GET http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

---

### 6. Update User

**Endpoint**: `PUT /api/auth/users/<user_id>/` or `PATCH /api/auth/users/<user_id>/`

**Description**: Update user information.

- **Users**: Can update their own profile
- **Admins**: Can update any user's profile

**Request Body** (fields are optional):
```json
{
  "first_name": "John",
  "last_name": "Doe Updated",
  "email_address": "newemail@example.com",
  "is_permitted": 1
}
```

**Response** (200 OK):
```json
{
  "user": {
    "user_id": 2,
    "first_name": "John",
    "last_name": "Doe Updated",
    "user_name": "johndoe",
    "email_address": "newemail@example.com",
    "is_permitted": 1,
    "is_admin": false,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-02T10:00:00Z"
  },
  "message": "User updated successfully"
}
```

**Error Responses**:
- `403 Forbidden`: Non-admin trying to update another user's profile
- `404 Not Found`: User not found

**Usage Example**:
```bash
curl -X PATCH http://localhost:8000/api/auth/users/2/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "first_name": "John",
    "last_name": "Doe Updated"
  }'
```

---

### 7. Delete User

**Endpoint**: `DELETE /api/auth/users/<user_id>/delete/`

**Description**: Delete a user account.

**Requirements**: Authenticated admin user only

**Response** (200 OK):
```json
{
  "message": "User johndoe deleted successfully"
}
```

**Error Responses**:
- `403 Forbidden`: User is not an admin
- `404 Not Found`: User not found
- `400 Bad Request`: Cannot delete the last admin user

**Usage Example**:
```bash
curl -X DELETE http://localhost:8000/api/auth/users/2/delete/ \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

---

## Authentication Flow

### Admin Workflow

1. **Initial Setup**:
   ```
   POST /api/auth/register/  (create first admin user)
   ↓
   POST /api/auth/login/     (admin logs in)
   ```

2. **Create Users**:
   ```
   POST /api/auth/register/  (admin creates regular users)
   POST /api/auth/users/     (admin views all users)
   PATCH /api/auth/users/<id>/  (admin updates users)
   DELETE /api/auth/users/<id>/delete/  (admin deletes users)
   ```

### User Workflow

1. **Login** (after admin creates account):
   ```
   POST /api/auth/login/     (user logs in)
   ↓
   GET /api/auth/profile/    (user views their profile)
   PATCH /api/auth/users/<id>/  (user updates their own profile)
   POST /api/auth/logout/    (user logs out)
   ```

---

## Authentication Methods

The API supports two authentication methods:

### 1. Session Authentication (Default)
- Cookies are automatically set after login
- Include cookies in subsequent requests
- Best for web applications

**Example**:
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"user_name": "admin", "password": "admin123"}' \
  -c cookies.txt

# Subsequent request with session cookie
curl -X GET http://localhost:8000/api/auth/profile/ \
  -b cookies.txt
```

### 2. Token Authentication
- Use the token in the Authorization header
- Better for API clients

**Example**:
```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## Error Handling

All errors follow a consistent format:

**Format**:
```json
{
  "error": "Error message or field-level errors"
}
```

**Common HTTP Status Codes**:
- `200 OK` - Successful request
- `201 Created` - User created successfully
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Invalid credentials or not authenticated
- `403 Forbidden` - Permission denied (not admin)
- `404 Not Found` - Resource not found

---

## Security Best Practices

1. **Password Requirements**:
   - Passwords must be at least 8 characters long
   - Passwords are hashed using Django's password hashers
   - Never store plain text passwords

2. **HTTPS in Production**:
   - Set `SESSION_COOKIE_SECURE = True`
   - Set `CSRF_COOKIE_SECURE = True`
   - Update `CORS_ALLOWED_ORIGINS` with your production domain

3. **CORS Configuration**:
   - Update `CORS_ALLOWED_ORIGINS` in settings.py
   - Only allow trusted frontend origins

4. **Session Management**:
   - Default session timeout: 24 hours
   - Sessions are stored in the database
   - User sessions are cleared on logout

---

## Frontend Integration Example

### React/JavaScript Example

```javascript
// Login
async function login(username, password) {
  const response = await fetch('http://localhost:8000/api/auth/login/', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_name: username,
      password: password,
    }),
  });
  
  if (!response.ok) throw new Error('Login failed');
  return await response.json();
}

// Get current user
async function getCurrentUser() {
  const response = await fetch('http://localhost:8000/api/auth/profile/', {
    method: 'GET',
    credentials: 'include',
  });
  
  if (!response.ok) throw new Error('Failed to get user');
  return await response.json();
}

// Logout
async function logout() {
  const response = await fetch('http://localhost:8000/api/auth/logout/', {
    method: 'POST',
    credentials: 'include',
  });
  
  if (!response.ok) throw new Error('Logout failed');
  return await response.json();
}

// Create user (admin only)
async function createUser(userData) {
  const response = await fetch('http://localhost:8000/api/auth/register/', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });
  
  if (!response.ok) throw new Error('User creation failed');
  return await response.json();
}
```

---

## Troubleshooting

### Issue: "Invalid username or password"
- Verify the username and password are correct
- Ensure the user account was created successfully
- Check that the user's `is_permitted` field is set to 1

### Issue: "You do not have permission to create users"
- Ensure you are logged in as an admin
- Check the `is_admin` field for your user

### Issue: "CORS error" in frontend
- Update `CORS_ALLOWED_ORIGINS` in settings.py
- Add your frontend URL to the allowed origins list
- Example: `"http://localhost:3000"`

### Issue: Session not persisting
- Ensure cookies are being sent with requests (`credentials: 'include'`)
- Check that `SESSION_ENGINE` is set to `'django.contrib.sessions.backends.db'`
- Verify the sessions table exists in the database

---

## Database Migrations

To apply the authentication schema changes:

```bash
# Apply migrations
python manage.py migrate

# Create superuser for Django admin (optional)
python manage.py createsuperuser
```

---

## Testing

Run the following commands to test the authentication:

```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test api.tests
```

---

## Next Steps

1. Update your frontend to use the authentication endpoints
2. Configure CORS settings for your production domain
3. Set up HTTPS in production
4. Create a proper admin panel for user management
5. Implement password reset functionality
