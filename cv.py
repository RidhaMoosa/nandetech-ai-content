# Regenerate the PDF without emojis
from fpdf import FPDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Set title font
pdf.set_font("Arial", size=16, style='B')
pdf.cell(200, 10, txt="Ntokozo Hadebe - CV", ln=True, align="C")
pdf.ln(10)

# Add Contact Section
pdf.set_font("Arial", size=12, style='B')
pdf.cell(0, 10, txt="Contact", ln=True)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="""066 549 5421 (Mobile)
hopein95@gmail.com
LinkedIn: https://www.linkedin.com/in/ntokozo-hadebe-0a2854279
""")
pdf.ln(5)

# Add Summary Section
pdf.set_font("Arial", size=12, style='B')
pdf.cell(0, 10, txt="Summary", ln=True)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="""Motivated graduate in Software Development with a solid foundation in programming, 
problem-solving, and Agile methodologies. I am passionate about creating robust, maintainable software 
and applying data science to deliver impactful insights. My experience spans multiple programming 
languages and tools, with recent exposure to C# for application development.

Key strengths include:
- Proficiency in C#, Python, Java, JavaScript, and SQL.
- Strong understanding of relational databases and version control systems like Git.
- Familiarity with testing methodologies to ensure software quality.
- Active participation in Agile development ceremonies and collaborative team projects.

I am eager to grow in roles that challenge me to build secure, scalable solutions while contributing 
to innovative software products.
""")
pdf.ln(5)

# Add Education Section
pdf.set_font("Arial", size=12, style='B')
pdf.cell(0, 10, txt="Education", ln=True)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="""WeThinkCode_
NQF Level 5 - Information Technology (Systems Development) | Computer Software Engineering
2022 – 2023

ExploreAI Academy
Data Science Certification
January 2024 – December 2024
""")
pdf.ln(5)

# Add Technical Skills Section
pdf.set_font("Arial", size=12, style='B')
pdf.cell(0, 10, txt="Technical Skills", ln=True)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="""- Programming Languages: C#, Python, Java, JavaScript, SQL
- Databases: Relational Databases (SQL)
- Version Control: Git (Distributed Version Control Systems)
- Development Practices: Agile Methodologies, Testing & Debugging
- Tools: GitHub, Streamlit
""")
pdf.ln(5)

# Add Experience & Projects Section
pdf.set_font("Arial", size=12, style='B')
pdf.cell(0, 10, txt="Experience & Projects", ln=True)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="""C# Application Development
- Built secure and maintainable codebases following best practices.
- Worked on implementing solutions that integrate seamlessly with relational databases.

SQL Projects
- Designed and managed relational database systems for application backends.
- Optimized queries for performance and data integrity.

Agile Collaboration
- Actively participated in Agile ceremonies like stand-ups and retrospectives to improve team workflows.

Recommendation Systems
- Developed machine learning models for personalized recommendations.
- Conducted exploratory data analysis to derive actionable insights.

Version Control with Git
- Collaborated on team projects using Git to manage codebases and track changes efficiently.
""")
pdf.ln(5)

# Add Top Skills Section
pdf.set_font("Arial", size=12, style='B')
pdf.cell(0, 10, txt="Top Skills", ln=True)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="""- Software Development: Strong coding skills in C#, Python, Java, and JavaScript.
- SQL & Databases: Proficient in designing, querying, and maintaining relational databases.
- Version Control: Experienced with Git for distributed version control.
- Collaboration & Communication: Proven ability to work in teams using Agile methodologies.
""")

# Save the PDF
file_path = "Ntokozo_Hadebe_CV.pdf"
pdf.output(file_path)
file_path
