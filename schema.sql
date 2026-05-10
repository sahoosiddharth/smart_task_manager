-- ═══════════════════════════════════════════════════════════
-- Smart Task Management System — Database Schema
-- Run: psql -U postgres -d smart_task_db -f schema.sql
-- ═══════════════════════════════════════════════════════════

-- Create database (run separately if needed)
-- CREATE DATABASE smart_task_db;

-- ── Users Table ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id         SERIAL PRIMARY KEY,                        -- primary key
    username   VARCHAR(100) UNIQUE NOT NULL,
    email      VARCHAR(150) UNIQUE NOT NULL,
    password   VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP        -- timestamp
);

-- ── Tasks Table ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS tasks (
    id           SERIAL PRIMARY KEY,                      -- primary key
    user_id      INTEGER NOT NULL
                   REFERENCES users(id) ON DELETE CASCADE, -- foreign key
    title        VARCHAR(200) NOT NULL,
    description  TEXT,
    priority     VARCHAR(20)
                   CHECK (priority IN ('low','medium','high'))
                   DEFAULT 'medium',
    status       VARCHAR(20)
                   CHECK (status IN ('pending','in_progress','completed'))
                   DEFAULT 'pending',
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- timestamp
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP      -- timestamp
);

-- ── Indexes for faster queries ─────────────────────────────
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status  ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
