# Wedding & Event Program Management System — Database Schema

---

## Domain 1 — Identity & Authentication

### `USERS`
Stores all system accounts regardless of role.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | |
| username | VARCHAR(80) | UNIQUE, NOT NULL | Used for login |
| email | VARCHAR(255) | UNIQUE, NOT NULL | |
| password_hash | TEXT | NULLABLE | Null when using OAuth only |
| auth_provider | VARCHAR(20) | DEFAULT 'local' | 'local', 'google' |
| oauth_token | TEXT | NULLABLE | Encrypted Google OAuth2 token |
| is_active | BOOLEAN | DEFAULT TRUE | Soft disable account |
| created_at | TIMESTAMPTZ | NOT NULL | |
| updated_at | TIMESTAMPTZ | NOT NULL | |

**Purpose:** Single source for all human actors — system admins, org owners, staff users.

---

### `ROLES`
Named role definitions (Admin, Staff, Viewer, etc.).

| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(50) | UNIQUE, NOT NULL |
| description | TEXT | NULLABLE |

---

### `PERMISSIONS`
Atomic action-resource pairs.

| Column | Type | Constraints | Example values |
|---|---|---|---|
| id | UUID | PK | |
| action | VARCHAR(30) | NOT NULL | 'create', 'read', 'update', 'delete' |
| resource | VARCHAR(50) | NOT NULL | 'guests', 'gift_records', 'reports' |

**Composite UNIQUE on (action, resource).**

---

### `ROLE_PERMISSIONS` *(junction)*
Maps roles to their allowed permissions. PK = (role_id, permission_id).

| Column | Type | Constraints |
|---|---|---|
| role_id | UUID | FK → ROLES |
| permission_id | UUID | FK → PERMISSIONS |

---

### `USER_ROLES` *(junction)*
Assigns roles to users, scoped to organization context (optional).

| Column | Type | Constraints |
|---|---|---|
| user_id | UUID | FK → USERS |
| role_id | UUID | FK → ROLES |
| assigned_by | UUID | FK → USERS |
| assigned_at | TIMESTAMPTZ | NOT NULL |

**PK = (user_id, role_id).**

---

## Domain 2 — Organizations

### `ORGANIZATIONS`
Represents the application/program owner entity (the business entity owning programs).

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | |
| owner_user_id | UUID | FK → USERS | Primary admin |
| name | VARCHAR(200) | NOT NULL | |
| slug | VARCHAR(100) | UNIQUE, NOT NULL | URL-friendly identifier |
| telegram_bot_token | TEXT | NULLABLE | Encrypted |
| telegram_group_id | VARCHAR(100) | NULLABLE | For group notifications |
| google_drive_folder_id | TEXT | NULLABLE | Root Drive folder |
| google_oauth_token | TEXT | NULLABLE | Encrypted refresh token |
| created_at | TIMESTAMPTZ | NOT NULL | |

---

### `ORG_MEMBERS`
Staff users who belong to an organization (multi-user under one org).

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | |
| org_id | UUID | FK → ORGANIZATIONS | |
| user_id | UUID | FK → USERS | |
| role | VARCHAR(30) | NOT NULL | 'admin', 'staff', 'viewer' |
| joined_at | TIMESTAMPTZ | NOT NULL | |

**UNIQUE on (org_id, user_id).**

---

## Domain 3 — Programs & Templates

### `PROGRAM_TEMPLATES`
Reusable starting configurations for wedding, engagement, birthday, etc.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | |
| name | VARCHAR(100) | NOT NULL | e.g., "Digital Wedding" |
| type | VARCHAR(50) | NOT NULL | 'wedding', 'birthday', 'corporate' |
| default_fields | JSONB | NULLABLE | Template-specific field defaults |
| created_at | TIMESTAMPTZ | NOT NULL | |

---

### `PROGRAMS`
Core entity — one record per event/program created by an org.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | |
| org_id | UUID | FK → ORGANIZATIONS | |
| template_id | UUID | FK → PROGRAM_TEMPLATES, NULLABLE | |
| created_by | UUID | FK → USERS | |
| title | VARCHAR(300) | NOT NULL | |
| type | VARCHAR(50) | NOT NULL | 'wedding', 'birthday', etc. |
| slug | VARCHAR(150) | UNIQUE, NOT NULL | Used in public URL |
| public_url | TEXT | GENERATED | Computed from slug |
| qr_code_url | TEXT | NULLABLE | Generated QR image URL |
| description | TEXT | NULLABLE | |
| event_date | DATE | NOT NULL | |
| venue | VARCHAR(300) | NULLABLE | |
| status | VARCHAR(20) | DEFAULT 'draft' | 'draft', 'active', 'completed' |
| settings | JSONB | NULLABLE | Flexible per-program config |
| created_at | TIMESTAMPTZ | NOT NULL | |

---

## Domain 4 — Guests

### `GUESTS`
Every invited or walk-in person linked to a program.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | |
| program_id | UUID | FK → PROGRAMS | |
| name | VARCHAR(200) | NOT NULL | |
| gender | VARCHAR(10) | CHECK ('male','female','other') | |
| email | VARCHAR(255) | NULLABLE | |
| phone | VARCHAR(30) | NULLABLE | |
| telegram_chat_id | VARCHAR(100) | NULLABLE | For private Telegram DM |
| guest_code | VARCHAR(50) | UNIQUE | Alphanumeric code on invitation |
| qr_token | VARCHAR(100) | UNIQUE | Token embedded in QR code |
| table_number | INTEGER | NULLABLE | Denormalized shortcut (see TABLE_ASSIGNMENTS) |
| status | VARCHAR(20) | DEFAULT 'invited' | 'invited', 'confirmed', 'attended', 'no-show' |
| invited_at | TIMESTAMPTZ | NULLABLE | |
| created_at | TIMESTAMPTZ | NOT NULL | |

**Note:** `guest_code` and `qr_token` are both unique per guest. `guest_code` is human-readable (for manual lookup); `qr_token` is machine-readable (for scanner). Walk-in guests are recorded here with `is_walk_in` flag carried by GIFT_RECORDS.

---

## Domain 5 — Messaging

### `MESSAGE_LOGS`
Audit trail of every message sent to guests (Telegram or Email).

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | |
| program_id | UUID | FK → PROGRAMS | |
| guest_id | UUID | FK → GUESTS, NULLABLE | Null = broadcast |
| channel | VARCHAR(20) | NOT NULL | 'telegram', 'email' |
| message_type | VARCHAR(30) | NOT NULL | 'invitation', 'reminder', 'thank_you', 'album_link' |
| status | VARCHAR(20) | NOT NULL | 'pending', 'sent', 'failed', 'delivered' |
| content | TEXT | NOT NULL | Rendered message body |
| sent_at | TIMESTAMPTZ | NULLABLE | |
| error_msg | TEXT | NULLABLE | |

---

## Domain 6 — Seating

### `TABLES`
Table definitions within a program.

| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| program_id | UUID | FK → PROGRAMS |
| table_number | INTEGER | NOT NULL |
| label | VARCHAR(100) | NULLABLE |
| capacity | INTEGER | NULLABLE |
| notes | TEXT | NULLABLE |

**UNIQUE on (program_id, table_number).**

---

### `TABLE_ASSIGNMENTS`
Links a guest to a table (can change over time).

| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| table_id | UUID | FK → TABLES |
| guest_id | UUID | FK → GUESTS |
| assigned_at | TIMESTAMPTZ | NOT NULL |
| assigned_by | UUID | FK → USERS |

**UNIQUE on (guest_id) to enforce one-table-per-guest at any time.**

---

## Domain 7 — Gift Recording (Handshake)

### `GIFT_RECORDS`
Records each gift/money envelope received at the event.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | |
| program_id | UUID | FK → PROGRAMS | |
| guest_id | UUID | FK → GUESTS, NULLABLE | Null if pure walk-in not matched |
| recorded_by | UUID | FK → USERS | Staff member who entered record |
| amount | DECIMAL(12,2) | NOT NULL | |
| currency | VARCHAR(10) | DEFAULT 'KHR' | |
| entry_method | VARCHAR(20) | NOT NULL | 'qr_scan', 'manual_search', 'new_walkin' |
| is_walk_in | BOOLEAN | DEFAULT FALSE | Guest not in invite list |
| walk_in_name | VARCHAR(200) | NULLABLE | Captured when is_walk_in=TRUE |
| walk_in_gender | VARCHAR(10) | NULLABLE | |
| notes | TEXT | NULLABLE | |
| is_adjusted | BOOLEAN | DEFAULT FALSE | Corrected after-the-fact entry |
| recorded_at | TIMESTAMPTZ | NOT NULL | Can be entered post-event |

**entry_method** distinguishes the three cases from spec:
- `qr_scan` — guest showed QR, scanner confirmed
- `manual_search` — guest found by name search (no QR)
- `new_walkin` — entirely new, not on invite list

---

## Domain 8 — Expenses

### `EXPENSES`
Program-related costs tracked for final report.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | |
| program_id | UUID | FK → PROGRAMS | |
| created_by | UUID | FK → USERS | |
| category | VARCHAR(100) | NOT NULL | 'catering', 'decoration', 'venue', etc. |
| description | TEXT | NOT NULL | |
| amount | DECIMAL(12,2) | NOT NULL | |
| currency | VARCHAR(10) | DEFAULT 'KHR' | |
| expense_date | DATE | NOT NULL | |
| created_at | TIMESTAMPTZ | NOT NULL | |

---

## Domain 9 — Media

### `MEDIA_ALBUMS`
References to Google Drive folders where wedding photos are stored.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PK | |
| program_id | UUID | FK → PROGRAMS | |
| title | VARCHAR(200) | NOT NULL | |
| drive_folder_id | TEXT | NOT NULL | Google Drive folder ID |
| shareable_link | TEXT | NOT NULL | Guest-accessible link |
| access_level | VARCHAR(20) | DEFAULT 'anyone_with_link' | |
| created_at | TIMESTAMPTZ | NOT NULL | |

---

## Domain 10 — Audit

### `AUDIT_LOGS`
Immutable log of all create/update/delete actions across the system.

| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK → USERS |
| action | VARCHAR(20) | 'INSERT', 'UPDATE', 'DELETE' |
| table_name | VARCHAR(100) | Target table name |
| record_id | UUID | PK of affected record |
| old_data | JSONB | Previous state |
| new_data | JSONB | New state |
| created_at | TIMESTAMPTZ | NOT NULL |

---

## Normalization Analysis (NF)

### First Normal Form (1NF) ✅
All tables satisfy 1NF:
- Every column holds atomic values. Arrays and flexible data are intentionally stored in JSONB (e.g., `settings`, `default_fields`) — these are treated as opaque documents, not multi-valued attributes.
- Each table has a single-column primary key (UUID), except pure junction tables which use composite PKs.
- No repeating groups exist anywhere.

### Second Normal Form (2NF) ✅
All non-key attributes depend on the full primary key:
- Junction tables (`ROLE_PERMISSIONS`, `USER_ROLES`) contain only foreign keys or metadata that depends on the full composite key.
- `GUESTS` is fully functionally dependent on its own `id`, not partially on `program_id`.
- `GIFT_RECORDS` stores `walk_in_name` and `walk_in_gender` which are conditional on `is_walk_in=TRUE` — this is acceptable because they apply to the full record key, not a partial key.

### Third Normal Form (3NF) ✅
No transitive dependencies:
- `GUESTS.program_id → org_id` does not create a transitive issue because `org_id` is not stored on GUESTS — it is derived via join to PROGRAMS.
- `GIFT_RECORDS.program_id` and `guest_id` are direct FKs, not derived from each other.
- `PROGRAMS.public_url` should be computed (GENERATED column or application-layer) from `slug` to avoid update anomalies.
- `ORG_MEMBERS.role` is a local role scoped to that org membership — this is not a transitive dependency on ROLES table because it is a simplified enum, not a FK.

### Boyce-Codd Normal Form (BCNF) ✅
- Every determinant is a candidate key. No non-trivial FDs exist where the determinant is not a superkey.
- Potential BCNF concern: `GUESTS.guest_code` is UNIQUE (a candidate key), so `guest_code → all guest fields` is valid and does not violate BCNF.

### Denormalization decisions (intentional)
| Column | Table | Reason |
|---|---|---|
| `walk_in_name`, `walk_in_gender` | GIFT_RECORDS | Walk-ins may never become full GUESTS rows; embedding avoids orphan records |
| `table_number` | GUESTS | Read-performance shortcut; TABLE_ASSIGNMENTS is the authoritative source |
| `public_url` | PROGRAMS | Should be a GENERATED column from `slug` to avoid deviation |
| `currency` | GIFT_RECORDS, EXPENSES | Denormalized per record to support multi-currency programs |

---

## Key Indexes (recommended)

```sql
-- Guest lookup by QR or code
CREATE UNIQUE INDEX idx_guests_qr_token ON GUESTS(qr_token);
CREATE UNIQUE INDEX idx_guests_guest_code ON GUESTS(guest_code);

-- Fast gift summary per program, per gender
CREATE INDEX idx_gift_program_gender ON GIFT_RECORDS(program_id, walk_in_gender);
CREATE INDEX idx_gift_guest ON GIFT_RECORDS(guest_id);

-- Message delivery status monitoring
CREATE INDEX idx_msg_status ON MESSAGE_LOGS(program_id, status, channel);

-- Audit trail lookups
CREATE INDEX idx_audit_table_record ON AUDIT_LOGS(table_name, record_id);
CREATE INDEX idx_audit_user ON AUDIT_LOGS(user_id);

-- Program listing per org
CREATE INDEX idx_programs_org ON PROGRAMS(org_id, event_date DESC);

-- Guest listing per program, gender filter
CREATE INDEX idx_guests_program_gender ON GUESTS(program_id, gender);
```

---

## Relationship Summary

| From | To | Cardinality | Notes |
|---|---|---|---|
| USERS | ORGANIZATIONS | 1 : N | One user owns many orgs |
| ORGANIZATIONS | ORG_MEMBERS | 1 : N | Many staff per org |
| ORGANIZATIONS | PROGRAMS | 1 : N | Many events per org |
| PROGRAM_TEMPLATES | PROGRAMS | 1 : N | Template used by many programs |
| PROGRAMS | GUESTS | 1 : N | Guest list per event |
| PROGRAMS | TABLES | 1 : N | Seating layout per event |
| TABLES | TABLE_ASSIGNMENTS | 1 : N | Multiple guests per table |
| GUESTS | TABLE_ASSIGNMENTS | 1 : 1 | One active table per guest |
| PROGRAMS | GIFT_RECORDS | 1 : N | All handshake records |
| GUESTS | GIFT_RECORDS | 1 : N | One guest may give multiple gifts |
| PROGRAMS | MESSAGE_LOGS | 1 : N | All outbound messages |
| GUESTS | MESSAGE_LOGS | 1 : N | Messages per guest |
| PROGRAMS | EXPENSES | 1 : N | Cost tracking per event |
| PROGRAMS | MEDIA_ALBUMS | 1 : N | Photo albums per event |
| ROLES | ROLE_PERMISSIONS | 1 : N | Permission grants |
| USERS | USER_ROLES | M : N | Role assignment via junction |
| USERS | AUDIT_LOGS | 1 : N | All actions logged |
