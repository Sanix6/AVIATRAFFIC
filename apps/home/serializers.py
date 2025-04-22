from rest_framework import serializers
from .models import Banner, PopularDirection, Information, SubInformation, FAQ

class BannerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['language', 'image', 'title', 'slug','description']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class PopularDirectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = PopularDirection
        fields = ['language', 'name', 'slug', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class SubInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubInformation
        fields = ['title', 'slug','description']

class InformationSerializers(serializers.ModelSerializer):
    subinfo = SubInfoSerializer(many=True)
    class Meta:
        model = Information
        fields = ['language', 'title', 'img','slug', 'subinfo']

    def get_img(self, obj):
        request = self.context.get('request')
        if obj.img and request:
            return request.build_absolute_uri(obj.img.url)
        return None


class FAQAnswersSerializers(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['answer']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['language','slug', 'question']