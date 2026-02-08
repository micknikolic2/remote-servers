-- 001_initial_schema.sql
-- Remote Servers Marketplace - Initial PostgreSQL Schema

------------------------------------------------------------
-- 0. Extensions
------------------------------------------------------------

CREATE EXTENSION IF NOT EXISTS pgcrypto;  -- for gen_random_uuid()


------------------------------------------------------------
-- 1. Table: users
------------------------------------------------------------

CREATE TABLE users (
    customer_id         UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    email               TEXT            NOT NULL UNIQUE,
    organization_name   TEXT,
    is_billing_account  BOOLEAN         NOT NULL DEFAULT FALSE,
    signup_date         TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Indexes for users
CREATE INDEX IF NOT EXISTS idx_users_signup_date
    ON users (signup_date);


------------------------------------------------------------
-- 2. Table: machines
------------------------------------------------------------

CREATE TABLE machines (
    hardware_id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id            UUID        NOT NULL,
    gpu_model              TEXT,
    cpu_model              TEXT,
    ram_gb                 INTEGER     NOT NULL CHECK (ram_gb > 0),
    disk_type              TEXT,
    disk_size_gb           INTEGER     CHECK (disk_size_gb IS NULL OR disk_size_gb > 0),
    network_bandwidth      TEXT,
    os                     TEXT,
    provider_agent_status  TEXT        NOT NULL DEFAULT 'offline',
    health_indicators      JSONB,

    CONSTRAINT fk_machines_customer
        FOREIGN KEY (customer_id)
        REFERENCES users (customer_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_provider_agent_status
        CHECK (provider_agent_status IN ('online', 'offline'))
);

-- Indexes for machines
CREATE INDEX IF NOT EXISTS idx_machines_customer_id
    ON machines (customer_id);

CREATE INDEX IF NOT EXISTS idx_machines_status
    ON machines (provider_agent_status);


------------------------------------------------------------
-- 3. Table: listings
------------------------------------------------------------

CREATE TABLE listings (
    listing_id      UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    hardware_id     UUID            NOT NULL,
    price_hour      NUMERIC(12,2),
    price_day       NUMERIC(12,2),
    price_week      NUMERIC(12,2),
    currency        CHAR(3)         NOT NULL DEFAULT 'EUR',
    status          TEXT            NOT NULL DEFAULT 'active',
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ,

    CONSTRAINT fk_listings_hardware
        FOREIGN KEY (hardware_id)
        REFERENCES machines (hardware_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_listing_status
        CHECK (status IN ('active', 'paused', 'archived')),

    CONSTRAINT chk_listing_price_non_negative
        CHECK (
            (price_hour IS NULL OR price_hour >= 0) AND
            (price_day  IS NULL OR price_day  >= 0) AND
            (price_week IS NULL OR price_week >= 0)
        )
);

-- Indexes for listings
CREATE INDEX IF NOT EXISTS idx_listings_hardware_id
    ON listings (hardware_id);

CREATE INDEX IF NOT EXISTS idx_listings_status
    ON listings (status);

CREATE INDEX IF NOT EXISTS idx_listings_created_at
    ON listings (created_at);


------------------------------------------------------------
-- 4. Table: bookings
------------------------------------------------------------

CREATE TABLE bookings (
    booking_id        UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    listing_id        UUID            NOT NULL,
    hardware_id       UUID            NOT NULL,
    buyer_id          UUID            NOT NULL,
    start_timestamp   TIMESTAMPTZ     NOT NULL,
    end_timestamp     TIMESTAMPTZ     NOT NULL,
    created_at        TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    booking_status    TEXT            NOT NULL DEFAULT 'pending',

    CONSTRAINT fk_bookings_listing
        FOREIGN KEY (listing_id)
        REFERENCES listings (listing_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_bookings_hardware
        FOREIGN KEY (hardware_id)
        REFERENCES machines (hardware_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_bookings_buyer
        FOREIGN KEY (buyer_id)
        REFERENCES users (customer_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_booking_status
        CHECK (booking_status IN ('pending', 'active', 'completed', 'canceled', 'disputed')),

    CONSTRAINT chk_booking_times
        CHECK (end_timestamp > start_timestamp)
);

-- Indexes for bookings
CREATE INDEX IF NOT EXISTS idx_bookings_listing_id
    ON bookings (listing_id);

CREATE INDEX IF NOT EXISTS idx_bookings_hardware_id
    ON bookings (hardware_id);

CREATE INDEX IF NOT EXISTS idx_bookings_buyer_id
    ON bookings (buyer_id);

CREATE INDEX IF NOT EXISTS idx_bookings_status
    ON bookings (booking_status);

CREATE INDEX IF NOT EXISTS idx_bookings_start_end
    ON bookings (start_timestamp, end_timestamp);


------------------------------------------------------------
-- 5. Table: benchmarks
------------------------------------------------------------

CREATE TABLE benchmarks (
    benchmark_id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    hardware_id               UUID            NOT NULL,
    gpu_throughput_fp16       NUMERIC(18,4),
    gpu_throughput_fp32       NUMERIC(18,4),
    cpu_score                 NUMERIC(18,4),
    disk_read_mb_s            NUMERIC(18,4),
    disk_write_mb_s           NUMERIC(18,4),
    network_bandwidth_gbps    NUMERIC(18,4),
    collected_at              TIMESTAMPTZ     NOT NULL,
    admin_verification_status TEXT            NOT NULL DEFAULT 'pending',
    verified_by_admin_id      UUID,

    CONSTRAINT fk_benchmarks_hardware
        FOREIGN KEY (hardware_id)
        REFERENCES machines (hardware_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_benchmarks_verified_by
        FOREIGN KEY (verified_by_admin_id)
        REFERENCES users (customer_id)
        ON DELETE SET NULL,

    CONSTRAINT chk_benchmark_status
        CHECK (admin_verification_status IN ('pending', 'approved', 'rejected'))
);

-- Indexes for benchmarks
CREATE INDEX IF NOT EXISTS idx_benchmarks_hardware_id
    ON benchmarks (hardware_id);

CREATE INDEX IF NOT EXISTS idx_benchmarks_collected_at
    ON benchmarks (collected_at);

CREATE INDEX IF NOT EXISTS idx_benchmarks_status
    ON benchmarks (admin_verification_status);


------------------------------------------------------------
-- 6. Table: payments
------------------------------------------------------------

CREATE TABLE payments (
    payment_id      UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id      UUID            NOT NULL,
    hardware_id     UUID            NOT NULL,
    payer_id        UUID            NOT NULL,
    provider_id     UUID,
    amount_total    NUMERIC(12,2)   NOT NULL CHECK (amount_total >= 0),
    currency        CHAR(3)         NOT NULL DEFAULT 'EUR',
    payment_status  TEXT            NOT NULL DEFAULT 'incomplete',
    timestamp       TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    invoice_number  TEXT,

    CONSTRAINT fk_payments_booking
        FOREIGN KEY (booking_id)
        REFERENCES bookings (booking_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_payments_hardware
        FOREIGN KEY (hardware_id)
        REFERENCES machines (hardware_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_payments_payer
        FOREIGN KEY (payer_id)
        REFERENCES users (customer_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_payments_provider
        FOREIGN KEY (provider_id)
        REFERENCES users (customer_id)
        ON DELETE SET NULL,

    CONSTRAINT chk_payment_status
        CHECK (payment_status IN ('incomplete', 'paid', 'failed'))
);

-- Indexes for payments
CREATE INDEX IF NOT EXISTS idx_payments_booking_id
    ON payments (booking_id);

CREATE INDEX IF NOT EXISTS idx_payments_payer_id
    ON payments (payer_id);

CREATE INDEX IF NOT EXISTS idx_payments_provider_id
    ON payments (provider_id);

CREATE INDEX IF NOT EXISTS idx_payments_timestamp
    ON payments (timestamp);

CREATE INDEX IF NOT EXISTS idx_payments_status
    ON payments (payment_status);


------------------------------------------------------------
-- 7. Table: data_wipes
------------------------------------------------------------

CREATE TABLE data_wipes (
    wipe_id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    hardware_id          UUID            NOT NULL,
    booking_id           UUID,
    timestamp            TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    wipe_method_executed TEXT            NOT NULL,
    status               TEXT            NOT NULL DEFAULT 'success',
    wipe_evidence_uri    TEXT,

    CONSTRAINT fk_data_wipes_hardware
        FOREIGN KEY (hardware_id)
        REFERENCES machines (hardware_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_data_wipes_booking
        FOREIGN KEY (booking_id)
        REFERENCES bookings (booking_id)
        ON DELETE SET NULL,

    CONSTRAINT chk_data_wipes_status
        CHECK (status IN ('success', 'failed', 'partial'))
);

-- Indexes for data_wipes
CREATE INDEX IF NOT EXISTS idx_data_wipes_hardware_id
    ON data_wipes (hardware_id);

CREATE INDEX IF NOT EXISTS idx_data_wipes_booking_id
    ON data_wipes (booking_id);

CREATE INDEX IF NOT EXISTS idx_data_wipes_timestamp
    ON data_wipes (timestamp);

CREATE INDEX IF NOT EXISTS idx_data_wipes_status
    ON data_wipes (status);
