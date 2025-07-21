"""
Healthcare Assistant Demo Module

Implements the healthcare industry demonstration using the BaseDemo framework.
"""
from typing import Dict, List, Any
import random
from faker import Faker
from .base_demo import BaseDemo

fake = Faker()


class HealthcareDemo(BaseDemo):
    """Healthcare assistant demonstration."""
    
    def __init__(self, ai_service=None, context_service=None):
        from services.prompt_service import Industry
        super().__init__("Healthcare", Industry.HEALTHCARE, ai_service, context_service)
    
    def generate_context(self) -> Dict[str, Any]:
        """Generate realistic patient context using Faker."""
        return {
            "age": random.randint(25, 65),
            "gender": random.choice(["Male", "Female"]),
            "medical_history": random.sample([
                "Hypertension", "Diabetes Type 2", "Seasonal allergies", "Asthma", 
                "High cholesterol", "Anxiety", "Migraines"
            ], 2),
            "current_medications": random.sample([
                "Lisinopril 10mg", "Metformin 500mg", "Claritin", "Albuterol inhaler",
                "Atorvastatin 20mg", "Sertraline 50mg", "Sumatriptan"
            ], 2),
            "allergies": random.sample(["Penicillin", "Shellfish", "Peanuts", "Latex", "Sulfa drugs"], 2),
            "recent_symptoms": random.sample([
                "Fatigue (3 days)", "Mild fever", "Headaches", "Joint pain", 
                "Sleep issues", "Dizziness", "Nausea"
            ], 2),
            "vital_signs": {
                "BP": f"{random.randint(110, 150)}/{random.randint(70, 95)}",
                "HR": f"{random.randint(65, 85)}",
                "Temp": f"{random.uniform(98.0, 100.5):.1f}°F",
                "Weight": f"{random.randint(120, 200)} lbs"
            },
            "last_visit": fake.date_between(start_date='-6m', end_date='today').strftime('%Y-%m-%d')
        }
    
    def generate_smart_context(self, query: str) -> Dict[str, Any]:
        """Generate context that intelligently enhances the user's query."""
        
        # Base realistic patient profile
        base_context = {
            "patient_profile": {
                "name": fake.name(),
                "age": random.randint(25, 65),
                "gender": random.choice(["Male", "Female"]),
                "last_visit": fake.date_between(start_date='-6m', end_date='-1m').strftime('%Y-%m-%d')
            }
        }
        
        # Query-aware enhancements
        query_lower = query.lower()
        
        # Headache/Pain intelligence
        if any(word in query_lower for word in ['headache', 'head', 'migraine']):
            base_context.update({
                "medical_history": ["Migraines", "Hypertension"],
                "current_medications": ["Sumatriptan 50mg", "Lisinopril 10mg"],
                "allergies": random.sample(["Aspirin", "Penicillin"], 1),
                "recent_symptoms": ["Headaches (recurring)", "Light sensitivity", "Mild nausea"],
                "vital_signs": {
                    "BP": f"{random.randint(140, 160)}/{random.randint(85, 95)}",  # Elevated
                    "HR": f"{random.randint(70, 85)}",
                    "Temp": f"{random.uniform(98.0, 99.2):.1f}°F",
                    "Weight": f"{random.randint(140, 180)} lbs"
                },
                "triggers": ["Stress", "Lack of sleep", "Certain foods"]
            })
        
        # Sleep issues intelligence
        elif any(word in query_lower for word in ['sleep', 'insomnia', 'tired', 'fatigue']):
            base_context.update({
                "medical_history": ["Anxiety", "Sleep apnea"],
                "current_medications": ["Sertraline 50mg", "CPAP therapy"],
                "allergies": random.sample(["Latex", "Sulfa drugs"], 1),
                "recent_symptoms": ["Sleep issues (2 weeks)", "Daytime fatigue", "Difficulty concentrating"],
                "vital_signs": {
                    "BP": f"{random.randint(120, 140)}/{random.randint(75, 85)}",
                    "HR": f"{random.randint(65, 80)}",
                    "Temp": f"{random.uniform(98.0, 98.8):.1f}°F",
                    "Weight": f"{random.randint(150, 200)} lbs"
                },
                "sleep_patterns": {
                    "bedtime": "11:30 PM",
                    "wake_time": "6:30 AM",
                    "sleep_quality": "Poor (frequent waking)"
                }
            })
        
        # Pain/Back issues intelligence
        elif any(word in query_lower for word in ['pain', 'back', 'hurt', 'ache', 'sore']):
            base_context.update({
                "medical_history": ["Chronic back pain", "Arthritis"],
                "current_medications": ["Ibuprofen 400mg", "Physical therapy"],
                "allergies": random.sample(["Codeine", "Shellfish"], 1),
                "recent_symptoms": ["Lower back pain (1 week)", "Stiffness in morning", "Limited mobility"],
                "vital_signs": {
                    "BP": f"{random.randint(125, 145)}/{random.randint(75, 90)}",
                    "HR": f"{random.randint(70, 85)}",
                    "Temp": f"{random.uniform(98.0, 99.0):.1f}°F",
                    "Weight": f"{random.randint(160, 220)} lbs"
                },
                "pain_level": f"{random.randint(4, 7)}/10",
                "activity_level": "Reduced due to pain"
            })
        
        # Fever/Cold symptoms intelligence
        elif any(word in query_lower for word in ['fever', 'cold', 'flu', 'sick', 'cough']):
            base_context.update({
                "medical_history": ["Seasonal allergies", "Asthma"],
                "current_medications": ["Claritin", "Albuterol inhaler"],
                "allergies": random.sample(["Penicillin", "Peanuts"], 1),
                "recent_symptoms": ["Fever (2 days)", "Cough", "Congestion", "Body aches"],
                "vital_signs": {
                    "BP": f"{random.randint(110, 130)}/{random.randint(70, 85)}",
                    "HR": f"{random.randint(80, 95)}",  # Elevated due to fever
                    "Temp": f"{random.uniform(100.2, 102.5):.1f}°F",  # Fever
                    "Weight": f"{random.randint(130, 180)} lbs"
                },
                "symptom_onset": "3 days ago",
                "exposure_history": "Coworker had similar symptoms last week"
            })
        
        # Medication/Drug questions intelligence
        elif any(word in query_lower for word in ['medication', 'drug', 'pill', 'prescription']):
            base_context.update({
                "medical_history": ["Diabetes Type 2", "High cholesterol"],
                "current_medications": ["Metformin 500mg", "Atorvastatin 20mg", "Multivitamin"],
                "allergies": random.sample(["Sulfa drugs", "Latex"], 1),
                "recent_symptoms": ["Mild stomach upset", "Occasional dizziness"],
                "vital_signs": {
                    "BP": f"{random.randint(130, 150)}/{random.randint(80, 90)}",
                    "HR": f"{random.randint(65, 80)}",
                    "Temp": f"{random.uniform(98.0, 98.6):.1f}°F",
                    "Weight": f"{random.randint(170, 220)} lbs"
                },
                "medication_adherence": "Good - takes medications as prescribed",
                "last_lab_work": fake.date_between(start_date='-3m', end_date='-1m').strftime('%Y-%m-%d')
            })
        
        # Default health context
        else:
            base_context.update({
                "medical_history": random.sample(["Hypertension", "Seasonal allergies"], 1),
                "current_medications": random.sample(["Lisinopril 10mg", "Claritin"], 1),
                "allergies": random.sample(["Penicillin", "Shellfish"], 1),
                "recent_symptoms": random.sample(["Mild fatigue", "Occasional headaches"], 1),
                "vital_signs": {
                    "BP": f"{random.randint(120, 140)}/{random.randint(75, 85)}",
                    "HR": f"{random.randint(65, 80)}",
                    "Temp": f"{random.uniform(98.0, 98.8):.1f}°F",
                    "Weight": f"{random.randint(140, 190)} lbs"
                }
            })
        
        return base_context
    
    def get_sample_queries(self) -> List[str]:
        """Get sample healthcare queries."""
        return [
            "I have a headache",
            "My back hurts",
            "I feel dizzy",
            "Should I take medication?",
            "When should I see a doctor?"
        ]
    
    def get_query_placeholder(self) -> str:
        """Get placeholder text for healthcare queries."""
        return "e.g., I have a headache, My back hurts, I feel dizzy"
    
    def get_system_message_generic(self) -> str:
        """Get system message for generic healthcare responses."""
        return "You are a general health information assistant. Provide general health advice without using specific personal medical context. Always recommend consulting healthcare providers for specific concerns."
    
    def get_system_message_contextual(self) -> str:
        """Get system message for contextual healthcare responses."""
        return """You are a personalized healthcare assistant. Use the provided patient context to give specific, relevant health guidance. Consider:
- Current medications and potential interactions
- Known allergies and medical history
- Recent symptoms and vital signs
- Age and gender-specific considerations

Always emphasize consulting healthcare providers for serious concerns. Be helpful but responsible."""
    
    def generate_fallback_generic_response(self, query: str) -> str:
        """Generate fallback generic response for healthcare queries."""
        query_lower = query.lower()
        
        if 'headache' in query_lower:
            return """🩺 **Headache Relief Guidance:**

**Immediate steps I recommend:**
- **Hydration first** - Drink 16-20 oz of water slowly
- **Rest in a quiet, dark room** - Light sensitivity is common
- **Apply gentle pressure** - Cold compress on forehead or warm on neck
- **Over-the-counter relief** - Acetaminophen or ibuprofen as directed

**When to be concerned:**
- Sudden, severe headache unlike any before
- Headache with fever, stiff neck, or vision changes
- Persistent headache lasting more than 2-3 days
- Headache after head injury

**Prevention tips:**
- Stay consistently hydrated
- Maintain regular sleep schedule
- Manage stress levels
- Identify and avoid triggers

⚠️ **Please consult your healthcare provider if headaches are frequent, severe, or accompanied by other concerning symptoms. This guidance doesn't replace professional medical evaluation.**"""
        
        elif any(word in query_lower for word in ['pain', 'hurt', 'ache']):
            return """🩺 **Pain Management Guidance:**

**Initial approach I recommend:**
- **R.I.C.E. method** - Rest, Ice, Compression, Elevation (for injuries)
- **Heat therapy** - For muscle tension and chronic pain (15-20 minutes)
- **Gentle movement** - Light stretching unless contraindicated
- **Over-the-counter options** - Acetaminophen or NSAIDs as appropriate

**Pain assessment questions to consider:**
- Scale of 1-10, how severe is your pain?
- Is it sharp, dull, throbbing, or burning?
- Does it radiate to other areas?
- What makes it better or worse?

**Red flags requiring immediate medical attention:**
- Severe pain (8-10/10) that's sudden onset
- Pain with numbness, tingling, or weakness
- Pain after trauma or injury
- Pain with fever, nausea, or other systemic symptoms

**Chronic pain considerations:**
- Keep a pain diary to identify patterns
- Consider physical therapy evaluation
- Discuss with your healthcare provider about comprehensive pain management

⚠️ **Important:** Persistent or severe pain requires professional medical evaluation. Don't delay seeking care for concerning symptoms."""
        
        elif any(word in query_lower for word in ['fever', 'temperature', 'hot']):
            return """🌡️ **Fever Management Guidance:**

**Immediate care recommendations:**
- **Monitor temperature** - Check every 2-4 hours
- **Stay hydrated** - Water, clear broths, electrolyte solutions
- **Rest is essential** - Your body needs energy to fight infection
- **Dress lightly** - Allow heat to escape, avoid bundling up
- **Fever reducers** - Acetaminophen or ibuprofen per package directions

**Fever facts:**
- Normal body temperature: 97-99°F (36-37.2°C)
- Low-grade fever: 100.4-102°F (38-38.9°C)
- High fever: Above 103°F (39.4°C)

**Seek immediate medical care if:**
- Temperature above 103°F (39.4°C)
- Fever with severe headache, stiff neck, or rash
- Difficulty breathing or chest pain
- Persistent vomiting or signs of dehydration
- Fever lasting more than 3 days
- Any fever in infants under 3 months

**Comfort measures:**
- Cool, damp washcloth on forehead
- Lukewarm bath or shower
- Light, breathable clothing
- Quiet, comfortable environment

⚠️ **Remember:** Fever is often your body's natural response to infection. However, high fevers or concerning symptoms require prompt medical evaluation.**"""
        
        else:
            return """🩺 **General Health & Wellness Guidance:**

**Foundation of good health:**
- **Nutrition** - Balanced diet with fruits, vegetables, lean proteins, whole grains
- **Physical activity** - 150 minutes moderate exercise weekly, or 75 minutes vigorous
- **Sleep hygiene** - 7-9 hours nightly, consistent sleep schedule
- **Hydration** - 8-10 glasses of water daily, more if active
- **Stress management** - Regular relaxation, mindfulness, social connections

**Preventive care essentials:**
- Annual physical exams and age-appropriate screenings
- Stay current with vaccinations
- Regular dental and vision care
- Know your family health history
- Monitor blood pressure, cholesterol, blood sugar

**When to seek medical care:**
- New or concerning symptoms
- Changes in existing conditions
- Preventive care and screenings
- Medication management
- Health questions or concerns

**Mental health matters:**
- Recognize signs of depression, anxiety
- Seek support when needed
- Maintain social connections
- Practice stress-reduction techniques

**Emergency warning signs:**
- Chest pain or difficulty breathing
- Severe abdominal pain
- Sudden weakness or numbness
- High fever with concerning symptoms
- Severe headache or vision changes

⚠️ **Important reminder:** This general guidance supports your health awareness but doesn't replace regular medical care. Always consult your healthcare provider for personalized medical advice, diagnosis, or treatment decisions.**"""
    
    def generate_fallback_contextual_response(self, query: str, context: Dict[str, Any]) -> str:
        """Generate fallback contextual response for healthcare queries."""
        query_lower = query.lower()
        age = context['age']
        medications = context['current_medications']
        allergies = context['allergies']
        recent_symptoms = context['recent_symptoms']
        vitals = context['vital_signs']
        
        if 'headache' in query_lower:
            return f"""🚨 **Important Considerations for Age {age}:**

Given your recent symptoms ({', '.join(recent_symptoms)}) and current BP reading ({vitals['BP']}), this headache could be related to:

1. **Hypertension-related** - Your BP is elevated
2. **Viral infection** - Combined with fever/fatigue

⚠️ **Medication Alert:** 
- Avoid aspirin (may interact with {medications[0]})
- Safe option: Acetaminophen (Tylenol)
- ❌ NO Penicillin-based medications (allergy alert)

🎯 **Recommended Actions:**
1. Monitor BP closely
2. Take Tylenol for pain (safe with your meds)
3. **Contact your doctor today** - combination of symptoms warrants evaluation

This is not routine - please seek medical attention."""
        
        elif any(word in query_lower for word in ['pain', 'hurt', 'ache']):
            return f"""🎯 **Personalized Pain Management:**

**Safe for your profile:**
- Acetaminophen (Tylenol) - safe with {medications[0]}
- Ice/heat therapy
- Gentle movement as tolerated

⚠️ **Avoid:**
- Aspirin (interacts with {medications[0]})
- Any medications containing {allergies[0]}

**Monitor for:** Changes in {recent_symptoms[0]} or {recent_symptoms[1]}

Given your recent symptoms, contact your healthcare provider if pain worsens."""
        
        else:
            return f"""🎯 **Personalized Health Guidance:**

**Your Current Status:**
- Age {age}, taking {', '.join(medications)}
- Recent concerns: {', '.join(recent_symptoms)}
- Vital signs: BP {vitals['BP']}, Temp {vitals['Temp']}

**Key Considerations:**
- Monitor blood pressure (currently elevated)
- Stay hydrated (especially with recent fever)
- Avoid {', '.join(allergies)} allergens

**Recommended:** Follow up with your doctor given recent symptom pattern."""