apps/carts/
├── domain/                     # Pure business logic (dataclasses)
│   ├── __init__.py
│   ├── cart_entity.py
│   └── cart_item_entity.py
│
├── services/                   # Application logic
│   ├── __init__.py
│   └── cart_service.py
│
├── repositories/               # ORM access only
│   ├── __init__.py
│   └── cart_repository.py
│
├── context/                    # Context managers
│   ├── __init__.py
│   └── unit_of_work.py
│
├── views.py                    # Thin DRF layer
├── serializers.py
├── models/
│   ├── cart.py
│   └── cartItem.py
