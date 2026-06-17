"""
Dataset Generator
================

Generates synthetic datasets for testing and demonstration purposes.
Creates realistic resume and job description content.
"""

import random
from typing import List, Dict, Optional
from pathlib import Path
import json
from datetime import datetime, timedelta


class DatasetGenerator:
    """Generate synthetic datasets for SkillFitAI testing"""
    
    def __init__(self):
        # Sample data for generation
        self.first_names = [
            "John", "Jane", "Michael", "Sarah", "David", "Emma", "Chris", "Lisa",
            "Robert", "Maria", "James", "Anna", "William", "Jennifer", "Daniel", "Amy",
            "Matthew", "Jessica", "Anthony", "Ashley", "Mark", "Michelle", "Paul", "Linda",
            "Steven", "Karen", "Kevin", "Nancy", "Brian", "Betty", "George", "Helen",
            "Edward", "Sandra", "Ronald", "Donna", "Timothy", "Carol", "Jason", "Ruth"
        ]
        
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
            "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
            "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
            "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
        ]
        
        self.companies = [
            "Microsoft", "Google", "Apple", "Amazon", "Meta", "Netflix", "Tesla", "IBM",
            "Oracle", "Salesforce", "Adobe", "Intel", "NVIDIA", "Cisco", "VMware", "Uber",
            "Airbnb", "Twitter", "LinkedIn", "Spotify", "Dropbox", "Slack", "Zoom", "PayPal",
            "eBay", "Yahoo", "Atlassian", "ServiceNow", "Workday", "Splunk", "MongoDB", "Snowflake"
        ]
        
        self.job_titles = [
            "Software Engineer", "Senior Software Engineer", "Lead Software Engineer",
            "Data Scientist", "Senior Data Scientist", "Machine Learning Engineer",
            "Product Manager", "Senior Product Manager", "Technical Product Manager",
            "DevOps Engineer", "Cloud Engineer", "Site Reliability Engineer",
            "Frontend Developer", "Backend Developer", "Full Stack Developer",
            "Mobile Developer", "iOS Developer", "Android Developer",
            "Data Engineer", "Analytics Engineer", "Business Intelligence Developer",
            "Security Engineer", "Cybersecurity Analyst", "Information Security Specialist",
            "UI/UX Designer", "Product Designer", "User Experience Researcher",
            "Database Administrator", "System Administrator", "Network Engineer",
            "Quality Assurance Engineer", "Test Engineer", "Automation Engineer"
        ]
        
        self.skills = {
            'programming': [
                'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
                'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'SQL'
            ],
            'frameworks': [
                'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask', 'Spring Boot',
                'Express.js', 'Next.js', 'Nuxt.js', 'Laravel', 'Rails', 'ASP.NET', 'FastAPI'
            ],
            'databases': [
                'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch', 'Oracle',
                'SQL Server', 'Cassandra', 'DynamoDB', 'Neo4j', 'InfluxDB', 'CouchDB'
            ],
            'cloud': [
                'AWS', 'Azure', 'Google Cloud Platform', 'Docker', 'Kubernetes',
                'Terraform', 'Jenkins', 'GitLab CI', 'GitHub Actions', 'Ansible'
            ],
            'tools': [
                'Git', 'JIRA', 'Confluence', 'Slack', 'VS Code', 'IntelliJ IDEA',
                'Eclipse', 'Postman', 'Figma', 'Adobe Creative Suite', 'Tableau', 'Power BI'
            ],
            'soft_skills': [
                'Leadership', 'Communication', 'Problem Solving', 'Team Collaboration',
                'Project Management', 'Time Management', 'Critical Thinking', 'Adaptability',
                'Mentoring', 'Strategic Planning', 'Cross-functional Collaboration', 'Innovation'
            ]
        }
        
        self.universities = [
            "Stanford University", "MIT", "Carnegie Mellon University", "UC Berkeley",
            "Harvard University", "University of Washington", "Georgia Tech",
            "University of Illinois", "Cornell University", "University of Michigan",
            "Caltech", "Princeton University", "Yale University", "Columbia University",
            "University of Texas at Austin", "University of California San Diego"
        ]
        
        self.degrees = [
            "Bachelor of Science in Computer Science",
            "Bachelor of Science in Software Engineering",
            "Bachelor of Science in Information Technology",
            "Master of Science in Computer Science",
            "Master of Science in Data Science",
            "Master of Science in Software Engineering",
            "Master of Business Administration",
            "Bachelor of Engineering in Computer Engineering",
            "Master of Science in Machine Learning",
            "Bachelor of Science in Mathematics"
        ]
    
    def generate_person_name(self) -> str:
        """Generate a random person name"""
        first = random.choice(self.first_names)
        last = random.choice(self.last_names)
        return f"{first} {last}"
    
    def generate_email(self, name: str) -> str:
        """Generate email from name"""
        name_parts = name.lower().split()
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'company.com']
        
        patterns = [
            f"{name_parts[0]}.{name_parts[1]}",
            f"{name_parts[0][0]}{name_parts[1]}",
            f"{name_parts[0]}{name_parts[1][0]}",
            f"{name_parts[0]}{name_parts[1]}"
        ]
        
        email_name = random.choice(patterns)
        domain = random.choice(domains)
        return f"{email_name}@{domain}"
    
    def generate_phone(self) -> str:
        """Generate a random phone number"""
        area_code = random.randint(200, 999)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        return f"({area_code}) {exchange}-{number}"
    
    def generate_skills_for_role(self, job_title: str, num_skills: int = None) -> List[str]:
        """Generate appropriate skills for a job role"""
        if num_skills is None:
            num_skills = random.randint(8, 15)
        
        selected_skills = []
        title_lower = job_title.lower()
        
        # Role-specific skill selection
        if 'data scientist' in title_lower or 'machine learning' in title_lower:
            # Data science focused
            must_have = ['Python', 'SQL', 'Machine Learning', 'Statistics', 'Pandas', 'NumPy']
            additional = ['R', 'TensorFlow', 'PyTorch', 'Jupyter', 'Scikit-learn', 'Tableau']
        elif 'frontend' in title_lower or 'ui' in title_lower:
            # Frontend focused
            must_have = ['JavaScript', 'HTML', 'CSS', 'React']
            additional = ['TypeScript', 'Angular', 'Vue.js', 'SASS', 'Webpack', 'Figma']
        elif 'backend' in title_lower or 'api' in title_lower:
            # Backend focused
            must_have = ['Python', 'Java', 'SQL', 'REST APIs']
            additional = ['Node.js', 'Django', 'Spring Boot', 'PostgreSQL', 'Redis', 'Docker']
        elif 'devops' in title_lower or 'cloud' in title_lower:
            # DevOps/Cloud focused
            must_have = ['AWS', 'Docker', 'Kubernetes', 'Linux']
            additional = ['Terraform', 'Jenkins', 'Ansible', 'Python', 'Bash', 'Monitoring']
        elif 'mobile' in title_lower:
            # Mobile focused
            if 'ios' in title_lower:
                must_have = ['Swift', 'iOS', 'Xcode', 'Objective-C']
            elif 'android' in title_lower:
                must_have = ['Kotlin', 'Android', 'Java', 'Android Studio']
            else:
                must_have = ['React Native', 'Flutter', 'JavaScript', 'Mobile Development']
            additional = ['Git', 'API Integration', 'UI/UX', 'Testing']
        else:
            # General software engineering
            must_have = ['Python', 'JavaScript', 'Git', 'SQL']
            additional = ['Java', 'React', 'Node.js', 'AWS', 'Docker', 'Agile']
        
        # Add must-have skills
        selected_skills.extend(must_have[:min(len(must_have), num_skills // 2)])
        
        # Add random skills from all categories
        remaining_slots = num_skills - len(selected_skills)
        all_skills = []
        for category_skills in self.skills.values():
            all_skills.extend(category_skills)
        
        additional_skills = [s for s in all_skills if s not in selected_skills]
        selected_skills.extend(random.sample(additional_skills, 
                                           min(remaining_slots, len(additional_skills))))
        
        return selected_skills[:num_skills]
    
    def generate_work_experience(self, num_jobs: int = None) -> List[Dict[str, any]]:
        """Generate work experience entries"""
        if num_jobs is None:
            num_jobs = random.randint(2, 5)
        
        experiences = []
        current_year = datetime.now().year
        
        for i in range(num_jobs):
            # Calculate years (most recent first)
            if i == 0:
                start_year = current_year - random.randint(0, 3)
                end_year = current_year
            else:
                prev_start = experiences[i-1]['start_year']
                duration = random.randint(1, 4)
                end_year = prev_start - random.randint(0, 1)
                start_year = end_year - duration
            
            experience = {
                'title': random.choice(self.job_titles),
                'company': random.choice(self.companies),
                'start_year': start_year,
                'end_year': end_year,
                'duration': f"{start_year} - {'Present' if end_year == current_year else str(end_year)}",
                'responsibilities': self._generate_responsibilities(),
                'skills_used': random.sample(
                    [skill for skills in self.skills.values() for skill in skills],
                    random.randint(3, 8)
                )
            }
            experiences.append(experience)
        
        return experiences
    
    def _generate_responsibilities(self) -> List[str]:
        """Generate job responsibilities"""
        templates = [
            "Developed and maintained {tech} applications serving {users} users",
            "Led a team of {team_size} engineers in {project_type} projects",
            "Implemented {feature_type} features using {tech_stack}",
            "Optimized system performance resulting in {improvement}% improvement",
            "Collaborated with cross-functional teams to deliver {deliverable}",
            "Designed and architected {system_type} solutions",
            "Mentored {mentee_count} junior developers in {skill_area}",
            "Established {process_type} processes improving {metric} by {percentage}%"
        ]
        
        replacements = {
            'tech': ['web', 'mobile', 'cloud', 'data', 'machine learning'],
            'users': ['10K', '50K', '100K', '500K', '1M'],
            'team_size': ['3', '5', '8', '12'],
            'project_type': ['feature development', 'infrastructure', 'data pipeline', 'API'],
            'feature_type': ['user-facing', 'backend', 'analytics', 'security'],
            'tech_stack': ['React/Node.js', 'Python/Django', 'Java/Spring', 'AWS services'],
            'improvement': ['20', '30', '50', '75'],
            'deliverable': ['product features', 'technical solutions', 'system integrations'],
            'system_type': ['microservices', 'distributed', 'real-time', 'scalable'],
            'mentee_count': ['2', '3', '5'],
            'skill_area': ['Python development', 'system design', 'best practices'],
            'process_type': ['CI/CD', 'testing', 'code review', 'deployment'],
            'metric': ['deployment time', 'code quality', 'team productivity'],
            'percentage': ['25', '40', '60', '80']
        }
        
        responsibilities = []
        for _ in range(random.randint(3, 6)):
            template = random.choice(templates)
            
            # Fill in placeholders
            for placeholder, options in replacements.items():
                if '{' + placeholder + '}' in template:
                    template = template.replace('{' + placeholder + '}', random.choice(options))
            
            responsibilities.append(template)
        
        return responsibilities
    
    def generate_education(self) -> List[Dict[str, any]]:
        """Generate education entries"""
        num_degrees = random.choices([1, 2], weights=[0.7, 0.3])[0]
        education = []
        
        current_year = datetime.now().year
        
        for i in range(num_degrees):
            if i == 0:  # Most recent/highest degree
                degree = random.choice(self.degrees)
                year = current_year - random.randint(1, 8)
            else:  # Earlier degree
                degree = random.choice([d for d in self.degrees if 'Bachelor' in d])
                year = current_year - random.randint(5, 12)
            
            education.append({
                'degree': degree,
                'university': random.choice(self.universities),
                'graduation_year': year,
                'gpa': f"{random.uniform(3.2, 4.0):.2f}" if random.random() > 0.3 else None
            })
        
        return education
    
    def generate_resume_content(self) -> Dict[str, any]:
        """Generate complete resume content"""
        name = self.generate_person_name()
        
        resume = {
            'personal_info': {
                'name': name,
                'email': self.generate_email(name),
                'phone': self.generate_phone(),
                'location': random.choice([
                    'San Francisco, CA', 'New York, NY', 'Seattle, WA', 'Austin, TX',
                    'Boston, MA', 'Los Angeles, CA', 'Chicago, IL', 'Denver, CO'
                ]),
                'linkedin': f"linkedin.com/in/{name.lower().replace(' ', '-')}",
                'github': f"github.com/{name.lower().replace(' ', '')}"
            },
            'summary': self._generate_professional_summary(),
            'experience': self.generate_work_experience(),
            'education': self.generate_education(),
            'skills': self.generate_skills_for_role('Software Engineer'),
            'projects': self._generate_projects(),
            'certifications': self._generate_certifications()
        }
        
        return resume
    
    def generate_job_description_content(self) -> Dict[str, any]:
        """Generate complete job description content"""
        title = random.choice(self.job_titles)
        company = random.choice(self.companies)
        
        job_desc = {
            'job_info': {
                'title': title,
                'company': company,
                'department': random.choice(['Engineering', 'Product', 'Data', 'Security']),
                'location': random.choice([
                    'San Francisco, CA', 'Remote', 'New York, NY', 'Seattle, WA',
                    'Hybrid - Bay Area', 'Austin, TX', 'Boston, MA'
                ]),
                'job_type': random.choice(['Full-time', 'Contract', 'Full-time Contract']),
                'level': random.choice(['Mid-level', 'Senior', 'Staff', 'Principal'])
            },
            'company_info': {
                'description': f"{company} is a leading technology company...",
                'industry': random.choice(['Technology', 'Software', 'Internet', 'Cloud Services']),
                'size': random.choice(['500-1000', '1000-5000', '5000+', 'Startup'])
            },
            'description': self._generate_job_description(title),
            'responsibilities': self._generate_job_responsibilities(title),
            'requirements': {
                'experience': f"{random.randint(3, 8)}+ years of experience",
                'education': random.choice([
                    "Bachelor's degree in Computer Science or related field",
                    "Master's degree preferred",
                    "Bachelor's or Master's in Engineering, Computer Science, or equivalent experience"
                ]),
                'required_skills': self.generate_skills_for_role(title, 6),
                'preferred_skills': random.sample(
                    [skill for skills in self.skills.values() for skill in skills], 4
                )
            },
            'benefits': {
                'salary': f"${random.randint(120, 300)}K - ${random.randint(300, 500)}K",
                'equity': True,
                'benefits': [
                    'Health, Dental, Vision Insurance',
                    '401k with company matching',
                    'Flexible PTO',
                    'Remote work options',
                    'Professional development budget'
                ]
            }
        }
        
        return job_desc
    
    def _generate_professional_summary(self) -> str:
        """Generate a professional summary"""
        templates = [
            "Experienced software engineer with {years} years of expertise in {domain}. "
            "Proven track record of delivering scalable solutions and leading technical initiatives.",
            
            "Results-driven {role} with strong background in {tech_area}. "
            "Passionate about building innovative products and mentoring engineering teams.",
            
            "Senior engineer specializing in {specialty} with experience at {company_type} companies. "
            "Expert in {tech_stack} and committed to engineering excellence."
        ]
        
        replacements = {
            'years': str(random.randint(3, 12)),
            'domain': random.choice(['web development', 'data systems', 'cloud infrastructure', 'mobile applications']),
            'role': random.choice(['Software Engineer', 'Tech Lead', 'Engineering Manager']),
            'tech_area': random.choice(['full-stack development', 'backend systems', 'data engineering']),
            'specialty': random.choice(['distributed systems', 'machine learning', 'frontend development']),
            'company_type': random.choice(['high-growth', 'Fortune 500', 'startup']),
            'tech_stack': random.choice(['Python/Django', 'React/Node.js', 'Java/Spring', 'AWS/Kubernetes'])
        }
        
        template = random.choice(templates)
        for placeholder, value in replacements.items():
            template = template.replace('{' + placeholder + '}', value)
        
        return template
    
    def _generate_projects(self) -> List[Dict[str, any]]:
        """Generate project entries"""
        project_names = [
            "E-commerce Platform", "Data Analytics Dashboard", "Mobile Banking App",
            "Real-time Chat System", "Machine Learning Pipeline", "Task Management Tool",
            "Social Media Platform", "Video Streaming Service", "IoT Monitoring System"
        ]
        
        projects = []
        for _ in range(random.randint(2, 4)):
            project = {
                'name': random.choice(project_names),
                'description': "Built and deployed a scalable application using modern technologies",
                'technologies': random.sample(
                    [skill for skills in self.skills.values() for skill in skills], 
                    random.randint(3, 6)
                ),
                'duration': f"{random.randint(3, 12)} months"
            }
            projects.append(project)
        
        return projects
    
    def _generate_certifications(self) -> List[str]:
        """Generate certifications"""
        cert_pool = [
            'AWS Certified Solutions Architect',
            'Google Cloud Professional Cloud Architect',
            'Certified Kubernetes Administrator',
            'Microsoft Azure Fundamentals',
            'Scrum Master Certification',
            'PMP Certification',
            'Certified Ethical Hacker',
            'Certified Information Systems Security Professional'
        ]
        
        return random.sample(cert_pool, random.randint(0, 3))
    
    def _generate_job_description(self, title: str) -> str:
        """Generate job description text"""
        return (f"We are looking for a talented {title} to join our growing team. "
                f"In this role, you will be responsible for designing, developing, and "
                f"maintaining high-quality software solutions. You'll work closely with "
                f"cross-functional teams to deliver innovative products that impact millions of users.")
    
    def _generate_job_responsibilities(self, title: str) -> List[str]:
        """Generate job responsibilities"""
        base_responsibilities = [
            "Design and implement scalable software solutions",
            "Collaborate with product managers and designers",
            "Write clean, maintainable, and well-tested code",
            "Participate in code reviews and technical discussions",
            "Mentor junior team members",
            "Stay up-to-date with latest technologies and best practices"
        ]
        
        # Add role-specific responsibilities
        if 'data' in title.lower():
            base_responsibilities.extend([
                "Build and maintain data pipelines",
                "Analyze large datasets to extract insights"
            ])
        elif 'frontend' in title.lower():
            base_responsibilities.extend([
                "Develop responsive user interfaces",
                "Optimize application performance"
            ])
        elif 'backend' in title.lower():
            base_responsibilities.extend([
                "Design and implement APIs",
                "Optimize database performance"
            ])
        
        return random.sample(base_responsibilities, random.randint(5, 8))
    
    def save_dataset(self, output_dir: str, num_resumes: int = 10, num_jobs: int = 5):
        """Generate and save a complete dataset"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Generate resumes
        resumes_dir = output_path / 'resumes'
        resumes_dir.mkdir(exist_ok=True)
        
        for i in range(num_resumes):
            resume_data = self.generate_resume_content()
            
            # Save as JSON
            with open(resumes_dir / f'resume_{i+1:02d}.json', 'w') as f:
                json.dump(resume_data, f, indent=2)
        
        # Generate job descriptions
        jobs_dir = output_path / 'job_descriptions'
        jobs_dir.mkdir(exist_ok=True)
        
        for i in range(num_jobs):
            job_data = self.generate_job_description_content()
            
            # Save as JSON
            with open(jobs_dir / f'job_{i+1:02d}.json', 'w') as f:
                json.dump(job_data, f, indent=2)
        
        print(f"Generated dataset with {num_resumes} resumes and {num_jobs} job descriptions")
        print(f"Saved to: {output_path.absolute()}")


# Example usage
if __name__ == "__main__":
    generator = DatasetGenerator()
    
    # Generate sample resume
    resume = generator.generate_resume_content()
    print("Sample Resume:")
    print(f"Name: {resume['personal_info']['name']}")
    print(f"Skills: {', '.join(resume['skills'][:5])}...")
    
    # Generate sample job description
    job = generator.generate_job_description_content()
    print(f"\nSample Job: {job['job_info']['title']} at {job['job_info']['company']}")
    print(f"Required Skills: {', '.join(job['requirements']['required_skills'])}")
    
    # Generate full dataset
    generator.save_dataset('generated_dataset', num_resumes=5, num_jobs=3)