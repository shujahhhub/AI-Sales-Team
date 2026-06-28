# 🤖 AI Sales Team: Autonomous Microservices Architecture

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.138.0-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B?logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)

An enterprise-grade, fully containerized AI Sales pipeline. This system features an autonomous lead-generation agent, an independent Python/FastAPI backend, and a human-in-the-loop Streamlit approval dashboard, orchestrated entirely via Docker Compose.

---

## 🏗️ System Architecture

This project strictly adheres to a decoupled microservices design pattern to ensure scalability and fault tolerance:

* **🧠 AI Brain (Port 8000):** A FastAPI microservice hosting a Hugging Face LLM. Handles heavy compute and generates highly customized sales pitches based on incoming business data.
* **⚙️ CRM Engine (Port 8001):** A lightweight FastAPI state-machine. Manages the persistent database of leads, enforces business rules, and acts as the secure gateway for the architecture.
* **📊 CEO Dashboard (Port 8501):** A Streamlit frontend application. Dynamically queries the CRM engine to display leads pending human approval.
* **🕵️ Autonomous Agent:** A Python worker script that simulates web scraping, interacts with the AI Brain to generate pitches, and autonomously injects new leads into the CRM queue.

---

## 🚀 Quick Start (Local Deployment)

This architecture is fully containerized. You do not need to configure virtual environments or local Python dependencies.

**Prerequisite:** Ensure Docker and the Docker Compose V2 plugin are installed.

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR_USERNAME/ai-sales-team.git](https://github.com/YOUR_USERNAME/ai-sales-team.git)
cd ai-sales-team
2. Launch the Microservices Fleet

Bash
docker compose up --build
3. Access the Network

Admin Dashboard: http://localhost:8501

AI Brain API Docs: http://localhost:8000/docs

CRM Engine API Docs: http://localhost:8001/docs

-- Triggering the AI Worker
Once the Docker network is online, you can deploy the autonomous agent to generate a lead and push it to your dashboard.

Open a separate terminal and execute:

Bash
python3 ai_agent.py
Wait for the success prompt, then refresh your Streamlit dashboard to approve the newly injected lead.

-- CI/CD Pipeline
This repository implements a Continuous Integration (CI) pipeline via GitHub Actions. Upon every push or pull request to the main branch, an isolated runner automatically provisions a fresh environment and rebuilds the multi-container Docker architecture to prevent regressions before deployment.
