from django.shortcuts import render
from rest_framework import viewsets, permissions
from api.models import User, Entry
from api.serializers import UserSerializer, EntrySerializer
from rest_framework.response import Response
from rest_framework.decorators import action

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
        date = self.request.query_params.get('date')

        if user.role == 'admin':
            queryset = Entry.objects.all()
        elif user.role == 'user_manager':
            queryset = Entry.objects.filter(user__role='regular')
        else:
            queryset = Entry.objects.filter(user=user)
        
        if date:
            queryset = queryset.filter(date=date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def below_expected(self, request):
        user = request.user
        entries = Entry.objects.filter(user=user, is_below_expected=True)
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data)