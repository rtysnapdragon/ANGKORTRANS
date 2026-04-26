MASTER DATA              TRANSACTIONS              LOGISTICS
┌─────────────┐         ┌─────────────┐            ┌─────────────┐
│  SUPPLIER   │────────▶│   PRODUCT   │◀───────────│  CATEGORY   │
└─────────────┘         └──────┬──────┘            └─────────────┘
       │                       │
       │              ┌─────────┴─────────┐
       │              │                   │
       ▼              ▼                   ▼
┌─────────────┐  ┌──────────┐      ┌──────────┐
│  ADDRESS    │  │ INVENTORY│      │ PURCHASE │
└─────────────┘  └──────────┘      │  ORDER   │
       ▲              ▲             └──────────┘
       │              │                   │
┌─────────────┐  ┌──────────┐            │
│  CUSTOMER   │  │ LOCATION │            │
└─────────────┘  └──────────┘            │
       │              ▲                  │
       │              │                  │
       └──────────────┴──────────────────┘
              WAREHOUSE

    
Operational Flows
Sales Flow: CUSTOMER → SALES_ORDER → SALES_ORDER_LINE → SHIPMENT → SHIPMENT_LINE → STOCK_MOVEMENT (OUTBOUND)
Purchase Flow: SUPPLIER → PURCHASE_ORDER → PURCHASE_ORDER_LINE → GOODS_RECEIPT → GOODS_RECEIPT_LINE → STOCK_MOVEMENT (INBOUND)