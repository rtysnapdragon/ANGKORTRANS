# INVENTORY, SALES & LOGISTICS DATABASE ANALYSIS
## MySQL 8.0 | 3NF Normalized | All Tables & Fields UPPERCASE

---

## 1. DATABASE FLOW (Data Flow Diagram)

### 1.1 Master Data Flow
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  SUPPLIER   │────▶│   PRODUCT   │◀────│  CATEGORY   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │
       │              ┌─────┴─────┐
       │              │           │
       ▼              ▼           ▼
┌─────────────┐  ┌──────────┐ ┌──────────┐
│  ADDRESS    │  │ INVENTORY│ │ PURCHASE │
└─────────────┘  └──────────┘ └──────────┘
       ▲              ▲           ▲
       │              │           │
┌─────────────┐  ┌──────────┐ ┌──────────┐
│  CUSTOMER   │  │ LOCATION │ │  ORDER   │
└─────────────┘  └──────────┘ └──────────┘
       │              ▲           │
       │              │           │
       └──────────────┴───────────┘
              WAREHOUSE
```

### 1.2 Transaction Flow
```
SALES FLOW:
CUSTOMER ──▶ SALES_ORDER ──▶ SALES_ORDER_LINE ──▶ SHIPMENT ──▶ SHIPMENT_LINE
                │                                    │
                └──────────────┬─────────────────────┘
                               ▼
                         STOCK_MOVEMENT (OUTBOUND)

PURCHASE FLOW:
SUPPLIER ──▶ PURCHASE_ORDER ──▶ PURCHASE_ORDER_LINE ──▶ GOODS_RECEIPT ──▶ GOODS_RECEIPT_LINE
                                                              │
                                                              ▼
                                                    STOCK_MOVEMENT (INBOUND)

INVENTORY UPDATE FLOW:
GOODS_RECEIPT_LINE ──▶ INVENTORY (+QTY)
SHIPMENT_LINE ───────▶ INVENTORY (-QTY, +RESERVED)
STOCK_MOVEMENT ──────▶ AUDIT TRAIL
```

### 1.3 Logistics Flow
```
WAREHOUSE ──▶ LOCATION ──▶ INVENTORY (Physical Storage)
   │
   ├─▶ SHIPMENT (Outbound to Customer)
   ├─▶ GOODS_RECEIPT (Inbound from Supplier)
   └─▶ STOCK_MOVEMENT (Internal Transfers)
```

---

## 2. DATABASE NORMALIZATION ANALYSIS

### 2.1 First Normal Form (1NF)
**Rule**: All columns contain atomic (indivisible) values; no repeating groups.

| Table | Compliance | Evidence |
|-------|-----------|----------|
| PRODUCT | ✓ | SKU is atomic; no multi-valued attributes |
| CUSTOMER | ✓ | Single email/phone per row; addresses referenced via FK |
| SALES_ORDER | ✓ | Line items moved to SALES_ORDER_LINE; no repeating groups |
| INVENTORY | ✓ | Single quantity per product-warehouse-location combination |

**Example of 1NF Application**:
- **Before (Unnormalized)**: `SALES_ORDER` with `PRODUCT_1`, `QTY_1`, `PRODUCT_2`, `QTY_2` columns
- **After (1NF)**: `SALES_ORDER` header + `SALES_ORDER_LINE` child table with one product per row

### 2.2 Second Normal Form (2NF)
**Rule**: All non-key attributes depend on the ENTIRE primary key (relevant for composite keys).

| Table | PK Type | Compliance | Evidence |
|-------|---------|-----------|----------|
| SALES_ORDER_LINE | Composite (ORDER_ID + LINE_NUMBER) | ✓ | `UNIT_PRICE` depends on both ORDER and LINE; `PRODUCT_ID` specific to line |
| PURCHASE_ORDER_LINE | Composite (PO_ID + LINE_NUMBER) | ✓ | `QUANTITY_ORDERED` is line-specific |
| INVENTORY | Composite (Implicit UK: PRODUCT+WAREHOUSE+LOCATION) | ✓ | `QUANTITY_ON_HAND` depends on all three keys |
| LOCATION | Single (LOCATION_ID) | ✓ N/A | Single-column PK, 2NF automatically satisfied |

### 2.3 Third Normal Form (3NF)
**Rule**: No transitive dependencies; non-key attributes depend ONLY on the primary key.

**Transitive Dependency Elimination**:

| Eliminated Dependency | Solution | Table |
|----------------------|----------|-------|
| PRODUCT → CATEGORY_NAME | Moved to CATEGORY table; PRODUCT only stores CATEGORY_ID | PRODUCT |
| PRODUCT → SUPPLIER_NAME | Moved to SUPPLIER table; PRODUCT only stores SUPPLIER_ID | PRODUCT |
| CUSTOMER → CITY/STATE | Moved to ADDRESS table; CUSTOMER stores ADDRESS_ID | CUSTOMER |
| WAREHOUSE → CITY/STATE | Moved to ADDRESS table; WAREHOUSE stores ADDRESS_ID | WAREHOUSE |
| SALES_ORDER → CUSTOMER_NAME | Kept in CUSTOMER table; referenced via CUSTOMER_ID | SALES_ORDER |

**3NF Verification Examples**:

**PRODUCT Table**:
```
PK: PRODUCT_ID
├─ SKU (depends on PRODUCT_ID)
├─ PRODUCT_NAME (depends on PRODUCT_ID)
├─ CATEGORY_ID (FK, not transitive - directly needed)
├─ SUPPLIER_ID (FK, not transitive - directly needed)
├─ UNIT_PRICE (depends on PRODUCT_ID)
└─ UNIT_COST (depends on PRODUCT_ID)
✓ No transitive dependencies: No non-key attribute depends on another non-key attribute
```

**SALES_ORDER Table**:
```
PK: SALES_ORDER_ID
├─ ORDER_NUMBER (depends on SALES_ORDER_ID)
├─ CUSTOMER_ID (FK, directly needed)
├─ ORDER_DATE (depends on SALES_ORDER_ID)
├─ SUBTOTAL (depends on SALES_ORDER_ID)
├─ TAX_AMOUNT (depends on SALES_ORDER_ID)
├─ TOTAL_AMOUNT (depends on SALES_ORDER_ID)
✓ No transitive dependencies: CUSTOMER_NAME is NOT stored here (in CUSTOMER table)
```

### 2.4 Normalization Summary

| Normal Form | Status | Notes |
|-------------|--------|-------|
| 1NF | ✓ Achieved | All fields atomic; repeating groups eliminated via child tables |
| 2NF | ✓ Achieved | All tables have single-column PKs or fully dependent composite keys |
| 3NF | ✓ Achieved | No transitive dependencies; all descriptive data in master tables |
| BCNF | ✓ Achieved | Every determinant is a candidate key (SKU, ORDER_NUMBER, PO_NUMBER are UNIQUE) |

---

## 3. DATABASE SCHEMA DETAILS

### 3.1 Table Inventory (18 Tables)

| # | Table Name | Type | Records | Purpose |
|---|-----------|------|---------|---------|
| 1 | ADDRESS | Reference | ~1,000 | Global address registry |
| 2 | CARRIER | Reference | ~50 | Shipping carriers |
| 3 | USER | Reference | ~500 | System users |
| 4 | CATEGORY | Master | ~200 | Product taxonomy |
| 5 | SUPPLIER | Master | ~1,000 | Vendors |
| 6 | PRODUCT | Master | ~50,000 | SKU catalog |
| 7 | CUSTOMER | Master | ~10,000 | Customers |
| 8 | WAREHOUSE | Master | ~20 | Storage facilities |
| 9 | LOCATION | Master | ~5,000 | Bin/shelf locations |
| 10 | INVENTORY | Transaction | ~100,000 | Stock balances |
| 11 | SALES_ORDER | Transaction | ~500,000 | Customer orders |
| 12 | SALES_ORDER_LINE | Transaction | ~2,000,000 | Order line items |
| 13 | PURCHASE_ORDER | Transaction | ~100,000 | Supplier orders |
| 14 | PURCHASE_ORDER_LINE | Transaction | ~500,000 | PO line items |
| 15 | SHIPMENT | Logistics | ~400,000 | Shipments |
| 16 | SHIPMENT_LINE | Logistics | ~1,500,000 | Shipment items |
| 17 | GOODS_RECEIPT | Logistics | ~150,000 | Receipts |
| 18 | GOODS_RECEIPT_LINE | Logistics | ~600,000 | Receipt items |
| 19 | STOCK_MOVEMENT | Audit | ~5,000,000 | All stock changes |

### 3.2 Relationship Matrix

| Parent Table | Child Table | Relationship | FK Column | Cardinality |
|-------------|------------|-------------|-----------|-------------|
| CATEGORY | PRODUCT | 1:N | CATEGORY_ID | One category has many products |
| SUPPLIER | PRODUCT | 1:N | SUPPLIER_ID | One supplier provides many products |
| ADDRESS | SUPPLIER | 1:N | ADDRESS_ID | One address for many suppliers (rare) |
| ADDRESS | CUSTOMER | 1:N | BILLING_ADDRESS_ID | One address used by many customers |
| ADDRESS | WAREHOUSE | 1:N | ADDRESS_ID | One address per warehouse |
| WAREHOUSE | LOCATION | 1:N | WAREHOUSE_ID | One warehouse has many locations |
| PRODUCT | INVENTORY | 1:N | PRODUCT_ID | One product in many warehouses |
| WAREHOUSE | INVENTORY | 1:N | WAREHOUSE_ID | One warehouse holds many products |
| LOCATION | INVENTORY | 1:N | LOCATION_ID | One location holds many products |
| CUSTOMER | SALES_ORDER | 1:N | CUSTOMER_ID | One customer places many orders |
| SALES_ORDER | SALES_ORDER_LINE | 1:N | SALES_ORDER_ID | One order has many lines |
| PRODUCT | SALES_ORDER_LINE | 1:N | PRODUCT_ID | One product appears in many lines |
| SUPPLIER | PURCHASE_ORDER | 1:N | SUPPLIER_ID | One supplier receives many POs |
| WAREHOUSE | PURCHASE_ORDER | 1:N | WAREHOUSE_ID | One warehouse receives many POs |
| PURCHASE_ORDER | PURCHASE_ORDER_LINE | 1:N | PURCHASE_ORDER_ID | One PO has many lines |
| CARRIER | SHIPMENT | 1:N | CARRIER_ID | One carrier handles many shipments |
| WAREHOUSE | SHIPMENT | 1:N | ORIGIN_WAREHOUSE_ID | One warehouse ships many orders |
| SHIPMENT | SHIPMENT_LINE | 1:N | SHIPMENT_ID | One shipment has many lines |
| SALES_ORDER_LINE | SHIPMENT_LINE | 1:N | SALES_ORDER_LINE_ID | One line shipped in multiple shipments |
| PURCHASE_ORDER | GOODS_RECEIPT | 1:N | PURCHASE_ORDER_ID | One PO received in multiple receipts |
| GOODS_RECEIPT | GOODS_RECEIPT_LINE | 1:N | RECEIPT_ID | One receipt has many lines |
| USER | STOCK_MOVEMENT | 1:N | USER_ID | One user creates many movements |

---

## 4. ENTITY-RELATIONSHIP DIAGRAM (ERD)

### 4.1 ERD Notation
- **Red Square (■)**: Primary Key
- **Blue Triangle (▲)**: Foreign Key
- **Solid Line (—)**: Identifying Relationship
- **Dashed Line (- -)**: Non-Identifying Relationship
- **N:1 Label**: Many-to-One cardinality

### 4.2 Entity Clusters

**Master Data Cluster (Blue)**:
- PRODUCT, CATEGORY, SUPPLIER, CUSTOMER, WAREHOUSE
- Slow-changing, reference data
- High read, low write

**Transaction Cluster (Orange)**:
- SALES_ORDER, SALES_ORDER_LINE, PURCHASE_ORDER, PURCHASE_ORDER_LINE
- High write, time-series data
- Business event records

**Logistics Cluster (Green)**:
- INVENTORY, LOCATION, SHIPMENT, SHIPMENT_LINE, GOODS_RECEIPT, GOODS_RECEIPT_LINE, STOCK_MOVEMENT
- Operational data
- Real-time updates

**Reference Cluster (Purple)**:
- ADDRESS, CARRIER, USER
- Lookup tables
- Shared across domains

### 4.3 Key Design Decisions

1. **ADDRESS as Separate Entity**: Eliminates transitive dependencies in CUSTOMER, SUPPLIER, WAREHOUSE. One address can be shared (e.g., headquarters billing for multiple customers).

2. **LINE_ITEM Pattern**: Both sales and purchase orders use header-line pattern. This is a classic 1NF/3NF design that eliminates repeating groups.

3. **INVENTORY as Associative Entity**: Links PRODUCT, WAREHOUSE, and LOCATION in a ternary relationship. The unique constraint `(PRODUCT_ID, WAREHOUSE_ID, LOCATION_ID)` ensures one stock record per location.

4. **STOCK_MOVEMENT as Audit Trail**: All inventory changes (receipts, sales, adjustments) are logged here for traceability. Uses `REFERENCE_ID` + `REFERENCE_TYPE` polymorphic pattern to link to any source document.

5. **Generated Columns**: `QUANTITY_AVAILABLE` and `LINE_TOTAL` are computed columns, ensuring data consistency without application logic.

---

## 5. PERFORMANCE & INTEGRITY FEATURES

### 5.1 Indexing Strategy
- **Primary Keys**: All tables use `BIGINT UNSIGNED AUTO_INCREMENT` for future-proofing
- **Foreign Key Indexes**: Every FK column has an index for JOIN performance
- **Business Key Indexes**: SKU, ORDER_NUMBER, PO_NUMBER, TRACKING_NUMBER have UNIQUE indexes
- **Query Indexes**: STATUS, DATE, and TYPE columns indexed for filtering/sorting

### 5.2 Constraints
- **Referential Integrity**: All FKs defined with appropriate ON DELETE actions (RESTRICT for business entities, CASCADE for child lines, SET NULL for optional references)
- **Check Constraints**: ENUM types enforce valid status values
- **Generated Columns**: Prevent calculation inconsistencies
- **Unique Constraints**: Prevent duplicate business keys

### 5.3 Triggers
- **Order Total Recalculation**: Automatically updates header totals when lines are inserted
- **Inventory Update**: Automatically updates stock on goods receipt
- **Movement Logging**: Automatically creates audit trail entries

---

## 6. SCALABILITY CONSIDERATIONS

| Aspect | Design | Rationale |
|--------|--------|-----------|
| PK Type | BIGINT UNSIGNED | Supports up to 18 quintillion rows |
| Partitioning | Ready for RANGE on DATE columns | SALES_ORDER, PURCHASE_ORDER, STOCK_MOVEMENT |
| Archiving | Soft-delete pattern via STATUS | Historical data preserved for compliance |
| Sharding | Natural by WAREHOUSE_ID | Geographic distribution possible |
| Read Replicas | Views for reporting | V_INVENTORY_STATUS, V_SALES_ORDER_SUMMARY |

---

*Generated: 2026-04-26 | MySQL 8.0+ | InnoDB Engine | UTF8MB4 Character Set*
