"""
SkillFitAI Architecture Visualization
=====================================

Creates comprehensive diagrams showing the system architecture,
data flow, and component interactions.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
colors = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#06A77D',
    'data': '#E63946',
    'utils': '#9B59B6'
}

def create_architecture_diagram():
    """Create the main architecture diagram"""
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 16)
    ax.axis('off')
    
    # Title
    ax.text(10, 15.5, 'SkillFitAI System Architecture', 
            fontsize=24, fontweight='bold', ha='center')
    ax.text(10, 14.8, 'Clean Architecture with Modular Components', 
            fontsize=12, ha='center', style='italic', color='gray')
    
    # Layer 1: Entry Point (Top)
    entry = FancyBboxPatch((7, 13), 6, 1.2, boxstyle="round,pad=0.1",
                           facecolor=colors['primary'], edgecolor='black', linewidth=2)
    ax.add_patch(entry)
    ax.text(10, 13.6, 'main.py', fontsize=14, fontweight='bold', 
            ha='center', va='center', color='white')
    ax.text(10, 13.3, 'Entry Point & Orchestrator', fontsize=9, 
            ha='center', va='center', color='white')
    
    # Layer 2: Main Application Class
    app_class = FancyBboxPatch((6.5, 10.5), 7, 1.8, boxstyle="round,pad=0.1",
                               facecolor=colors['secondary'], edgecolor='black', linewidth=2)
    ax.add_patch(app_class)
    ax.text(10, 11.8, 'SkillFitAI Class', fontsize=14, fontweight='bold', 
            ha='center', va='center', color='white')
    ax.text(10, 11.4, '• Initialize Components', fontsize=8, ha='center', va='center', color='white')
    ax.text(10, 11.1, '• Orchestrate Workflow', fontsize=8, ha='center', va='center', color='white')
    ax.text(10, 10.8, '• Generate Results', fontsize=8, ha='center', va='center', color='white')
    
    # Arrow from entry to app class
    arrow1 = FancyArrowPatch((10, 13), (10, 12.3), 
                            arrowstyle='->', mutation_scale=30, 
                            linewidth=3, color='black')
    ax.add_patch(arrow1)
    
    # Layer 3: Core Components
    core_y = 7.5
    core_components = [
        {'name': 'DocumentProcessor', 'x': 1, 'desc': ['Read Documents', 'Extract Text', 'Clean Data']},
        {'name': 'SkillExtractor', 'x': 7, 'desc': ['Extract Skills', 'Categorize', 'Calculate Confidence']},
        {'name': 'ResumeJobMatcher', 'x': 13, 'desc': ['Match Algorithm', 'Score Calculation', 'Generate Results']}
    ]
    
    for comp in core_components:
        box = FancyBboxPatch((comp['x'], core_y), 5, 2.2, boxstyle="round,pad=0.1",
                            facecolor=colors['accent'], edgecolor='black', linewidth=2)
        ax.add_patch(box)
        ax.text(comp['x'] + 2.5, core_y + 1.8, comp['name'], 
                fontsize=12, fontweight='bold', ha='center', color='white')
        
        for i, desc in enumerate(comp['desc']):
            ax.text(comp['x'] + 2.5, core_y + 1.3 - i*0.3, f"• {desc}", 
                   fontsize=8, ha='center', color='white')
        
        # Arrows from app class to core components
        arrow = FancyArrowPatch((10, 10.5), (comp['x'] + 2.5, core_y + 2.2), 
                               arrowstyle='->', mutation_scale=20, 
                               linewidth=2, color='black', alpha=0.7)
        ax.add_patch(arrow)
    
    # Layer 4: Data Models
    model_y = 4.5
    models = [
        {'name': 'Resume Model', 'x': 3, 'attrs': ['file_path', 'raw_text', 'all_skills']},
        {'name': 'JobDescription Model', 'x': 12, 'attrs': ['file_path', 'raw_text', 'all_skills']}
    ]
    
    for model in models:
        box = FancyBboxPatch((model['x'], model_y), 4.5, 1.8, boxstyle="round,pad=0.1",
                            facecolor=colors['data'], edgecolor='black', linewidth=2)
        ax.add_patch(box)
        ax.text(model['x'] + 2.25, model_y + 1.4, model['name'], 
                fontsize=11, fontweight='bold', ha='center', color='white')
        
        for i, attr in enumerate(model['attrs']):
            ax.text(model['x'] + 2.25, model_y + 0.9 - i*0.25, f"• {attr}", 
                   fontsize=7, ha='center', color='white')
        
        # Arrow from DocumentProcessor to models
        arrow = FancyArrowPatch((3.5, core_y), (model['x'] + 2.25, model_y + 1.8), 
                               arrowstyle='->', mutation_scale=15, 
                               linewidth=1.5, color='gray', linestyle='dashed')
        ax.add_patch(arrow)
    
    # Layer 5: Utility Components
    util_y = 1.5
    utils = [
        {'name': 'FileHandler', 'x': 1, 'func': 'File I/O'},
        {'name': 'Logger', 'x': 5.5, 'func': 'Logging'},
        {'name': 'TextProcessor', 'x': 10, 'func': 'Text Cleanup'},
        {'name': 'Results Export', 'x': 14.5, 'func': 'JSON/CSV/TXT'}
    ]
    
    for util in utils:
        box = FancyBboxPatch((util['x'], util_y), 3.5, 1, boxstyle="round,pad=0.05",
                            facecolor=colors['utils'], edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(util['x'] + 1.75, util_y + 0.65, util['name'], 
                fontsize=9, fontweight='bold', ha='center', color='white')
        ax.text(util['x'] + 1.75, util_y + 0.3, util['func'], 
                fontsize=7, ha='center', color='white', style='italic')
    
    # Data flow arrows
    ax.annotate('', xy=(15.5, model_y), xytext=(15.5, core_y),
                arrowprops=dict(arrowstyle='->', lw=2, color=colors['success']))
    ax.text(16, (model_y + core_y) / 2, 'Match', fontsize=8, 
            rotation=270, ha='center', va='center', color=colors['success'])
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=colors['primary'], label='Entry Point'),
        mpatches.Patch(facecolor=colors['secondary'], label='Main Controller'),
        mpatches.Patch(facecolor=colors['accent'], label='Core Processors'),
        mpatches.Patch(facecolor=colors['data'], label='Data Models'),
        mpatches.Patch(facecolor=colors['utils'], label='Utilities')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    # Add border
    border = mpatches.Rectangle((0.2, 0.2), 19.6, 15.6, fill=False, 
                                edgecolor='black', linewidth=2)
    ax.add_patch(border)
    
    plt.tight_layout()
    return fig

def create_workflow_diagram():
    """Create the workflow/data flow diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'SkillFitAI Processing Workflow', 
            fontsize=22, fontweight='bold', ha='center')
    
    # Step 1: Input
    step1 = FancyBboxPatch((0.5, 8), 3, 0.8, boxstyle="round,pad=0.05",
                          facecolor='#E8F4F8', edgecolor=colors['primary'], linewidth=2)
    ax.add_patch(step1)
    ax.text(2, 8.4, '1. Load Data', fontsize=11, fontweight='bold', ha='center')
    
    # Input sources
    resume_box = FancyBboxPatch((0.2, 6.8), 1.5, 0.6, boxstyle="round,pad=0.03",
                               facecolor='#FFE5E5', edgecolor='black')
    ax.add_patch(resume_box)
    ax.text(0.95, 7.1, 'Resumes', fontsize=9, ha='center', fontweight='bold')
    
    jd_box = FancyBboxPatch((2.3, 6.8), 1.5, 0.6, boxstyle="round,pad=0.03",
                           facecolor='#E5F5FF', edgecolor='black')
    ax.add_patch(jd_box)
    ax.text(3.05, 7.1, 'Job Desc', fontsize=9, ha='center', fontweight='bold')
    
    # Step 2: Document Processing
    step2 = FancyBboxPatch((4.5, 8), 3, 0.8, boxstyle="round,pad=0.05",
                          facecolor='#FFF4E5', edgecolor=colors['accent'], linewidth=2)
    ax.add_patch(step2)
    ax.text(6, 8.4, '2. Process Docs', fontsize=11, fontweight='bold', ha='center')
    ax.text(6, 8.1, 'Extract & Clean Text', fontsize=8, ha='center', style='italic')
    
    # Step 3: Skill Extraction
    step3 = FancyBboxPatch((8.5, 8), 3, 0.8, boxstyle="round,pad=0.05",
                          facecolor='#F0E5FF', edgecolor=colors['secondary'], linewidth=2)
    ax.add_patch(step3)
    ax.text(10, 8.4, '3. Extract Skills', fontsize=11, fontweight='bold', ha='center')
    ax.text(10, 8.1, 'Technical & Soft Skills', fontsize=8, ha='center', style='italic')
    
    # Step 4: Matching
    step4 = FancyBboxPatch((5.5, 6), 3, 1.2, boxstyle="round,pad=0.05",
                          facecolor='#E5FFE5', edgecolor=colors['success'], linewidth=2)
    ax.add_patch(step4)
    ax.text(7, 6.9, '4. Match & Score', fontsize=11, fontweight='bold', ha='center')
    ax.text(7, 6.55, '• Compare Skills', fontsize=8, ha='center')
    ax.text(7, 6.25, '• Calculate Similarity', fontsize=8, ha='center')
    
    # Step 5: Results
    step5 = FancyBboxPatch((5.5, 4), 3, 1.2, boxstyle="round,pad=0.05",
                          facecolor='#FFE5F5', edgecolor=colors['data'], linewidth=2)
    ax.add_patch(step5)
    ax.text(7, 4.9, '5. Generate Results', fontsize=11, fontweight='bold', ha='center')
    ax.text(7, 4.55, '• JSON Output', fontsize=8, ha='center')
    ax.text(7, 4.25, '• CSV Export', fontsize=8, ha='center')
    
    # Output types
    outputs = [
        {'name': 'JSON', 'x': 1, 'y': 2},
        {'name': 'CSV', 'x': 4.5, 'y': 2},
        {'name': 'Report', 'x': 8, 'y': 2},
        {'name': 'Summary', 'x': 11.5, 'y': 2}
    ]
    
    for out in outputs:
        box = FancyBboxPatch((out['x'], out['y']), 2, 0.6, boxstyle="round,pad=0.03",
                            facecolor='white', edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(out['x'] + 1, out['y'] + 0.3, out['name'], 
               fontsize=10, ha='center', fontweight='bold')
    
    # Arrows connecting steps
    arrows = [
        ((3.5, 8.4), (4.5, 8.4)),  # 1 to 2
        ((7.5, 8.4), (8.5, 8.4)),  # 2 to 3
        ((10, 8), (7, 7.2)),       # 3 to 4
        ((7, 6), (7, 5.2)),        # 4 to 5
    ]
    
    for start, end in arrows:
        arrow = FancyArrowPatch(start, end, arrowstyle='->', 
                              mutation_scale=25, linewidth=3, color='black')
        ax.add_patch(arrow)
    
    # Connect outputs
    for out in outputs:
        arrow = FancyArrowPatch((7, 4), (out['x'] + 1, out['y'] + 0.6), 
                              arrowstyle='->', mutation_scale=15, 
                              linewidth=1.5, color='gray', linestyle='dashed')
        ax.add_patch(arrow)
    
    # Add data flow indicators
    ax.annotate('', xy=(0.95, 6.8), xytext=(2, 8),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='red', alpha=0.5))
    ax.annotate('', xy=(3.05, 6.8), xytext=(2, 8),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='blue', alpha=0.5))
    
    # Processing metrics box
    metrics_box = FancyBboxPatch((10.5, 5), 3, 2.5, boxstyle="round,pad=0.08",
                                facecolor='#FFFACD', edgecolor='black', linewidth=2)
    ax.add_patch(metrics_box)
    ax.text(12, 7.1, 'Key Metrics', fontsize=11, fontweight='bold', ha='center')
    metrics_text = [
        '• Match Score (0-100%)',
        '• Skill Overlap',
        '• Missing Skills',
        '• Confidence Level',
        '• Recommendations'
    ]
    for i, metric in enumerate(metrics_text):
        ax.text(12, 6.6 - i*0.3, metric, fontsize=8, ha='center')
    
    plt.tight_layout()
    return fig

def create_component_interaction_diagram():
    """Create detailed component interaction diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Component Interaction & Data Flow', 
            fontsize=22, fontweight='bold', ha='center')
    
    # Main components with detailed interactions
    components_data = {
        'FileHandler': {'pos': (1, 7.5), 'size': (2.5, 1.2), 'color': '#9B59B6'},
        'DocumentProcessor': {'pos': (4.5, 7.5), 'size': (2.5, 1.2), 'color': '#F18F01'},
        'SkillExtractor': {'pos': (8, 7.5), 'size': (2.5, 1.2), 'color': '#06A77D'},
        'Matcher': {'pos': (11.5, 7.5), 'size': (2.5, 1.2), 'color': '#E63946'},
        'Resume': {'pos': (2, 5), 'size': (2, 1), 'color': '#FFE5E5'},
        'JobDescription': {'pos': (6, 5), 'size': (2, 1), 'color': '#E5F5FF'},
        'MatchResult': {'pos': (10, 5), 'size': (2, 1), 'color': '#E5FFE5'},
        'Logger': {'pos': (1, 3), 'size': (2, 0.8), 'color': '#D3D3D3'},
        'Results': {'pos': (6, 2), 'size': (2.5, 1.2), 'color': '#FFE5F5'}
    }
    
    # Draw components
    for name, data in components_data.items():
        box = FancyBboxPatch(data['pos'], data['size'][0], data['size'][1], 
                            boxstyle="round,pad=0.05",
                            facecolor=data['color'], edgecolor='black', linewidth=2)
        ax.add_patch(box)
        ax.text(data['pos'][0] + data['size'][0]/2, 
               data['pos'][1] + data['size'][1]/2, 
               name, fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Interaction arrows with labels
    interactions = [
        # (from_comp, to_comp, label)
        ('FileHandler', 'DocumentProcessor', 'files'),
        ('DocumentProcessor', 'SkillExtractor', 'text'),
        ('SkillExtractor', 'Resume', 'skills'),
        ('SkillExtractor', 'JobDescription', 'skills'),
        ('Resume', 'Matcher', 'resume data'),
        ('JobDescription', 'Matcher', 'job data'),
        ('Matcher', 'MatchResult', 'scores'),
        ('MatchResult', 'Results', 'data'),
        ('Logger', 'Results', 'logs')
    ]
    
    for from_comp, to_comp, label in interactions:
        from_pos = components_data[from_comp]['pos']
        from_size = components_data[from_comp]['size']
        to_pos = components_data[to_comp]['pos']
        to_size = components_data[to_comp]['size']
        
        start = (from_pos[0] + from_size[0]/2, from_pos[1])
        end = (to_pos[0] + to_size[0]/2, to_pos[1] + to_size[1])
        
        arrow = FancyArrowPatch(start, end, arrowstyle='->', 
                              mutation_scale=20, linewidth=2, color='black', alpha=0.6)
        ax.add_patch(arrow)
        
        # Add label
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x, mid_y, label, fontsize=7, ha='center', 
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Processing pipeline annotation
    pipeline_box = FancyBboxPatch((0.5, 0.5), 13, 0.8, boxstyle="round,pad=0.05",
                                 facecolor='#F0F8FF', edgecolor='black', linewidth=1.5)
    ax.add_patch(pipeline_box)
    ax.text(7, 0.9, 'Pipeline: Load → Process → Extract → Match → Export', 
           fontsize=10, ha='center', fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_skills_analysis_diagram():
    """Create skills categorization and matching visualization"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # Left: Skill Categories
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('Skill Extraction & Categorization', fontsize=16, fontweight='bold', pad=20)
    
    # Center circle
    center = Circle((5, 5), 1.5, facecolor=colors['primary'], edgecolor='black', linewidth=2)
    ax1.add_patch(center)
    ax1.text(5, 5, 'Skill\nExtractor', fontsize=12, fontweight='bold', 
            ha='center', va='center', color='white')
    
    # Skill categories around
    categories = [
        {'name': 'Technical\nSkills', 'angle': 0, 'color': '#FF6B6B'},
        {'name': 'Soft\nSkills', 'angle': 72, 'color': '#4ECDC4'},
        {'name': 'Domain\nSkills', 'angle': 144, 'color': '#95E1D3'},
        {'name': 'Tools &\nFrameworks', 'angle': 216, 'color': '#FFA07A'},
        {'name': 'Languages', 'angle': 288, 'color': '#87CEEB'}
    ]
    
    radius = 3.5
    for cat in categories:
        angle_rad = np.radians(cat['angle'])
        x = 5 + radius * np.cos(angle_rad)
        y = 5 + radius * np.sin(angle_rad)
        
        circle = Circle((x, y), 0.8, facecolor=cat['color'], 
                       edgecolor='black', linewidth=1.5)
        ax1.add_patch(circle)
        ax1.text(x, y, cat['name'], fontsize=9, fontweight='bold', 
                ha='center', va='center')
        
        # Connect to center
        ax1.plot([5, x], [5, y], 'k--', linewidth=1, alpha=0.5)
    
    # Right: Matching Process
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('Matching Algorithm', fontsize=16, fontweight='bold', pad=20)
    
    # Resume skills
    resume_box = FancyBboxPatch((0.5, 7), 3.5, 2, boxstyle="round,pad=0.08",
                               facecolor='#FFE5E5', edgecolor='black', linewidth=2)
    ax2.add_patch(resume_box)
    ax2.text(2.25, 8.5, 'Resume Skills', fontsize=11, fontweight='bold', ha='center')
    skills = ['Python', 'Java', 'AWS', 'Docker', 'SQL']
    for i, skill in enumerate(skills):
        ax2.text(2.25, 7.9 - i*0.3, f'• {skill}', fontsize=9, ha='center')
    
    # Job skills
    job_box = FancyBboxPatch((6, 7), 3.5, 2, boxstyle="round,pad=0.08",
                            facecolor='#E5F5FF', edgecolor='black', linewidth=2)
    ax2.add_patch(job_box)
    ax2.text(7.75, 8.5, 'Job Requirements', fontsize=11, fontweight='bold', ha='center')
    jd_skills = ['Python', 'AWS', 'K8s', 'React', 'SQL']
    for i, skill in enumerate(jd_skills):
        ax2.text(7.75, 7.9 - i*0.3, f'• {skill}', fontsize=9, ha='center')
    
    # Matching result
    match_box = FancyBboxPatch((2.5, 3.5), 5, 2.5, boxstyle="round,pad=0.08",
                              facecolor='#E5FFE5', edgecolor=colors['success'], linewidth=3)
    ax2.add_patch(match_box)
    ax2.text(5, 5.5, 'Match Result', fontsize=12, fontweight='bold', ha='center')
    ax2.text(5, 5.0, '✓ Matched: Python, AWS, SQL (60%)', fontsize=9, ha='center', color='green')
    ax2.text(5, 4.6, '✗ Missing: K8s, React (40%)', fontsize=9, ha='center', color='red')
    ax2.text(5, 4.2, '+ Extra: Java, Docker', fontsize=9, ha='center', color='blue')
    ax2.text(5, 3.8, 'Overall Score: 75%', fontsize=10, ha='center', fontweight='bold')
    
    # Arrows
    arrow1 = FancyArrowPatch((2.25, 7), (4, 6), arrowstyle='->', 
                           mutation_scale=20, linewidth=2, color='black')
    ax2.add_patch(arrow1)
    
    arrow2 = FancyArrowPatch((7.75, 7), (6, 6), arrowstyle='->', 
                           mutation_scale=20, linewidth=2, color='black')
    ax2.add_patch(arrow2)
    
    plt.tight_layout()
    return fig

def main():
    """Generate all diagrams"""
    print("🎨 Generating SkillFitAI Architecture Visualizations...")
    
    # Create output directory
    from pathlib import Path
    output_dir = Path("results/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate diagrams
    print("\n1. Creating Architecture Diagram...")
    fig1 = create_architecture_diagram()
    fig1.savefig(output_dir / "architecture.png", dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {output_dir}/architecture.png")
    
    print("\n2. Creating Workflow Diagram...")
    fig2 = create_workflow_diagram()
    fig2.savefig(output_dir / "workflow.png", dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {output_dir}/workflow.png")
    
    print("\n3. Creating Component Interaction Diagram...")
    fig3 = create_component_interaction_diagram()
    fig3.savefig(output_dir / "component_interactions.png", dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {output_dir}/component_interactions.png")
    
    print("\n4. Creating Skills Analysis Diagram...")
    fig4 = create_skills_analysis_diagram()
    fig4.savefig(output_dir / "skills_analysis.png", dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {output_dir}/skills_analysis.png")
    
    print("\n✅ All visualizations generated successfully!")
    print(f"📁 Output directory: {output_dir.absolute()}")
    
    # Show all figures
    plt.show()

if __name__ == "__main__":
    main()
