# All Products Response

{
  "success": true,
  "code": 200,
  "message": "Products fetched successfully (cache)",
  "request": {
    "id": "2d5e292b-0c39-411f-a60d-ce50e6fa8f57",
    "timestamp": "2025-09-09T08:14:06.011532Z",
    "latency_ms": 0.13,
    "region": "Nepal-01",
    "cache": "HIT"
  },
  "meta": {
    "next_cursor": "cD0yMDI1LTA5LTA3KzA5JTNBMTElM0EyMS4yNTI0NTclMkIwMCUzQTAw",
    "has_next": true
  },
  "errors": null,
  "data": [
    {
      "id": "574ac81c-3eb2-4173-b048-68472c501952",
      "title": "Street range",
      "description": "Total now large learn these marriage rich its. Stand thank type state. Performance class fact speech.",
      "price": "479.33",
      "image": "http://localhost:8000/media/products/images/picture-participant.jpg",
      "images": [
        {
          "id": 2246,
          "product": "574ac81c-3eb2-4173-b048-68472c501952",
          "image": "http://localhost:8000/media/products/images/picture-participant-1.jpg"
        },
      ],
      "category": {
        "id": 1,
        "name": "Default Category",
        "description": "Auto-created default category"
      },
      "brand": {
        "id": 1,
        "name": "Default Brand",
        "description": "Auto-created default brand"
      },
      "created_at": "2025-09-07T09:11:21.497504Z",
      "updated_at": "2025-09-07T11:24:36.017785Z"
    },

  ]
}

# Single Product Response

{
  "success": true,
  "code": 200,
  "message": "Single Product fetched successfully",
  "request": {
    "id": "546306ea-c907-4021-9c8e-c22b1efd6bc2",
    "timestamp": "2025-09-11T05:37:09.181412Z",
    "latency_ms": 0.05,
    "region": "Nepal-01",
    "cache": "MISS"
  },
  "meta": {},
  "errors": null,
  "data": {
    "id": "753c1017-2735-42a6-afab-5d771cbc70a7",
    "title": "Before student none",
    "description": "Hot style newspaper citizen hour. Quite over future rock.\nSet already American movie. Political rich probably once somebody raise job performance.",
    "price": "317.26",
    "image": "<http://localhost:8000/media/products/images/of-religious.jpg>",
    "images": [
      {
        "id": 246,
        "product": "753c1017-2735-42a6-afab-5d771cbc70a7",
        "image": "http://localhost:8000/media/products/images/of-religious-1.jpg"
      },
      {
        "id": 247,
        "product": "753c1017-2735-42a6-afab-5d771cbc70a7",
        "image": "http://localhost:8000/media/products/images/of-religious-2.jpg"
      },
      {
        "id": 248,
        "product": "753c1017-2735-42a6-afab-5d771cbc70a7",
        "image": "http://localhost:8000/media/products/images/of-religious-3.jpg"
      },
      {
        "id": 249,
        "product": "753c1017-2735-42a6-afab-5d771cbc70a7",
        "image": "http://localhost:8000/media/products/images/of-religious-4.jpg"
      },
      {
        "id": 250,
        "product": "753c1017-2735-42a6-afab-5d771cbc70a7",
        "image": "http://localhost:8000/media/products/images/of-religious-5.jpg"
      }
    ],
    "category": {
      "id": 1,
      "name": "Default Category",
      "description": "Auto-created default category"
    },
    "brand": {
      "id": 1,
      "name": "Default Brand",
      "description": "Auto-created default brand"
    },
    "created_at": "2025-09-06T05:53:01.782086Z",
    "updated_at": "2025-09-06T05:53:01.790535Z"
  }
}

# error layers

{
  "success": false,
  "code": 400,
  "message": "Validation failed",
  "request": {
    "id": "d70b2330-c7c3-4e21-a2d7-1bfde448c735",
    "timestamp": "2025-09-09T08:18:40.915393Z",
    "latency_ms": 0.13,
    "region": "Nepal-01",
    "cache": "MISS"
  },
  "meta": {},
  "errors": [
    {
      "code": "USERNAME",
      "message": "user with this username already exists."
    },
    {
      "code": "EMAIL",
      "message": "Enter a valid email address."
    },
    {
      "code": "PHONE_NUMBER",
      "message": "Enter a valid phone number (digits only, 7-15)."
    },
    {
      "code": "PASSWORD",
      "message": "Ensure this field has at least 8 characters."
    },
    {
      "code": "ROLE",
      "message": "\"b\" is not a valid choice."
    }
  ],
  "data": null
}
