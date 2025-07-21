"""
Education Demo Module

Implements the education industry demonstration using the BaseDemo framework.
"""
from typing import Dict, List, Any
import random
from faker import Faker
from .base_demo import BaseDemo

fake = Faker()


class EducationDemo(BaseDemo):
    """Education assistant demonstration."""
    
    def __init__(self, ai_service=None, context_service=None):
        from services.prompt_service import Industry
        super().__init__("Education", Industry.EDUCATION, ai_service, context_service)
    
    def generate_context(self) -> Dict[str, Any]:
        """Generate realistic education context using Faker."""
        user_type = random.choice(["Student", "Parent", "Educator"])
        
        context = {
            "user_profile": {
                "name": fake.name(),
                "email": fake.email(),
                "user_type": user_type,
                "institution": f"{fake.city()} {random.choice(['Elementary', 'Middle', 'High School', 'University', 'Community College'])}",
                "location": f"{fake.city()}, {fake.state()}"
            },
            "academic_info": {
                "current_semester": random.choice(["Fall 2024", "Spring 2025", "Summer 2025"]),
                "academic_year": "2024-2025",
                "grade_level": random.choice([
                    "Kindergarten", "1st Grade", "2nd Grade", "3rd Grade", "4th Grade", "5th Grade",
                    "6th Grade", "7th Grade", "8th Grade", "9th Grade", "10th Grade", "11th Grade", "12th Grade",
                    "College Freshman", "College Sophomore", "College Junior", "College Senior", "Graduate Student"
                ]) if user_type == "Student" else "N/A",
                "gpa": round(random.uniform(2.5, 4.0), 2) if user_type == "Student" else None,
                "credit_hours": None  # Will be set after grade_level is determined
            },
            "learning_profile": {
                "learning_style": random.choice(["Visual", "Auditory", "Kinesthetic", "Reading/Writing"]),
                "subject_strengths": random.sample([
                    "Mathematics", "Science", "English", "History", "Art", "Music", "Physical Education"
                ], random.randint(2, 3)),
                "challenging_subjects": random.sample([
                    "Mathematics", "Science", "Foreign Language", "Writing", "Public Speaking"
                ], random.randint(1, 2)),
                "study_preferences": {
                    "environment": random.choice(["Quiet library", "Study group", "Home", "Coffee shop"]),
                    "time_of_day": random.choice(["Early morning", "Afternoon", "Evening", "Late night"]),
                    "break_frequency": random.choice(["Every 30 min", "Every hour", "Every 2 hours"])
                }
            },
            "current_situation": {
                "upcoming_deadlines": [
                    {
                        "assignment": random.choice(["Research paper", "Math test", "Science project", "Book report", "Presentation"]),
                        "subject": random.choice(["English", "Mathematics", "Science", "History", "Art"]),
                        "due_date": fake.date_between(start_date='+1d', end_date='+14d').strftime('%Y-%m-%d'),
                        "completion_status": random.choice(["Not started", "In progress", "Nearly complete"])
                    }
                    for _ in range(random.randint(1, 3))
                ],
                "current_challenges": random.sample([
                    "Time management", "Test anxiety", "Understanding concepts", "Staying motivated",
                    "Balancing activities", "Note-taking", "Study habits"
                ], random.randint(1, 3)),
                "support_needed": random.choice(["Tutoring", "Study strategies", "Organization help", "Motivation", "Test prep"])
            },
            "resources_and_tools": {
                "technology_access": {
                    "devices": random.sample(["Laptop", "Tablet", "Smartphone", "Desktop"], random.randint(2, 3)),
                    "internet_quality": random.choice(["Excellent", "Good", "Fair", "Poor"]),
                    "software_access": random.sample([
                        "Microsoft Office", "Google Workspace", "Adobe Creative", "Programming tools", "Research databases"
                    ], random.randint(2, 4))
                },
                "study_resources": {
                    "textbooks": random.choice(["All required", "Most required", "Some required", "Few required"]),
                    "online_resources": random.sample([
                        "Khan Academy", "Coursera", "YouTube tutorials", "Library databases", "Study apps"
                    ], random.randint(2, 4)),
                    "support_services": random.sample([
                        "Tutoring center", "Writing center", "Library assistance", "Counseling services", "Study groups"
                    ], random.randint(1, 3))
                }
            },
            "goals_and_aspirations": {
                "short_term_goals": random.sample([
                    "Improve grades", "Better study habits", "Reduce stress", "Complete assignments on time",
                    "Participate more in class", "Join study group"
                ], random.randint(2, 3)),
                "long_term_goals": random.sample([
                    "Graduate with honors", "Get into college", "Choose career path", "Develop leadership skills",
                    "Master difficult subjects", "Build confidence"
                ], random.randint(1, 2)),
                "career_interests": random.sample([
                    "STEM fields", "Healthcare", "Education", "Business", "Arts", "Social services", "Technology"
                ], random.randint(1, 3)) if user_type == "Student" else []
            }
        }
        
        # Set credit hours for college students
        if user_type == "Student" and "College" in context["academic_info"]["grade_level"]:
            context["academic_info"]["credit_hours"] = random.randint(12, 18)
        
        # Add user-type specific context
        if user_type == "Parent":
            context["children"] = [
                {
                    "name": fake.first_name(),
                    "age": random.randint(5, 18),
                    "grade": random.choice(["K", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"]),
                    "school": f"{fake.city()} {random.choice(['Elementary', 'Middle', 'High School'])}"
                }
                for _ in range(random.randint(1, 3))
            ]
        elif user_type == "Educator":
            context["teaching_info"] = {
                "role": random.choice(["Teacher", "Principal", "Counselor", "Tutor", "Administrator"]),
                "subject_area": random.choice(["Mathematics", "English", "Science", "History", "Art", "Music", "Special Education"]),
                "years_experience": random.randint(1, 30),
                "class_size": random.randint(15, 35),
                "grade_levels": random.choice(["K-2", "3-5", "6-8", "9-12", "Mixed"])
            }
        
        return context
    
    def get_sample_queries(self) -> List[str]:
        """Get sample education queries."""
        return [
            "Help me study for my math test",
            "How can I improve my writing skills?",
            "I'm struggling with time management",
            "What study techniques work best?",
            "How do I prepare for college applications?"
        ]
    
    def get_query_placeholder(self) -> str:
        """Get placeholder text for education queries."""
        return "e.g., Help me study for my math test, How can I improve my writing skills?"
    
    def get_system_message_generic(self) -> str:
        """Get system message for generic education responses."""
        return "You are a helpful education assistant. Provide general study tips, learning strategies, and educational guidance without using specific student context."
    
    def get_system_message_contextual(self) -> str:
        """Get system message for contextual education responses."""
        return """You are a personalized education assistant. Use the provided student/parent/educator context to give specific, relevant educational guidance. Consider:
- Learning style and academic strengths/challenges
- Current assignments and deadlines
- Grade level and academic goals
- Available resources and technology
- Individual learning needs and preferences

Provide actionable, encouraging, and age-appropriate advice."""
    
    def generate_fallback_generic_response(self, query: str) -> str:
        """Generate fallback generic response for education queries."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['study', 'test', 'exam', 'quiz']):
            return """📚 **Effective Study Strategies - My Academic Guidance:**

**As your academic advisor, here's my proven study framework:**

**The SMART Study System:**
- **S**paced repetition - Review material multiple times over days/weeks
- **M**ulti-modal learning - Use visual, auditory, and kinesthetic methods
- **A**ctive recall - Test yourself instead of just re-reading
- **R**egular breaks - 25-minute focused sessions with 5-minute breaks
- **T**eaching others - Explain concepts to solidify understanding

**Pre-Test Preparation Strategy:**
1. **2 weeks before:** Create comprehensive study schedule
2. **1 week before:** Focus on practice problems and weak areas
3. **3 days before:** Review key concepts, no new material
4. **1 day before:** Light review, early bedtime, prepare materials
5. **Test day:** Healthy breakfast, arrive early, stay calm

**Study Environment Optimization:**
- **Consistent location** - Train your brain for focus
- **Eliminate distractions** - Phone away, notifications off
- **Good lighting and ventilation** - Physical comfort aids mental performance
- **All materials ready** - Avoid interruptions to find supplies

**Memory Enhancement Techniques:**
- **Mnemonics** - Create memorable associations
- **Mind mapping** - Visual organization of information
- **Flashcards** - Active recall practice
- **Practice tests** - Simulate exam conditions
- **Study groups** - Collaborative learning and accountability

**Test-Taking Strategies:**
- **Read instructions carefully** - Understand what's being asked
- **Time management** - Allocate time per section/question
- **Answer easy questions first** - Build confidence and momentum
- **Review answers** - Check for careless mistakes if time permits

Remember: Consistent daily study beats cramming every time. I'm here to help you develop sustainable study habits! 🎯"""
        
        elif any(word in query_lower for word in ['writing', 'essay', 'paper']):
            return """✍️ **Writing Excellence - My Academic Writing Guidance:**

**As your writing instructor, let me guide you through the writing process:**

**The 5-Stage Writing Process:**
1. **Pre-writing (25%)** - Brainstorm, research, outline
2. **Drafting (25%)** - Get ideas down, don't worry about perfection
3. **Revising (25%)** - Reorganize, strengthen arguments, improve flow
4. **Editing (15%)** - Grammar, punctuation, sentence structure
5. **Proofreading (10%)** - Final check for errors

**Essay Structure Framework:**
**Introduction:**
- Hook to grab reader's attention
- Background context
- Clear thesis statement (your main argument)

**Body Paragraphs:**
- Topic sentence supporting thesis
- Evidence and examples
- Analysis explaining significance
- Transition to next point

**Conclusion:**
- Restate thesis in new words
- Summarize key points
- End with broader implications or call to action

**My Writing Improvement Strategies:**
- **Read actively** - Analyze how good writers structure arguments
- **Write regularly** - Daily journaling builds fluency
- **Seek feedback** - Fresh eyes catch what you miss
- **Revise ruthlessly** - First draft is just the beginning
- **Read aloud** - Hear awkward phrasing and run-on sentences

**Research and Citation:**
- **Credible sources** - Academic databases, peer-reviewed articles
- **Take detailed notes** - Include page numbers for citations
- **Avoid plagiarism** - Always cite sources, paraphrase properly
- **Multiple perspectives** - Consider different viewpoints

**Common Writing Challenges I Help Students Overcome:**
- **Writer's block** - Start with freewriting, outline, or discussion
- **Weak thesis** - Make it specific, arguable, and significant
- **Poor organization** - Use topic sentences and transitions
- **Wordiness** - Every word should serve a purpose
- **Weak conclusions** - Don't just repeat, synthesize and extend

**Editing Checklist:**
- Does each paragraph support the thesis?
- Are transitions smooth and logical?
- Is the tone appropriate for the audience?
- Are sentences varied in length and structure?
- Have you eliminated unnecessary words?

Your writing is your voice - let's make it clear, compelling, and confident! 📝"""
        
        elif any(word in query_lower for word in ['time', 'management', 'organize']):
            return """⏰ **Time Management Mastery - My Academic Success Coaching:**

**As your academic success coach, time management is the foundation of achievement:**

**The Academic Time Management System:**
**Priority Matrix (Eisenhower Method):**
- **Urgent + Important** - Do immediately (upcoming deadlines)
- **Important + Not Urgent** - Schedule (long-term projects)
- **Urgent + Not Important** - Delegate or minimize (interruptions)
- **Neither** - Eliminate (time wasters)

**Weekly Planning Ritual:**
- **Sunday evening** - Review upcoming week, plan major tasks
- **Daily check-ins** - 5 minutes each morning to prioritize
- **Weekly review** - What worked? What needs adjustment?

**The Academic Calendar Strategy:**
1. **Semester overview** - Mark all major deadlines, exams, breaks
2. **Monthly goals** - Break large projects into monthly milestones
3. **Weekly schedules** - Balance study time across all subjects
4. **Daily priorities** - 3 most important tasks each day

**Study Time Optimization:**
- **Time blocking** - Dedicated hours for specific subjects
- **Energy management** - Schedule difficult tasks during peak hours
- **Batch similar tasks** - Group reading, writing, problem-solving
- **Buffer time** - Always add 25% more time than estimated

**Procrastination Solutions:**
- **2-minute rule** - If it takes less than 2 minutes, do it now
- **Pomodoro Technique** - 25 minutes focused work, 5-minute break
- **Accountability partners** - Study buddies and check-ins
- **Reward systems** - Celebrate completed tasks

**Digital Organization Tools:**
- **Calendar apps** - Google Calendar, Apple Calendar for scheduling
- **Task managers** - Todoist, Any.do for assignment tracking
- **Note-taking** - Notion, OneNote for organized class materials
- **Focus apps** - Forest, Freedom to eliminate distractions

**Balance and Self-Care:**
- **Sleep schedule** - 7-9 hours nightly, consistent bedtime
- **Exercise routine** - 30 minutes daily improves focus and memory
- **Social connections** - Maintain friendships and family relationships
- **Downtime** - Schedule relaxation and hobbies

**Emergency Strategies (When Behind):**
- **Triage** - Focus on highest-impact, nearest-deadline tasks
- **Communicate** - Talk to professors about extensions if needed
- **Simplify** - Reduce commitments temporarily
- **Learn** - Analyze what went wrong to prevent future issues

**My Time Management Mantras:**
- "Perfect is the enemy of done"
- "You can't manage time, only your choices"
- "Consistency beats intensity"
- "Plan your work, work your plan"

Remember: Time management is really energy and attention management. Let's optimize all three! ⚡"""
        
        elif any(word in query_lower for word in ['technique', 'method', 'learn']):
            return """🧠 **Learning Science - My Evidence-Based Teaching Methods:**

**As your learning specialist, let me share the most effective techniques backed by research:**

**The Science of Learning - Top 6 Methods:**

**1. Active Recall (Most Powerful)**
- **What:** Testing yourself instead of re-reading
- **How:** Flashcards, practice problems, explaining without notes
- **Why:** Forces brain to retrieve information, strengthening memory
- **Example:** Close your book and write everything you remember

**2. Spaced Repetition**
- **What:** Reviewing material at increasing intervals
- **How:** Review after 1 day, 3 days, 1 week, 2 weeks, 1 month
- **Why:** Fights forgetting curve, builds long-term retention
- **Tools:** Anki, Quizlet with spaced repetition algorithms

**3. Interleaving**
- **What:** Mixing different topics/problem types in one session
- **How:** Don't do 20 algebra problems in a row; mix algebra, geometry, statistics
- **Why:** Improves discrimination and transfer of learning
- **Application:** Alternate between subjects during study sessions

**4. Elaborative Interrogation**
- **What:** Asking "why" and "how" questions
- **How:** "Why does this work?" "How does this connect to...?"
- **Why:** Creates deeper understanding and connections
- **Practice:** Explain concepts in your own words

**5. Dual Coding**
- **What:** Combining visual and verbal information
- **How:** Diagrams + explanations, mind maps + notes
- **Why:** Uses multiple memory pathways
- **Example:** Draw concepts while explaining them aloud

**6. Self-Explanation**
- **What:** Explaining steps and reasoning to yourself
- **How:** Talk through problem-solving process
- **Why:** Identifies gaps in understanding
- **Method:** "I'm doing this because..."

**Learning Style Optimization:**
**Visual Learners:**
- Mind maps, diagrams, color-coding
- Charts, graphs, infographics
- Highlighting and visual organization

**Auditory Learners:**
- Record and replay lectures
- Discuss concepts with others
- Read aloud, use rhymes and music

**Kinesthetic Learners:**
- Hands-on activities and experiments
- Movement while studying
- Building models, using manipulatives

**Reading/Writing Learners:**
- Detailed note-taking
- Rewriting information
- Lists, outlines, written summaries

**Memory Palace Technique:**
- Associate information with familiar locations
- Create vivid, unusual mental images
- Follow a consistent route through your "palace"
- Practice regularly to strengthen associations

**Metacognitive Strategies:**
- **Planning:** What do I need to learn? How will I approach it?
- **Monitoring:** Do I understand this? Am I making progress?
- **Evaluating:** What worked well? What should I change?

**Common Learning Mistakes to Avoid:**
- **Highlighting everything** - Be selective, focus on key concepts
- **Re-reading without testing** - Passive review creates illusion of knowledge
- **Cramming** - Distributed practice is far more effective
- **Single-method studying** - Combine multiple techniques
- **Ignoring mistakes** - Errors are learning opportunities

**Creating Your Personal Learning System:**
1. **Assess your current methods** - What's working? What isn't?
2. **Choose 2-3 new techniques** - Don't try to change everything at once
3. **Practice consistently** - New habits take 21-66 days to form
4. **Monitor and adjust** - Track what improves your performance
5. **Teach others** - Ultimate test of understanding

**The Growth Mindset Advantage:**
- View challenges as opportunities to grow
- See effort as the path to mastery
- Learn from criticism and setbacks
- Find inspiration in others' success

Remember: Learning how to learn is the most valuable skill you can develop. It will serve you throughout your entire life! 🌟"""
        
        elif any(word in query_lower for word in ['college', 'application', 'university']):
            return """🎓 **College Success Planning - My Comprehensive Guidance:**

**As your college counselor, let me guide you through this important journey:**

**The Complete College Preparation Timeline:**

**Freshman Year - Foundation Building:**
- **Academics:** Take challenging courses, establish good study habits
- **Exploration:** Join clubs, try different activities, discover interests
- **Relationships:** Build connections with teachers and mentors
- **Planning:** Start thinking about potential career paths

**Sophomore Year - Skill Development:**
- **Academics:** Continue rigorous coursework, maintain strong GPA
- **Leadership:** Take on leadership roles in activities you enjoy
- **Community:** Begin volunteer work in areas of interest
- **Exploration:** Consider summer programs or internships

**Junior Year - Intensive Preparation:**
- **Academics:** Take AP/IB courses, maintain upward grade trend
- **Testing:** Prepare for and take SAT/ACT (multiple times if needed)
- **Research:** Create preliminary college list, visit campuses
- **Essays:** Begin brainstorming and drafting personal statements

**Senior Year - Application Excellence:**
- **Applications:** Submit early decision/action applications
- **Essays:** Polish personal statements and supplemental essays
- **Interviews:** Prepare for and attend college interviews
- **Decisions:** Make final college choice and prepare for transition

**Academic Excellence Strategies:**
**GPA Optimization:**
- Aim for upward trend - colleges love improvement
- Take challenging courses but don't overload
- Seek help early when struggling
- Build relationships with teachers for recommendations

**Standardized Test Success:**
- **Preparation timeline:** 3-6 months of consistent practice
- **Practice tests:** Take full-length tests under timed conditions
- **Score improvement:** Focus on your weakest areas first
- **Test dates:** Plan for 2-3 attempts with time between

**Extracurricular Impact:**
**Quality over Quantity:**
- Deep involvement in 3-5 activities
- Leadership positions and meaningful contributions
- Long-term commitment showing dedication
- Connection to your intended major or interests

**Community Service:**
- Choose causes you genuinely care about
- Consistent, long-term involvement
- Leadership or initiative in service projects
- Reflection on impact and learning

**Application Strategy:**
**College List Building:**
- **Reach schools (20-30%)** - Dream schools, competitive admission
- **Target schools (40-50%)** - Good fit, reasonable admission chances
- **Safety schools (20-30%)** - Likely admission, still excited to attend

**Essay Excellence:**
- **Show, don't tell** - Use specific examples and stories
- **Authentic voice** - Write in your natural style
- **Unique perspective** - What makes you different?
- **Multiple drafts** - Revise, revise, revise

**Financial Planning:**
- **FAFSA preparation** - Gather tax documents early
- **Scholarship search** - Apply for local and national scholarships
- **Cost comparison** - Consider total cost vs. potential debt
- **Work-study options** - Campus jobs and internships

**Interview Preparation:**
- **Research the school** - Know specific programs and opportunities
- **Practice common questions** - Why this school? Tell me about yourself?
- **Prepare questions** - Show genuine interest and engagement
- **Professional presentation** - Dress appropriately, arrive early

**Transition Planning:**
**Senior Spring:**
- **Course selection** - Plan first-year schedule
- **Housing decisions** - Roommate matching, dorm preferences
- **Orientation preparation** - Summer programs, placement tests
- **Life skills** - Laundry, budgeting, time management

**My College Success Principles:**
1. **Authenticity wins** - Be genuinely yourself in applications
2. **Fit matters most** - Choose schools where you'll thrive
3. **Process over outcome** - Focus on growth, not just admission
4. **Multiple paths to success** - There's no single "right" college
5. **Preparation prevents panic** - Start early, stay organized

**Red Flags to Avoid:**
- Choosing schools based only on rankings
- Overloading on activities without depth
- Procrastinating on applications
- Ignoring financial considerations
- Letting stress overwhelm the experience

**Remember:** College admission is not just about getting in - it's about finding the right place for your growth, learning, and future success. I'm here to help you navigate this journey with confidence and clarity! 🌟

What specific aspect of college preparation would you like to focus on first?"""
        
        else:
            return """🎓 **Academic Success Guidance - My Educational Philosophy:**

**Welcome! As your academic advisor and educator, I'm here to support your learning journey:**

**My Core Educational Beliefs:**
- **Every student can succeed** with the right support and strategies
- **Learning is a skill** that can be developed and improved
- **Growth mindset** - challenges are opportunities, not obstacles
- **Individual approach** - what works for one student may not work for another
- **Holistic development** - academic, social, and emotional growth matter

**The Foundation of Academic Success:**

**1. Learning How to Learn**
- **Study strategies** that match your learning style
- **Time management** skills for balancing multiple demands
- **Critical thinking** to analyze and evaluate information
- **Problem-solving** approaches for academic and life challenges

**2. Building Strong Habits**
- **Consistent daily routines** for studying and self-care
- **Organization systems** for materials, assignments, and deadlines
- **Goal setting** with specific, measurable, achievable targets
- **Self-reflection** to monitor progress and adjust strategies

**3. Academic Skills Development**
- **Reading comprehension** for understanding complex texts
- **Writing proficiency** for clear communication of ideas
- **Mathematical reasoning** for logical problem-solving
- **Research skills** for finding and evaluating information

**4. Social-Emotional Learning**
- **Self-awareness** of strengths, challenges, and emotions
- **Relationship skills** for collaboration and communication
- **Stress management** for handling academic pressure
- **Resilience building** for bouncing back from setbacks

**My Student Support Services:**

**Academic Coaching:**
- Personalized study strategies
- Time management and organization
- Test preparation and anxiety management
- Assignment planning and execution

**Learning Strategies:**
- Note-taking methods
- Memory techniques
- Reading comprehension strategies
- Writing process guidance

**College and Career Guidance:**
- Academic pathway planning
- College preparation and applications
- Career exploration and planning
- Scholarship and financial aid guidance

**Personal Development:**
- Goal setting and achievement
- Confidence building
- Leadership skill development
- Character and values formation

**Common Challenges I Help Students Overcome:**
- **Procrastination and time management**
- **Test anxiety and performance pressure**
- **Difficulty with specific subjects**
- **Lack of motivation or direction**
- **Balancing academics with other commitments**
- **Transition challenges (new school, grade level, etc.)**

**My Teaching Philosophy:**
- **Student-centered approach** - your needs and goals drive our work
- **Strengths-based focus** - build on what you do well
- **Scaffolded learning** - break complex tasks into manageable steps
- **Multiple modalities** - visual, auditory, kinesthetic learning options
- **Real-world connections** - link learning to life applications

**Success Indicators I Track:**
- **Academic performance** - grades, test scores, assignment quality
- **Learning behaviors** - study habits, participation, effort
- **Personal growth** - confidence, independence, resilience
- **Goal achievement** - progress toward short and long-term objectives

**My Commitment to You:**
- **Individualized attention** - strategies tailored to your unique needs
- **Consistent support** - regular check-ins and progress monitoring
- **High expectations** - believing in your potential for excellence
- **Caring environment** - safe space for questions, mistakes, and growth
- **Collaborative partnership** - working together toward your success

**Getting Started:**
1. **Assessment** - Understanding your current situation and goals
2. **Planning** - Creating a personalized success strategy
3. **Implementation** - Putting strategies into practice
4. **Monitoring** - Regular check-ins and adjustments
5. **Celebration** - Recognizing progress and achievements

**Remember:** Education is not just about grades and test scores - it's about developing the knowledge, skills, and character that will serve you throughout your life. Every challenge is an opportunity to grow, and every success builds confidence for future achievements.

**What specific area would you like to focus on first?** I'm here to help you succeed! 🌟

Whether you're struggling with a particular subject, planning for college, or just want to improve your overall academic performance, we'll work together to create a plan that works for you."""
    
    def generate_fallback_contextual_response(self, query: str, context: Dict[str, Any]) -> str:
        """Generate fallback contextual response for education queries."""
        query_lower = query.lower()
        user = context['user_profile']
        academic = context['academic_info']
        learning = context['learning_profile']
        situation = context['current_situation']
        resources = context['resources_and_tools']
        goals = context['goals_and_aspirations']
        
        if any(word in query_lower for word in ['study', 'test', 'exam', 'quiz']):
            upcoming_test = next((d for d in situation['upcoming_deadlines'] if 'test' in d['assignment'].lower()), situation['upcoming_deadlines'][0] if situation['upcoming_deadlines'] else None)
            
            return f"""📚 **Personalized Study Plan for {user['name']}:**

**Your Learning Profile:**
- Learning Style: {learning['learning_style']}
- Strengths: {', '.join(learning['subject_strengths'])}
- Challenges: {', '.join(learning['challenging_subjects'])}

{"**Upcoming Test:** " + upcoming_test['assignment'] + " in " + upcoming_test['subject'] + " (Due: " + upcoming_test['due_date'] + ")" if upcoming_test else "**General Study Strategy:**"}

**Customized Study Approach:**
{f"Since you're a {learning['learning_style'].lower()} learner:" if learning['learning_style'] else ""}
- {"📊 Use diagrams, charts, and visual aids" if learning['learning_style'] == 'Visual' else "🎧 Record lectures and use audio materials" if learning['learning_style'] == 'Auditory' else "✋ Use hands-on practice and movement" if learning['learning_style'] == 'Kinesthetic' else "📝 Take detailed notes and rewrite key concepts"}
- Study in your preferred environment: {learning['study_preferences']['environment']}
- Optimal study time: {learning['study_preferences']['time_of_day']}
- Take breaks {learning['study_preferences']['break_frequency']}

**Available Resources:**
- Technology: {', '.join(resources['technology_access']['devices'])}
- Online tools: {', '.join(resources['study_resources']['online_resources'][:2])}
- Support: {', '.join(resources['study_resources']['support_services'][:2])}

**Action Plan:**
1. Focus extra time on {learning['challenging_subjects'][0]} (your challenging area)
2. Leverage your strength in {learning['subject_strengths'][0]}
3. {"Address current challenge: " + situation['current_challenges'][0] if situation['current_challenges'] else "Use your preferred study methods"}

You've got this! 🌟"""
        
        elif any(word in query_lower for word in ['writing', 'essay', 'paper']):
            writing_assignment = next((d for d in situation['upcoming_deadlines'] if any(w in d['assignment'].lower() for w in ['paper', 'essay', 'report'])), None)
            
            return f"""✍️ **Writing Success Plan for {user['name']}:**

{"**Current Assignment:** " + writing_assignment['assignment'] + " in " + writing_assignment['subject'] + " (Due: " + writing_assignment['due_date'] + ", Status: " + writing_assignment['completion_status'] + ")" if writing_assignment else "**General Writing Improvement:**"}

**Your Academic Context:**
- Grade Level: {academic['grade_level']}
- {"Current GPA: " + str(academic['gpa']) if academic['gpa'] else ""}
- Writing is {"a strength" if "English" in learning['subject_strengths'] else "challenging"} for you

**Personalized Writing Strategy:**
{f"As a {learning['learning_style'].lower()} learner:" if learning['learning_style'] else ""}
- {"Create visual outlines and mind maps" if learning['learning_style'] == 'Visual' else "Read your work aloud and use speech-to-text" if learning['learning_style'] == 'Auditory' else "Write by hand first, then type" if learning['learning_style'] == 'Kinesthetic' else "Focus on detailed note-taking and multiple drafts"}

**Available Tools:**
- Software: {', '.join([s for s in resources['technology_access']['software_access'] if 'Office' in s or 'Google' in s])}
- Support: {resources['study_resources']['support_services'][0] if 'Writing center' in resources['study_resources']['support_services'] else 'Tutoring available'}

**Step-by-Step Plan:**
1. **Planning** (Day 1-2): Research and outline
2. **Drafting** (Day 3-5): Write without editing
3. **Revising** (Day 6-7): Focus on content and structure
4. **Editing** (Day 8): Grammar and style

**Addressing Your Challenge:** {situation['current_challenges'][0] if situation['current_challenges'] else "Stay organized"}
- Set small daily writing goals
- Use your {learning['study_preferences']['time_of_day'].lower()} energy for writing

Ready to tackle that writing project! 📝"""
        
        elif any(word in query_lower for word in ['time', 'management', 'organize']):
            return f"""⏰ **Time Management System for {user['name']}:**

**Your Current Situation:**
- Grade Level: {academic['grade_level']}
- {"Credit Hours: " + str(academic['credit_hours']) if academic['credit_hours'] else ""}
- Main Challenge: {situation['current_challenges'][0] if 'Time management' in situation['current_challenges'] else situation['current_challenges'][0]}

**Upcoming Deadlines:**
{chr(10).join([f"• {d['assignment']} ({d['subject']}) - {d['due_date']} - {d['completion_status']}" for d in situation['upcoming_deadlines'][:3]])}

**Personalized Schedule:**
- **Peak Performance:** {learning['study_preferences']['time_of_day']}
- **Study Environment:** {learning['study_preferences']['environment']}
- **Break Pattern:** {learning['study_preferences']['break_frequency']}

**Technology Tools Available:**
- Devices: {', '.join(resources['technology_access']['devices'])}
- Apps: Calendar, task management, study timers

**Weekly Schedule Template:**
- **Monday-Wednesday:** Focus on {learning['subject_strengths'][0]} (your strength)
- **Thursday-Friday:** Tackle {learning['challenging_subjects'][0]} (needs more time)
- **Weekend:** Review and catch up

**Daily Routine:**
1. **Morning:** Quick review (15 min)
2. **{learning['study_preferences']['time_of_day']}:** Main study block (2-3 hours)
3. **Evening:** Light review and next-day prep

**Goal Alignment:**
- Short-term: {goals['short_term_goals'][0]}
- Long-term: {goals['long_term_goals'][0] if goals['long_term_goals'] else 'Academic success'}

Start with just one new habit this week! 🎯"""
        
        elif any(word in query_lower for word in ['technique', 'method', 'learn']):
            return f"""🧠 **Learning Techniques for {user['name']}:**

**Your Learning Profile:**
- Primary Style: {learning['learning_style']}
- Academic Strengths: {', '.join(learning['subject_strengths'])}
- Areas for Growth: {', '.join(learning['challenging_subjects'])}

**Customized Learning Methods:**

**For {learning['learning_style']} Learners:**
{
"📊 **Visual Techniques:**" + chr(10) +
"- Create colorful mind maps and diagrams" + chr(10) +
"- Use highlighters and color-coding" + chr(10) +
"- Watch educational videos and animations" + chr(10) +
"- Draw concepts and use flowcharts"
if learning['learning_style'] == 'Visual' else

"🎧 **Auditory Techniques:**" + chr(10) +
"- Record and replay lectures" + chr(10) +
"- Study with background music" + chr(10) +
"- Explain concepts out loud" + chr(10) +
"- Join study groups for discussion"
if learning['learning_style'] == 'Auditory' else

"✋ **Kinesthetic Techniques:**" + chr(10) +
"- Use hands-on experiments and models" + chr(10) +
"- Take walking breaks while studying" + chr(10) +
"- Use manipulatives and physical objects" + chr(10) +
"- Practice with real-world applications"
if learning['learning_style'] == 'Kinesthetic' else

"📝 **Reading/Writing Techniques:**" + chr(10) +
"- Take detailed, organized notes" + chr(10) +
"- Rewrite key concepts in your own words" + chr(10) +
"- Create written summaries and outlines" + chr(10) +
"- Use flashcards with written explanations"
}

**Subject-Specific Strategies:**
- **{learning['subject_strengths'][0]}:** Use this as your confidence builder
- **{learning['challenging_subjects'][0]}:** Break into smaller chunks, get extra help

**Available Resources:**
- Online: {', '.join(resources['study_resources']['online_resources'][:2])}
- Support: {', '.join(resources['study_resources']['support_services'][:2])}

**Practice Schedule:**
- Daily: 30 min using your preferred method
- Weekly: Try one new technique
- Monthly: Evaluate what's working best

Your {learning['learning_style'].lower()} approach is your superpower! 🌟"""
        
        elif any(word in query_lower for word in ['college', 'application', 'university']):
            return f"""🎓 **College Prep Plan for {user['name']}:**

**Your Academic Profile:**
- Current Level: {academic['grade_level']}
- {"GPA: " + str(academic['gpa']) + " (Keep it up!)" if academic['gpa'] and academic['gpa'] >= 3.5 else "GPA: " + str(academic['gpa']) + " (Room for improvement)" if academic['gpa'] else ""}
- Strengths: {', '.join(learning['subject_strengths'])}

**Career Interests:** {', '.join(goals['career_interests']) if goals['career_interests'] else 'Still exploring (that\'s okay!)'}

**College Readiness Checklist:**

**Academic Preparation:**
- ✅ Strong performance in {learning['subject_strengths'][0]}
- 🎯 Improve in {learning['challenging_subjects'][0]} (take extra help)
- 📚 Consider AP/Honors courses in your strength areas

**Standardized Tests:**
- {"Plan for SAT/ACT prep" if "12th" in academic['grade_level'] or "College" in academic['grade_level'] else "Start thinking about test prep timeline"}
- Use your {learning['learning_style'].lower()} learning style for test prep

**Extracurriculars & Goals:**
- Current focus: {goals['short_term_goals'][0]}
- Long-term vision: {goals['long_term_goals'][0] if goals['long_term_goals'] else 'Define your path'}

**Application Strategy:**
{"**Senior Year Focus:**" + chr(10) + "- Complete applications by December" + chr(10) + "- Write compelling personal essays" + chr(10) + "- Request recommendation letters" if "12th" in academic['grade_level'] else "**Timeline Planning:**" + chr(10) + "- Build strong academic record" + chr(10) + "- Develop leadership experiences" + chr(10) + "- Research college options"}

**Available Resources:**
- Technology: {', '.join(resources['technology_access']['devices'])}
- Support: School counseling, college prep resources

**Next Steps:**
1. Meet with school counselor monthly
2. Research colleges matching your interests
3. {"Focus on application essays" if "12th" in academic['grade_level'] else "Build your academic foundation"}

Your future is bright! 🌟"""
        
        else:
            return f"""🎓 **Personalized Education Support for {user['name']}:**

**Your Profile:**
- Role: {user['user_type']} at {user['institution']}
- Level: {academic['grade_level']}
- {"Current GPA: " + str(academic['gpa']) if academic['gpa'] else ""}

**Learning Strengths & Challenges:**
- 💪 Strengths: {', '.join(learning['subject_strengths'])}
- 🎯 Growth Areas: {', '.join(learning['challenging_subjects'])}
- 🧠 Learning Style: {learning['learning_style']}

**Current Focus Areas:**
- Main Challenge: {situation['current_challenges'][0]}
- Support Needed: {situation['support_needed']}
- Short-term Goal: {goals['short_term_goals'][0]}

**Immediate Action Plan:**
1. **This Week:** Address {situation['current_challenges'][0]}
2. **This Month:** Work on {goals['short_term_goals'][0]}
3. **This Semester:** Progress toward {goals['long_term_goals'][0] if goals['long_term_goals'] else 'academic excellence'}

**Available Resources:**
- Technology: {', '.join(resources['technology_access']['devices'])}
- Online Tools: {', '.join(resources['study_resources']['online_resources'][:2])}
- Support Services: {', '.join(resources['study_resources']['support_services'][:2])}

**Upcoming Priorities:**
{chr(10).join([f"• {d['assignment']} in {d['subject']} (Due: {d['due_date']})" for d in situation['upcoming_deadlines'][:2]])}

**Encouragement:** You're doing great! Your {learning['learning_style'].lower()} learning style and strength in {learning['subject_strengths'][0]} are valuable assets. Keep building on your successes! 🌟

What specific area would you like to focus on first?"""