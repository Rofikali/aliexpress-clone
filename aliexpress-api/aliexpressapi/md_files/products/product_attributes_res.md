✅ Product Variant Attributes
3. List attributes for a variant (strict)
GET /api/v1/products/{product_pk}/variants/{variant_pk}/attributes/
ProductAttributeViewSet.list

Response (200, cache MISS example)

{
  "status": "success",
  "message": "Product attributes fetched successfully",
  "cache": "MISS",
  "data": {
    "items": [
      {
        "id": "d7a45f87-86f3-4df0-bcf4-9b64d6ff2b5d",
        "name": "Color",
        "sort_order": 1,
        "values": [
          { "id": "1", "attribute": "d7a45f87-86f3-4df0-bcf4-9b64d6ff2b5d", "name": "Red" },
          { "id": "2", "attribute": "d7a45f87-86f3-4df0-bcf4-9b64d6ff2b5d", "name": "Blue" }
        ]
      },
      {
        "id": "83dbf524-04c5-4d9d-8c15-112f24a9d7c9",
        "name": "Size",
        "sort_order": 2,
        "values": [
          { "id": "3", "attribute": "83dbf524-04c5-4d9d-8c15-112f24a9d7c9", "name": "S" },
          { "id": "4", "attribute": "83dbf524-04c5-4d9d-8c15-112f24a9d7c9", "name": "M" },
          { "id": "5", "attribute": "83dbf524-04c5-4d9d-8c15-112f24a9d7c9", "name": "L" }
        ]
      }
    ],
    "pagination": {
      "next": null,
      "previous": null,
      "count": 2
    }
  }
}


4. Retrieve a single attribute for a variant
GET /api/v1/products/{product_pk}/variants/{variant_pk}/attributes/{attribute_pk}/
ProductAttributeViewSet.retrieve

Response (200)

{
  "status": "success",
  "message": "Product attribute fetched successfully",
  "data": {
    "id": "83dbf524-04c5-4d9d-8c15-112f24a9d7c9",
    "name": "Size",
    "sort_order": 2,
    "values": [
      { "id": "3", "attribute": "83dbf524-04c5-4d9d-8c15-112f24a9d7c9", "name": "S" },
      { "id": "4", "attribute": "83dbf524-04c5-4d9d-8c15-112f24a9d7c9", "name": "M" },
      { "id": "5", "attribute": "83dbf524-04c5-4d9d-8c15-112f24a9d7c9", "name": "L" }
    ]
  }
}
