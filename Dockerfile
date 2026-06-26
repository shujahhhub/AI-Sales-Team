# 1. Start with a lightweight, blank Linux server that has Python pre-installed
FROM python:3.12-slim

# 2. Create a folder inside the container to hold our company code
WORKDIR /app

# 3. Copy the "recipe" we just made into the container
COPY requirements.txt .

# 4. Tell the container to install everything in the recipe
# (We use --default-timeout to prevent the PyTorch download from failing!)
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# 5. Copy all of your actual Python files (app.py, crm_api.py, dashboard.py) into the container
COPY . .

# NOTE: We are intentionally leaving the "start" command blank here, 
# because we will use Docker Compose to start all 3 files simultaneously!