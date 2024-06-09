from rest_framework import serializers

from authapp.models import profiledb


class ProfileModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=11, source='user.username')
  
    class Meta:
        model = profiledb
        fields = ['id','user_id','firstname','lastname','username','wellid','Email','address1','phone1','job','address2','phone3','isActive']
        read_only_fields = ['id','user_id']