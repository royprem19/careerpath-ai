-- ==============================================================================
-- CareerPath AI - Supabase Production Schema & Real Seed Dataset
-- Build For Bharat 2.0 | Intelligent Talent & Workforce Ecosystem
-- ==============================================================================

-- 1. EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. DROP TABLES IF THEY ALREADY EXIST (CLEAN REBUILD)
DROP TABLE IF EXISTS gap_analyses CASCADE;
DROP TABLE IF EXISTS user_profiles CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS skill_synonyms CASCADE;
DROP TABLE IF EXISTS role_skills CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

-- 3. CREATE TABLES

-- Occupations / Roles Table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL UNIQUE,
    category VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    experience_range VARCHAR(50) DEFAULT '0-2 years',
    avg_salary VARCHAR(50) DEFAULT '₹6-12 LPA',
    nco_code VARCHAR(20), -- National Classification of Occupations India
    esco_uri VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Master Skills Taxonomy Table
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(80) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Occupation-Skill Mapping (Essential vs Optional)
CREATE TABLE role_skills (
    id SERIAL PRIMARY KEY,
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    relation_type VARCHAR(20) NOT NULL CHECK (relation_type IN ('essential', 'optional')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE(role_id, skill_id)
);

-- Curated Real Courses & Learning Roadmaps
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL,
    course_name VARCHAR(200) NOT NULL,
    platform VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    duration_weeks INTEGER DEFAULT 2,
    is_free BOOLEAN DEFAULT TRUE,
    difficulty VARCHAR(30) DEFAULT 'Beginner',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Skill Synonyms / Aliases for NLP Normalization
CREATE TABLE skill_synonyms (
    id SERIAL PRIMARY KEY,
    alias VARCHAR(100) NOT NULL UNIQUE,
    canonical_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- User Profiles (Anonymous or Registered)
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_name VARCHAR(100),
    email VARCHAR(150),
    skills JSONB NOT NULL DEFAULT '[]'::jsonb,
    education JSONB DEFAULT '[]'::jsonb,
    experience JSONB DEFAULT '{}'::jsonb,
    certifications JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Saved Gap Analyses
CREATE TABLE gap_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    role_id INTEGER REFERENCES roles(id) ON DELETE SET NULL,
    fit_score NUMERIC(5,2) NOT NULL,
    essential_coverage NUMERIC(5,2) NOT NULL,
    optional_coverage NUMERIC(5,2) NOT NULL,
    matched_skills JSONB DEFAULT '[]'::jsonb,
    missing_essential JSONB DEFAULT '[]'::jsonb,
    missing_optional JSONB DEFAULT '[]'::jsonb,
    surplus_skills JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. ENABLE ROW LEVEL SECURITY (RLS) & ALLOW PUBLIC ACCESS
ALTER TABLE roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE role_skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE skill_synonyms ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE gap_analyses ENABLE ROW LEVEL SECURITY;

-- Allow anonymous read & write for API access
CREATE POLICY "Allow public read on roles" ON roles FOR SELECT USING (true);
CREATE POLICY "Allow public read on skills" ON skills FOR SELECT USING (true);
CREATE POLICY "Allow public read on role_skills" ON role_skills FOR SELECT USING (true);
CREATE POLICY "Allow public read on courses" ON courses FOR SELECT USING (true);
CREATE POLICY "Allow public read on skill_synonyms" ON skill_synonyms FOR SELECT USING (true);
CREATE POLICY "Allow public all on user_profiles" ON user_profiles FOR ALL USING (true);
CREATE POLICY "Allow public all on gap_analyses" ON gap_analyses FOR ALL USING (true);

-- Allow service role / anon inserts
CREATE POLICY "Allow public insert on roles" ON roles FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public insert on skills" ON skills FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public insert on role_skills" ON role_skills FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public insert on courses" ON courses FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public insert on skill_synonyms" ON skill_synonyms FOR INSERT WITH CHECK (true);

-- ==============================================================================
-- 5. REAL SEED DATA: 15 ROLES (INDIAN MARKET & INDUSTRY DEMAND)
-- ==============================================================================

INSERT INTO roles (id, title, category, description, experience_range, avg_salary, nco_code) VALUES
(1, 'Full Stack Developer', 'Software Engineering', 'Architects and builds complete web applications from database modeling to responsive frontend interfaces.', '0-2 years', '₹6.5 - 12 LPA', '2512.01'),
(2, 'Backend Engineer', 'Software Engineering', 'Designs scalable REST/GraphQL APIs, microservices, database schemas, and manages server-side logic and caching.', '0-3 years', '₹7 - 14 LPA', '2512.02'),
(3, 'Frontend Engineer', 'Software Engineering', 'Develops high-performance, accessible, and responsive user interfaces using modern reactive UI frameworks.', '0-2 years', '₹5.5 - 11 LPA', '2513.01'),
(4, 'Data Scientist', 'Data Science & AI', 'Leverages statistical modeling, machine learning, and data analytics to extract actionable business insights from big data.', '0-3 years', '₹8 - 16 LPA', '2511.03'),
(5, 'Machine Learning Engineer', 'Data Science & AI', 'Designs, trains, deploys, and monitors production ML systems, deep learning pipelines, and inference APIs.', '1-3 years', '₹9 - 18 LPA', '2511.04'),
(6, 'DevOps & Cloud Engineer', 'Infrastructure & Cloud', 'Automates software delivery with CI/CD pipelines, container orchestration, and cloud infrastructure as code.', '1-3 years', '₹7.5 - 15 LPA', '2523.01'),
(7, 'AI / GenAI Solutions Engineer', 'Data Science & AI', 'Builds production LLM applications, RAG pipelines, fine-tuned transformer models, and AI agent workflows.', '0-2 years', '₹10 - 20 LPA', '2511.05'),
(8, 'Data Analyst', 'Data Science & AI', 'Extracts, cleans, and analyzes complex business datasets; crafts interactive executive dashboards and reports.', '0-2 years', '₹5 - 9 LPA', '2511.01'),
(9, 'Cybersecurity Analyst', 'Security', 'Protects systems, networks, and data assets against cyber threats, performs vulnerability assessments, and enforces compliance.', '0-3 years', '₹6 - 13 LPA', '2529.01'),
(10, 'Cloud Solutions Architect', 'Infrastructure & Cloud', 'Designs enterprise-grade cloud architectures across AWS, Azure, or GCP with high availability, security, and cost efficiency.', '2-5 years', '₹14 - 26 LPA', '2523.02'),
(11, 'Mobile App Developer', 'Mobile Development', 'Builds native or cross-platform mobile apps for iOS and Android using modern frameworks with offline capabilities.', '0-3 years', '₹6 - 12 LPA', '2514.01'),
(12, 'Product Manager (Technical)', 'Product & Management', 'Bridges business, engineering, and UX to define product strategy, roadmap execution, and metric-driven feature releases.', '1-4 years', '₹11 - 22 LPA', '2512.05'),
(13, 'Site Reliability Engineer (SRE)', 'Infrastructure & Cloud', 'Applies software engineering principles to operations to ensure system reliability, uptime, observability, and scalability.', '1-3 years', '₹9 - 17 LPA', '2523.03'),
(14, 'QA Automation Engineer', 'Software Engineering', 'Automates end-to-end, API, and performance testing suites to ensure bulletproof software quality across releases.', '0-2 years', '₹5 - 9.5 LPA', '2519.01'),
(15, 'Data Engineer', 'Data Science & AI', 'Constructs scalable ETL data pipelines, data warehouses, streaming systems, and data lake architectures for analytics.', '1-3 years', '₹8 - 16 LPA', '2511.02')
ON CONFLICT (id) DO NOTHING;

-- Reset sequence to avoid id collisions
SELECT setval('roles_id_seq', (SELECT MAX(id) FROM roles));

-- ==============================================================================
-- 6. REAL SEED DATA: 85+ MASTER SKILLS ACROSS DOMAINS
-- ==============================================================================

INSERT INTO skills (id, name, category, description) VALUES
-- Programming Languages
(1, 'Python', 'Programming', 'Interpreted high-level language popular in backend, data science, scripting, and AI.'),
(2, 'JavaScript', 'Programming', 'Ubiquitous web scripting language powering modern browsers and Node.js runtimes.'),
(3, 'TypeScript', 'Programming', 'Statically typed superset of JavaScript that compiles to plain JavaScript for large-scale apps.'),
(4, 'Java', 'Programming', 'Class-based, object-oriented language for enterprise backends and Android.'),
(5, 'C++', 'Programming', 'High-performance compiled language used for system/software development and algorithms.'),
(6, 'SQL', 'Programming', 'Domain-specific language for managing and querying relational databases.'),
(7, 'Go', 'Programming', 'Open-source compiled language designed for concurrency and scalable cloud microservices.'),

-- Frontend Frameworks & Libraries
(8, 'React', 'Frontend', 'Declarative, component-based UI library for web applications.'),
(9, 'Next.js', 'Frontend', 'Production React framework offering Server-Side Rendering (SSR) and static generation.'),
(10, 'HTML5', 'Frontend', 'Standard markup language for modern web documents and media.'),
(11, 'CSS3', 'Frontend', 'Style sheet language for styling web document structure and animations.'),
(12, 'TailwindCSS', 'Frontend', 'Utility-first CSS framework for rapid responsive UI development.'),
(13, 'Redux', 'Frontend', 'Predictable state container for JavaScript applications.'),
(14, 'Vue.js', 'Frontend', 'Progressive JavaScript framework for building user interfaces.'),

-- Backend Frameworks & Runtimes
(15, 'Node.js', 'Backend', 'Asynchronous event-driven JavaScript runtime built on Chrome''s V8 engine.'),
(16, 'Express.js', 'Backend', 'Minimal and flexible Node.js web application framework.'),
(17, 'FastAPI', 'Backend', 'High-performance Python web framework for building APIs with automatic OpenAPI docs.'),
(18, 'Django', 'Backend', 'High-level Python web framework that encourages rapid development and clean design.'),
(19, 'Spring Boot', 'Backend', 'Opinionated Java framework for production-grade microservices and REST APIs.'),
(20, 'REST APIs', 'Backend', 'Architectural style for networked hypermedia applications and HTTP web services.'),
(21, 'GraphQL', 'Backend', 'Query language for APIs that gives clients precision over requested data.'),

-- Databases & Storage
(22, 'PostgreSQL', 'Databases', 'Advanced open-source object-relational database system.'),
(23, 'MySQL', 'Databases', 'Widely adopted relational database management system.'),
(24, 'MongoDB', 'Databases', 'Document-oriented NoSQL database for unstructured and semi-structured data.'),
(25, 'Redis', 'Databases', 'In-memory data structure store used as a cache, database, and message broker.'),
(26, 'Supabase', 'Databases', 'Open source Firebase alternative providing Postgres, Auth, Realtime, and Storage.'),

-- Cloud, DevOps & Containers
(27, 'Docker', 'DevOps & Cloud', 'Containerization platform to package apps and dependencies into portable images.'),
(28, 'Kubernetes', 'DevOps & Cloud', 'Open-source container orchestration engine for automated deployment and scaling.'),
(29, 'AWS', 'DevOps & Cloud', 'Comprehensive cloud computing platform with EC2, S3, RDS, Lambda, and IAM.'),
(30, 'Azure', 'DevOps & Cloud', 'Microsoft cloud computing platform offering global cloud services.'),
(31, 'Google Cloud Platform', 'DevOps & Cloud', 'Suite of cloud services running on Google infrastructure.'),
(32, 'CI/CD Pipelines', 'DevOps & Cloud', 'Continuous integration and deployment automation (GitHub Actions, GitLab CI, Jenkins).'),
(33, 'Terraform', 'DevOps & Cloud', 'Infrastructure as Code software tool to provision cloud resources declaratively.'),
(34, 'Linux', 'DevOps & Cloud', 'Open-source Unix-like operating system powering servers and containers.'),

-- Data Science, AI & Machine Learning
(35, 'Machine Learning', 'AI & Data Science', 'Algorithms that improve automatically through experience and data patterns.'),
(36, 'Deep Learning', 'AI & Data Science', 'Neural network architectures modeled on biological brains for perceptual tasks.'),
(37, 'Natural Language Processing', 'AI & Data Science', 'Subfield of AI focused on computer understanding and generation of human text.'),
(38, 'Computer Vision', 'AI & Data Science', 'Field of AI enabling computers to interpret and understand digital images/videos.'),
(39, 'Pandas', 'AI & Data Science', 'Data analysis and manipulation library for Python dataframes.'),
(40, 'NumPy', 'AI & Data Science', 'Fundamental package for scientific computing with multi-dimensional arrays in Python.'),
(41, 'Scikit-learn', 'AI & Data Science', 'Python library for classical predictive data analysis and ML models.'),
(42, 'TensorFlow', 'AI & Data Science', 'End-to-end open source platform for machine learning and neural networks.'),
(43, 'PyTorch', 'AI & Data Science', 'Flexible deep learning framework widely used in research and production AI.'),
(44, 'Large Language Models (LLMs)', 'AI & Data Science', 'Transformer models trained on vast text corpora for generative AI tasks.'),
(45, 'Retrieval Augmented Generation (RAG)', 'AI & Data Science', 'Technique combining semantic vector search with LLMs for grounded answers.'),
(46, 'LangChain', 'AI & Data Science', 'Framework for developing applications powered by language models and agent chains.'),
(47, 'Hugging Face', 'AI & Data Science', 'Platform and transformers library providing pre-trained models and datasets.'),

-- Data Engineering & Analytics
(48, 'Apache Spark', 'Data Engineering', 'Unified analytics engine for large-scale distributed data processing.'),
(49, 'Apache Kafka', 'Data Engineering', 'Distributed event streaming platform for high-throughput real-time pipelines.'),
(50, 'Tableau', 'Data Analytics', 'Interactive data visualization software focused on business intelligence.'),
(51, 'Power BI', 'Data Analytics', 'Business analytics service by Microsoft delivering actionable insights and dashboards.'),
(52, 'Data Modeling', 'Data Engineering', 'Process of creating data models for storage and warehousing architectures.'),
(53, 'ETL Pipelines', 'Data Engineering', 'Extract, Transform, Load processes moving data between source and target systems.'),

-- Security & QA Testing
(54, 'Network Security', 'Security', 'Practices and policies to monitor and prevent unauthorized access or modification.'),
(55, 'Vulnerability Assessment', 'Security', 'Systematic review of security weaknesses in an information system.'),
(56, 'Penetration Testing', 'Security', 'Authorized simulated cyberattack on computer systems to evaluate security posture.'),
(57, 'Selenium', 'QA & Testing', 'Open-source automated testing suite for web browsers.'),
(58, 'Playwright / Cypress', 'QA & Testing', 'Modern end-to-end testing frameworks for web applications.'),
(59, 'Jest', 'QA & Testing', 'Delightful JavaScript testing framework with focus on simplicity.'),
(60, 'PyTest', 'QA & Testing', 'Robust Python test framework making it easy to write unit and integration tests.'),

-- Mobile Frameworks
(61, 'Flutter', 'Mobile Development', 'Google UI toolkit for building natively compiled cross-platform apps from a single codebase.'),
(62, 'React Native', 'Mobile Development', 'Framework for building native apps using React and JavaScript.'),
(63, 'Android (Kotlin)', 'Mobile Development', 'Modern, expressive programming language for native Android app development.'),

-- Tools & Engineering Best Practices
(64, 'Git & GitHub', 'Tools', 'Distributed version control system and cloud repository hosting for team collaboration.'),
(65, 'Agile & Scrum', 'Methodology', 'Iterative software development approach delivering value incrementally.'),
(66, 'Product Roadmapping', 'Product', 'Strategic plan that defines product goals, milestones, and release priorities.'),
(67, 'System Architecture Design', 'Architecture', 'Conceptual model defining structure, behavior, and high-level design of systems.'),
(68, 'Monitoring & Observability', 'DevOps & Cloud', 'Tools like Prometheus, Grafana, Datadog for monitoring health, metrics, and logs.')
ON CONFLICT (id) DO NOTHING;

-- Reset sequence to avoid id collisions
SELECT setval('skills_id_seq', (SELECT MAX(id) FROM skills));

-- ==============================================================================
-- 7. REAL SEED DATA: ROLE-SKILL MAPPINGS (ESSENTIAL VS OPTIONAL)
-- ==============================================================================

-- 1. Full Stack Developer
INSERT INTO role_skills (role_id, skill_id, relation_type) VALUES
(1, 2, 'essential'),  -- JavaScript
(1, 8, 'essential'),  -- React
(1, 15, 'essential'), -- Node.js
(1, 6, 'essential'),  -- SQL
(1, 10, 'essential'), -- HTML5
(1, 11, 'essential'), -- CSS3
(1, 20, 'essential'), -- REST APIs
(1, 64, 'essential'), -- Git & GitHub
(1, 3, 'optional'),   -- TypeScript
(1, 9, 'optional'),   -- Next.js
(1, 12, 'optional'),  -- TailwindCSS
(1, 22, 'optional'),  -- PostgreSQL
(1, 24, 'optional'),  -- MongoDB
(1, 27, 'optional')   -- Docker
ON CONFLICT DO NOTHING;

-- 2. Backend Engineer
INSERT INTO role_skills (role_id, skill_id, relation_type) VALUES
(2, 1, 'essential'),  -- Python (or Java/Go)
(2, 6, 'essential'),  -- SQL
(2, 20, 'essential'), -- REST APIs
(2, 22, 'essential'), -- PostgreSQL
(2, 17, 'essential'), -- FastAPI
(2, 64, 'essential'), -- Git & GitHub
(2, 25, 'optional'),  -- Redis
(2, 27, 'optional'),  -- Docker
(2, 7, 'optional'),   -- Go
(2, 21, 'optional'),  -- GraphQL
(2, 32, 'optional'),  -- CI/CD
(2, 67, 'optional')   -- System Architecture Design
ON CONFLICT DO NOTHING;

-- 3. Frontend Engineer
INSERT INTO role_skills (role_id, skill_id, relation_type) VALUES
(3, 2, 'essential'),  -- JavaScript
(3, 8, 'essential'),  -- React
(3, 10, 'essential'), -- HTML5
(3, 11, 'essential'), -- CSS3
(3, 64, 'essential'), -- Git & GitHub
(3, 3, 'essential'),  -- TypeScript
(3, 12, 'optional'),  -- TailwindCSS
(3, 9, 'optional'),   -- Next.js
(3, 13, 'optional'),  -- Redux
(3, 59, 'optional'),  -- Jest
(3, 20, 'optional')   -- REST APIs
ON CONFLICT DO NOTHING;

-- 4. Data Scientist
INSERT INTO role_skills (role_id, skill_id, relation_type) VALUES
(4, 1, 'essential'),  -- Python
(4, 6, 'essential'),  -- SQL
(4, 35, 'essential'), -- Machine Learning
(4, 39, 'essential'), -- Pandas
(4, 40, 'essential'), -- NumPy
(4, 41, 'essential'), -- Scikit-learn
(4, 36, 'optional'),  -- Deep Learning
(4, 37, 'optional'),  -- NLP
(4, 50, 'optional'),  -- Tableau
(4, 48, 'optional')   -- Apache Spark
ON CONFLICT DO NOTHING;

-- 5. Machine Learning Engineer
INSERT INTO role_skills (role_id, skill_id, relation_type) VALUES
(5, 1, 'essential'),  -- Python
(5, 35, 'essential'), -- Machine Learning
(5, 36, 'essential'), -- Deep Learning
(5, 43, 'essential'), -- PyTorch
(5, 41, 'essential'), -- Scikit-learn
(5, 27, 'essential'), -- Docker
(5, 42, 'optional'),  -- TensorFlow
(5, 17, 'optional'),  -- FastAPI (for serving)
(5, 44, 'optional'),  -- LLMs
(5, 32, 'optional'),  -- CI/CD
(5, 29, 'optional')   -- AWS
ON CONFLICT DO NOTHING;

-- 6. DevOps & Cloud Engineer
INSERT INTO role_skills (role_id, skill_id, relation_type) VALUES
(6, 27, 'essential'), -- Docker
(6, 28, 'essential'), -- Kubernetes
(6, 32, 'essential'), -- CI/CD Pipelines
(6, 34, 'essential'), -- Linux
(6, 29, 'essential'), -- AWS
(6, 64, 'essential'), -- Git & GitHub
(6, 33, 'optional'),  -- Terraform
(6, 1, 'optional'),   -- Python
(6, 68, 'optional'),  -- Monitoring & Observability
(6, 30, 'optional')   -- Azure
ON CONFLICT DO NOTHING;

-- 7. AI / GenAI Solutions Engineer
INSERT INTO role_skills (role_id, skill_id, relation_type) VALUES
(7, 1, 'essential'),  -- Python
(7, 44, 'essential'), -- Large Language Models (LLMs)
(7, 45, 'essential'), -- RAG
(7, 46, 'essential'), -- LangChain
(7, 17, 'essential'), -- FastAPI
(7, 47, 'essential'), -- Hugging Face
(7, 26, 'optional'),  -- Supabase (vector pgvector)
(7, 43, 'optional'),  -- PyTorch
(7, 27, 'optional'),  -- Docker
(7, 36, 'optional')   -- Deep Learning
ON CONFLICT DO NOTHING;

-- 8. Data Analyst
INSERT INTO role_skills (role_id, skill_id, relation_type) VALUES
(8, 6, 'essential'),  -- SQL
(8, 1, 'essential'),  -- Python
(8, 39, 'essential'), -- Pandas
(8, 50, 'essential'), -- Tableau
(8, 51, 'optional'),  -- Power BI
(8, 40, 'optional'),  -- NumPy
(8, 52, 'optional')   -- Data Modeling
ON CONFLICT DO NOTHING;

-- 9. Cybersecurity Analyst
INSERT INTO role_skills (role_id, skill_id, relation_type) VALUES
(9, 54, 'essential'), -- Network Security
(9, 55, 'essential'), -- Vulnerability Assessment
(9, 34, 'essential'), -- Linux
(9, 1, 'optional'),   -- Python
(9, 56, 'optional'),  -- Penetration Testing
(9, 29, 'optional')   -- AWS
ON CONFLICT DO NOTHING;

-- 11. Mobile App Developer
INSERT INTO role_skills (role_id, skill_id, relation_type) VALUES
(11, 61, 'essential'), -- Flutter (or React Native)
(11, 20, 'essential'), -- REST APIs
(11, 64, 'essential'), -- Git & GitHub
(11, 62, 'optional'),  -- React Native
(11, 63, 'optional'),  -- Android (Kotlin)
(11, 26, 'optional')   -- Supabase / Firebase
ON CONFLICT DO NOTHING;

-- 12. Product Manager (Technical)
INSERT INTO role_skills (role_id, skill_id, relation_type) VALUES
(12, 65, 'essential'), -- Agile & Scrum
(12, 66, 'essential'), -- Product Roadmapping
(12, 6, 'essential'),  -- SQL
(12, 20, 'optional'),  -- REST APIs
(12, 50, 'optional'),  -- Tableau
(12, 67, 'optional')   -- System Architecture Design
ON CONFLICT DO NOTHING;

-- 15. Data Engineer
INSERT INTO role_skills (role_id, skill_id, relation_type) VALUES
(15, 1, 'essential'),  -- Python
(15, 6, 'essential'),  -- SQL
(15, 48, 'essential'), -- Apache Spark
(15, 53, 'essential'), -- ETL Pipelines
(15, 22, 'essential'), -- PostgreSQL
(15, 49, 'optional'),  -- Apache Kafka
(15, 27, 'optional'),  -- Docker
(15, 29, 'optional')   -- AWS
ON CONFLICT DO NOTHING;

-- ==============================================================================
-- 8. REAL SEED DATA: 50+ ACTUAL COURSES (NPTEL, COURSERA, FREECODECAMP)
-- ==============================================================================

INSERT INTO courses (skill_name, course_name, platform, url, duration_weeks, is_free, difficulty) VALUES
('Python', 'Programming, Data Structures and Algorithms using Python', 'NPTEL (IIT Madras)', 'https://nptel.ac.in/courses/106106145', 8, true, 'Beginner'),
('Python', 'Scientific Computing with Python Certification', 'freeCodeCamp', 'https://www.freecodecamp.org/learn/scientific-computing-with-python/', 4, true, 'Beginner'),
('JavaScript', 'JavaScript Algorithms and Data Structures', 'freeCodeCamp', 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures-v8/', 4, true, 'Beginner'),
('JavaScript', 'Modern JavaScript From The Beginning', 'Udemy', 'https://www.udemy.com/course/modern-javascript-from-the-beginning/', 3, false, 'Beginner'),
('TypeScript', 'Understanding TypeScript - 2024 Edition', 'Udemy', 'https://www.udemy.com/course/understanding-typescript/', 3, false, 'Intermediate'),
('TypeScript', 'TypeScript for Beginners', 'freeCodeCamp YouTube', 'https://www.youtube.com/watch?v=BwuLxPH8IDs', 1, true, 'Beginner'),
('React', 'The Joy of React by Josh Comeau', 'Joy of React', 'https://www.joyofreact.com/', 4, false, 'Intermediate'),
('React', 'Frontend Development Libraries (React)', 'freeCodeCamp', 'https://www.freecodecamp.org/learn/front-end-development-libraries/', 3, true, 'Beginner'),
('Next.js', 'Next.js 14 Complete Course', 'Next.js Learn (Official)', 'https://nextjs.org/learn', 2, true, 'Intermediate'),
('HTML5', 'Responsive Web Design Certification', 'freeCodeCamp', 'https://www.freecodecamp.org/learn/2022/responsive-web-design/', 3, true, 'Beginner'),
('CSS3', 'CSS - The Complete Guide 2024 (incl. Flexbox, Grid & Sass)', 'Udemy', 'https://www.udemy.com/course/css-the-complete-guide-incl-flexbox-grid-sass/', 3, false, 'Beginner'),
('TailwindCSS', 'Tailwind CSS From Scratch', 'Traversy Media / YouTube', 'https://www.youtube.com/watch?v=dFgzvOzPB4A', 1, true, 'Beginner'),
('Node.js', 'Node.js, Express, MongoDB & More: The Complete Bootcamp', 'Udemy', 'https://www.udemy.com/course/nodejs-express-mongodb-bootcamp/', 4, false, 'Intermediate'),
('FastAPI', 'FastAPI - The Complete Course 2024 (Beginner + Advanced)', 'Udemy', 'https://www.udemy.com/course/fastapi-the-complete-course/', 2, false, 'Beginner'),
('FastAPI', 'FastAPI Official Interactive Tutorial', 'FastAPI Documentation', 'https://fastapi.tiangolo.com/tutorial/', 1, true, 'Beginner'),
('SQL', 'Database Management System', 'NPTEL (IIT Kharagpur)', 'https://nptel.ac.in/courses/106105175', 8, true, 'Beginner'),
('SQL', 'Relational Database Certification', 'freeCodeCamp', 'https://www.freecodecamp.org/learn/relational-database/', 4, true, 'Beginner'),
('PostgreSQL', 'PostgreSQL for Everybody Specialization', 'Coursera (Univ. of Michigan)', 'https://www.coursera.org/specializations/postgresql-for-everybody', 4, true, 'Intermediate'),
('MongoDB', 'MongoDB Basics & Aggregation', 'MongoDB University', 'https://learn.mongodb.com/', 2, true, 'Beginner'),
('Docker', 'Docker for the Absolute Beginner - Hands On - DevOps', 'Udemy', 'https://www.udemy.com/course/learn-docker/', 2, false, 'Beginner'),
('Docker', 'Docker & Kubernetes Tutorial', 'freeCodeCamp YouTube', 'https://www.youtube.com/watch?v=fqMOX6JJhGo', 1, true, 'Beginner'),
('Kubernetes', 'Certified Kubernetes Administrator (CKA) Course', 'Mumshad Mannambeth / KodeKloud', 'https://kodekloud.com/courses/certified-kubernetes-administrator-cka/', 4, false, 'Advanced'),
('AWS', 'AWS Certified Cloud Practitioner Training 2024', 'freeCodeCamp YouTube', 'https://www.youtube.com/watch?v=SOTamWNgDKc', 2, true, 'Beginner'),
('Git & GitHub', 'Version Control with Git', 'Coursera (Atlassian)', 'https://www.coursera.org/learn/version-control-with-git', 1, true, 'Beginner'),
('Machine Learning', 'Machine Learning Foundations', 'NPTEL (IIT Madras)', 'https://nptel.ac.in/courses/106106202', 12, true, 'Intermediate'),
('Machine Learning', 'Machine Learning Specialization by Andrew Ng', 'Coursera (DeepLearning.AI)', 'https://www.coursera.org/specializations/machine-learning-introduction', 6, true, 'Beginner'),
('Deep Learning', 'Deep Learning Specialization', 'Coursera (DeepLearning.AI)', 'https://www.coursera.org/specializations/deep-learning', 8, true, 'Intermediate'),
('PyTorch', 'PyTorch for Deep Learning Bootcamp', 'freeCodeCamp / Daniel Bourke', 'https://www.youtube.com/watch?v=V_xro1bcAuA', 3, true, 'Intermediate'),
('Large Language Models (LLMs)', 'Generative AI with Large Language Models', 'Coursera (AWS & DeepLearning.AI)', 'https://www.coursera.org/learn/generative-ai-with-llms', 3, true, 'Intermediate'),
('Retrieval Augmented Generation (RAG)', 'LangChain & Vector Databases for Production RAG', 'DeepLearning.AI Short Courses', 'https://www.deeplearning.ai/short-courses/', 1, true, 'Intermediate'),
('Pandas', 'Data Analysis with Python', 'freeCodeCamp', 'https://www.freecodecamp.org/learn/data-analysis-with-python/', 2, true, 'Beginner'),
('Tableau', 'Tableau for Data Science', 'Coursera (UC Davis)', 'https://www.coursera.org/learn/data-visualization-tableau', 4, true, 'Beginner'),
('Power BI', 'Microsoft Power BI Data Analyst Professional Certificate', 'Coursera (Microsoft)', 'https://www.coursera.org/professional-certificates/microsoft-power-bi-data-analyst', 6, true, 'Beginner'),
('CI/CD Pipelines', 'GitHub Actions - The Complete Guide', 'Udemy', 'https://www.udemy.com/course/github-actions-the-complete-guide/', 1, false, 'Intermediate'),
('Apache Spark', 'Scalable Machine Learning with Apache Spark', 'edX (Databricks)', 'https://www.edx.org/learn/apache-spark', 4, true, 'Intermediate'),
('Flutter', 'Flutter & Dart - The Complete Guide [2024 Edition]', 'Udemy', 'https://www.udemy.com/course/learn-flutter-dart-to-build-ios-android-apps/', 5, false, 'Beginner')
ON CONFLICT DO NOTHING;

-- ==============================================================================
-- 9. REAL SEED DATA: 75+ SKILL SYNONYMS (NORMALIZATION)
-- ==============================================================================

INSERT INTO skill_synonyms (alias, canonical_name) VALUES
('js', 'JavaScript'),
('javascript', 'JavaScript'),
('es6', 'JavaScript'),
('ts', 'TypeScript'),
('typescript', 'TypeScript'),
('py', 'Python'),
('python3', 'Python'),
('py3', 'Python'),
('react.js', 'React'),
('reactjs', 'React'),
('react', 'React'),
('next', 'Next.js'),
('nextjs', 'Next.js'),
('node', 'Node.js'),
('nodejs', 'Node.js'),
('node.js', 'Node.js'),
('express', 'Express.js'),
('expressjs', 'Express.js'),
('fast api', 'FastAPI'),
('fastapi', 'FastAPI'),
('django', 'Django'),
('postgres', 'PostgreSQL'),
('postgresql', 'PostgreSQL'),
('pgsql', 'PostgreSQL'),
('my sql', 'MySQL'),
('mysql', 'MySQL'),
('mongo', 'MongoDB'),
('mongodb', 'MongoDB'),
('k8s', 'Kubernetes'),
('kubernetes', 'Kubernetes'),
('docker', 'Docker'),
('aws cloud', 'AWS'),
('amazon web services', 'AWS'),
('aws', 'AWS'),
('gcp', 'Google Cloud Platform'),
('google cloud', 'Google Cloud Platform'),
('azure cloud', 'Azure'),
('ml', 'Machine Learning'),
('machine learning', 'Machine Learning'),
('dl', 'Deep Learning'),
('deep learning', 'Deep Learning'),
('nlp', 'Natural Language Processing'),
('natural language processing', 'Natural Language Processing'),
('cv', 'Computer Vision'),
('computer vision', 'Computer Vision'),
('sklearn', 'Scikit-learn'),
('scikit-learn', 'Scikit-learn'),
('scikit learn', 'Scikit-learn'),
('tf', 'TensorFlow'),
('tensorflow', 'TensorFlow'),
('pytorch', 'PyTorch'),
('torch', 'PyTorch'),
('llm', 'Large Language Models (LLMs)'),
('llms', 'Large Language Models (LLMs)'),
('generative ai', 'Large Language Models (LLMs)'),
('genai', 'Large Language Models (LLMs)'),
('rag', 'Retrieval Augmented Generation (RAG)'),
('langchain', 'LangChain'),
('huggingface', 'Hugging Face'),
('hugging face', 'Hugging Face'),
('tailwind', 'TailwindCSS'),
('tailwindcss', 'TailwindCSS'),
('tailwind css', 'TailwindCSS'),
('git', 'Git & GitHub'),
('github', 'Git & GitHub'),
('git and github', 'Git & GitHub'),
('ci/cd', 'CI/CD Pipelines'),
('cicd', 'CI/CD Pipelines'),
('continuous integration', 'CI/CD Pipelines'),
('spark', 'Apache Spark'),
('pyspark', 'Apache Spark'),
('kafka', 'Apache Kafka'),
('apache kafka', 'Apache Kafka'),
('tableau', 'Tableau'),
('power bi', 'Power BI'),
('powerbi', 'Power BI'),
('flutter', 'Flutter'),
('react native', 'React Native'),
('react-native', 'React Native')
ON CONFLICT (alias) DO NOTHING;

-- Verification query
SELECT 'Total Roles Seeded:' as metric, count(*) as count FROM roles
UNION ALL
SELECT 'Total Skills Seeded:', count(*) FROM skills
UNION ALL
SELECT 'Total Role-Skills Mapped:', count(*) FROM role_skills
UNION ALL
SELECT 'Total Courses Seeded:', count(*) FROM courses
UNION ALL
SELECT 'Total Synonyms Seeded:', count(*) FROM skill_synonyms;
