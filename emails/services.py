import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
import base64
import os

def validate_recipients(recipients):
    allowed_domains = ['gmail.com', 'hotmail.com', 'yahoo.com', 'accelx.net']
    valid_recipients = []
    
    for email in recipients:
        domain = email.split('@')[-1].lower()
        if domain in allowed_domains or email.lower() == 'careers@accelx.net':
            valid_recipients.append(email)
    
    return valid_recipients

def send_email_with_brevo(name, education, contact, address, project_idea, screenshot, recipients):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    # Validate recipients
    valid_recipients = validate_recipients(recipients)
    if not valid_recipients:
        raise ValueError("No valid recipients found. Only Gmail, Hotmail, Yahoo, and careers@accelx.net are allowed")
    
    # Read and encode the image file
    screenshot_data = screenshot.read()
    encoded_image = base64.b64encode(screenshot_data).decode('utf-8')
    
    # Get the image content type based on file extension
    file_extension = os.path.splitext(screenshot.name)[1].lower()
    content_type = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif'
    }.get(file_extension, 'image/png')  # default to png if unknown
    
    # Prepare HTML content with embedded image as data URL
    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f4f4f4; padding: 10px; text-align: center; }}
                .info {{ margin: 20px 0; }}
                .image-container {{ text-align: center; margin: 20px 0; }}
                .project-idea {{ background-color: #f9f9f9; padding: 15px; border-left: 4px solid #ccc; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Python Backend Engineer Candidate Information</h2>
                </div>
                
                <div class="info">
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Education:</strong> {education}</p>
                    <p><strong>Contact:</strong> {contact}</p>
                    <p><strong>Address:</strong> {address}</p>
                </div>
                
                <div class="image-container">
                    <p><strong>GitHub Profile Screenshot:</strong></p>
                    <img src="data:{content_type};base64,{encoded_image}" alt="GitHub Screenshot" style="max-width: 100%; height: auto;">
                </div>
                
                <div class="project-idea">
                    <h3>Project Idea</h3>
                    <p>{project_idea}</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    # Prepare the email
    subject = f"Python Backend Engineer Selection Task - {name}"
    sender = {"name": settings.FROM_NAME, "email": settings.FROM_EMAIL}
    to = [{"email": email} for email in valid_recipients]
    
    # Create email 
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        html_content=html_content,
        sender=sender,
        subject=subject
    )
    
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return len(valid_recipients)
    except ApiException as e:
        raise Exception(f"Exception when calling SMTPApi->send_transac_email: {e}")