from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    education = serializers.CharField(required=True)
    contact = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    project_idea = serializers.CharField(required=True)
    screenshot = serializers.ImageField(required=True)
    recipients = serializers.ListField(
        child=serializers.EmailField(),
        required=True
    )
    
    def validate_recipients(self, value):
        allowed_domains = ['gmail.com', 'hotmail.com', 'yahoo.com', 'accelx.net']
        invalid_emails = []
        
        for email in value:
            domain = email.split('@')[-1].lower()
            if domain not in allowed_domains and email.lower() != 'careers@accelx.net':
                invalid_emails.append(email)
        
        if invalid_emails:
            raise serializers.ValidationError(
                f"Only Gmail, Hotmail, Yahoo, and careers@accelx.net are allowed. Invalid emails: {', '.join(invalid_emails)}"
            )
        return value