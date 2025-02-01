CREATE TABLE exercises (
    exercise_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    instructions TEXT,
    target_muscles TEXT,
    difficulty INTEGER);
CREATE TABLE user (
	id INTEGER NOT NULL, 
	public_id VARCHAR(50), 
	name VARCHAR(50), 
	password VARCHAR(90), 
	PRIMARY KEY (id), 
	UNIQUE (public_id)
);
CREATE TABLE workout_plan_final (
	id INTEGER NOT NULL, 
	user_id VARCHAR(50) NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	frequency VARCHAR(50), 
	goal VARCHAR(255), 
	session_duration INTEGER, 
	selected_exercises VARCHAR(5000), 
	PRIMARY KEY (id)
);
CREATE TABLE exercise_goal (
	id INTEGER NOT NULL, 
	fitness_goal_id INTEGER NOT NULL, 
	exercise_name VARCHAR(255) NOT NULL, 
	current_weight FLOAT, 
	current_reps INTEGER, 
	target_weight FLOAT, 
	target_reps INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(fitness_goal_id) REFERENCES fitness_goal (id)
);
CREATE TABLE fitness_goals_final (
	id INTEGER NOT NULL, 
	user_id VARCHAR(50) NOT NULL, 
	current_weight FLOAT NOT NULL, 
	weight_goal FLOAT NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE token_blacklist (
	id INTEGER NOT NULL, 
	token_id VARCHAR(255) NOT NULL, 
	user_id VARCHAR(50) NOT NULL, 
	blacklisted_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (token_id)
);
CREATE TABLE workout_session (
	id INTEGER NOT NULL, 
	user_id VARCHAR(50) NOT NULL, 
	workout_plan_id INTEGER NOT NULL, 
	exercise_name VARCHAR(255) NOT NULL, 
	sets INTEGER, 
	reps INTEGER, 
	completed BOOLEAN, 
	rest_time INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (id)
);
