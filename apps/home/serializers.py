from rest_framework import serializers
from .models import Banner, PopularDirection, Information, SubInformation, FAQ
from bs4 import BeautifulSoup
from django.conf import settings
import re
from urllib.parse import urljoin

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
    description = serializers.SerializerMethodField()
    class Meta:
        model = SubInformation
        fields = ['title', 'slug','subject','description']

    def get_description(self, obj):
        domain = self.context['request'].build_absolute_uri('/') 
        pattern = r'src=[\'"](/media[^\'"]+)[\'"]'

        def replacer(match):
            relative_url = match.group(1)
            full_url = urljoin(domain, relative_url.lstrip('/'))
            return f'src="{full_url}"'

        return re.sub(pattern, replacer, obj.description)

class InformationSerializers(serializers.ModelSerializer):
    subinfo = SubInfoSerializer(many=True)
    class Meta:
        model = Information
        fields = ['language', 'title', 'img','slug','background_color', 'subinfo']

    def get_img(self, obj):
        request = self.context.get('request')
        if obj.img and request:
            return request.build_absolute_uri(obj.img.url)
        return None


class FAQAnswersSerializers(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question','answer']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['language','slug', 'question']