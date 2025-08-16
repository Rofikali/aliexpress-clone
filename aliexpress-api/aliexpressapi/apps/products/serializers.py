# from rest_framework.serializers import ModelSerializer
# from .models import Products
# from django.conf import settings


# class ProductSerializer(ModelSerializer):
#     class Meta:
#         model = Products
#         fields = ["title", "description", "price", "image", "created_at", "updated_at"]

#         read_only_fields = ["created_at", "updated_at"]
#         # Ensure the request context is passed to the serializer
#         extra_kwargs = {
#             "image": {"required": True, "allow_null": True},
#             "description": {"required": True, "allow_blank": True},
#         }
#         # This allows the serializer to handle the request context properly

#         depth = 1  # Adjust the depth as needed for nested relationships

#     # def to_representation(self, instance):
#     #     representation = super().to_representation(instance)
#     #     # Custom representation logic can be added here if needed
#     #     return representation

#     def get_image(self, obj):

#         """
#         Returns the full URL of the image if it exists, otherwise returns None.
#         """
#         request = self.context.get("request")

#         if hasattr(obj, "image") and obj.image and hasattr(obj.image, "url"):
#             # print(f"[DEBUG] Image field is present and has URL: {obj.image}")
#             try:
#                 image_url = obj.image.url
#                 # print(f"[DEBUG] Image URL resolved: {image_url}")
#                 full_url = (
#                     request.build_absolute_uri(image_url)
#                     if request
#                     else f"{settings.MEDIA_URL}{image_url}"
#                 )
#                 # print(f"[DEBUG] Final image URL: {full_url}")
#                 return full_url
#             except ValueError as e:
#                 print(f"[ERROR] No image file for user {obj.id}: {e}")
#             except Exception as e:
#                 print(f"[ERROR] Unexpected error for user {obj.id}: {e}")
#         else:
#             print(
#                 f"[WARNING] User {obj.id} has no image or image has no associated file (empty or missing)."
#             )

#         return None


from rest_framework import serializers
from django.conf import settings
from .models import Products, ProductImages


class ProductImagesSerialzers(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = [
            "id",
            "product_id",
            "img_name",
            # "created_at",
            # "updated_at",
        ]
        # read_only_fields = ["created_at", "updated_at"]
        


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    images = ProductImagesSerialzers(many=True, source='product_images')

    class Meta:
        model = Products
        fields = [
            "id",
            "title",
            "description",
            "price",
            "image",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {
            "image": {"required": True, "allow_null": True},
            "description": {"required": True, "allow_blank": True},
        }

    def get_image(self, obj):
        """
        Returns the absolute image URL if available, otherwise None.
        """
        if not obj.image:
            return None

        try:
            request = self.context.get("request")
            image = obj.image.url
            # image_url = obj.image.url

            if request:
                return request.build_absolute_uri(image)
            return f"{settings.MEDIA_URL}{image.lstrip('/')}"
        except Exception:
            # Optional: log the error if you have logging set up
            # logger.warning(f"Image URL error for product {obj.pk}: {e}")
            return None
