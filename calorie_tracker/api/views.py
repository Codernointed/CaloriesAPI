from rest_framework import viewsets, permissions
from api.models import User, Entry
from api.serializers import UserSerializer, EntrySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action == 'list':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated()]


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Entry.objects.all()
        elif user.role == 'user_manager':
            return Entry.objects.filter(user__role='regular')
        else:
            return Entry.objects.filter(user=user)
