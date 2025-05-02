# Django Email API with Brevo Integration

A REST API for sending HTML emails with embedded images using Django REST Framework and Brevo (formerly SendinBlue).

## Features

- Send multipart emails with embedded images
- Support for multiple email providers (Gmail, hotmail, Yahoo, careers@accelx.net.)
- Image optimization and validation
- Recipient domain validation
- Base64 embedding strategy

## Prerequisites

- Python 3.10+
- Django 4.2+
- Brevo API account ([sign up here](https://www.brevo.com/))

## Setup Instructions

### 1. Clone the repository


git clone https://github.com/Abdullah-Al-Fahad/email_api.git


### 3. Install dependencies


pip install -r requirements.txt


### 4. Configure environment variables

Create a .env file based on the example:


cp .env.example .env


Edit the .env file with your credentials:


BREVO_API_KEY=keygoeshere
FROM_EMAIL=youremail
FROM_NAME=AccelX Careers

### 5. Run migrations


python manage.py migrate


### 6. Start the development server


python manage.py runserver


## API Documentation

### Endpoint

POST /api/send-selection-email/

### Request Format (multipart/form-data)

| Field        | Type     | Required | Description                          |
|--------------|----------|----------|--------------------------------------|
| name         | string   | Yes      | Candidate's full name                |
| education    | string   | Yes      | Education information                |
| contact      | string   | Yes      | Phone number                         |
| address      | string   | Yes      | Current address                      |
| project_idea | string   | Yes      | Description of project idea          |
| screenshot   | file     | Yes      | GitHub profile screenshot (jpg/png)  |
| recipients   | string[] | Yes      | List of email addresses              |

### Example cURL Request


curl -X POST 
  http://localhost:8000/api/send-selection-email/ 
  -H 'Content-Type: multipart/form-data' 
  -F 'name=John Doe' 
  -F 'education=BSc Computer Science' 
  -F 'contact=+1234567890' 
  -F 'address=123 Main St, City' 
  -F 'project_idea=AI email classifier'
  -F 'screenshot=@screenshot.png' 
  -F 'recipients=test@gmail.com' 
  -F 'recipients=careers@accelx.net'


### Response Examples

**Success:**

{
  "status": "success",
  "message": "Email sent to 2 recipients"
}


**Error:**

{
  "status": "error",
  "message": "Invalid recipient domains detected"
}
