from rest_framework import serializers
from .models import Banner, PopularDirection, Category, SubCategory

class BannerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['language', 'image', 'title', 'slug','description']

class PopularDirectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = PopularDirection
        fields = ['language', 'name', 'slug', 'image']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['title', 'slug','description']

class CategorySerializers(serializers.ModelSerializer):
    subcategory = SubCategorySerializer(many=True)
    class Meta:
        model = Category
        fields = ['language', 'title','slug', 'subcategory']