import csv
from app import create_app, db
from app.models import Exercises

# Create the Flask app and database context
app = create_app()
app.app_context().push()

# Path to the CSV file
CSV_FILE_PATH = 'exercises.csv'


def load_exercises_from_csv(file_path):
    """
    Load data from a CSV file and insert it into the Exercises table.
    """
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Create a new Exercises object
            exercise = Exercises(
                name=row['name'],
                description=row['description'],
                instructions=row['instructions'],
                target_muscles=row['target_muscles'],
                difficulty=int(row['difficulty'])
            )
            # Add the object to the session
            db.session.add(exercise)

        # Commit the session to save the data to the database
        db.session.commit()

    print(f"Data from {file_path} has been successfully loaded into the Exercises table.")


if __name__ == '__main__':
    load_exercises_from_csv(CSV_FILE_PATH)
