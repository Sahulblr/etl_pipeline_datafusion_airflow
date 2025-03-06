from faker import Faker
import pandas as pd
from google.cloud import storage


# Initialize Faker
fake = Faker('en_US')

# Function to generate employee data
def generate_employee_data(num_employees):
    employees = []
    for i in range(1, num_employees + 1):
        employee = {
            "Employee ID": i,
            "First Name": fake.first_name(),
            "Last Name": fake.last_name(),
            "Email": fake.unique.email(),
            "Phone Number": fake.phone_number(),
            "Address": fake.address().replace("\n", ", "),
            "Job Title": fake.job(),
            "Salary": fake.random_int(min=30000, max=150000),
            "Date of Birth": fake.date_of_birth(minimum_age=18, maximum_age=65).strftime('%Y-%m-%d'),
            "SSN": "XXX-XX-" + fake.ssn().split("-")[2],  # Masked SSN
            "Hire Date": fake.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d')
        }
        employees.append(employee)
    return employees

# Number of employees to generate
num_employees = 100

# Generate employee data
employee_data = generate_employee_data(num_employees)

# Convert to DataFrame
df = pd.DataFrame(employee_data)

# Save to CSV
csv_file = "employee_data.csv"
df.to_csv(csv_file, index=False)

print(f"CSV file '{csv_file}' generated successfully.")

# --- Upload to GCS ---
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the Google Cloud Storage bucket."""
    # Initialize a storage client
    storage_client = storage.Client()
    
    # Get the bucket
    bucket = storage_client.bucket(bucket_name)
    
    # Create a blob (file) inside the bucket
    blob = bucket.blob(destination_blob_name)
    
    # Upload file
    blob.upload_from_filename(source_file_name)
    
    print(f"File {source_file_name} uploaded to {bucket_name}/{destination_blob_name}")

# Replace with your GCS bucket name
GCS_BUCKET_NAME = "bkt-employee-data0"

# Upload the file to GCS
upload_to_gcs(GCS_BUCKET_NAME, csv_file, f"data/{csv_file}")
