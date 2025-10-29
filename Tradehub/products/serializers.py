from rest_framework import serializers
from . models import Product, category


class Categoryserializer(serializers.ModelSerializer):

    class Meta:
        model = category
        fields = ["id", "name", "slug"]

class Productserializer(serializers.ModelSerializer):
    category = Categoryserializer(read_only = True)
    category_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset = category.objects.all(),source ="category",required = False)

    class Meta:
        model = Product
        fields = "__all__"

        read_only_fields = ["id", "created_at", "created_by", "category"]


        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty")
            return value
        
        def validate_price(self, value):
            if value < 0:
                raise serializers.ValidationError("Price must be positive")
            return value
        
        def validate_stock_quantity(self, value):
            if value < 0:
                raise serializers.ValidationError("Stock quantity must be positive")
            return value
        
        def create(self, validated_data):
            user = self.context["request"].user
            validated_data["created_by"] = user if user.is_authenticated else None
            return super().create(validated_data)