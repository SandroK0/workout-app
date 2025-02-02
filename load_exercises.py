import csv
import os
from app.models import Exercises
from app import create_app, db

# Create the Flask app and database context
app = create_app()
app.app_context().push()

# Path to the CSV file
CSV_FILE_PATH = 'exercises.csv'

def load_exercises_from_csv(file_path):
    """
    Load data from a CSV file and insert it into the Exercises table.
    Handles errors and checks for existing entries.
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found at {file_path}")

        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Check required columns
            required_columns = ['name', 'difficulty']
            for col in required_columns:
                if col not in reader.fieldnames:
                    raise ValueError(f"Missing required column: {col}")

            exercises_data = []
            existing_count = 0
            new_count = 0

            for row in reader:
                # Check if exercise already exists
                if Exercises.query.filter_by(name=row['name']).first():
                    existing_count += 1
                    continue

                # Validate difficulty
                try:
                    difficulty = int(row['difficulty'])
                    if not (1 <= difficulty <= 3):
                        raise ValueError("Difficulty must be between 1 and 5")
                except ValueError:
                    print(f"Invalid difficulty value for {row['name']}: {row['difficulty']}")
                    continue

                exercises_data.append({
                    'name': row['name'],
                    'description': row.get('description', ''),
                    'instructions': row.get('instructions', ''),
                    'target_muscles': row.get('target_muscles', ''),
                    'difficulty': difficulty
                })

                new_count += 1

            # Bulk insert in batches
            if exercises_data:
                db.session.bulk_insert_mappings(Exercises, exercises_data)
                db.session.commit()

            print(f"Successfully added {new_count} new exercises")
            print(f"Skipped {existing_count} duplicate exercises")

    except Exception as e:
        db.session.rollback()
        print(f"Error loading exercises: {str(e)}")
        raise

if __name__ == '__main__':
    try:
        load_exercises_from_csv(CSV_FILE_PATH)
        print("Exercise loading process completed successfully!")
    except Exception as e:
        print(f"Failed to load exercises: {str(e)}")