from rapidfuzz import fuzz
from .skill_extractor import ALL_SKILLS

# Real synonym mappings aligned with Indian job market & industry jargon
SYNONYM_DICT = {
    'js': 'JavaScript',
    'javascript': 'JavaScript',
    'es6': 'JavaScript',
    'ts': 'TypeScript',
    'typescript': 'TypeScript',
    'py': 'Python',
    'python3': 'Python',
    'py3': 'Python',
    'react.js': 'React',
    'reactjs': 'React',
    'react': 'React',
    'next': 'Next.js',
    'nextjs': 'Next.js',
    'node': 'Node.js',
    'nodejs': 'Node.js',
    'node.js': 'Node.js',
    'express': 'Express.js',
    'expressjs': 'Express.js',
    'fast api': 'FastAPI',
    'fastapi': 'FastAPI',
    'django': 'Django',
    'postgres': 'PostgreSQL',
    'postgresql': 'PostgreSQL',
    'pgsql': 'PostgreSQL',
    'my sql': 'MySQL',
    'mysql': 'MySQL',
    'mongo': 'MongoDB',
    'mongodb': 'MongoDB',
    'k8s': 'Kubernetes',
    'kubernetes': 'Kubernetes',
    'docker': 'Docker',
    'aws cloud': 'AWS',
    'amazon web services': 'AWS',
    'aws': 'AWS',
    'gcp': 'Google Cloud Platform',
    'google cloud': 'Google Cloud Platform',
    'azure cloud': 'Azure',
    'ml': 'Machine Learning',
    'machine learning': 'Machine Learning',
    'dl': 'Deep Learning',
    'deep learning': 'Deep Learning',
    'nlp': 'Natural Language Processing',
    'natural language processing': 'Natural Language Processing',
    'cv': 'Computer Vision',
    'computer vision': 'Computer Vision',
    'sklearn': 'Scikit-learn',
    'scikit-learn': 'Scikit-learn',
    'scikit learn': 'Scikit-learn',
    'tf': 'TensorFlow',
    'tensorflow': 'TensorFlow',
    'pytorch': 'PyTorch',
    'torch': 'PyTorch',
    'llm': 'Large Language Models (LLMs)',
    'llms': 'Large Language Models (LLMs)',
    'generative ai': 'Large Language Models (LLMs)',
    'genai': 'Large Language Models (LLMs)',
    'rag': 'Retrieval Augmented Generation (RAG)',
    'langchain': 'LangChain',
    'huggingface': 'Hugging Face',
    'hugging face': 'Hugging Face',
    'tailwind': 'TailwindCSS',
    'tailwindcss': 'TailwindCSS',
    'tailwind css': 'TailwindCSS',
    'git': 'Git & GitHub',
    'github': 'Git & GitHub',
    'git and github': 'Git & GitHub',
    'ci/cd': 'CI/CD Pipelines',
    'cicd': 'CI/CD Pipelines',
    'continuous integration': 'CI/CD Pipelines',
    'spark': 'Apache Spark',
    'pyspark': 'Apache Spark',
    'kafka': 'Apache Kafka',
    'apache kafka': 'Apache Kafka',
    'tableau': 'Tableau',
    'power bi': 'Power BI',
    'powerbi': 'Power BI',
    'flutter': 'Flutter',
    'react native': 'React Native',
    'react-native': 'React Native',
    'rest': 'REST APIs',
    'rest api': 'REST APIs',
    'rest apis': 'REST APIs',
    'restful': 'REST APIs',
    'html': 'HTML5',
    'html5': 'HTML5',
    'css': 'CSS3',
    'css3': 'CSS3',
    'graphql': 'GraphQL',
    'redis': 'Redis',
    'terraform': 'Terraform',
    'linux': 'Linux',
    'agile': 'Agile & Scrum',
    'scrum': 'Agile & Scrum'
}

def normalize_skill(skill: str) -> str:
    s_clean = skill.strip()
    s_lower = s_clean.lower()
    
    if s_lower in SYNONYM_DICT:
        return SYNONYM_DICT[s_lower]
        
    for canonical in ALL_SKILLS:
        if s_lower == canonical.lower():
            return canonical
            
    match = fuzzy_match_skill(s_clean, ALL_SKILLS, threshold=84)
    if match:
        return match
        
    return s_clean

def normalize_skills(skills: list[str]) -> list[str]:
    normalized = []
    seen = set()
    for s in skills:
        norm = normalize_skill(s)
        if norm and norm.lower() not in seen:
            seen.add(norm.lower())
            normalized.append(norm)
    return normalized

def fuzzy_match_skill(skill: str, canonical_skills: list[str], threshold=80) -> str | None:
    best_match = None
    best_score = 0
    for canon in canonical_skills:
        score = fuzz.ratio(skill.lower(), canon.lower())
        if score > best_score and score >= threshold:
            best_score = score
            best_match = canon
    return best_match
