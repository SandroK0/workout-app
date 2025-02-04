CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
CREATE TABLE exercises (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	description TEXT, 
	instructions TEXT, 
	target_muscles VARCHAR(255), 
	difficulty INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(50) NOT NULL, 
	password VARCHAR(90) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username)
);
CREATE TABLE workout_plans (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	frequency VARCHAR(50), 
	session_duration INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);
CREATE INDEX ix_workout_plans_user_id ON workout_plans (user_id);
CREATE TABLE selected_exercises (
	id INTEGER NOT NULL, 
	workout_plan_id INTEGER NOT NULL, 
	exercise_id INTEGER NOT NULL, 
	sets INTEGER, 
	reps INTEGER, 
	duration VARCHAR(100), 
	distance VARCHAR(100), 
	PRIMARY KEY (id), 
	FOREIGN KEY(exercise_id) REFERENCES exercises (id) ON DELETE CASCADE, 
	FOREIGN KEY(workout_plan_id) REFERENCES workout_plans (id) ON DELETE CASCADE
);
CREATE INDEX ix_selected_exercises_exercise_id ON selected_exercises (exercise_id);
CREATE INDEX ix_selected_exercises_workout_plan_id ON selected_exercises (workout_plan_id);
CREATE TABLE workout_sessions (
	id INTEGER NOT NULL, 
	workout_plan_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	date DATETIME NOT NULL, 
	duration INTEGER NOT NULL, 
	notes TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	FOREIGN KEY(workout_plan_id) REFERENCES workout_plans (id) ON DELETE CASCADE
);
CREATE INDEX ix_workout_sessions_user_id ON workout_sessions (user_id);
CREATE INDEX ix_workout_sessions_workout_plan_id ON workout_sessions (workout_plan_id);
CREATE TABLE IF NOT EXISTS "exercise_goals" (
	id INTEGER NOT NULL, 
	target_sets INTEGER NOT NULL, 
	target_reps INTEGER NOT NULL, 
	target_duration VARCHAR(50), 
	target_distance VARCHAR(50), 
	exercise_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_exercise_goals_exercise_id FOREIGN KEY(exercise_id) REFERENCES exercises (id) ON DELETE CASCADE, 
	CONSTRAINT fk_exercise_goals_user_id FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);
CREATE INDEX ix_exercise_goals_exercise_id ON exercise_goals (exercise_id);
CREATE INDEX ix_exercise_goals_user_id ON exercise_goals (user_id);
CREATE TABLE IF NOT EXISTS "user_profiles" (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	current_weight FLOAT, 
	height FLOAT, 
	age INTEGER, 
	body_fat_percentage FLOAT, 
	muscle_mass FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);
CREATE INDEX ix_user_profiles_user_id ON user_profiles (user_id);
CREATE TABLE fitness_goals (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	target_weight FLOAT, 
	target_muscle_mass FLOAT, 
	target_body_fat_percentage FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);
CREATE INDEX ix_fitness_goals_user_id ON fitness_goals (user_id);
