"""Contact API view — POST only."""

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import ContactMessageSerializer


class ContactMessageCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"detail": "Message sent successfully."},
            status=status.HTTP_201_CREATED,
        )
