# Workout App API

## Overview

This API provides functionalities for users to manage exercises, fitness goals, and workout plans. The API uses JWT-based authentication.

# Table of Contents

- [Installation](#docker)
- [API Documentation](#api-documentation)

## Docker

### Prerequisites

- Git
- Docker
- Docker Compose

### Building and Running the Application

1. Clone this repository:

   ```
    git clone https://github.com/SandroK0/workout-app.git
    cd workout-app
   ```

2. Build the Docker containers:

   ```
   docker compose build
   ```

3. Start the application:

   ```
   docker compose up
   ```

4. Access the application in your web browser at `http://localhost:5000` (or the appropriate port if you've configured it differently).

To stop the application, press `Ctrl+C` in the terminal where it's running, or run:

```
docker compose down
```

## Authentication

All authenticated requests require a Bearer token in the `Authorization` header:

```bash
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

# API Documentation

The API provides a Swagger UI interface for interactive documentation at the root route:

- **Swagger UI:** `http://your-api-domain.com/`
- This interface provides interactive documentation where you can test endpoints directly from your browser



## Responses

The API follows standard HTTP status codes:

- `200 OK`: Request successful
- `201 Created`: Resource successfully created
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Authentication failure
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate entry

---

## Notes

- Make sure to replace `YOUR_ACCESS_TOKEN` with a valid token after authentication.
- Update the base URL with your actual API domain.
- Ensure your request payloads match the expected schema.