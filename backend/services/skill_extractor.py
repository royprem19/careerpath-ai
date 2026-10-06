import re

# Comprehensive list of 300+ skills
SKILLS_DB = {
    "Programming": [
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "Go", "Rust", "Ruby", 
        "PHP", "Kotlin", "Swift", "Scala", "R", "MATLAB", "Julia", "Perl", "Dart", "Objective-C",
        "Haskell", "Lua", "Groovy", "Shell", "Bash", "PowerShell", "F#", "Cobol", "Fortran", "Assembly",
        "VBA", "ABAP", "Solidity", "Elixir", "Clojure", "Erlang", "Apex", "VBScript", "ActionScript",
        "Scratch", "Logo", "Prolog", "Lisp", "Ada", "Pascal", "Delphi", "Smalltalk", "Tcl", "Verilog"
    ],
    "Frontend": [
        "React", "Angular", "Vue.js", "Next.js", "Svelte", "HTML", "CSS", "SASS", "LESS", "Bootstrap", 
        "TailwindCSS", "jQuery", "Redux", "MobX", "Recoil", "Gatsby", "Nuxt.js", "Ember.js", "Backbone.js",
        "Preact", "Alpine.js", "Lit", "SolidJS", "Material UI", "Chakra UI", "Ant Design", "Bulma",
        "Foundation", "Semantic UI", "Webpack", "Vite", "Parcel", "Rollup", "Babel", "ESLint", "Prettier",
        "Jest", "Cypress", "Playwright", "Puppeteer", "Selenium", "Mocha", "Chai", "Jasmine", "Karma",
        "Enzyme", "Testing Library", "Storybook", "Apollo GraphQL", "Relay", "SWR", "React Query"
    ],
    "Backend": [
        "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring Boot", ".NET", "Laravel", "Ruby on Rails", 
        "NestJS", "Koa", "Hapi", "Sails.js", "Meteor", "AdonisJS", "Phoenix", "Sinatra", "CakePHP", "CodeIgniter",
        "Symfony", "Zend", "Yii", "ASP.NET", "WCF", "Entity Framework", "Hibernate", "JPA", "MyBatis",
        "Spring MVC", "Spring Data", "Spring Security", "Dropwizard", "Play Framework", "Grails", "Struts",
        "Tornado", "CherryPy", "Bottle", "Falcon", "Pyramid", "Sanic", "Starlette", "Aiohttp",
        "Gin", "Echo", "Fiber", "Beego", "Revel", "Rocket", "Actix", "Iron"
    ],
    "Databases": [
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "DynamoDB", "Firebase", "Supabase", 
        "Neo4j", "Oracle", "SQL Server", "SQLite", "MariaDB", "CouchDB", "Couchbase", "RavenDB", "ArangoDB",
        "OrientDB", "HBase", "Bigtable", "CockroachDB", "TiDB", "InfluxDB", "TimescaleDB", "Prometheus",
        "Elasticsearch", "Solr", "Splunk", "Logstash", "Kibana", "Hazelcast", "Memcached", "etcd", "Consul",
        "Zookeeper", "Realm", "Core Data", "Room", "Greenplum", "Teradata", "Vertica", "Snowflake", "Redshift",
        "BigQuery", "Athena", "Presto", "Trino", "Druid", "ClickHouse", "Pinot"
    ],
    "Cloud": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD", "Jenkins", "GitHub Actions", 
        "GitLab CI", "CircleCI", "Travis CI", "Bitbucket Pipelines", "Bamboo", "TeamCity", "Octopus Deploy",
        "Ansible", "Chef", "Puppet", "SaltStack", "Vagrant", "Packer", "Pulumi", "CloudFormation", "ARM Templates",
        "OpenStack", "VMware", "Xen", "KVM", "Hyper-V", "Docker Swarm", "Mesos", "Nomad", "Rancher",
        "OpenShift", "Helm", "Istio", "Linkerd", "Envoy", "Nginx", "HAProxy", "Traefik", "Apache",
        "Tomcat", "Jetty", "Undertow", "IIS", "Lighttpd", "Caddy", "Cloudflare", "Akamai", "Fastly"
    ],
    "ML/AI": [
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "TensorFlow", "PyTorch", "Scikit-learn", 
        "Keras", "OpenCV", "Hugging Face", "LLM", "GenAI", "XGBoost", "LightGBM", "CatBoost", "NLTK", "Spacy",
        "Gensim", "FastText", "Word2Vec", "BERT", "GPT", "Transformer", "YOLO", "ResNet", "VGG", "Inception",
        "GAN", "RL", "Q-Learning", "DQN", "PPO", "A3C", "DDPG", "SAC", "TD3", "AutoML", "H2O", "DataRobot",
        "Sagemaker", "Vertex AI", "Azure ML", "Databricks", "MLflow", "Kubeflow", "TFX", "ONNX", "TensorRT",
        "CoreML", "ML.NET", "Weka", "RapidMiner", "KNIME"
    ],
    "Data": [
        "Pandas", "NumPy", "Matplotlib", "Seaborn", "Tableau", "Power BI", "Apache Spark", "Hadoop", "Airflow", 
        "dbt", "Plotly", "Bokeh", "Dash", "Streamlit", "Gradio", "Superset", "Metabase", "Looker", "Qlik",
        "Kafka", "RabbitMQ", "ActiveMQ", "ZeroMQ", "Pulsar", "NATS", "Kinesis", "Event Hubs", "Pub/Sub",
        "Flink", "Storm", "Samza", "Beam", "NiFi", "Talend", "Pentaho", "Informatica", "DataStage", "Ab Initio",
        "SSIS", "Alteryx", "Fivetran", "Stitch", "Airbyte", "Meltano", "Great Expectations", "Prefect"
    ],
    "Tools": [
        "Git", "GitHub", "Linux", "Jira", "Figma", "Postman", "VS Code", "Bitbucket", "GitLab", "SVN", "Mercurial",
        "Trello", "Asana", "Monday", "ClickUp", "Notion", "Confluence", "Slack", "Microsoft Teams", "Discord",
        "Zoom", "Webex", "Skype", "IntelliJ IDEA", "Eclipse", "NetBeans", "Visual Studio", "PyCharm", "WebStorm",
        "PhpStorm", "RubyMine", "CLion", "Rider", "Android Studio", "Xcode", "Vim", "Emacs", "Sublime Text",
        "Atom", "Notepad++", "Sketch", "Adobe XD", "InVision", "Zeplin", "Miro", "Lucidchart", "Draw.io",
        "Swagger", "Insomnia", "SoapUI", "JMeter", "Gatling", "Locust", "WireShark", "Fiddler", "Charles"
    ],
    "Soft Skills": [
        "Communication", "Leadership", "Problem Solving", "Team Work", "Project Management", "Agile", "Scrum", 
        "Kanban", "Lean", "Six Sigma", "Time Management", "Critical Thinking", "Adaptability", "Creativity",
        "Work Ethic", "Attention to Detail", "Conflict Resolution", "Decision Making", "Emotional Intelligence",
        "Empathy", "Mentoring", "Negotiation", "Networking", "Presentation Skills", "Public Speaking",
        "Active Listening", "Collaboration", "Customer Service", "Interpersonal Skills", "Motivation"
    ],
    "Design & Creative": [
        "UI/UX Design", "Figma", "User Research", "Wireframing", "Prototyping", "Design Systems",
        "Interaction Design", "Graphic Design", "Usability Testing", "Design Thinking", "Information Architecture",
        "Adobe XD", "Sketch", "Visual Design", "Design Sprints"
    ],
    "Business & Product": [
        "Product Management", "Business Analysis", "Requirements Gathering", "Process Mapping",
        "Product Roadmapping", "Sprint Planning", "Market Research", "Financial Modeling", "Stakeholder Management",
        "User Stories", "Competitive Analysis", "Agile & Scrum", "Business Intelligence", "KPI Tracking"
    ],
    "Marketing & Growth": [
        "Digital Marketing", "SEO", "SEM", "Content Strategy", "Google Analytics", "Social Media Marketing",
        "Email Marketing", "Copywriting", "Data Storytelling", "Brand Strategy", "A/B Testing", "Growth Marketing"
    ],
    "Operations & Quality": [
        "Quality Assurance", "Manual Testing", "Test Automation", "Technical Support", "Customer Success",
        "CRM", "Salesforce", "Zoho", "Technical Writing", "Incident Management", "Vendor Management", "ITIL"
    ]
}

ALL_SKILLS = [skill for category in SKILLS_DB.values() for skill in category]

# Comprehensive Indian Degree & Educational Qualifications Mapping
INDIAN_EDUCATION_MAPPINGS = [
    (re.compile(r'\b(b\.?tech|btech|bachelor\s+of\s+technology)\b', re.IGNORECASE), "B.Tech (Bachelor of Technology)"),
    (re.compile(r'\b(b\.?e\.?|be\b|bachelor\s+of\s+engineering)\b', re.IGNORECASE), "B.E. (Bachelor of Engineering)"),
    (re.compile(r'\b(bca|bachelor\s+of\s+computer\s+applications)\b', re.IGNORECASE), "BCA (Bachelor of Computer Applications)"),
    (re.compile(r'\b(mca|master\s+of\s+computer\s+applications)\b', re.IGNORECASE), "MCA (Master of Computer Applications)"),
    (re.compile(r'\b(m\.?tech|mtech|master\s+of\s+technology)\b', re.IGNORECASE), "M.Tech (Master of Technology)"),
    (re.compile(r'\b(m\.?e\.?|master\s+of\s+engineering)\b', re.IGNORECASE), "M.E. (Master of Engineering)"),
    (re.compile(r'\b(b\.?sc|bsc|bachelor\s+of\s+science)\b', re.IGNORECASE), "B.Sc (Bachelor of Science)"),
    (re.compile(r'\b(m\.?sc|msc|master\s+of\s+science)\b', re.IGNORECASE), "M.Sc (Master of Science)"),
    (re.compile(r'\b(mba|pgdm|master\s+of\s+business\s+administration)\b', re.IGNORECASE), "MBA (Master of Business Administration)"),
    (re.compile(r'\b(bba|bachelor\s+of\s+business\s+administration)\b', re.IGNORECASE), "BBA (Bachelor of Business Administration)"),
    (re.compile(r'\b(b\.?com|bcom|bachelor\s+of\s+commerce)\b', re.IGNORECASE), "B.Com (Bachelor of Commerce)"),
    (re.compile(r'\b(b\.?voc|bachelor\s+of\s+vocation)\b', re.IGNORECASE), "B.Voc (Vocational Degree)"),
    (re.compile(r'\b(polytechnic|diploma\s+in\s+engineering|diploma)\b', re.IGNORECASE), "Diploma / Polytechnic"),
    (re.compile(r'\b(ph\.?d|doctorate)\b', re.IGNORECASE), "Ph.D. / Doctorate"),
    (re.compile(r'\b(self[-\s]?taught|bootcamp\s+graduate|skill\s+india\s+certified)\b', re.IGNORECASE), "Non-Traditional / Skill Certified"),
]

def extract_skills(text: str) -> list[str]:
    found_skills = set()
    text_lower = " " + text.lower() + " "
    text_lower = re.sub(r'[^\w\s\+#\-\.]', ' ', text_lower)
    
    for skill in ALL_SKILLS:
        skill_lower = skill.lower()
        if skill_lower == "c":
            if re.search(r'\bc\b', text_lower):
                found_skills.add(skill)
        elif skill_lower == "r":
            if re.search(r'\br\b', text_lower):
                found_skills.add(skill)
        elif "+" in skill_lower or "#" in skill_lower or "." in skill_lower:
            escaped = re.escape(skill_lower)
            if re.search(r'\b' + escaped + r'(?!\w)', text_lower):
                found_skills.add(skill)
        else:
            if re.search(r'\b' + re.escape(skill_lower) + r'\b', text_lower):
                found_skills.add(skill)
                
    return list(found_skills)

def extract_education(text: str) -> list[str]:
    found = set()
    for pattern, canonical_name in INDIAN_EDUCATION_MAPPINGS:
        if pattern.search(text):
            found.add(canonical_name)
    return sorted(list(found))

def extract_experience(text: str) -> dict:
    match = re.search(r'(\d+)\+?\s*(years?|yrs?)\s+of\s+experience', text.lower())
    if match:
        return {"years": int(match.group(1))}
    return {"years": 0}

def extract_certifications(text: str) -> list[str]:
    cert_keywords = ["AWS", "Azure", "Google Cloud", "GCP", "Cisco", "CompTIA", "Oracle", "Microsoft Certified"]
    found = set()
    for kw in cert_keywords:
        if kw.lower() in text.lower():
            found.add(kw)
    return list(found)
