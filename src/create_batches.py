"""
Generates a set of csv files to be used for batch email sending.

Each csv file contains a number of email adresses defined by BATCH_SIZE.
"""

import csv
import os
import sys

BATCH_ROOT_DIR = "batches"
BATCH_SIZE = 20

def main():
  if len(sys.argv) < 2 or len(sys.argv) > 3:
    print(f"\nUsage: {sys.argv[0]} <email_input_file.csv> [email_exclusions.csv]\n")
    exit(1)

  patients = get_patients(sys.argv[1])
  exclusions = get_exclusions(sys.argv)

  generate_batches(patients, exclusions)

def ensure_dir_exists(dir_name):
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)

def get_patients(source):
    patients = []
    previous_emails = set()
    with open(source, newline='') as input_file:
      email_reader = csv.reader(input_file)
      for row in email_reader:
        first_name = row[1].capitalize()
        last_name = row[2].capitalize()
        email = row[-1].strip().lower()
        if email not in previous_emails:
          patients.append((last_name, first_name, email))
          previous_emails.add(email)
        else:
          print(f"Skipping patient {first_name} {last_name}, email already exists: {email}")

    return sorted(patients, key=lambda patient: patient[0])

def get_exclusions(args):
  exclusions = []
  if (len(args) == 3):
    exclusions_source = args[2]
    with open(exclusions_source, newline='') as input_file:
      email_reader = csv.reader(input_file)
      for row in email_reader:
        exclusions.extend(row)
  
  if exclusions:
    print(f"Excluding emails: {exclusions}")    
  else:
    print("Including all emails...")

  return exclusions

def generate_batches(patients, exclusions):
  batch_number = 1
  names = []
  emails = []
  for patient in patients:
    if patient[2] in exclusions:
      print(f"Skipping patient {patient[1]} {patient[0]} from batch {batch_number}")
    else:
      # Add email to current batch...
      if len(emails) < BATCH_SIZE:
        names.append((patient[0], patient[1]))
        emails.append(patient[2])
      else:
        # Reached batch size..
        # create_batch_file(f"{BATCH_DIR}/batch{batch_number}", emails)
        create_files(f"batch{batch_number}", names, emails)
        batch_number += 1
        emails.clear()
        names.clear()

  if emails:
    # Include last set of emails, which may be less than batch size
    # create_batch_file(f"{BATCH_DIR}/batch{batch_number}", emails)
    create_files(f"batch{batch_number}", names, emails)
      

def create_files(batch_dir, names, emails):
  ensure_dir_exists(BATCH_ROOT_DIR)
  dir_path = f"{BATCH_ROOT_DIR}/{batch_dir}"
  ensure_dir_exists(dir_path)
  
  create_names_file(f"{dir_path}/names.txt", names)
  create_emails_file(f"{dir_path}/emails.csv", emails)

def create_names_file(file_name, names):
  with open(file_name, 'w', encoding='utf-8') as name_file:
    for name in names:
      print(name)
      name_file.write(f"{name[0]}, {name[1]}\n")

def create_emails_file(file_name, emails):
    with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
      csv_writer = csv.writer(csv_file)
      csv_writer.writerow(emails)

if __name__ == "__main__":
  main()
    