from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailSerializer
from .services import send_email_with_brevo

class SendSelectionEmailView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "error",
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            recipients_count = send_email_with_brevo(
                name=serializer.validated_data['name'],
                education=serializer.validated_data['education'],
                contact=serializer.validated_data['contact'],
                address=serializer.validated_data['address'],
                project_idea=serializer.validated_data['project_idea'],
                screenshot=serializer.validated_data['screenshot'],
                recipients=serializer.validated_data['recipients']
            )
            
            return Response({
                "status": "success",
                "message": f"Email sent to {recipients_count} recipients"
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)