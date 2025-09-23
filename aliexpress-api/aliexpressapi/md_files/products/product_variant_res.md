Handled by
ProductVariantViewSet.list
GET /api/v1/products/{product_pk}/variants/
Response (200) 

{
  "status": "success",
  "message": "Product variants retrieved successfully.",
  "data": {
    "items": [
      {
        "id": "0eeb4485-ef1e-4cc8-9ce6-347d37e3d435",
        "product": "557897ff-e7af-4bbc-8b87-b34eed0a7e1a",
        "sku": "SKU-12345",
        "price": "1999.00",
        "discount_price": "1499.00",
        "stock": 42,
        "currency": "USD",
        "image": "http://localhost:8000/media/variants/v1.png",
        "is_active": true,
        "created_at": "2025-09-19T10:12:33Z",
        "updated_at": "2025-09-19T10:12:33Z"
      }
    ],
    "pagination": {}
  }
}



2. Retrieve single variant
GET /api/v1/products/{product_pk}/variants/{variant_pk}/
ProductVariantViewSet.retrieve

Response (200)

{
  "status": "success",
  "message": "Product variant retrieved successfully.",
  "data": {
    "id": "0eeb4485-ef1e-4cc8-9ce6-347d37e3d435",
    "product": "557897ff-e7af-4bbc-8b87-b34eed0a7e1a",
    "sku": "SKU-12345",
    "price": "1999.00",
    "discount_price": "1499.00",
    "stock": 42,
    "currency": "USD",
    "image": "http://localhost:8000/media/variants/v1.png",
    "is_active": true,
    "created_at": "2025-09-19T10:12:33Z",
    "updated_at": "2025-09-19T10:12:33Z"
  }
}
