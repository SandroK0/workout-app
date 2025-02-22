# Workout App API

## Overview

This API provides functionalities for users to manage exercises, fitness goals, and workout plans. 

## Technology Used

- Python (Flask)
- SQLite


# Table of Contents

- [Installation](#docker)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)


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

---

# API Documentation

## Swagger

- **Swagger UI:** `http://your-api-domain.com/api/docs`
- This interface provides interactive documentation where you can test endpoints directly from your browser

## Authentication

All authenticated requests require a Bearer token in the `Authorization` header:

## Endpoints

- [User](#user-endpoints)
- [Exercises](#exercises-endpoints)
- [Workout Plans](#workout-plans-endpoints)
- [Exercise Goals](#exercise-goals-endpoints)
- [Workout Sessions](#workout-sessions-endpoints)
- [Fitness Goals](#fitness-goals-endpoints)

## User Endpoints

### User Registration

- **Endpoint:** `/api/user/register`
- **Method:** POST
- **Description:** Register a new user
- **Responses:**
  - 201: User registered successfully
  - 400: Missing required fields
  - 409: Username already taken

**Example:**

```bash
curl -X POST https://api.example.com/api/user/register \
     -H "Content-Type: application/json" \
     -d '{"username": "user123", "password": "securepass123"}'
```

### User Login

- **Endpoint:** `/api/user/login`
- **Method:** POST
- **Description:** Login a user
- **Responses:**
  - 200: Login successful
  - 400: Missing required fields
  - 401: Invalid credentials

**Example:**

```bash
curl -X POST https://api.example.com/api/user/login \
     -H "Content-Type: application/json" \
     -d '{"username": "user123", "password": "securepass123"}'
```

### User Profile

#### Get Profile

- **Endpoint:** `/api/user/profile`
- **Method:** GET
- **Description:** Retrieve current user's profile information
- **Responses:**
  - 200: Profile retrieved successfully
  - 401: Unauthorized
  - 404: Profile not found

**Example:**

```bash
curl -X GET https://api.example.com/api/user/profile \
     -H "Authorization: Bearer YOUR_TOKEN"
```

#### Update Profile

- **Endpoint:** `/api/user/profile`
- **Method:** PUT
- **Description:** Update user profile information
- **Responses:**
  - 200: Profile updated successfully
  - 400: Invalid input data
  - 401: Unauthorized
  - 404: Profile not found

**Example:**

```bash
curl -X PUT https://api.example.com/api/user/profile \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"current_weight": 70.5, "height": 175, "age": 30, "body_fat_percentage": 15.5, "muscle_mass": 35.2}'
```

## Exercises Endpoints

### List Exercises

- **Endpoint:** `/api/exercises`
- **Method:** GET
- **Description:** Retrieve a list of all exercises
- **Responses:**
  - 200: Success (returns array of exercises)
  - 404: Exercises Not Found

**Example:**

```bash
curl -X GET https://api.example.com/api/exercises \
```

### Get Single Exercise

- **Endpoint:** `/api/exercises/{exercise_id}`
- **Method:** GET
- **Description:** Retrieve details of a specific exercise
- **Responses:**
  - 200: Success (returns exercise details)
  - 404: Exercise Not Found

**Example:**

```bash
curl -X GET https://api.example.com/api/exercises/1
```

## Workout Plans Endpoints

### Create Workout Plan

- **Endpoint:** `/api/workout-plans`
- **Method:** POST
- **Description:** Create a new workout plan with exercises
- **Responses:**
  - 201: Workout plan created successfully
  - 400: Validation error
  - 404: User not found
  - 500: Server error

**Example:**

```bash
curl -X POST https://api.example.com/api/workout-plans \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
         "name": "My Workout Plan",
         "frequency": "3x per week",
         "session_duration": 60,
         "selected_exercises": [
           {
             "exercise_id": 1,
             "sets": 3,
             "reps": 12,
             "duration": "30s",
             "distance": "none"
           }
         ]
     }'
```

### Get Workout Plan Summaries

- **Endpoint:** `/api/workout-plans/summary`
- **Method:** GET
- **Description:** Get all workout plan summaries for current user
- **Responses:**
  - 200: Workout plan summaries retrieved successfully

**Example:**

```bash
curl -X GET https://api.example.com/api/workout-plans/summary \
     -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Single Workout Plan

- **Endpoint:** `/api/workout-plans/{plan_id}`
- **Method:** GET
- **Description:** Retrieve a specific workout plan by its ID
- **Responses:**
  - 200: Success (returns workout plan details)
  - 404: Workout plan not found

**Example:**

```bash
curl -X GET https://api.example.com/api/workout-plans/1 \
     -H "Authorization: Bearer YOUR_TOKEN"
```

### Update Workout Plan

- **Endpoint:** `/api/workout-plans/{plan_id}`
- **Method:** PUT
- **Description:** Update an existing workout plan
- **Responses:**
  - 200: Workout plan updated successfully
  - 400: Validation error
  - 404: Workout plan not found

**Example:**

```bash
curl -X PUT https://api.example.com/api/workout-plans/1 \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
         "name": "Updated Workout Plan",
         "frequency": "4x per week",
         "session_duration": 45
     }'
```

### Delete Workout Plan

- **Endpoint:** `/api/workout-plans/{plan_id}`
- **Method:** DELETE
- **Description:** Delete a workout plan
- **Responses:**
  - 204: Workout plan deleted successfully
  - 400: Error deleting workout plan
  - 404: Workout plan not found

**Example:**

```bash
curl -X DELETE https://api.example.com/api/workout-plans/1 \
     -H "Authorization: Bearer YOUR_TOKEN"
```

### Workout Plan Exercises

#### List Exercises in Workout Plan

- **Endpoint:** `/api/workout-plans/{plan_id}/exercises`
- **Method:** GET
- **Description:** Retrieve all exercises in a specific workout plan
- **Responses:**
  - 200: Exercises retrieved successfully
  - 404: Workout plan not found

**Example:**

```bash
curl -X GET https://api.example.com/api/workout-plans/1/exercises \
     -H "Authorization: Bearer YOUR_TOKEN"
```

#### Add Exercise to Workout Plan

- **Endpoint:** `/api/workout-plans/{plan_id}/exercises`
- **Method:** POST
- **Description:** Add a new exercise to a workout plan
- **Responses:**
  - 201: Exercise added to workout plan successfully
  - 400: Validation error
  - 404: Workout plan or exercise not found

**Example:**

```bash
curl -X POST https://api.example.com/api/workout-plans/1/exercises \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
         "exercise_id": 1,
         "sets": 3,
         "reps": 12,
         "duration": "30s",
         "distance": "none"
     }'
```

#### Get Single Exercise in Workout Plan

- **Endpoint:** `/api/workout-plans/{plan_id}/exercise/{id}`
- **Method:** GET
- **Description:** Retrieve details of an exercise in a specific workout plan
- **Responses:**
  - 200: Exercise retrieved successfully
  - 404: Workout plan or exercise not found

**Example:**

```bash
curl -X GET https://api.example.com/api/workout-plans/1/exercise/1 \
     -H "Authorization: Bearer YOUR_TOKEN"
```

#### Update Exercise in Workout Plan

- **Endpoint:** `/api/workout-plans/{plan_id}/exercise/{id}`
- **Method:** PUT
- **Description:** Update an exercise in a specific workout plan
- **Responses:**
  - 200: Exercise updated successfully
  - 400: Validation error
  - 404: Workout plan or exercise not found

**Example:**

```bash
curl -X PUT https://api.example.com/api/workout-plans/1/exercise/1 \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
         "sets": 4,
         "reps": 15,
         "duration": "45s",
         "distance": "none"
     }'
```

#### Delete Exercise from Workout Plan

- **Endpoint:** `/api/workout-plans/{plan_id}/exercise/{id}`
- **Method:** DELETE
- **Description:** Delete an exercise from a specific workout plan
- **Responses:**
  - 204: Exercise deleted successfully
  - 400: Error deleting exercise
  - 404: Workout plan or exercise not found

**Example:**

```bash
curl -X DELETE https://api.example.com/api/workout-plans/1/exercise/1 \
     -H "Authorization: Bearer YOUR_TOKEN"
```

## Workout Sessions Endpoints

### List Workout Sessions

- **Endpoint:** `/api/workout-sessions`
- **Method:** GET
- **Description:** Get a list of completed workout sessions for the authenticated user
- **Responses:**
  - 200: Success (returns array of workout sessions)
  - 401: Unauthorized
  - 404: User not found

**Example:**

```bash
curl -X GET https://api.example.com/api/workout-sessions \
     -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Workout Session

- **Endpoint:** `/api/workout-sessions`
- **Method:** POST
- **Description:** Create a new workout session for the authenticated user
- **Responses:**
  - 201: Workout session created successfully
  - 400: Invalid input

**Example:**

```bash
curl -X POST https://api.example.com/api/workout-sessions \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
         "workout_plan_id": 1,
         "user_id": 1,
         "date": "2025-02-04T14:30:00Z",
         "duration": 45,
         "notes": "Great workout session"
     }'
```

### Get Single Workout Session

- **Endpoint:** `/api/workout-sessions/{session_id}`
- **Method:** GET
- **Description:** Retrieve a single completed workout session by ID
- **Responses:**
  - 200: Success
  - 404: Workout session not found

**Example:**

```bash
curl -X GET https://api.example.com/api/workout-sessions/1 \
     -H "Authorization: Bearer YOUR_TOKEN"
```

## Exercise Goals Endpoints

### List Exercise Goals

- **Endpoint:** `/api/exercise-goals`
- **Method:** GET
- **Description:** Get a list of exercise goals for the authenticated user
- **Responses:**
  - 200: Success (returns array of exercise goals)
  - 401: Unauthorized
  - 404: User not found

**Example:**

```bash
curl -X GET https://api.example.com/api/exercise-goals \
     -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Exercise Goal

- **Endpoint:** `/api/exercise-goals`
- **Method:** POST
- **Description:** Create a new exercise goal for the authenticated user
- **Responses:**
  - 201: Exercise goal created successfully
  - 400: Invalid input
  - 401: Unauthorized
  - 404: User not found

**Example:**

```bash
curl -X POST https://api.example.com/api/exercise-goals \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
         "exercise_id": 1,
         "target_sets": 4,
         "target_reps": 15,
         "target_duration": "45s",
         "target_distance": "5km"
     }'
```

### Get Single Exercise Goal

- **Endpoint:** `/api/exercise-goals/{exercise_goal_id}`
- **Method:** GET
- **Description:** Retrieve a single exercise goal by ID
- **Responses:**
  - 200: Success
  - 404: Exercise goal not found

**Example:**

```bash
curl -X GET https://api.example.com/api/exercise-goals/1 \
     -H "Authorization: Bearer YOUR_TOKEN"
```

### Update Exercise Goal

- **Endpoint:** `/api/exercise-goals/{exercise_goal_id}`
- **Method:** PUT
- **Description:** Update an existing exercise goal
- **Responses:**
  - 200: Exercise goal updated successfully
  - 400: Invalid input
  - 404: Exercise goal not found

**Example:**

```bash
curl -X PUT https://api.example.com/api/exercise-goals/1 \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
         "target_sets": 5,
         "target_reps": 12,
         "target_duration": "60s",
         "target_distance": "10km"
     }'
```

### Delete Exercise Goal

- **Endpoint:** `/api/exercise-goals/{exercise_goal_id}`
- **Method:** DELETE
- **Description:** Delete an existing exercise goal
- **Responses:**
  - 200: Exercise goal deleted successfully
  - 404: Exercise goal not found

**Example:**

```bash
curl -X DELETE https://api.example.com/api/exercise-goals/1 \
     -H "Authorization: Bearer YOUR_TOKEN"
```

## Fitness Goals Endpoints

### Get Fitness Goal

- **Endpoint:** `/api/fitness-goals`
- **Method:** GET
- **Description:** Get current user's fitness goals
- **Responses:**
  - 200: Fitness Goal retrieved successfully
  - 401: Unauthorized
  - 404: User not found

**Example:**

```bash
curl -X GET https://api.example.com/api/fitness-goals \
     -H "Authorization: Bearer YOUR_TOKEN"
```

### Update Fitness Goal

- **Endpoint:** `/api/fitness-goals`
- **Method:** PUT
- **Description:** Update user fitness goals
- **Responses:**
  - 200: Fitness Goal updated successfully
  - 400: Invalid input data
  - 401: Unauthorized
  - 404: User not found

**Example:**

```bash
curl -X PUT https://api.example.com/api/fitness-goals \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
         "target_weight": 75.0,
         "target_body_fat_percentage": 12.0,
         "target_muscle_mass": 40.0
     }'
```

## Database Schema

```
                                  +---------------------+
                                  |     users           |
                                  +---------------------+
                                  | id (PK)             |
                                  | username (UQ)       |
                                  | password            |
                                  +---------------------+
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  │                                               │
          +---------------------+                        +---------------------+
          |  user_profiles      |                        |  fitness_goals      |
          +---------------------+                        +---------------------+
          | id (PK)             |                        | id (PK)             |
          | user_id (FK)        |                        | user_id (FK)        |
          | current_weight      |                        | target_weight       |
          | height              |                        | target_muscle_mass  |
          | age                 |                        | target_body_fat     |
          | body_fat_percentage |                        +---------------------+
          | muscle_mass         |
          +---------------------+

          +---------------------+                        +---------------------+                   
          | workout_plans       |                        |     exercises       |
          +---------------------+                        +---------------------+
          | id (PK)             |                        | id (PK)             |
          | user_id (FK)        |                        | name (UQ)           |
          | name                |                        | description         |
          | frequency           |                        | instructions        |
          | session_duration    |                        | target_muscles      |
          +---------------------+                        | difficulty          |
                  │                                      +---------------------+
          +---------------------+                                  |
          | selected_exercises  |                                  |
          +---------------------+                        +---------------------+
          | id (PK)             |                        |  exercise_goals     |
          | workout_plan_id FK  |                        +---------------------+
          | exercise_id (FK)    |                        | id (PK)             |
          | sets                |                        | exercise_id (FK)    |
          | reps                |                        | user_id (FK)        |
          | duration            |                        | target_sets         |
          | distance            |                        | target_reps         |
          +---------------------+                        | target_duration     |
                                                         | target_distance     |
                                                         +---------------------+
          +---------------------+
          | workout_sessions    |
          +---------------------+
          | id (PK)             |
          | workout_plan_id FK  |
          | user_id (FK)        |
          | date                |
          | duration            |
          | notes               |
          +---------------------+
    

```

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
