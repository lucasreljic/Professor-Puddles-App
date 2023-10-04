# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SendFrameAPIView(APIView):
    def post(self, request, *args, **kwargs):
        frame_base64 = request.data.get('frame')

        if not frame_base64:
            return Response({'error': 'Frame data is missing.'}, status=status.HTTP_400_BAD_REQUEST)

        # You can process the frame data here if needed

        return Response({'message': 'Frame received successfully.'}, status=status.HTTP_200_OK)
