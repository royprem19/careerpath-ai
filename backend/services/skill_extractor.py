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
    ]
}

ALL_SKILLS = [skill for category in SKILLS_DB.values() for skill in category]

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
    education_keywords = ["B.Tech", "B.E.", "M.Tech", "MBA", "BCA", "MCA", "B.Sc", "M.Sc", "PhD", "Bachelor", "Master", "Degree", "Diploma"]
    found = set()
    for kw in education_keywords:
        if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text.lower()):
            found.add(kw)
    return list(found)

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
