# API Specification v0.1

## Search Endpoint
- POST `/api/v1/source`
- Body: `{ "image": "url/base64" }`
- Response: `{ "top_suppliers": [...], "suggested_script": "..." }`

## Supplier Endpoint
- GET `/api/v1/suppliers?product_id=xyz`
- Response: `[{ "name": "...", "price": 10.0, ... }]`

## Negotiation Endpoint
- POST `/api/v1/negotiate`
- Body: `{ "supplier_id": "...", "script": "..." }`
- Response: `{ "status": "sent", "timestamp": "..." }`
