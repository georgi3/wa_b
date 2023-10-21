from rest_framework import serializers
from api.models import WAPhotos, WAGallery


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WAPhotos
        fields = ["image"]


class WAGallerySerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WAGallery
        fields = ["name", "images"]

    def get_images(self, obj):
        images = WAPhotos.objects.filter(gallery__name=obj.name)
        return PhotoSerializer(images, many=True).data
