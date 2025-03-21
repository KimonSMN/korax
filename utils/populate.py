import sqlite3
from faker import Faker
import random

def populate_database(num_entries=1000):
    """Populates the database with random patients if it's empty."""
    fake = Faker()
    conn = sqlite3.connect("database.db")
    curr = conn.cursor()

    # 🛠️ **Ensure the table exists BEFORE querying**
    curr.execute("""CREATE TABLE IF NOT EXISTS patients (
                    amka INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    surname TEXT,
                    father TEXT,
                    age INTEGER,
                    address TEXT,
                    allergies TEXT,
                    medications TEXT
                );""")
    conn.commit()  # ✅ Commit the table creation to avoid errors

    # ✅ Now check if the table has records
    curr.execute("SELECT COUNT(*) FROM patients")
    count = curr.fetchone()[0]

    if count >= num_entries:
        print(f"✅ Database already contains {count} patients. Skipping population.")
        conn.close()
        return

    print(f"⚡ Populating database with {num_entries} random patients...")
    for _ in range(num_entries):
        name = fake.first_name()
        surname = fake.last_name()
        father = fake.first_name_male()
        age = random.randint(1, 100)
        address = fake.address().replace("\n", ", ")
        amka = "".join([str(random.randint(0, 9)) for _ in range(11)])
        allergies = fake.sentence(nb_words=5) if random.random() > 0.5 else ""
        medications = fake.sentence(nb_words=5) if random.random() > 0.5 else ""

        curr.execute("INSERT INTO patients (amka, name, surname, father, age, address, allergies, medications) "
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                     (amka, name, surname, father, age, address, allergies, medications))

    conn.commit()
    conn.close()
    print(f"✅ Successfully inserted {num_entries} random patients!")