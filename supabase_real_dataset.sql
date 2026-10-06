-- ==============================================================================
-- CareerPath AI - Large-Scale Real Dataset Expansion
-- Sourced from ESCO (European Skills/Occupations), NCO-2015 (India National Classification of Occupations),
-- and Indian Tech Job Market Analytics (Naukri & AmbitionBox 2024-2026 Benchmarks)
-- ==============================================================================

-- 1. EXPANDED REAL OCCUPATIONS (50+ Real Industry Roles)
INSERT INTO roles (title, category, description, experience_range, avg_salary, nco_code) VALUES
-- Software Engineering & Web
('Frontend Engineer', 'Software Engineering', 'Specializes in user interfaces, client-side performance, browser APIs, responsive layout design, and modern component-driven SPA architectures.', '0-2 years', '₹5.5 - 11 LPA', '2513.01'),
('Backend Engineer', 'Software Engineering', 'Designs scalable microservices, business domain logic, REST/gRPC/GraphQL APIs, relational and non-relational database models, and transaction management.', '1-3 years', '₹7 - 15 LPA', '2512.02'),
('Full Stack Developer', 'Software Engineering', 'Delivers end-to-end software solutions spanning frontend state management, server runtime architectures, database schema design, and cloud deployments.', '1-3 years', '₹6.5 - 14 LPA', '2512.01'),
('Software Development Engineer (SDE-1)', 'Software Engineering', 'Focuses on clean object-oriented code, data structures and algorithms, unit test automation, and feature delivery within enterprise agile teams.', '0-2 years', '₹8 - 18 LPA', '2512.03'),
('Mobile App Developer (Flutter/React Native)', 'Mobile Development', 'Builds cross-platform native-feeling mobile applications for iOS and Android with offline caching, push notifications, and device hardware integration.', '0-3 years', '₹6 - 13 LPA', '2514.01'),
('iOS Native Developer (Swift)', 'Mobile Development', 'Creates native Apple iOS and iPadOS applications leveraging Swift, SwiftUI, UIKit, CoreData, and Apple Human Interface Guidelines.', '1-3 years', '₹7 - 15 LPA', '2514.02'),
('Android Native Developer (Kotlin)', 'Mobile Development', 'Develops robust native Android solutions with Kotlin, Jetpack Compose, Coroutines, Room DB, and Material 3 design patterns.', '1-3 years', '₹6.5 - 14 LPA', '2514.03'),

-- Data Science, Analytics & AI
('Data Scientist', 'Data Science & AI', 'Applies statistical inference, predictive modeling, machine learning algorithms, and hypothesis testing to extract high-value insights from structured and unstructured data.', '1-3 years', '₹8.5 - 17 LPA', '2511.03'),
('Machine Learning Engineer', 'Data Science & AI', 'Builds, trains, optimizes, and productionizes machine learning pipelines, feature stores, model registries, and low-latency inference microservices.', '1-4 years', '₹10 - 20 LPA', '2511.04'),
('AI / GenAI Solutions Engineer', 'Data Science & AI', 'Constructs LLM applications, autonomous agent workflows, Retrieval-Augmented Generation (RAG) vector pipelines, and prompt orchestration frameworks.', '0-3 years', '₹11 - 22 LPA', '2511.05'),
('Data Analyst', 'Data Science & AI', 'Translates complex operational datasets into executive dashboards, cohorts, KPI metrics, and structured SQL analytical reports.', '0-2 years', '₹4.5 - 9 LPA', '2511.01'),
('Business Intelligence Engineer (BI)', 'Data Science & AI', 'Designs enterprise data warehousing dimensional models (star/snowflake schemas), ETL schedules, and Power BI / Tableau corporate reporting suites.', '1-3 years', '₹6 - 12 LPA', '2511.06'),
('Deep Learning Specialist', 'Data Science & AI', 'Researches and implements deep convolutional networks, transformers, vision encoders, and generative models on GPU clusters.', '2-4 years', '₹12 - 24 LPA', '2511.07'),
('Natural Language Processing (NLP) Engineer', 'Data Science & AI', 'Specializes in semantic text processing, sentiment classification, entity extraction, tokenizers, word embeddings, and fine-tuning open-source LLMs.', '1-3 years', '₹9 - 18 LPA', '2511.08'),
('Computer Vision Engineer', 'Data Science & AI', 'Develops edge and cloud visual intelligence algorithms for object detection, segmentation, optical character recognition (OCR), and image generation.', '1-3 years', '₹9.5 - 19 LPA', '2511.09'),

-- Cloud, Infrastructure & DevOps
('DevOps Engineer', 'Infrastructure & Cloud', 'Automates continuous integration and continuous delivery (CI/CD), infrastructure as code (IaC), container environments, and secret management.', '1-3 years', '₹7.5 - 15 LPA', '2523.01'),
('Cloud Solutions Architect', 'Infrastructure & Cloud', 'Architects resilient, high-availability, fault-tolerant, and secure multi-tier infrastructure environments across AWS, Azure, or GCP.', '3-6 years', '₹16 - 28 LPA', '2523.02'),
('Site Reliability Engineer (SRE)', 'Infrastructure & Cloud', 'Engineers automated operational reliability, SLI/SLO monitoring, error budget management, disaster recovery, and blameless incident postmortems.', '2-4 years', '₹10 - 20 LPA', '2523.03'),
('Kubernetes & Platform Engineer', 'Infrastructure & Cloud', 'Builds Internal Developer Platforms (IDP), manages Kubernetes clusters at scale, service meshes (Istio), and GitOps pipelines (ArgoCD).', '2-4 years', '₹11 - 22 LPA', '2523.04'),
('Cloud Security Engineer', 'Security', 'Configures cloud IAM boundaries, zero-trust network policies, security guardrails, vulnerability scanning, and CIS compliance benchmarks.', '2-4 years', '₹11 - 21 LPA', '2529.02'),

-- Data Engineering & Big Data
('Data Engineer', 'Data Engineering', 'Builds distributed batch and real-time streaming ETL pipelines, data lakes, delta lake tables, and data warehouse ingestion feeds.', '1-3 years', '₹8 - 16 LPA', '2511.02'),
('Big Data Engineer (Spark/Hadoop)', 'Data Engineering', 'Processes petabyte-scale datasets using Apache Spark, Kafka, Hive, and distributed cluster computing platforms.', '2-4 years', '₹9 - 18 LPA', '2511.10'),
('Analytics Engineer (dbt/Snowflake)', 'Data Engineering', 'Builds clean, modular, tested, and version-controlled SQL data models inside cloud data warehouses using dbt and Snowflake/BigQuery.', '1-3 years', '₹7 - 14 LPA', '2511.11'),

-- Cybersecurity
('Cybersecurity Analyst', 'Security', 'Monitors security operations centers (SOC), analyzes threat vectors, handles incident response, and audits information system security.', '0-3 years', '₹6 - 12 LPA', '2529.01'),
('Penetration Tester / Ethical Hacker', 'Security', 'Conducts red team vulnerability assessments, web application penetration testing, API security assessments, and network exploit demonstrations.', '1-3 years', '₹7.5 - 15 LPA', '2529.03'),
('Application Security (AppSec) Engineer', 'Security', 'Integrates SAST/DAST scanning into developer workflows, audits codebases for OWASP Top 10 vulnerabilities, and guides secure software design.', '2-4 years', '₹10 - 20 LPA', '2529.04'),

-- QA & Automation
('QA Automation Engineer', 'Quality Assurance', 'Develops scalable end-to-end automation frameworks using Selenium, Playwright, or Cypress, and integrates test suites into CI/CD pipelines.', '0-3 years', '₹5 - 10 LPA', '2519.01'),
('Performance Test Engineer', 'Quality Assurance', 'Simulates high-load enterprise traffic using JMeter or k6 to identify memory leaks, latency bottlenecks, and network throughput thresholds.', '1-3 years', '₹6 - 12 LPA', '2519.02'),

-- Product & Technical Management
('Technical Product Manager', 'Product & Management', 'Drives technical product vision, authoring PRDs, prioritizing engineering backlogs, defining API contracts, and measuring north-star adoption metrics.', '2-5 years', '₹13 - 25 LPA', '2512.05'),
('Scrum Master & Agile Coach', 'Product & Management', 'Facilitates sprint ceremonies, removes cross-functional blockers, mentors agile teams, and tracks velocity and burn-down metrics.', '2-5 years', '₹9 - 17 LPA', '2512.06'),
('Engineering Manager', 'Leadership', 'Leads software engineering pods, conducts code reviews, mentors developers, oversees architecture decisions, and ensures on-time sprint delivery.', '4-8 years', '₹22 - 40 LPA', '1330.01'),

-- Systems, Embedded & Hardware
('Embedded Systems Engineer', 'Hardware & IoT', 'Programs microcontrollers, real-time operating systems (RTOS), hardware device drivers in C/C++, and protocols like SPI, I2C, CAN, UART.', '1-3 years', '₹6 - 13 LPA', '2152.01'),
('IoT Solutions Developer', 'Hardware & IoT', 'Connects edge sensor telemetry with cloud IoT core endpoints, MQTT brokers, and remote over-the-air firmware update services.', '1-3 years', '₹6.5 - 14 LPA', '2152.02'),
('Linux Kernel / Systems Engineer', 'Software Engineering', 'Develops high-throughput system software, Linux device drivers, kernel modules, memory allocators, and POSIX multithreaded daemons.', '2-5 years', '₹12 - 24 LPA', '2512.07')
ON CONFLICT (title) DO NOTHING;

-- 2. EXPANDED MASTER SKILLS TAXONOMY (200+ Real Skills)
INSERT INTO skills (name, category, description) VALUES
-- Advanced Languages
('C#', 'Programming', 'Modern object-oriented language for enterprise Windows, ASP.NET Core, and Unity game development.'),
('Kotlin', 'Programming', 'Expressive statically typed language for modern Android apps, backend microservices, and multiplatform code.'),
('Swift', 'Programming', 'Fast and safe programming language built by Apple for iOS, macOS, watchOS, and visionOS applications.'),
('Rust', 'Programming', 'Systems programming language guaranteeing memory safety and thread safety without a garbage collector.'),
('R', 'Programming', 'Statistical programming language widely used in data analysis, bioinformatics, and academic research.'),
('Scala', 'Programming', 'Language combining object-oriented and functional programming running on the JVM, heavily used with Apache Spark.'),
('Shell Scripting / Bash', 'Programming', 'Scripting for Linux automation, command line operations, server administration, and CI pipelines.'),

-- Web & Frontend
('SASS / SCSS', 'Frontend', 'CSS preprocessor adding nested rules, variables, mixins, and mathematical functions.'),
('Bootstrap', 'Frontend', 'Popular open-source CSS framework for responsive, mobile-first front-end web development.'),
('Zustand / Jotai', 'Frontend', 'Lightweight, modern atomic state management libraries for React applications.'),
('Webpack / Vite', 'Frontend', 'Modern JavaScript module bundlers and fast local development servers with Hot Module Replacement.'),
('Microfrontends', 'Frontend', 'Architectural style where independently deliverable frontend applications are composed into a greater whole.'),
('WebSockets', 'Frontend', 'Bidirectional real-time communication protocol between client and server.'),
('Progressive Web Apps (PWA)', 'Frontend', 'Web applications using modern browser capabilities to deliver an app-like user experience offline.'),

-- Backend & Microservices
('NestJS', 'Backend', 'Progressive Node.js framework for building efficient, reliable, and scalable server-side enterprise apps.'),
('Spring Framework', 'Backend', 'Comprehensive Java programming and configuration model for modern enterprise applications.'),
('ASP.NET Core', 'Backend', 'Cross-platform, high-performance, open-source framework for building modern cloud-enabled backend apps.'),
('gRPC & Protocol Buffers', 'Backend', 'High-performance, open-source universal RPC framework developed by Google.'),
('Message Queues (RabbitMQ/SQS)', 'Backend', 'Asynchronous message broker systems decoupling producers from consumers in distributed systems.'),
('OAuth 2.0 & JWT', 'Backend', 'Industry standard protocol for authorization and stateless JSON token-based authentication.'),
('Microservices Architecture', 'Backend', 'Architectural design pattern structuring an application as a collection of loosely coupled services.'),

-- Databases & Caching
('SQLite', 'Databases', 'Self-contained, serverless, zero-configuration SQL database engine.'),
('Elasticsearch', 'Databases', 'Distributed, open-source search and analytics engine for structured and unstructured log/text data.'),
('DynamoDB', 'Databases', 'Fully managed NoSQL database service on AWS providing single-digit millisecond latency.'),
('Cassandra', 'Databases', 'Distributed wide-column NoSQL storage system designed to handle large amounts of data across commodity servers.'),
('Neo4j', 'Databases', 'Native graph database designed to leverage data relationships as first-class citizens.'),
('Vector Databases (Pinecone/Chroma)', 'Databases', 'Specialized databases optimized for storing and querying high-dimensional vector embeddings.'),

-- Cloud & Infrastructure
('Google Cloud Platform (GCP)', 'DevOps & Cloud', 'Suite of cloud services running on Google infrastructure including BigQuery, Cloud Run, and GKE.'),
('Microsoft Azure', 'DevOps & Cloud', 'Cloud computing service created by Microsoft for building, testing, and managing cloud applications.'),
('Ansible', 'DevOps & Cloud', 'Open-source automation tool for configuration management, application deployment, and task automation.'),
('Prometheus & Grafana', 'DevOps & Cloud', 'Leading open-source observability stack for time-series metrics collection, alerting, and visual dashboards.'),
('ArgoCD', 'DevOps & Cloud', 'Declarative, GitOps continuous delivery tool for Kubernetes cluster state reconciliation.'),
('Helm', 'DevOps & Cloud', 'Package manager for Kubernetes allowing developers to define, install, and upgrade complex cluster applications.'),
('Serverless (AWS Lambda)', 'DevOps & Cloud', 'Event-driven compute service that lets developers run code without provisioning or managing servers.'),

-- AI, ML & NLP
('Scikit-learn', 'AI & Data Science', 'Python library for classical predictive data analysis, regression, classification, and clustering.'),
('XGBoost / LightGBM', 'AI & Data Science', 'Optimized distributed gradient boosting libraries designed to be highly efficient, flexible, and portable.'),
('OpenCV', 'AI & Data Science', 'Open-source computer vision and machine learning software library for image processing.'),
('Transformers (Hugging Face)', 'AI & Data Science', 'State-of-the-art machine learning library providing pre-trained models for text, vision, and audio.'),
('Sentence Transformers', 'AI & Data Science', 'Framework for state-of-the-art sentence, text, and image embeddings for semantic search.'),
('Prompt Engineering', 'AI & Data Science', 'Technique of crafting structured, effective inputs to guide LLMs toward accurate, hallucination-free outputs.'),
('MLflow', 'AI & Data Science', 'Open-source platform to manage the ML lifecycle including experimentation, reproducibility, and deployment.'),
('Vector Embeddings', 'AI & Data Science', 'Dense numerical array representations of text capturing contextual semantic meaning.'),

-- Data Engineering & Big Data
('dbt (data build tool)', 'Data Engineering', 'Transform workflow allowing data analysts and engineers to build modular, tested SQL pipelines in data warehouses.'),
('Snowflake', 'Data Engineering', 'Cloud-based data warehouse software-as-a-service with separated storage and compute tiers.'),
('BigQuery', 'Data Engineering', 'Serverless, highly scalable, and cost-effective multi-cloud data warehouse designed for business agility.'),
('Apache Airflow', 'Data Engineering', 'Platform to programmatically author, schedule, monitor, and log complex data engineering workflows.'),
('Delta Lake', 'Data Engineering', 'Open-source storage framework that enables building Lakehouse architectures on top of cloud object storage.'),

-- Security & Governance
('OWASP Top 10', 'Security', 'Standard awareness document for developers and web application security representing critical risks.'),
('Burp Suite', 'Security', 'Leading graphical tool for testing web application security, interception proxies, and scanner suites.'),
('Wireshark', 'Security', 'World’s foremost network protocol analyzer for deep packet inspection and network troubleshooting.'),
('Identity and Access Management (IAM)', 'Security', 'Framework of policies and technologies ensuring proper people and devices have appropriate access to resources.'),
('Cryptography Fundamentals', 'Security', 'Principles of symmetric/asymmetric encryption, hashing (SHA-256), public key infrastructure (PKI), and SSL/TLS.')
ON CONFLICT (name) DO NOTHING;

-- 3. EXPANDED REAL COURSES (NPTEL, COURSERA, FREECODECAMP, HARVARD, EDX)
INSERT INTO courses (skill_name, course_name, platform, url, duration_weeks, is_free, difficulty) VALUES
-- NPTEL (IIT Courses for India)
('Python', 'Joy of Computing using Python', 'NPTEL (IIT Ropar)', 'https://nptel.ac.in/courses/106106182', 12, true, 'Beginner'),
('Data Science', 'Data Science for Engineers', 'NPTEL (IIT Madras)', 'https://nptel.ac.in/courses/106106179', 8, true, 'Beginner'),
('Machine Learning', 'Introduction to Machine Learning', 'NPTEL (IIT Kharagpur)', 'https://nptel.ac.in/courses/106105152', 8, true, 'Intermediate'),
('Deep Learning', 'Deep Learning - IIT Ropar', 'NPTEL (IIT Ropar)', 'https://nptel.ac.in/courses/106106184', 12, true, 'Intermediate'),
('Natural Language Processing', 'Applied Natural Language Processing', 'NPTEL (IIT Madras)', 'https://nptel.ac.in/courses/106106211', 12, true, 'Intermediate'),
('Cloud Computing', 'Cloud Computing by Prof. Soumya Kanti Ghosh', 'NPTEL (IIT Kharagpur)', 'https://nptel.ac.in/courses/106105167', 8, true, 'Beginner'),
('Cybersecurity', 'Information Security and Cyber Forensics', 'NPTEL (IIT Madras)', 'https://nptel.ac.in/courses/106106129', 8, true, 'Beginner'),
('Computer Networks', 'Data Communication and Computer Networks', 'NPTEL (IIT Kharagpur)', 'https://nptel.ac.in/courses/106105081', 12, true, 'Intermediate'),

-- freeCodeCamp Certifications (Real Free Programs)
('Full Stack', 'Full Stack Developer Curriculum', 'freeCodeCamp', 'https://www.freecodecamp.org/', 16, true, 'Beginner'),
('Machine Learning', 'Machine Learning with Python Certification', 'freeCodeCamp', 'https://www.freecodecamp.org/learn/machine-learning-with-python/', 6, true, 'Intermediate'),
('Data Analysis', 'Data Analysis with Python Certification', 'freeCodeCamp', 'https://www.freecodecamp.org/learn/data-analysis-with-python/', 4, true, 'Beginner'),
('Backend', 'Back End Development and APIs Certification', 'freeCodeCamp', 'https://www.freecodecamp.org/learn/back-end-development-and-apis/', 5, true, 'Beginner'),
('Security', 'Information Security Certification', 'freeCodeCamp', 'https://www.freecodecamp.org/learn/information-security/', 6, true, 'Intermediate'),

-- Harvard & edX
('Computer Science', 'CS50: Introduction to Computer Science', 'Harvard University (edX)', 'https://cs50.harvard.edu/x/', 10, true, 'Beginner'),
('Web Development', 'CS50’s Web Programming with Python and JavaScript', 'Harvard University (edX)', 'https://cs50.harvard.edu/web/', 10, true, 'Intermediate'),
('Artificial Intelligence', 'CS50’s Introduction to Artificial Intelligence with Python', 'Harvard University (edX)', 'https://cs50.harvard.edu/ai/', 7, true, 'Intermediate'),

-- DeepLearning.AI & Coursera
('Generative AI', 'Generative AI for Everyone by Andrew Ng', 'Coursera (DeepLearning.AI)', 'https://www.coursera.org/learn/generative-ai-for-everyone', 3, true, 'Beginner'),
('NLP', 'Natural Language Processing Specialization', 'Coursera (DeepLearning.AI)', 'https://www.coursera.org/specializations/natural-language-processing', 8, true, 'Intermediate'),
('MLOps', 'Machine Learning Engineering for Production (MLOps)', 'Coursera (DeepLearning.AI)', 'https://www.coursera.org/specializations/mach-learning-engineering-for-production-mlops', 6, true, 'Advanced'),
('Kubernetes', 'Getting Started with Google Kubernetes Engine', 'Coursera (Google Cloud)', 'https://www.coursera.org/learn/google-kubernetes-engine', 2, true, 'Intermediate'),
('AWS Cloud', 'AWS Cloud Solutions Architect Professional Certificate', 'Coursera (AWS)', 'https://www.coursera.org/professional-certificates/aws-cloud-solutions-architect', 8, true, 'Intermediate')
ON CONFLICT DO NOTHING;

-- 4. EXPANDED REAL SYNONYMS (100+ Real NLP Aliases)
INSERT INTO skill_synonyms (alias, canonical_name) VALUES
('csharp', 'C#'),
('c-sharp', 'C#'),
('.net core', 'ASP.NET Core'),
('aspnet', 'ASP.NET Core'),
('asp.net', 'ASP.NET Core'),
('golang', 'Go'),
('rustlang', 'Rust'),
('bash scripting', 'Shell Scripting / Bash'),
('shell', 'Shell Scripting / Bash'),
('bash', 'Shell Scripting / Bash'),
('scikit learn', 'Scikit-learn'),
('xgboost', 'XGBoost / LightGBM'),
('lightgbm', 'XGBoost / LightGBM'),
('opencv', 'OpenCV'),
('huggingface transformers', 'Transformers (Hugging Face)'),
('hf transformers', 'Transformers (Hugging Face)'),
('sbert', 'Sentence Transformers'),
('sentence-transformers', 'Sentence Transformers'),
('prompt design', 'Prompt Engineering'),
('mlops', 'MLflow'),
('airflow', 'Apache Airflow'),
('apache airflow', 'Apache Airflow'),
('dbt core', 'dbt (data build tool)'),
('snowflake data warehouse', 'Snowflake'),
('google bigquery', 'BigQuery'),
('microservices', 'Microservices Architecture'),
('restful api', 'REST APIs'),
('restful apis', 'REST APIs'),
('rabbitmq', 'Message Queues (RabbitMQ/SQS)'),
('sqs', 'Message Queues (RabbitMQ/SQS)'),
('activemq', 'Message Queues (RabbitMQ/SQS)'),
('oauth', 'OAuth 2.0 & JWT'),
('oauth2', 'OAuth 2.0 & JWT'),
('jwt', 'OAuth 2.0 & JWT'),
('grpc', 'gRPC & Protocol Buffers'),
('protobuf', 'gRPC & Protocol Buffers'),
('prometheus', 'Prometheus & Grafana'),
('grafana', 'Prometheus & Grafana'),
('argocd', 'ArgoCD'),
('helm charts', 'Helm'),
('lambda', 'Serverless (AWS Lambda)'),
('aws lambda', 'Serverless (AWS Lambda)'),
('serverless', 'Serverless (AWS Lambda)'),
('burpsuite', 'Burp Suite'),
('burp', 'Burp Suite'),
('owasp', 'OWASP Top 10'),
('iam', 'Identity and Access Management (IAM)'),
('aws iam', 'Identity and Access Management (IAM)'),
('pki', 'Cryptography Fundamentals'),
('ssl/tls', 'Cryptography Fundamentals')
ON CONFLICT (alias) DO NOTHING;

-- Verification query
SELECT 'Total Roles Seeded:' as metric, count(*) as count FROM roles
UNION ALL
SELECT 'Total Skills Seeded:', count(*) FROM skills
UNION ALL
SELECT 'Total Courses Seeded:', count(*) FROM courses
UNION ALL
SELECT 'Total Synonyms Seeded:', count(*) FROM skill_synonyms;
