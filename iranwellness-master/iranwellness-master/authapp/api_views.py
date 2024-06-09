from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from index.custom_drf_permissions import *

from django.contrib.auth.models import User
from .models import *

from .serializers import *


class ProfileAPIViewset(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    required_groups = [u'manager']
    queryset = profiledb.objects.all()
    serializer_class = ProfileModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        self.permission_classes =  [IsSuperUser|GroupBasePermission]
        if (self.action == 'create'):
            self.permission_classes = [IsAuthenticated]
        elif (self.action == 'retrieve'):
            self.permission_classes = [IsSuperUser|GroupBasePermission|IsObjectOwner]
        return super(self.__class__, self).get_permissions()

    def get_object(self):
        username = self.kwargs['username']
        obj=get_object_or_404(profiledb, user__username=username)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
    
    def perform_create(self, serializer):
        ## update user
        validated_username = serializer.data['username']
        if ( validated_username != self.request.user.username ):
            self.request.user.username = validated_username
            self.request.user.save()
        ## update or create profile
        profile_data = serializer.data
        profile_data.pop('username')
        profile_instance, created_profile = profiledb.objects.update_or_create(user=user_instance, defaults=profile_data)

    @action(detail=False, methods=['post'])
    def super_create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ## update or create user
        validated_username = serializer.data['username']
        user_instance, created_user = User.objects.update_or_create(username=validated_username)
        ## update or create profile
        profile_data = serializer.data
        profile_data.pop('username')
        profile_instance, created_profile = profiledb.objects.update_or_create(user=user_instance, defaults=profile_data)
        ## return data
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

