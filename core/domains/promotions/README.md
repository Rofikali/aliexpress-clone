🎟️ COUPONS & PROMOTIONS DOMAIN — REVENUE RULES ENGINE

📄 Save as
core/domains/promotions/README.md

📁 FULL PROMOTIONS DOMAIN FOLDER STRUCTURE
core/domains/promotions/
├── README.md                          # Promo philosophy & money rules
│
├── domain/                            # PURE DISCOUNT LOGIC
│   ├── aggregates/
│   │   └── promotion.py               # Aggregate root
│   │
│   ├── entities/
│   │   ├── coupon.py                  # Redeemable code
│   │   ├── promotion_rule.py          # Conditions
│   │   ├── promotion_effect.py        # Discount result
│   │   └── usage_limit.py
│   │
│   ├── value_objects/
│   │   ├── promotion_id.py
│   │   ├── coupon_code.py
│   │   ├── discount_type.py           # %, fixed, BOGO
│   │   ├── discount_value.py
│   │   ├── eligibility_scope.py       # product, seller, cart
│   │   ├── date_range.py
│   │   └── usage_counter.py
│   │
│   ├── policies/                      # 🧠 MONEY SAFETY
│   │   ├── stacking_policy.py
│   │   ├── eligibility_policy.py
│   │   ├── expiration_policy.py
│   │   └── usage_policy.py
│   │
│   ├── services/
│   │   └── discount_calculation_service.py
│   │
│   └── exceptions.py                  # Abuse & invalid states
│
├── application/                       # USE CASES
│   ├── use_cases/
│   │   ├── validate_coupon/
│   │   ├── apply_promotion/
│   │   ├── reserve_coupon_usage/
│   │   ├── confirm_coupon_usage/
│   │   └── release_coupon_usage/
│   │
│   └── ports/
│       ├── inbound/
│       │   ├── validate_coupon_port.py
│       │   └── apply_promotion_port.py
│       │
│       └── outbound/
│           ├── promotion_repository_port.py
│           ├── cart_snapshot_port.py
│           ├── event_publisher_port.py
│           └── usage_counter_port.py
│
├── adapters/                          # FRAMEWORK & INTEGRATION
│   ├── inbound/
│   │   └── rest/
│   │       ├── views.py
│   │       ├── serializers.py
│   │       └── urls.py
│   │
│   └── outbound/
│       ├── persistence/
│       │   ├── models/
│       │   │   ├── promotion_model.py
│   │   │   ├── coupon_model.py
│   │   │   └── usage_model.py
│   │   │
│   │   └── repositories/
│   │       └── django_promotion_repository.py
│       │
│       └── messaging/
│           └── promotion_event_publisher.py
│
├── events/                            # IMMUTABLE FACTS
│   ├── coupon_applied.py
│   ├── coupon_reserved.py
│   ├── coupon_released.py
│   └── coupon_consumed.py
│
├── sagas/                             # LONG-RUNNING PROMO FLOWS
│   └── checkout_promotion_saga.py
│
├── contracts/                         # CROSS-DOMAIN AGREEMENTS
│   ├── events/
│   │   └── coupon_consumed.v1.json
│   │
│   └── apis/
│       └── promotions.v1.yaml
│
├── read_models/                       # FAST PROMO LOOKUPS
│   ├── active_promotions/
│   └── coupon_status/
│
├── jobs/                              # BACKGROUND SAFETY
│   ├── expire_promotions/
│   └── reconcile_usage_counts/
│
├── tests/
│   ├── domain/
│   ├── application/
│   └── adapters/
│
└── __init__.py

🧠 PROMOTION AGGREGATE — MENTAL MODEL
Promotion (Aggregate Root)
│
├── Coupons (optional)
├── Rules (conditions)
├── Effects (discounts)
│
└── Invariants:
    • Cannot exceed usage limits
    • Cannot apply after expiry
    • Cannot stack if forbidden

🔄 PROMOTIONS IN CHECKOUT FLOW
StartCheckout
 → ValidateCoupon
 → ReserveCouponUsage
 → ApplyPromotion


On payment success:

PaymentCaptured
 → ConfirmCouponUsage


On failure:

CheckoutAborted
 → ReleaseCouponUsage

🧨 WHY COUPON RESERVATION IS MANDATORY

❌ Validate only = race conditions
❌ No reservation = abuse
❌ No release = dead limits

Reservation protects:
✔ Limited coupons
✔ Flash sales
✔ Fraud

🔥 STACKING POLICY (CRITICAL)

Defined explicitly:
• Can coupons stack?
• Can promo + coupon stack?
• Max discount cap?

Never implicit.

🧪 TEST STRATEGY
Domain
→ Eligibility
→ Discount math
→ Usage limits

Application
→ Reservation lifecycle

Adapters
→ DB & API

🧭 SAFE REFACTOR PATH
Week 1

✔ Create promotions folders

Week 2

✔ Extract coupon logic

Week 3

✔ Add reservation flow

Week 4

✔ Enforce stacking rules

🚫 PROMOTIONS ANTI-PATTERNS

❌ Discount logic in frontend
❌ Silent stacking
❌ No usage tracking
❌ Cart recalculates price

🧠 PRINCIPAL-LEVEL LAW

Every discount is a business decision.
Treat promotions like money leaving your system.

🔜 NEXT OPTIONS

1️⃣ Shipping & fulfillment
2️⃣ Orders deep dive (final boss)
3️⃣ Search & read-model scaling
4️⃣ Map your current coupons into this design
5️⃣ Create ADRs for pricing & promotions