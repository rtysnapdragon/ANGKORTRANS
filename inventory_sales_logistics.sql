-- ============================================================
--  INVENTORY, SALES & LOGISTICS — MySQL DDL
--  ENGINE  : InnoDB
--  CHARSET : utf8mb4 / utf8mb4_unicode_ci
--  GENERATED FOR MySQL 8.0+
--  NOTE    : All table names and column names are UPPERCASE
-- ============================================================

CREATE DATABASE IF NOT EXISTS INVENTORY_SALES_LOGISTICS
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE INVENTORY_SALES_LOGISTICS;

-- ============================================================
--  MASTER DATA
-- ============================================================

-- ------------------------------------------------------------
--  CATEGORIES
-- ------------------------------------------------------------
CREATE TABLE CATEGORIES (
  CATEGORY_ID   INT UNSIGNED  NOT NULL AUTO_INCREMENT,
  CATEGORY_NAME VARCHAR(100)  NOT NULL,
  PARENT_ID     INT UNSIGNED      NULL DEFAULT NULL COMMENT 'Self-referencing FK for subcategories',
  CREATED_AT    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (CATEGORY_ID),
  UNIQUE  KEY UQ_CATEGORY_NAME (CATEGORY_NAME),
  CONSTRAINT FK_CATEGORY_PARENT
    FOREIGN KEY (PARENT_ID) REFERENCES CATEGORIES (CATEGORY_ID)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Product category hierarchy (self-referencing)';


-- ------------------------------------------------------------
--  SUPPLIERS
-- ------------------------------------------------------------
CREATE TABLE SUPPLIERS (
  SUPPLIER_ID     INT UNSIGNED      NOT NULL AUTO_INCREMENT,
  SUPPLIER_NAME   VARCHAR(150)      NOT NULL,
  CONTACT_NAME    VARCHAR(100)          NULL,
  EMAIL           VARCHAR(255)          NULL,
  PHONE           VARCHAR(30)           NULL,
  ADDRESS_LINE    VARCHAR(255)          NULL,
  CITY            VARCHAR(100)          NULL,
  COUNTRY         CHAR(2)               NULL COMMENT 'ISO 3166-1 alpha-2',
  LEAD_TIME_DAYS  SMALLINT UNSIGNED NOT NULL DEFAULT 7,
  IS_ACTIVE       TINYINT(1)        NOT NULL DEFAULT 1,
  CREATED_AT      DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UPDATED_AT      DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP
                                             ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (SUPPLIER_ID),
  KEY IDX_SUPPLIER_COUNTRY (COUNTRY)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Supplier / vendor master';


-- ------------------------------------------------------------
--  CUSTOMERS
-- ------------------------------------------------------------
CREATE TABLE CUSTOMERS (
  CUSTOMER_ID   INT UNSIGNED  NOT NULL AUTO_INCREMENT,
  FIRST_NAME    VARCHAR(80)   NOT NULL,
  LAST_NAME     VARCHAR(80)   NOT NULL,
  EMAIL         VARCHAR(255)  NOT NULL,
  PHONE         VARCHAR(30)       NULL,
  ADDRESS_LINE  VARCHAR(255)      NULL,
  CITY          VARCHAR(100)      NULL,
  COUNTRY       CHAR(2)           NULL COMMENT 'ISO 3166-1 alpha-2',
  CREATED_AT    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UPDATED_AT    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
                                       ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (CUSTOMER_ID),
  UNIQUE KEY UQ_CUSTOMER_EMAIL (EMAIL),
  KEY IDX_CUSTOMER_COUNTRY (COUNTRY)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Customer master';


-- ------------------------------------------------------------
--  PRODUCTS
-- ------------------------------------------------------------
CREATE TABLE PRODUCTS (
  PRODUCT_ID    INT UNSIGNED   NOT NULL AUTO_INCREMENT,
  SKU           VARCHAR(50)    NOT NULL COMMENT 'Stock-Keeping Unit — globally unique',
  PRODUCT_NAME  VARCHAR(200)   NOT NULL,
  CATEGORY_ID   INT UNSIGNED       NULL,
  UNIT_PRICE    DECIMAL(10,2)  NOT NULL,
  COST_PRICE    DECIMAL(10,2)      NULL COMMENT 'Landed cost for margin calculation',
  WEIGHT_KG     DECIMAL(8,3)       NULL,
  IS_ACTIVE     TINYINT(1)     NOT NULL DEFAULT 1,
  CREATED_AT    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UPDATED_AT    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP
                                        ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (PRODUCT_ID),
  UNIQUE KEY UQ_PRODUCT_SKU (SKU),
  KEY IDX_PRODUCT_CATEGORY (CATEGORY_ID),
  CONSTRAINT FK_PRODUCT_CATEGORY
    FOREIGN KEY (CATEGORY_ID) REFERENCES CATEGORIES (CATEGORY_ID)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Product / SKU master';


-- ============================================================
--  INVENTORY MODULE
-- ============================================================

-- ------------------------------------------------------------
--  WAREHOUSES
-- ------------------------------------------------------------
CREATE TABLE WAREHOUSES (
  WAREHOUSE_ID    INT UNSIGNED   NOT NULL AUTO_INCREMENT,
  WAREHOUSE_NAME  VARCHAR(100)   NOT NULL,
  ADDRESS_LINE    VARCHAR(255)       NULL,
  CITY            VARCHAR(100)       NULL,
  COUNTRY         CHAR(2)            NULL COMMENT 'ISO 3166-1 alpha-2',
  CAPACITY_M3     DECIMAL(10,2)      NULL COMMENT 'Total physical capacity in cubic metres',
  IS_ACTIVE       TINYINT(1)     NOT NULL DEFAULT 1,
  CREATED_AT      DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (WAREHOUSE_ID),
  UNIQUE KEY UQ_WAREHOUSE_NAME (WAREHOUSE_NAME)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Physical warehouse / fulfilment centre locations';


-- ------------------------------------------------------------
--  INVENTORY
--  One row per (PRODUCT_ID, WAREHOUSE_ID) combination.
--  QTY_RESERVED is a denormalised cache updated by trigger / app.
-- ------------------------------------------------------------
CREATE TABLE INVENTORY (
  INVENTORY_ID   INT UNSIGNED  NOT NULL AUTO_INCREMENT,
  PRODUCT_ID     INT UNSIGNED  NOT NULL,
  WAREHOUSE_ID   INT UNSIGNED  NOT NULL,
  QTY_ON_HAND    INT           NOT NULL DEFAULT 0,
  QTY_RESERVED   INT           NOT NULL DEFAULT 0 COMMENT 'Denorm: open-order reservations',
  REORDER_POINT  INT           NOT NULL DEFAULT 10 COMMENT 'Triggers purchase order suggestion',
  UPDATED_AT     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
                                        ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (INVENTORY_ID),
  UNIQUE KEY UQ_INVENTORY_PRODUCT_WAREHOUSE (PRODUCT_ID, WAREHOUSE_ID),
  KEY IDX_INVENTORY_WAREHOUSE (WAREHOUSE_ID),
  CONSTRAINT FK_INVENTORY_PRODUCT
    FOREIGN KEY (PRODUCT_ID)   REFERENCES PRODUCTS   (PRODUCT_ID)   ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT FK_INVENTORY_WAREHOUSE
    FOREIGN KEY (WAREHOUSE_ID) REFERENCES WAREHOUSES (WAREHOUSE_ID) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT CHK_INVENTORY_QTY
    CHECK (QTY_ON_HAND >= 0 AND QTY_RESERVED >= 0 AND QTY_RESERVED <= QTY_ON_HAND)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Stock levels per product per warehouse';


-- ------------------------------------------------------------
--  PURCHASE_ORDERS  (inbound restocking from suppliers)
-- ------------------------------------------------------------
CREATE TABLE PURCHASE_ORDERS (
  PO_ID           INT UNSIGNED  NOT NULL AUTO_INCREMENT,
  SUPPLIER_ID     INT UNSIGNED  NOT NULL,
  WAREHOUSE_ID    INT UNSIGNED  NOT NULL COMMENT 'Receiving warehouse',
  PO_DATE         DATE          NOT NULL,
  EXPECTED_DATE   DATE              NULL,
  RECEIVED_DATE   DATE              NULL,
  STATUS          ENUM('DRAFT','SENT','PARTIAL','RECEIVED','CANCELLED')
                                NOT NULL DEFAULT 'DRAFT',
  TOTAL_COST      DECIMAL(12,2)     NULL COMMENT 'Denorm: sum of PO_ITEMS line costs',
  NOTES           TEXT              NULL,
  CREATED_AT      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UPDATED_AT      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
                                         ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (PO_ID),
  KEY IDX_PO_SUPPLIER  (SUPPLIER_ID),
  KEY IDX_PO_WAREHOUSE (WAREHOUSE_ID),
  KEY IDX_PO_STATUS    (STATUS),
  CONSTRAINT FK_PO_SUPPLIER
    FOREIGN KEY (SUPPLIER_ID)  REFERENCES SUPPLIERS  (SUPPLIER_ID)  ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT FK_PO_WAREHOUSE
    FOREIGN KEY (WAREHOUSE_ID) REFERENCES WAREHOUSES (WAREHOUSE_ID) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Inbound purchase orders from suppliers';


-- ------------------------------------------------------------
--  PO_ITEMS  (line items for each purchase order)
-- ------------------------------------------------------------
CREATE TABLE PO_ITEMS (
  PO_ITEM_ID    INT UNSIGNED   NOT NULL AUTO_INCREMENT,
  PO_ID         INT UNSIGNED   NOT NULL,
  PRODUCT_ID    INT UNSIGNED   NOT NULL,
  QUANTITY      INT UNSIGNED   NOT NULL,
  UNIT_COST     DECIMAL(10,2)  NOT NULL COMMENT 'Negotiated cost at time of order',
  QTY_RECEIVED  INT UNSIGNED   NOT NULL DEFAULT 0,

  PRIMARY KEY (PO_ITEM_ID),
  UNIQUE KEY UQ_PO_ITEM (PO_ID, PRODUCT_ID),
  KEY IDX_PO_ITEM_PRODUCT (PRODUCT_ID),
  CONSTRAINT FK_PO_ITEM_PO
    FOREIGN KEY (PO_ID)      REFERENCES PURCHASE_ORDERS (PO_ID)      ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT FK_PO_ITEM_PRODUCT
    FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCTS        (PRODUCT_ID) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT CHK_PO_ITEM_QTY
    CHECK (QUANTITY > 0 AND QTY_RECEIVED <= QUANTITY)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Line items on purchase orders';


-- ============================================================
--  SALES MODULE
-- ============================================================

-- ------------------------------------------------------------
--  SALES_ORDERS
--  ORDER_TOTAL is a denormalised cache; maintained by trigger.
-- ------------------------------------------------------------
CREATE TABLE SALES_ORDERS (
  ORDER_ID          INT UNSIGNED  NOT NULL AUTO_INCREMENT,
  CUSTOMER_ID       INT UNSIGNED  NOT NULL,
  ORDER_DATE        DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  STATUS            ENUM('PENDING','CONFIRMED','PROCESSING','SHIPPED','DELIVERED','CANCELLED','REFUNDED')
                                  NOT NULL DEFAULT 'PENDING',
  SHIPPING_ADDRESS  TEXT              NULL,
  ORDER_TOTAL       DECIMAL(12,2)     NULL COMMENT 'Denorm: sum of ORDER_ITEMS line totals',
  CURRENCY          CHAR(3)       NOT NULL DEFAULT 'USD' COMMENT 'ISO 4217',
  NOTES             TEXT              NULL,
  CREATED_AT        DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UPDATED_AT        DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
                                           ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (ORDER_ID),
  KEY IDX_ORDER_CUSTOMER (CUSTOMER_ID),
  KEY IDX_ORDER_STATUS   (STATUS),
  KEY IDX_ORDER_DATE     (ORDER_DATE),
  CONSTRAINT FK_ORDER_CUSTOMER
    FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMERS (CUSTOMER_ID)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Customer sales orders';


-- ------------------------------------------------------------
--  ORDER_ITEMS
--  UNIT_PRICE is snapshotted at time of sale — NOT a live FK to
--  PRODUCTS.UNIT_PRICE — to preserve historical accuracy.
-- ------------------------------------------------------------
CREATE TABLE ORDER_ITEMS (
  ITEM_ID       INT UNSIGNED      NOT NULL AUTO_INCREMENT,
  ORDER_ID      INT UNSIGNED      NOT NULL,
  PRODUCT_ID    INT UNSIGNED      NOT NULL,
  WAREHOUSE_ID  INT UNSIGNED          NULL COMMENT 'Fulfilment source warehouse',
  QUANTITY      SMALLINT UNSIGNED NOT NULL,
  UNIT_PRICE    DECIMAL(10,2)     NOT NULL COMMENT 'Price snapshot at time of sale',
  DISCOUNT_PCT  DECIMAL(5,2)      NOT NULL DEFAULT 0.00,

  PRIMARY KEY (ITEM_ID),
  KEY IDX_OI_ORDER   (ORDER_ID),
  KEY IDX_OI_PRODUCT (PRODUCT_ID),
  CONSTRAINT FK_OI_ORDER
    FOREIGN KEY (ORDER_ID)     REFERENCES SALES_ORDERS (ORDER_ID)     ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT FK_OI_PRODUCT
    FOREIGN KEY (PRODUCT_ID)   REFERENCES PRODUCTS     (PRODUCT_ID)   ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT FK_OI_WAREHOUSE
    FOREIGN KEY (WAREHOUSE_ID) REFERENCES WAREHOUSES   (WAREHOUSE_ID) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT CHK_OI_QTY
    CHECK (QUANTITY > 0),
  CONSTRAINT CHK_OI_DISCOUNT
    CHECK (DISCOUNT_PCT BETWEEN 0.00 AND 100.00)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Line items on sales orders';


-- ============================================================
--  LOGISTICS MODULE
-- ============================================================

-- ------------------------------------------------------------
--  SHIPMENTS
--  LAST_STATUS is a denormalised cache of the latest tracking event.
-- ------------------------------------------------------------
CREATE TABLE SHIPMENTS (
  SHIPMENT_ID       INT UNSIGNED  NOT NULL AUTO_INCREMENT,
  ORDER_ID          INT UNSIGNED  NOT NULL,
  WAREHOUSE_ID      INT UNSIGNED  NOT NULL COMMENT 'Dispatch warehouse',
  TRACKING_NUMBER   VARCHAR(100)      NULL,
  CARRIER           VARCHAR(80)       NULL,
  SERVICE_LEVEL     VARCHAR(60)       NULL COMMENT 'e.g. STANDARD, EXPRESS, OVERNIGHT',
  SHIPPED_AT        DATETIME          NULL,
  EXPECTED_DELIVERY DATE              NULL,
  DELIVERED_AT      DATETIME          NULL,
  LAST_STATUS       VARCHAR(60)       NULL COMMENT 'Denorm: latest TRACKING_EVENTS.STATUS_CODE',
  CREATED_AT        DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UPDATED_AT        DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
                                           ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (SHIPMENT_ID),
  UNIQUE KEY UQ_TRACKING_NUMBER (TRACKING_NUMBER),
  KEY IDX_SHIPMENT_ORDER     (ORDER_ID),
  KEY IDX_SHIPMENT_WAREHOUSE (WAREHOUSE_ID),
  KEY IDX_SHIPMENT_SHIPPED   (SHIPPED_AT),
  CONSTRAINT FK_SHIPMENT_ORDER
    FOREIGN KEY (ORDER_ID)     REFERENCES SALES_ORDERS (ORDER_ID)     ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT FK_SHIPMENT_WAREHOUSE
    FOREIGN KEY (WAREHOUSE_ID) REFERENCES WAREHOUSES   (WAREHOUSE_ID) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Outbound shipments linked to sales orders';


-- ------------------------------------------------------------
--  SHIPMENT_ITEMS
--  Bridge table supporting partial shipments
--  (one order → multiple shipments).
-- ------------------------------------------------------------
CREATE TABLE SHIPMENT_ITEMS (
  SHIPMENT_ITEM_ID  INT UNSIGNED      NOT NULL AUTO_INCREMENT,
  SHIPMENT_ID       INT UNSIGNED      NOT NULL,
  ORDER_ITEM_ID     INT UNSIGNED      NOT NULL,
  QTY_SHIPPED       SMALLINT UNSIGNED NOT NULL,

  PRIMARY KEY (SHIPMENT_ITEM_ID),
  KEY IDX_SI_SHIPMENT   (SHIPMENT_ID),
  KEY IDX_SI_ORDER_ITEM (ORDER_ITEM_ID),
  CONSTRAINT FK_SI_SHIPMENT
    FOREIGN KEY (SHIPMENT_ID)   REFERENCES SHIPMENTS   (SHIPMENT_ID) ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT FK_SI_ORDER_ITEM
    FOREIGN KEY (ORDER_ITEM_ID) REFERENCES ORDER_ITEMS (ITEM_ID)     ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT CHK_SI_QTY
    CHECK (QTY_SHIPPED > 0)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Individual items within a shipment (supports partial shipments)';


-- ------------------------------------------------------------
--  TRACKING_EVENTS  (append-only event log per shipment)
-- ------------------------------------------------------------
CREATE TABLE TRACKING_EVENTS (
  EVENT_ID     INT UNSIGNED  NOT NULL AUTO_INCREMENT,
  SHIPMENT_ID  INT UNSIGNED  NOT NULL,
  EVENT_TIME   DATETIME      NOT NULL,
  LOCATION     VARCHAR(200)      NULL,
  STATUS_CODE  VARCHAR(40)   NOT NULL COMMENT 'e.g. IN_TRANSIT, OUT_FOR_DELIVERY, DELIVERED',
  DESCRIPTION  TEXT              NULL,
  CREATED_AT   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (EVENT_ID),
  KEY IDX_TE_SHIPMENT   (SHIPMENT_ID),
  KEY IDX_TE_EVENT_TIME (EVENT_TIME),
  CONSTRAINT FK_TE_SHIPMENT
    FOREIGN KEY (SHIPMENT_ID) REFERENCES SHIPMENTS (SHIPMENT_ID)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Immutable tracking event log per shipment';


-- ============================================================
--  VIEWS  (reporting layer)
-- ============================================================

-- Sales order summary with calculated vs cached total
CREATE OR REPLACE VIEW VW_ORDER_SUMMARY AS
SELECT
  O.ORDER_ID,
  CONCAT(C.FIRST_NAME, ' ', C.LAST_NAME)                              AS CUSTOMER_NAME,
  C.EMAIL                                                              AS CUSTOMER_EMAIL,
  O.ORDER_DATE,
  O.STATUS,
  O.CURRENCY,
  COUNT(OI.ITEM_ID)                                                    AS LINE_ITEMS,
  SUM(OI.QUANTITY)                                                     AS TOTAL_UNITS,
  SUM(OI.QUANTITY * OI.UNIT_PRICE * (1 - OI.DISCOUNT_PCT / 100))      AS CALCULATED_TOTAL,
  O.ORDER_TOTAL                                                        AS CACHED_TOTAL
FROM  SALES_ORDERS O
JOIN  CUSTOMERS    C  ON C.CUSTOMER_ID = O.CUSTOMER_ID
JOIN  ORDER_ITEMS  OI ON OI.ORDER_ID   = O.ORDER_ID
GROUP BY
  O.ORDER_ID, C.FIRST_NAME, C.LAST_NAME, C.EMAIL,
  O.ORDER_DATE, O.STATUS, O.CURRENCY, O.ORDER_TOTAL;


-- Inventory stock status with low-stock alert flag
CREATE OR REPLACE VIEW VW_STOCK_STATUS AS
SELECT
  P.PRODUCT_ID,
  P.SKU,
  P.PRODUCT_NAME,
  W.WAREHOUSE_ID,
  W.WAREHOUSE_NAME,
  I.QTY_ON_HAND,
  I.QTY_RESERVED,
  (I.QTY_ON_HAND - I.QTY_RESERVED)                    AS QTY_AVAILABLE,
  I.REORDER_POINT,
  CASE
    WHEN (I.QTY_ON_HAND - I.QTY_RESERVED) <= I.REORDER_POINT THEN 'LOW'
    ELSE 'OK'
  END                                                   AS STOCK_ALERT
FROM  INVENTORY  I
JOIN  PRODUCTS   P ON P.PRODUCT_ID   = I.PRODUCT_ID
JOIN  WAREHOUSES W ON W.WAREHOUSE_ID = I.WAREHOUSE_ID;


-- Shipment delivery performance / SLA tracking
CREATE OR REPLACE VIEW VW_DELIVERY_PERFORMANCE AS
SELECT
  S.SHIPMENT_ID,
  S.ORDER_ID,
  S.CARRIER,
  S.SERVICE_LEVEL,
  S.SHIPPED_AT,
  S.EXPECTED_DELIVERY,
  S.DELIVERED_AT,
  S.LAST_STATUS,
  DATEDIFF(S.DELIVERED_AT,      S.SHIPPED_AT)          AS TRANSIT_DAYS,
  DATEDIFF(S.EXPECTED_DELIVERY, S.SHIPPED_AT)          AS PROMISED_DAYS,
  CASE
    WHEN S.DELIVERED_AT IS NULL                                 THEN 'IN_TRANSIT'
    WHEN DATE(S.DELIVERED_AT) <= S.EXPECTED_DELIVERY            THEN 'ON_TIME'
    ELSE 'LATE'
  END                                                   AS SLA_STATUS
FROM SHIPMENTS S;


-- ============================================================
--  ADDITIONAL PERFORMANCE INDEXES
-- ============================================================

-- Full-text search on PRODUCTS.PRODUCT_NAME
ALTER TABLE PRODUCTS
  ADD FULLTEXT INDEX FT_PRODUCT_NAME (PRODUCT_NAME);

-- Composite index for inventory low-stock alert queries
CREATE INDEX IDX_INVENTORY_ALERT
  ON INVENTORY (REORDER_POINT, QTY_ON_HAND, QTY_RESERVED);

-- Order date + status range queries
CREATE INDEX IDX_ORDERS_DATE_STATUS
  ON SALES_ORDERS (ORDER_DATE, STATUS);

-- Tracking event lookups by shipment ordered by most recent first
CREATE INDEX IDX_TE_SHIPMENT_TIME
  ON TRACKING_EVENTS (SHIPMENT_ID, EVENT_TIME DESC);


-- ============================================================
--  TRIGGERS
-- ============================================================

DELIMITER $$

-- Recalculate SALES_ORDERS.ORDER_TOTAL after INSERT on ORDER_ITEMS
CREATE TRIGGER TRG_OI_AFTER_INSERT
AFTER INSERT ON ORDER_ITEMS
FOR EACH ROW
BEGIN
  UPDATE SALES_ORDERS
  SET ORDER_TOTAL = (
    SELECT SUM(QUANTITY * UNIT_PRICE * (1 - DISCOUNT_PCT / 100))
    FROM   ORDER_ITEMS
    WHERE  ORDER_ID = NEW.ORDER_ID
  )
  WHERE ORDER_ID = NEW.ORDER_ID;
END$$

-- Recalculate SALES_ORDERS.ORDER_TOTAL after UPDATE on ORDER_ITEMS
CREATE TRIGGER TRG_OI_AFTER_UPDATE
AFTER UPDATE ON ORDER_ITEMS
FOR EACH ROW
BEGIN
  UPDATE SALES_ORDERS
  SET ORDER_TOTAL = (
    SELECT SUM(QUANTITY * UNIT_PRICE * (1 - DISCOUNT_PCT / 100))
    FROM   ORDER_ITEMS
    WHERE  ORDER_ID = NEW.ORDER_ID
  )
  WHERE ORDER_ID = NEW.ORDER_ID;
END$$

-- Recalculate SALES_ORDERS.ORDER_TOTAL after DELETE on ORDER_ITEMS
CREATE TRIGGER TRG_OI_AFTER_DELETE
AFTER DELETE ON ORDER_ITEMS
FOR EACH ROW
BEGIN
  UPDATE SALES_ORDERS
  SET ORDER_TOTAL = (
    SELECT COALESCE(SUM(QUANTITY * UNIT_PRICE * (1 - DISCOUNT_PCT / 100)), 0)
    FROM   ORDER_ITEMS
    WHERE  ORDER_ID = OLD.ORDER_ID
  )
  WHERE ORDER_ID = OLD.ORDER_ID;
END$$

-- Update SHIPMENTS.LAST_STATUS when a new tracking event is inserted
CREATE TRIGGER TRG_TE_AFTER_INSERT
AFTER INSERT ON TRACKING_EVENTS
FOR EACH ROW
BEGIN
  UPDATE SHIPMENTS
  SET LAST_STATUS = NEW.STATUS_CODE,
      UPDATED_AT  = CURRENT_TIMESTAMP
  WHERE SHIPMENT_ID = NEW.SHIPMENT_ID;
END$$

DELIMITER ;

-- ============================================================
--  END OF SCRIPT
-- ============================================================
