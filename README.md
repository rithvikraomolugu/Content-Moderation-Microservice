# Content Moderation Microservice

## Overview
This project implements a rule-based Content Moderation Microservice designed to analyze, classify, and manage user-generated comments using FastAPI and MySQL. The system applies weighted toxicity scoring across multiple severity categories including Violent Threats, Hate Speech, Direct Abuse, Profanity, and Mass Negativity. 

The service provides RESTful endpoints for comment ingestion, automatic classification, persistence, and moderation workflow management (approve/reject lifecycle). The architecture simulates a real-world Trust & Safety backend system used in content platforms.

---

## Objectives
- Build a RESTful backend microservice for automated comment moderation
- Implement weighted toxicity scoring using structured keyword classification
- Categorize comments into severity levels based on risk prioritization
- Persist moderation records using relational database integration
- Implement moderation workflow lifecycle (Pending → Approved / Rejected)
- Provide filtered retrieval of flagged comments for admin review

---

## System Architecture
The microservice follows a backend service architecture:

- **FastAPI** handles REST endpoints and request validation
- **Rule-Based Engine** performs weighted toxicity classification
- **MySQL Database** persists moderation records
- **SQLAlchemy** manages secure parameterized database operations
- Moderation workflow supports lifecycle state transitions

---

## Moderation Model

### Severity Categories
The system classifies comments into the following structured levels:

- **Violent Threat** (Weight: 4)
- **Hate Speech** (Weight: 3)
- **Direct Abuse** (Weight: 2)
- **Profanity** (Weight: 1)
- **Mass Negativity** (Weight: 1)
- **Neutral**

Severity is determined using weighted scoring combined with priority-based categorization logic.

Each comment record includes:
- `toxicity_score`
- `severity_category`
- `is_flagged`
- `moderation_status`

---

## Database Structure

The `content_moderation` database includes:

### comments Table

- `id` (Primary Key)
- `comment` (Text)
- `toxicity_score` (Integer)
- `severity_category` (String)
- `is_flagged` (Boolean)
- `moderation_status` (Pending / Approved / Rejected)
- `created_at` (Timestamp)

The database enables persistent storage and moderation state management.

---

## API Endpoints

### Comment Analysis
- `POST /analyze`
  - Accepts comment text
  - Returns classification result
  - Stores moderation record

### Retrieval
- `GET /comments`
  - Retrieve all stored comments

- `GET /comments/flagged`
  - Retrieve only flagged comments

### Moderation Workflow
- `PUT /comments/{id}/approve`
- `PUT /comments/{id}/reject`

Implements administrative review lifecycle.

---

## Key Features
- Weighted rule-based toxicity engine
- Multi-level severity classification
- Persistent relational storage
- Secure parameterized SQL queries
- Moderation lifecycle management
- RESTful API design with structured validation

---

## Tools Used
- Python
- FastAPI
- MySQL
- SQLAlchemy
- Uvicorn
