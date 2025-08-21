"""
🧠 TASK 6.1: INTELLIGENT CLARIFICATION SYSTEM FOR UNCLEAR MEDICAL INPUTS
==========================================================================

World-class intelligent clarification system that handles any type of unclear, vague,
or ambiguous medical communication from patients. This system goes beyond simple pattern 
matching to understand the intent behind unclear expressions and asks precisely the right 
clarifying questions to gather meaningful medical information.

Enhanced Phase 6 Implementation: Robust Error Handling & Fallbacks
"""

import re
import json
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logger
logger = logging.getLogger(__name__)


class UnclearInputType(Enum):
    """Types of unclear medical inputs"""
    VAGUE_EMOTIONAL = "vague_emotional"           # "not good", "bad", "terrible"
    SINGLE_WORD = "single_word"                   # "pain", "sick", "tired"
    EMOTION_ONLY = "emotion_only"                 # "scared", "worried", "anxious"
    BODY_PART_ONLY = "body_part_only"            # "stomach", "head", "back"
    MINIMAL_DESCRIPTION = "minimal_description"    # "hurts", "aches", "sore"
    NONSPECIFIC_COMPLAINT = "nonspecific_complaint" # "something wrong", "issues"
    INCOMPLETE_SENTENCE = "incomplete_sentence"    # "when I...", "after..."
    MEDICAL_JARGON_UNCLEAR = "medical_jargon_unclear" # unclear medical terms
    TEMPORAL_VAGUE = "temporal_vague"             # "recently", "lately", "sometimes"
    SEVERITY_UNCLEAR = "severity_unclear"         # "really bad", "kind of"
    SYMPTOM_CLUSTER_VAGUE = "symptom_cluster_vague" # "everything hurts"
    QUALITY_UNCLEAR = "quality_unclear"           # "weird feeling", "strange"
    FUNCTIONAL_IMPACT_VAGUE = "functional_impact_vague" # "can't do things"


@dataclass
class ClarificationAnalysisResult:
    """Result of analyzing unclear medical input"""
    input_type: UnclearInputType
    confidence_score: float
    detected_elements: List[str]
    missing_critical_info: List[str]
    clarification_priority: str  # high, medium, low
    suggested_questions: List[str]
    medical_context_clues: Dict[str, Any]
    urgency_indicators: List[str]
    patient_communication_style: str
    processing_time_ms: float


@dataclass
class IntelligentClarificationQuestion:
    """Intelligent clarifying question with context"""
    question_text: str
    question_type: str
    medical_reasoning: str
    priority_level: int  # 1-5, 1 is highest priority
    expected_info_type: str
    follow_up_strategy: str
    empathy_level: str  # high, medium, low


class IntelligentClarificationEngine:
    """
    🔬 REVOLUTIONARY INTELLIGENT CLARIFICATION ENGINE
    
    World-class clarification system that understands the nuanced reasons why 
    medical communication is unclear and generates precisely targeted questions
    to extract meaningful medical information from any type of unclear input.
    """
    
    def __init__(self):
        self.vague_emotional_patterns = self._load_vague_emotional_patterns()
        self.body_part_patterns = self._load_body_part_patterns()
        self.symptom_quality_patterns = self._load_symptom_quality_patterns()
        self.temporal_patterns = self._load_temporal_patterns()
        self.emotional_indicators = self._load_emotional_indicators()
        self.medical_context_extractors = self._load_medical_context_extractors()
        
        # Question generation templates
        self.clarification_templates = self._load_clarification_templates()
        
    def _load_vague_emotional_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for vague emotional expressions"""
        return {
            "general_negative": [
                r"\b(not\s+good|no\s+good|not\s+well|unwell|poorly)\b",
                r"\b(bad|terrible|awful|horrible|miserable)\b",
                r"\b(sick|ill|feeling\s+off|under\s+the\s+weather)\b",
                r"\b(wrong|something\s+wrong|not\s+right|off)\b",
                r"\b(crappy|crap|shit|shitty|lousy)\b",  # informal language
            ],
            "intensity_vague": [
                r"\b(really\s+bad|very\s+bad|so\s+bad|extremely\s+bad)\b",
                r"\b(kind\s+of\s+bad|sort\s+of\s+bad|a\s+bit\s+bad)\b",
                r"\b(pretty\s+bad|quite\s+bad|fairly\s+bad)\b",
            ],
            "comparative_vague": [
                r"\b(worse\s+than\s+usual|not\s+as\s+good|different)\b",
                r"\b(better\s+than\s+before|same\s+as\s+always)\b",
            ],
            "functional_vague": [
                r"\b(can't\s+do\s+anything|everything\s+is\s+hard|struggle)\b",
                r"\b(tired\s+all\s+the\s+time|always\s+exhausted)\b",
                r"\b(nothing\s+works|nothing\s+helps)\b",
            ]
        }
    
    def _load_body_part_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load body part patterns with clarification strategies"""
        return {
            "chest": {
                "keywords": ["chest", "heart", "cardiac"],
                "urgent_questions": [
                    "Are you experiencing chest pain, pressure, or tightness?",
                    "Is there any pain radiating to your arm, jaw, or neck?",
                    "Are you having any difficulty breathing or shortness of breath?"
                ],
                "specific_symptoms": ["pain", "pressure", "tightness", "burning", "stabbing"],
                "urgency_level": "high"
            },
            "head": {
                "keywords": ["head", "headache", "brain", "skull"],
                "urgent_questions": [
                    "Are you experiencing headache pain? If so, where exactly?",
                    "Is this a sudden severe headache or gradual onset?",
                    "Any nausea, vomiting, or vision changes with the headache?"
                ],
                "specific_symptoms": ["headache", "dizziness", "vision changes", "nausea"],
                "urgency_level": "medium"
            },
            "stomach": {
                "keywords": ["stomach", "belly", "tummy", "abdomen", "gut"],
                "urgent_questions": [
                    "Are you experiencing stomach pain, nausea, or digestive issues?",
                    "Where exactly in your abdomen do you feel discomfort?",
                    "Any vomiting, diarrhea, or changes in bowel movements?"
                ],
                "specific_symptoms": ["pain", "nausea", "vomiting", "bloating", "cramping"],
                "urgency_level": "medium"
            },
            "back": {
                "keywords": ["back", "spine", "lumbar", "lower back"],
                "urgent_questions": [
                    "Where exactly in your back are you experiencing discomfort?",
                    "Is the back pain sharp, dull, or burning?",
                    "Does the pain radiate down your leg or to other areas?"
                ],
                "specific_symptoms": ["pain", "stiffness", "spasms", "radiating"],
                "urgency_level": "low"
            },
            "breathing": {
                "keywords": ["breathing", "breath", "lungs", "air"],
                "urgent_questions": [
                    "Are you having difficulty breathing or shortness of breath?",
                    "Is this breathing difficulty sudden or gradual?",
                    "Any chest pain or wheezing with the breathing problems?"
                ],
                "specific_symptoms": ["shortness of breath", "wheezing", "cough"],
                "urgency_level": "high"
            }
        }
    
    def _load_symptom_quality_patterns(self) -> List[str]:
        """Load patterns for unclear symptom quality descriptions"""
        return [
            r"\b(weird|strange|odd|unusual|different)\s+(feeling|sensation)\b",
            r"\b(funny|bizarre|abnormal|peculiar)\b",
            r"\b(can't\s+describe|hard\s+to\s+explain|difficult\s+to\s+say)\b",
            r"\b(like\s+nothing\s+I've\s+felt|never\s+felt\s+this)\b",
            r"\b(uncomfortable|uneasy|disturbing)\b",
        ]
    
    def _load_temporal_patterns(self) -> Dict[str, List[str]]:
        """Load temporal vagueness patterns"""
        return {
            "vague_recent": [
                r"\b(recently|lately|these\s+days|now)\b",
                r"\b(for\s+a\s+while|some\s+time|bit)\b",
            ],
            "vague_frequency": [
                r"\b(sometimes|occasionally|once\s+in\s+a\s+while)\b",
                r"\b(often|frequently|all\s+the\s+time)\b",
            ],
            "vague_duration": [
                r"\b(long\s+time|short\s+time|bit)\b",
                r"\b(forever|ages|eternity)\b",
            ]
        }
    
    def _load_emotional_indicators(self) -> Dict[str, Dict[str, Any]]:
        """Load emotional state indicators with appropriate responses"""
        return {
            "anxiety": {
                "keywords": ["scared", "worried", "anxious", "nervous", "panicked"],
                "response_style": "calm_reassuring",
                "clarification_approach": "gentle_exploration"
            },
            "frustration": {
                "keywords": ["frustrated", "angry", "mad", "annoyed", "irritated"],
                "response_style": "validating_professional",
                "clarification_approach": "systematic_inquiry"
            },
            "depression": {
                "keywords": ["depressed", "sad", "hopeless", "down", "blue"],
                "response_style": "supportive_caring",
                "clarification_approach": "compassionate_exploration"
            },
            "overwhelmed": {
                "keywords": ["overwhelmed", "confused", "lost", "don't know"],
                "response_style": "organizing_helpful",
                "clarification_approach": "step_by_step_guidance"
            }
        }
    
    def _load_medical_context_extractors(self) -> Dict[str, List[str]]:
        """Load patterns to extract medical context from unclear inputs"""
        return {
            "pain_indicators": [
                r"\b(hurts?|ache|aches|aching|sore|painful|tender)\b",
                r"\b(sharp|dull|throbbing|burning|stabbing)\b",
            ],
            "severity_indicators": [
                r"\b(severe|mild|moderate|intense|slight)\b",
                r"\b(little|tiny|huge|massive|unbearable)\b",
            ],
            "temporal_indicators": [
                r"\b(started|began|since|for|during|when)\b",
                r"\b(morning|evening|night|day|week|month)\b",
            ],
            "functional_impact": [
                r"\b(can't|unable|difficult|hard|impossible)\b",
                r"\b(sleep|work|walk|eat|think|concentrate)\b",
            ]
        }
    
    def _load_clarification_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load intelligent clarification question templates"""
        return {
            "vague_emotional": [
                {
                    "template": "I understand you're not feeling well. Could you help me understand what specific symptoms you're experiencing? For example, do you have pain anywhere, nausea, fever, or other discomfort?",
                    "priority": 1,
                    "type": "symptom_exploration",
                    "empathy": "high"
                },
                {
                    "template": "I hear that you're feeling unwell. To better help you, could you describe what exactly is bothering you? Are there specific areas of your body that hurt, or particular symptoms like headache, stomach issues, or breathing problems?",
                    "priority": 2,
                    "type": "body_system_exploration",
                    "empathy": "high"
                },
                {
                    "template": "I understand this is concerning for you. Can you tell me more about what specific changes you've noticed in how you feel? For instance, are you experiencing pain, fatigue, digestive issues, or other specific symptoms?",
                    "priority": 3,
                    "type": "change_exploration",
                    "empathy": "medium"
                }
            ],
            "single_word": [
                {
                    "template": "When you say '{input}', can you help me understand what specific symptoms you're experiencing? For example, where do you feel this, how long has it been happening, and what does it feel like?",
                    "priority": 1,
                    "type": "symptom_specification",
                    "empathy": "medium"
                }
            ],
            "emotion_only": [
                {
                    "template": "I understand you're feeling {emotion}, and that's completely natural when dealing with health concerns. Can you help me understand what specific symptoms or changes you've noticed that are causing you to feel this way?",
                    "priority": 1,
                    "type": "emotion_to_symptom_bridge",
                    "empathy": "high"
                }
            ],
            "body_part_only": [
                {
                    "template": "What specific symptoms are you experiencing with your {body_part}? For example, is it pain, discomfort, changes in function, or something else? Can you describe what you're feeling?",
                    "priority": 1,
                    "type": "organ_system_specification",
                    "empathy": "medium"
                }
            ],
            "quality_unclear": [
                {
                    "template": "You mentioned feeling something '{quality_description}' - I'd like to understand this better. Can you try to describe what this feels like in more specific terms? For example, is it more like pain, pressure, tingling, burning, or something else?",
                    "priority": 1,
                    "type": "quality_specification",
                    "empathy": "medium"
                }
            ]
        }
    
    async def analyze_unclear_input(self, patient_input: str, medical_context: Dict[str, Any] = None) -> ClarificationAnalysisResult:
        """
        Analyze unclear patient input and determine the best clarification approach
        """
        start_time = time.time()
        
        # Normalize input for analysis
        normalized_input = patient_input.lower().strip()
        words = normalized_input.split()
        
        # Detect type of unclear input
        input_type, confidence = self._detect_unclear_input_type(normalized_input, words)
        
        # Extract available medical elements
        detected_elements = self._extract_available_elements(normalized_input)
        
        # Identify missing critical information
        missing_info = self._identify_missing_critical_info(input_type, detected_elements)
        
        # Determine clarification priority
        priority = self._determine_clarification_priority(input_type, detected_elements, medical_context)
        
        # Generate suggested questions
        suggested_questions = await self._generate_intelligent_questions(
            input_type, patient_input, detected_elements, missing_info, medical_context
        )
        
        # Extract medical context clues
        context_clues = self._extract_medical_context_clues(normalized_input)
        
        # Detect urgency indicators
        urgency_indicators = self._detect_urgency_indicators(normalized_input, context_clues)
        
        # Assess patient communication style
        communication_style = self._assess_communication_style(normalized_input, words)
        
        processing_time = (time.time() - start_time) * 1000
        
        return ClarificationAnalysisResult(
            input_type=input_type,
            confidence_score=confidence,
            detected_elements=detected_elements,
            missing_critical_info=missing_info,
            clarification_priority=priority,
            suggested_questions=suggested_questions,
            medical_context_clues=context_clues,
            urgency_indicators=urgency_indicators,
            patient_communication_style=communication_style,
            processing_time_ms=processing_time
        )
    
    def _detect_unclear_input_type(self, normalized_input: str, words: List[str]) -> Tuple[UnclearInputType, float]:
        """Detect the specific type of unclear input"""
        
        # Single word inputs
        if len(words) == 1:
            word = words[0]
            
            # Check if it's an emotion
            for emotion_type, emotion_data in self.emotional_indicators.items():
                if word in emotion_data["keywords"]:
                    return UnclearInputType.EMOTION_ONLY, 0.95
            
            # Check if it's a body part
            for body_part, body_data in self.body_part_patterns.items():
                if word in body_data["keywords"]:
                    return UnclearInputType.BODY_PART_ONLY, 0.90
            
            # Check if it's a minimal symptom description
            if word in ["pain", "hurt", "ache", "sick", "tired", "sore", "weak"]:
                return UnclearInputType.MINIMAL_DESCRIPTION, 0.85
            
            return UnclearInputType.SINGLE_WORD, 0.80
        
        # Check for vague emotional expressions
        for category, patterns in self.vague_emotional_patterns.items():
            for pattern in patterns:
                if re.search(pattern, normalized_input, re.IGNORECASE):
                    return UnclearInputType.VAGUE_EMOTIONAL, 0.90
        
        # Check for symptom quality unclear
        for pattern in self.symptom_quality_patterns:
            if re.search(pattern, normalized_input, re.IGNORECASE):
                return UnclearInputType.QUALITY_UNCLEAR, 0.85
        
        # Check for temporal vagueness
        for category, patterns in self.temporal_patterns.items():
            for pattern in patterns:
                if re.search(pattern, normalized_input, re.IGNORECASE):
                    return UnclearInputType.TEMPORAL_VAGUE, 0.75
        
        # Check for incomplete sentences
        if normalized_input.endswith('...') or len(words) <= 3 and any(word in normalized_input for word in ['when', 'after', 'before', 'during']):
            return UnclearInputType.INCOMPLETE_SENTENCE, 0.80
        
        # Check for nonspecific complaints
        if any(phrase in normalized_input for phrase in ['something wrong', 'issues', 'problems', 'concerns']):
            return UnclearInputType.NONSPECIFIC_COMPLAINT, 0.75
        
        # Check for functional impact vagueness
        if any(phrase in normalized_input for phrase in ["can't do", "everything", "nothing works"]):
            return UnclearInputType.FUNCTIONAL_IMPACT_VAGUE, 0.70
        
        # Default to vague emotional if short and no specific pattern
        if len(words) <= 4:
            return UnclearInputType.VAGUE_EMOTIONAL, 0.60
        
        return UnclearInputType.MINIMAL_DESCRIPTION, 0.50
    
    def _extract_available_elements(self, normalized_input: str) -> List[str]:
        """Extract any available medical elements from unclear input"""
        elements = []
        
        # Extract pain indicators
        for pattern in self.medical_context_extractors["pain_indicators"]:
            matches = re.findall(pattern, normalized_input, re.IGNORECASE)
            elements.extend([f"pain_indicator: {match}" for match in matches])
        
        # Extract severity indicators
        for pattern in self.medical_context_extractors["severity_indicators"]:
            matches = re.findall(pattern, normalized_input, re.IGNORECASE)
            elements.extend([f"severity: {match}" for match in matches])
        
        # Extract temporal indicators
        for pattern in self.medical_context_extractors["temporal_indicators"]:
            matches = re.findall(pattern, normalized_input, re.IGNORECASE)
            elements.extend([f"temporal: {match}" for match in matches])
        
        # Extract functional impact
        for pattern in self.medical_context_extractors["functional_impact"]:
            matches = re.findall(pattern, normalized_input, re.IGNORECASE)
            elements.extend([f"functional_impact: {match}" for match in matches])
        
        return elements
    
    def _identify_missing_critical_info(self, input_type: UnclearInputType, detected_elements: List[str]) -> List[str]:
        """Identify what critical medical information is missing"""
        missing_info = []
        
        # Always need symptom specification if unclear
        if not any("pain_indicator" in element for element in detected_elements):
            missing_info.append("specific_symptoms")
        
        # Location is critical for most symptoms
        if input_type not in [UnclearInputType.BODY_PART_ONLY]:
            missing_info.append("anatomical_location")
        
        # Onset and duration are important
        if not any("temporal" in element for element in detected_elements):
            missing_info.extend(["onset_timing", "duration"])
        
        # Quality and severity
        if not any("severity" in element for element in detected_elements):
            missing_info.append("severity_assessment")
        
        # For emotional inputs, need to bridge to physical symptoms
        if input_type == UnclearInputType.EMOTION_ONLY:
            missing_info.extend(["physical_symptoms", "symptom_trigger"])
        
        # For functional impact, need specific limitations
        if input_type == UnclearInputType.FUNCTIONAL_IMPACT_VAGUE:
            missing_info.extend(["specific_limitations", "activity_impact"])
        
        return missing_info
    
    def _determine_clarification_priority(self, input_type: UnclearInputType, detected_elements: List[str], medical_context: Dict[str, Any] = None) -> str:
        """Determine the priority level for clarification"""
        
        # High priority for potential emergencies
        high_priority_types = [
            UnclearInputType.VAGUE_EMOTIONAL,
            UnclearInputType.EMOTION_ONLY
        ]
        
        # Check for urgent body parts
        urgent_indicators = ["chest", "heart", "breathing", "severe"]
        if any(indicator in str(detected_elements).lower() for indicator in urgent_indicators):
            return "high"
        
        if input_type in high_priority_types:
            return "high"
        
        # Medium priority for symptom-related unclear inputs
        medium_priority_types = [
            UnclearInputType.BODY_PART_ONLY,
            UnclearInputType.MINIMAL_DESCRIPTION,
            UnclearInputType.QUALITY_UNCLEAR,
            UnclearInputType.NONSPECIFIC_COMPLAINT
        ]
        
        if input_type in medium_priority_types:
            return "medium"
        
        return "low"
    
    async def _generate_intelligent_questions(self, input_type: UnclearInputType, original_input: str, 
                                           detected_elements: List[str], missing_info: List[str], 
                                           medical_context: Dict[str, Any] = None) -> List[str]:
        """Generate intelligent clarifying questions based on input analysis"""
        
        questions = []
        
        if input_type == UnclearInputType.VAGUE_EMOTIONAL:
            # Use sophisticated templates for vague emotional expressions
            template = self.clarification_templates["vague_emotional"][0]
            questions.append(template["template"])
            
        elif input_type == UnclearInputType.EMOTION_ONLY:
            # Extract the emotion and create personalized question
            emotion = self._extract_primary_emotion(original_input.lower())
            template = self.clarification_templates["emotion_only"][0]["template"]
            questions.append(template.format(emotion=emotion))
            
        elif input_type == UnclearInputType.BODY_PART_ONLY:
            # Extract body part and use specific clarification
            body_part = self._extract_body_part(original_input.lower())
            if body_part and body_part in self.body_part_patterns:
                questions.extend(self.body_part_patterns[body_part]["urgent_questions"])
            else:
                template = self.clarification_templates["body_part_only"][0]["template"]
                questions.append(template.format(body_part=body_part or original_input))
                
        elif input_type == UnclearInputType.SINGLE_WORD:
            template = self.clarification_templates["single_word"][0]["template"]
            questions.append(template.format(input=original_input))
            
        elif input_type == UnclearInputType.QUALITY_UNCLEAR:
            template = self.clarification_templates["quality_unclear"][0]["template"]
            quality_desc = self._extract_quality_description(original_input)
            questions.append(template.format(quality_description=quality_desc))
            
        elif input_type == UnclearInputType.MINIMAL_DESCRIPTION:
            questions.append(
                f"You mentioned '{original_input}' - can you help me understand this better? "
                f"Where exactly do you feel this, what does it feel like, and when did it start?"
            )
            
        elif input_type == UnclearInputType.NONSPECIFIC_COMPLAINT:
            questions.append(
                f"I understand you have some health concerns. Can you describe any specific symptoms "
                f"you're experiencing? For example, do you have pain, discomfort, changes in how you feel, "
                f"or specific areas of your body that are bothering you?"
            )
            
        elif input_type == UnclearInputType.INCOMPLETE_SENTENCE:
            questions.append(
                f"It looks like you were starting to tell me something about '{original_input}' - "
                f"can you complete that thought? I'd like to understand what you were going to say "
                f"about your symptoms or health concerns."
            )
            
        elif input_type == UnclearInputType.TEMPORAL_VAGUE:
            questions.append(
                f"You mentioned something happening '{original_input}' - can you be more specific "
                f"about the timing? For example, how many days, weeks, or months ago did this start? "
                f"And what specific symptoms or changes did you notice?"
            )
            
        elif input_type == UnclearInputType.FUNCTIONAL_IMPACT_VAGUE:
            questions.append(
                f"I understand that this is affecting your daily activities. Can you tell me what "
                f"specific symptoms are making it difficult for you to function? For example, is it "
                f"pain, fatigue, dizziness, or other specific problems?"
            )
            
        else:
            # Fallback comprehensive question
            questions.append(
                f"I want to make sure I understand your concerns clearly. Can you help me by describing "
                f"any specific symptoms you're experiencing, where you feel them, and when they started? "
                f"This will help me provide you with the best possible guidance."
            )
        
        # Add follow-up questions based on missing information
        if "severity_assessment" in missing_info:
            questions.append("How would you rate the severity of these symptoms on a scale of 1-10?")
        
        if "onset_timing" in missing_info and input_type != UnclearInputType.TEMPORAL_VAGUE:
            questions.append("When exactly did you first notice these symptoms - was it sudden or gradual?")
        
        return questions[:3]  # Return top 3 most relevant questions
    
    def _extract_primary_emotion(self, input_text: str) -> str:
        """Extract the primary emotion from emotional input"""
        for emotion_type, emotion_data in self.emotional_indicators.items():
            for keyword in emotion_data["keywords"]:
                if keyword in input_text:
                    return keyword
        return "concerned"
    
    def _extract_body_part(self, input_text: str) -> Optional[str]:
        """Extract body part from input"""
        for body_part, body_data in self.body_part_patterns.items():
            for keyword in body_data["keywords"]:
                if keyword in input_text:
                    return body_part
        return None
    
    def _extract_quality_description(self, input_text: str) -> str:
        """Extract quality description from unclear input"""
        quality_words = ["weird", "strange", "odd", "unusual", "different", "funny", "bizarre"]
        for word in quality_words:
            if word in input_text.lower():
                return word
        return "unusual"
    
    def _extract_medical_context_clues(self, normalized_input: str) -> Dict[str, Any]:
        """Extract any available medical context clues"""
        context_clues = {
            "pain_present": False,
            "severity_mentioned": False,
            "temporal_info": [],
            "body_systems": [],
            "functional_impact": False
        }
        
        # Check for pain presence
        pain_patterns = [r"\b(hurt|pain|ache|sore|tender)\b"]
        for pattern in pain_patterns:
            if re.search(pattern, normalized_input, re.IGNORECASE):
                context_clues["pain_present"] = True
                break
        
        # Check for severity indicators
        severity_patterns = [r"\b(severe|mild|terrible|awful|intense|slight)\b"]
        for pattern in severity_patterns:
            if re.search(pattern, normalized_input, re.IGNORECASE):
                context_clues["severity_mentioned"] = True
                break
        
        # Extract body systems mentioned
        for body_part in self.body_part_patterns.keys():
            if body_part in normalized_input:
                context_clues["body_systems"].append(body_part)
        
        # Check for functional impact
        functional_patterns = [r"\b(can't|unable|difficult|hard|impossible)\b"]
        for pattern in functional_patterns:
            if re.search(pattern, normalized_input, re.IGNORECASE):
                context_clues["functional_impact"] = True
                break
        
        return context_clues
    
    def _detect_urgency_indicators(self, normalized_input: str, context_clues: Dict[str, Any]) -> List[str]:
        """Detect potential urgency indicators in unclear input"""
        urgency_indicators = []
        
        # High urgency words
        high_urgency_patterns = [
            r"\b(emergency|urgent|severe|terrible|unbearable|can't breathe)\b",
            r"\b(chest|heart|breathing)\b",
            r"\b(sudden|suddenly|all of a sudden)\b"
        ]
        
        for pattern in high_urgency_patterns:
            matches = re.findall(pattern, normalized_input, re.IGNORECASE)
            urgency_indicators.extend(matches)
        
        # Check context clues for urgency
        if "chest" in context_clues.get("body_systems", []):
            urgency_indicators.append("chest_related")
        
        if context_clues.get("severity_mentioned"):
            urgency_indicators.append("severity_mentioned")
        
        return urgency_indicators
    
    def _assess_communication_style(self, normalized_input: str, words: List[str]) -> str:
        """Assess patient's communication style"""
        
        # Very brief/minimal
        if len(words) <= 2:
            return "minimal_communicator"
        
        # Emotional/expressive
        emotional_words = ["scared", "worried", "terrible", "awful", "horrible"]
        if any(word in normalized_input for word in emotional_words):
            return "emotional_expressive"
        
        # Vague/uncertain
        uncertain_words = ["maybe", "kind of", "sort of", "i think", "not sure"]
        if any(phrase in normalized_input for phrase in uncertain_words):
            return "uncertain_vague"
        
        # Direct/factual
        if len(words) > 5 and not any(word in normalized_input for word in emotional_words + uncertain_words):
            return "direct_factual"
        
        return "balanced_communicator"


# Global instance
intelligent_clarification_engine = IntelligentClarificationEngine()


async def analyze_and_clarify_unclear_input(patient_input: str, medical_context: Dict[str, Any] = None) -> ClarificationAnalysisResult:
    """
    Main function to analyze unclear patient input and generate intelligent clarification
    """
    return await intelligent_clarification_engine.analyze_unclear_input(patient_input, medical_context)


async def generate_clarification_response(clarification_result: ClarificationAnalysisResult, 
                                        patient_input: str) -> str:
    """
    Generate the final clarification response based on analysis
    """
    if not clarification_result.suggested_questions:
        return ("I want to make sure I understand your health concerns properly. "
                "Can you help me by describing any specific symptoms you're experiencing?")
    
    # Use the most appropriate question based on priority
    primary_question = clarification_result.suggested_questions[0]
    
    # Add empathetic context based on communication style
    if clarification_result.patient_communication_style == "emotional_expressive":
        empathy_prefix = "I understand this is concerning for you. "
    elif clarification_result.patient_communication_style == "minimal_communicator":
        empathy_prefix = "I'd like to help you with your health concerns. "
    elif clarification_result.patient_communication_style == "uncertain_vague":
        empathy_prefix = "It's completely normal to feel unsure about describing symptoms. "
    else:
        empathy_prefix = "Thank you for reaching out about your health. "
    
    # Check for urgency indicators
    if clarification_result.urgency_indicators:
        if any(indicator in ["chest_related", "breathing", "emergency"] for indicator in clarification_result.urgency_indicators):
            urgency_note = " If you're experiencing chest pain, difficulty breathing, or any emergency symptoms, please seek immediate medical attention. "
            return empathy_prefix + urgency_note + primary_question
    
    return empathy_prefix + primary_question