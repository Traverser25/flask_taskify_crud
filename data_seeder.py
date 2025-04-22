import requests
import random
from faker import Faker

#i made this to  add random task and to test

fake = Faker()

# Base URLs
REGISTER_URL = "http://127.0.0.1:3000/api/auth/register"
LOGIN_URL = "http://127.0.0.1:3000/api/auth/login"
ADD_TASK_URL = "http://127.0.0.1:3000/api/add_task"

users = []

print("📦 Registering 50 users...")
# Step 1: Register 50 users
for i in range(1):
    email = f"user{i}@test.com"
    password = "testpass123"
    username = f"user{i}"

    res = requests.post(REGISTER_URL, json={
        "email": email,
        "password": password,
        "username": username
    })

    if res.status_code == 201:
        print(f"✅ Registered: {username}")
    else:
        print(f"❌ Failed to register: {username} | {res.status_code} | {res.text}")

    users.append({
        "email": email,
        "password": password,
        "username": username,
        "id": i + 1  # Storing the user ID for later assignment
    })

print("\n🔑 Logging in users...")
# Step 2: Login each user and store token
for user in users:
    login_res = requests.post(LOGIN_URL, json={
        "email": user["email"],
        "password": user["password"]
    })

    login_json = login_res.json()
    token = login_json.get("data", {}).get("token")

    if token:
        user["token"] = token
        print(f"✅ Logged in: {user['username']}")
    else:
        print(f"❌ Login failed for {user['email']} | {login_res.text}")

print("\n📝 Creating 100 tasks...")
# Step 3: Add 100 random tasks using random users
task_count = 0
for user in users:
    if "token" not in user:
        continue

    headers = {
        "Authorization": f"Bearer {user['token']}"
    }

    for _ in range(random.randint(5)):  # 50 users × 2 = 100 tasks
        assignee = random.choice([u for u in users if u["id"] != user["id"]])  # Choose a different user ID

        task_payload = {
            "title": fake.sentence(nb_words=6),
            "description": fake.paragraph(nb_sentences=2),
            "due_date": fake.future_date().isoformat(),
            "priority": random.choice([1, 2]),
            "status": random.choice([1, 2, 3, 4]),
            "assigned_to": assignee["id"]  # Assign by user ID, not username
        }

        task_res = requests.post(ADD_TASK_URL, json=task_payload, headers=headers)

        if task_res.status_code == 201:
            task_count += 1
            print(f"✅ Task #{task_count} added by {user['username']} -> assigned to User #{assignee['id']}")
        else:
            print(f"❌ Failed to create task by {user['username']} | {task_res.status_code} | {task_res.text}")

print(f"\n🎉 Finished creating {task_count} tasks.")
