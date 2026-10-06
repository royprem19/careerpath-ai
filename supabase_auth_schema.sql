-- ==============================================================================
-- CareerPath AI - Supabase Auth & Institution Schema Migration
-- Build For Bharat 2.0 | Intelligent Talent & Workforce Ecosystem
-- Run this in your Supabase SQL Editor to add auth & institution columns
-- ==============================================================================

-- 1. ADD AUTH COLUMNS TO USER_PROFILES
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS password_hash TEXT;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS role VARCHAR(30) DEFAULT 'candidate';
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS institution_name VARCHAR(150);
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS department VARCHAR(100);
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS graduation_year INTEGER DEFAULT 2026;

-- 2. CREATE INSTITUTIONS TABLE (OPTIONAL)
CREATE TABLE IF NOT EXISTS institutions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    state VARCHAR(50),
    tier VARCHAR(20) DEFAULT 'Tier-1',
    curriculum_alignment_score NUMERIC(5,2) DEFAULT 68.5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Seed top Indian academic institutions
INSERT INTO institutions (name, state, tier, curriculum_alignment_score) VALUES
('IIT Madras', 'Tamil Nadu', 'Tier-1', 78.5),
('IIT Bombay', 'Maharashtra', 'Tier-1', 79.0),
('IIT Delhi', 'Delhi', 'Tier-1', 77.8),
('BITS Pilani', 'Rajasthan', 'Tier-1', 76.2),
('Delhi Technological University (DTU)', 'Delhi', 'Tier-1', 72.4),
('VIT Vellore', 'Tamil Nadu', 'Tier-2', 68.0),
('NIT Trichy', 'Tamil Nadu', 'Tier-1', 74.5)
ON CONFLICT (name) DO NOTHING;

-- 3. ENABLE RLS
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read-write for demo" ON user_profiles FOR ALL USING (true);
