"""
Simple ASCII-based Architecture Diagram Generator
Creates easy-to-view diagrams without external dependencies
"""

def print_main_architecture():
    """Print the main architecture diagram"""
    diagram = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        SKILLFITAI SYSTEM ARCHITECTURE                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

                                  ┌──────────┐
                                  │ main.py  │
                                  │  Entry   │
                                  └─────┬────┘
                                        │
                        ┌───────────────┴───────────────┐
                        │                               │
                        ▼                               ▼
             ┌─────────────────────┐       ┌─────────────────────┐
             │  Command Line Args  │       │    Validation       │
             │  • --resumes        │       │  • Check paths      │
             │  • --jobs           │       │  • Verify files     │
             │  • --output         │       │  • Count inputs     │
             └──────────┬──────────┘       └──────────┬──────────┘
                        │                               │
                        └───────────────┬───────────────┘
                                        │
                                        ▼
                            ┌───────────────────────┐
                            │  SkillFitAI Class     │
                            │  (Main Controller)    │
                            └───────────┬───────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
┌───────────────┐             ┌───────────────┐             ┌───────────────┐
│  Document     │             │     Skill     │             │    Resume     │
│  Processor    │────────────▶│   Extractor   │────────────▶│  Job Matcher  │
│               │             │               │             │               │
│ • Read Files  │             │ • Tech Skills │             │ • Compare     │
│ • Parse Text  │             │ • Soft Skills │             │ • Score       │
│ • Clean Data  │             │ • Categories  │             │ • Results     │
└───────────────┘             └───────────────┘             └───────┬───────┘
        │                               │                           │
        │                               │                           │
        ▼                               ▼                           ▼
┌───────────────┐             ┌───────────────┐             ┌───────────────┐
│ Resume Object │             │ JobDesc Object│             │ MatchResult   │
│               │             │               │             │               │
│ • file_path   │             │ • file_path   │             │ • score       │
│ • raw_text    │             │ • raw_text    │             │ • matched     │
│ • all_skills  │             │ • all_skills  │             │ • missing     │
└───────────────┘             └───────────────┘             └───────┬───────┘
                                                                    │
                                                                    │
                                    ┌───────────────────────────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │  Save Results │
                            └───────┬───────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
            ┌──────────┐    ┌──────────┐    ┌──────────┐
            │   JSON   │    │   CSV    │    │   TXT    │
            │  Output  │    │  Output  │    │  Report  │
            └──────────┘    └──────────┘    └──────────┘
"""
    print(diagram)

def print_workflow():
    """Print the processing workflow"""
    workflow = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          PROCESSING WORKFLOW                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

   ┌─────────────────────────────────────────────────────────────────────┐
   │  PHASE 1: INPUT & INITIALIZATION                                    │
   └─────────────────────────────────────────────────────────────────────┘
         │
         ├──▶ Parse command line arguments
         ├──▶ Validate input directories
         ├──▶ Setup logging system
         └──▶ Initialize components
              │
              ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  PHASE 2: DOCUMENT LOADING                                          │
   └─────────────────────────────────────────────────────────────────────┘
         │
         ├──▶ Scan Resume Directory
         │    ├─ Find all supported files (.pdf, .docx, .doc, .txt, .rtf)
         │    ├─ Read file contents
         │    ├─ Extract text data
         │    └─ Store in memory
         │
         ├──▶ Scan Job Description Directory
         │    ├─ Find all supported files
         │    ├─ Read file contents
         │    ├─ Extract text data
         │    └─ Store in memory
         │
         └──▶ Progress logging (every 5 files)
              │
              ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  PHASE 3: SKILL EXTRACTION                                          │
   └─────────────────────────────────────────────────────────────────────┘
         │
         ├──▶ For each Resume:
         │    ├─ Apply regex patterns for skill matching
         │    ├─ Categorize skills (Technical/Soft/Domain)
         │    ├─ Calculate confidence scores
         │    └─ Create Resume object with skills
         │
         ├──▶ For each Job Description:
         │    ├─ Apply regex patterns for skill matching
         │    ├─ Categorize requirements
         │    ├─ Calculate importance weights
         │    └─ Create JobDescription object with skills
         │
         └──▶ Skills Database:
              ├─ 100+ Programming languages & frameworks
              ├─ 50+ Tools & platforms
              ├─ 30+ Soft skills
              └─ Domain-specific skills
              │
              ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  PHASE 4: MATCHING ALGORITHM                                        │
   └─────────────────────────────────────────────────────────────────────┘
         │
         ├──▶ Nested Loop: For each JD × Resume combination
         │    │
         │    ├──▶ STEP 1: Skill Set Comparison
         │    │    ├─ Find intersection (matched skills)
         │    │    ├─ Find difference (missing skills)
         │    │    └─ Find extras (bonus skills)
         │    │
         │    ├──▶ STEP 2: Score Calculation
         │    │    ├─ Base score = |matched| / |required|
         │    │    ├─ Add frequency bonus
         │    │    ├─ Add context bonus
         │    │    └─ Normalize to 0-100%
         │    │
         │    ├──▶ STEP 3: Generate MatchResult
         │    │    ├─ Overall score
         │    │    ├─ Matched skills list
         │    │    ├─ Missing skills list
         │    │    ├─ Confidence level
         │    │    └─ Recommendation
         │    │
         │    └──▶ Store result in list
         │
         └──▶ Progress logging (every 50 matches)
              │
              ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  PHASE 5: RESULTS GENERATION                                        │
   └─────────────────────────────────────────────────────────────────────┘
         │
         ├──▶ Calculate Statistics
         │    ├─ Average match score
         │    ├─ Best match
         │    ├─ Score distribution
         │    └─ Processing time
         │
         ├──▶ Export JSON File
         │    ├─ Full match details
         │    ├─ All skills listed
         │    └─ Structured format
         │
         ├──▶ Export CSV File
         │    ├─ Tabular format
         │    ├─ Summary columns
         │    └─ Easy to analyze
         │
         └──▶ Generate Text Report
              ├─ Executive summary
              ├─ Top 10 matches
              ├─ Score distribution chart
              └─ Detailed statistics
              │
              ▼
         ┌────────────┐
         │  COMPLETE  │
         └────────────┘

   Example Processing Stats:
   ┌──────────────────────────────────────┐
   │ Resumes:              25             │
   │ Job Descriptions:     25             │
   │ Total Matches:        625            │
   │ Processing Time:      ~3 seconds     │
   │ Average Score:        70.28%         │
   │ Best Match:           100.00%        │
   └──────────────────────────────────────┘
"""
    print(workflow)

def print_skill_matching():
    """Print the skill matching algorithm"""
    matching = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        SKILL MATCHING ALGORITHM                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

   EXAMPLE SCENARIO:
   ─────────────────────────────────────────────────────────────────────────

   Resume Skills:        {Python, Java, AWS, Docker, SQL, Git, Linux}
   Job Requirements:     {Python, AWS, Kubernetes, React, SQL, TypeScript}

   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 1: SET OPERATIONS                                             │
   └─────────────────────────────────────────────────────────────────────┘
   
   Matched Skills (Intersection):
   ┌────────────────────────────┐
   │  ✓ Python                  │
   │  ✓ AWS                     │
   │  ✓ SQL                     │
   └────────────────────────────┘
   Total Matched: 3
   
   Missing Skills (Required but not present):
   ┌────────────────────────────┐
   │  ✗ Kubernetes              │
   │  ✗ React                   │
   │  ✗ TypeScript              │
   └────────────────────────────┘
   Total Missing: 3
   
   Bonus Skills (Extra skills candidate has):
   ┌────────────────────────────┐
   │  + Java                    │
   │  + Docker                  │
   │  + Git                     │
   │  + Linux                   │
   └────────────────────────────┘
   Total Bonus: 4

   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 2: SCORE CALCULATION                                          │
   └─────────────────────────────────────────────────────────────────────┘
   
   Base Jaccard Similarity:
   ═══════════════════════════
   Intersection = 3 (Python, AWS, SQL)
   Union = 10 (all unique skills)
   
   Jaccard = |Intersection| / |Union|
          = 3 / 10
          = 0.30 (30%)
   
   Skill Match Percentage:
   ════════════════════════
   Required Skills = 6
   Matched Skills = 3
   
   Match % = (Matched / Required) × 100
          = (3 / 6) × 100
          = 50%
   
   Bonuses:
   ════════
   • Frequency Bonus:     +5%  (skills appear multiple times)
   • Critical Skills:     +15% (Python, AWS are high-value)
   • Context Bonus:       +10% (skills in relevant context)
   
   Final Overall Score:
   ═══════════════════
   Base Score:      50%
   + Bonuses:       30%
   ─────────────────────
   Total:           80%

   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 3: GENERATE RECOMMENDATION                                    │
   └─────────────────────────────────────────────────────────────────────┘
   
   Score Range         Recommendation       Action
   ───────────────────────────────────────────────────────────────────
   90% - 100%     │    Excellent Match   │   Strong Candidate
   80% - 89%      │    Good Match        │   Interview
   60% - 79%      │    Fair Match        │   Consider with training
   40% - 59%      │    Moderate Match    │   Review carefully
   0%  - 39%      │    Poor Match        │   Not recommended
   
   This Example: 80% → "Good Match" → Recommend for Interview

   ┌─────────────────────────────────────────────────────────────────────┐
   │  FINAL MATCH RESULT                                                 │
   └─────────────────────────────────────────────────────────────────────┘
   
   {
     "overall_score": 80.0,
     "skill_match_percentage": 50.0,
     "matched_skills": ["Python", "AWS", "SQL"],
     "missing_skills": ["Kubernetes", "React", "TypeScript"],
     "bonus_skills": ["Java", "Docker", "Git", "Linux"],
     "recommendation": "Good Match",
     "confidence": 0.75
   }

   ┌─────────────────────────────────────────────────────────────────────┐
   │  CONFIDENCE CALCULATION                                             │
   └─────────────────────────────────────────────────────────────────────┘
   
   Confidence = min(1.0, matched_count / max(5, required_count))
              = min(1.0, 3 / 6)
              = 0.50
   
   Context Boost:     +0.15 (skills in experience section)
   Frequency Boost:   +0.10 (skills mentioned multiple times)
   ─────────────────────────────────────────────────────────────────
   Final Confidence:  0.75 (High Confidence)
"""
    print(matching)

def print_component_details():
    """Print detailed component information"""
    details = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        COMPONENT DETAILS                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────────┐
│  1. DOCUMENT PROCESSOR (src/core/document_processor.py)                      │
└──────────────────────────────────────────────────────────────────────────────┘

   Purpose: Extract text from various document formats
   
   Supported Formats:
   ┌────────────┬─────────────────────────────────────────────────────────┐
   │ Format     │ Processing Method                                       │
   ├────────────┼─────────────────────────────────────────────────────────┤
   │ .txt       │ Direct text reading with UTF-8 encoding                 │
   │ .pdf       │ pdfplumber library (with fallback)                      │
   │ .docx      │ python-docx library (with fallback)                     │
   │ .doc       │ Text extraction with encoding detection                 │
   │ .rtf       │ RTF control sequence removal                            │
   └────────────┴─────────────────────────────────────────────────────────┘
   
   Key Methods:
   • read_document()          - Main entry point
   • clean_text()             - Remove noise and normalize
   • redact_sensitive_info()  - Remove PII
   • extract_metadata()       - File information
   • validate_document()      - Format validation

┌──────────────────────────────────────────────────────────────────────────────┐
│  2. SKILL EXTRACTOR (src/core/skill_extractor.py)                           │
└──────────────────────────────────────────────────────────────────────────────┘

   Purpose: Identify and categorize skills from text
   
   Skill Categories (150+ total skills):
   
   ┌─ Technical Skills ───────────────────────────────────────────────┐
   │                                                                  │
   │  Programming Languages (25+):                                   │
   │    Python, Java, JavaScript, TypeScript, C++, C#, Go, Rust...  │
   │                                                                  │
   │  Web Technologies (30+):                                        │
   │    React, Angular, Vue.js, Node.js, HTML5, CSS3, Bootstrap...  │
   │                                                                  │
   │  Backend Frameworks (15+):                                      │
   │    Django, Flask, FastAPI, Spring Boot, Express.js...          │
   │                                                                  │
   │  Databases (15+):                                               │
   │    MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch...         │
   │                                                                  │
   │  Cloud & DevOps (30+):                                          │
   │    AWS, Azure, GCP, Docker, Kubernetes, Jenkins, Terraform...  │
   │                                                                  │
   │  ML/AI Tools (15+):                                             │
   │    TensorFlow, PyTorch, Keras, scikit-learn, Pandas, NumPy... │
   └──────────────────────────────────────────────────────────────────┘
   
   ┌─ Soft Skills ────────────────────────────────────────────────────┐
   │  • Communication & Presentation                                  │
   │  • Leadership & Team Management                                  │
   │  • Problem Solving & Critical Thinking                           │
   │  • Collaboration & Teamwork                                      │
   │  • Adaptability & Learning Agility                               │
   └──────────────────────────────────────────────────────────────────┘
   
   Extraction Process:
   ┌────────────────────────────────────────────────────────────────┐
   │  Text Input                                                    │
   │     ↓                                                          │
   │  Regex Pattern Matching (compiled patterns for performance)    │
   │     ↓                                                          │
   │  Context Analysis (check surrounding words)                    │
   │     ↓                                                          │
   │  Confidence Scoring (0.0 to 1.0)                              │
   │     ↓                                                          │
   │  Categorization (Technical/Soft/Domain)                        │
   │     ↓                                                          │
   │  Frequency Counting                                            │
   │     ↓                                                          │
   │  SkillMatch Objects                                            │
   └────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  3. RESUME JOB MATCHER (src/core/matcher.py)                                │
└──────────────────────────────────────────────────────────────────────────────┘

   Purpose: Match resumes with job descriptions
   
   Matching Algorithm:
   ┌────────────────────────────────────────────────────────────────┐
   │  INPUT:                                                        │
   │    • Resume object with skills                                 │
   │    • JobDescription object with requirements                   │
   │                                                                │
   │  PROCESS:                                                      │
   │    1. Convert skills to sets                                   │
   │    2. Calculate intersection (matched)                         │
   │    3. Calculate differences (missing/extra)                    │
   │    4. Compute base similarity (Jaccard)                        │
   │    5. Apply weighting factors                                  │
   │    6. Generate confidence score                                │
   │    7. Create recommendation                                    │
   │                                                                │
   │  OUTPUT:                                                       │
   │    • MatchResult object with scores and lists                  │
   └────────────────────────────────────────────────────────────────┘
   
   Scoring Formula:
   ═══════════════════════════════════════════════════════════════
   
   overall_score = base_score + bonus_factor
   
   base_score = |matched_skills| / |required_skills|
   
   bonus_factor = min(0.3, extra_skills_count × 0.01)
   
   confidence = min(1.0, matched_count / max(5, required_count))
   
   ═══════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│  4. DATA MODELS (src/models/)                                               │
└──────────────────────────────────────────────────────────────────────────────┘

   Resume Model (resume.py):
   ┌──────────────────────────────────────┐
   │  Attributes:                         │
   │    • file_path: str                  │
   │    • file_name: str                  │
   │    • raw_text: str                   │
   │    • all_skills: Set[str]            │
   │    • file_format: str                │
   │    • metadata: Dict                  │
   │                                      │
   │  Methods:                            │
   │    • __init__()                      │
   │    • __repr__()                      │
   └──────────────────────────────────────┘
   
   JobDescription Model (job_description.py):
   ┌──────────────────────────────────────┐
   │  Attributes:                         │
   │    • file_path: str                  │
   │    • file_name: str                  │
   │    • raw_text: str                   │
   │    • all_skills: Set[str]            │
   │    • file_format: str                │
   │    • metadata: Dict                  │
   │                                      │
   │  Methods:                            │
   │    • __init__()                      │
   │    • __repr__()                      │
   └──────────────────────────────────────┘
   
   MatchResult Model:
   ┌──────────────────────────────────────┐
   │  Attributes:                         │
   │    • overall_score: float            │
   │    • skill_match_percentage: float   │
   │    • matched_skills: List[str]       │
   │    • missing_skills: List[str]       │
   │    • bonus_skills: List[str]         │
   │    • recommendation: str             │
   │    • confidence: float               │
   └──────────────────────────────────────┘
"""
    print(details)

def main():
    """Generate all diagrams"""
    print("\n" + "="*80)
    print("SKILLFITAI - SYSTEM ARCHITECTURE & COMPONENT DIAGRAMS")
    print("="*80 + "\n")
    
    print_main_architecture()
    input("\nPress Enter to continue to Workflow...")
    
    print("\n" + "="*80 + "\n")
    print_workflow()
    input("\nPress Enter to continue to Skill Matching...")
    
    print("\n" + "="*80 + "\n")
    print_skill_matching()
    input("\nPress Enter to continue to Component Details...")
    
    print("\n" + "="*80 + "\n")
    print_component_details()
    
    print("\n" + "="*80)
    print("END OF DOCUMENTATION")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
