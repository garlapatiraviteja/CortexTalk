import streamlit as st
import speech_recognition as sr
import random
import numpy as np
import io
import threading
from datetime import datetime
import time
import json
import pyttsx3
import base64
import streamlit.components.v1 as components
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="AI Language Tutor",
    page_icon="🗣",
    layout="wide",
    initial_sidebar_state="expanded"
)
CONTACT_INFO = {
    "email": "abdul99.rc@gmail.com",
    "Phone": "+447776619604",
    "instagram": "@AILanguageTutorOfficial"
}

SUBSCRIPTION_PLANS = {
    "Free": {
        "features": ["Basic levels", "5 questions/day", "No audio feedback"],
        "price": "$0/month"
    },
    "Premium": {
        "features": ["All levels", "Unlimited questions", "Audio feedback", "Progress tracking", "Offline mode"],
        "price": "$9.99/month"
    }
}

# Enhanced sample prompts data with complete structure for all languages
sample_prompts = {
    'es': {
        'level_1': [
            {'type': 'vocabulary', 'word': 'hello', 'context': 'A greeting when you meet someone', 'translation': 'hola', 'audio_text': 'OH-lah'},
            {'type': 'vocabulary', 'word': 'goodbye', 'context': 'A farewell when you leave', 'translation': 'adiós', 'audio_text': 'ah-DYOHS'},
            {'type': 'vocabulary', 'word': 'thank you', 'context': 'Expression of gratitude', 'translation': 'gracias', 'audio_text': 'GRAH-see-ahs'},
            {'type': 'vocabulary', 'word': 'water', 'context': 'A clear liquid we drink', 'translation': 'agua', 'audio_text': 'AH-gwah'},
            {'type': 'vocabulary', 'word': 'food', 'context': 'What we eat to survive', 'translation': 'comida', 'audio_text': 'koh-MEE-dah'},
            {'type': 'vocabulary', 'word': 'house', 'context': 'A place where people live', 'translation': 'casa', 'audio_text': 'KAH-sah'},
            {'type': 'vocabulary', 'word': 'friend', 'context': 'Someone you like and trust', 'translation': 'amigo', 'audio_text': 'ah-MEE-goh'},
            {'type': 'vocabulary', 'word': 'family', 'context': 'Your relatives', 'translation': 'familia', 'audio_text': 'fah-MEE-lee-ah'},
            {'type': 'fill_blank', 'sentence': 'Hola, ¿cómo _____?', 'options': ['estás', 'comes', 'vives'], 'correct': 'estás', 'translation': 'Hello, how are you?'},
            {'type': 'fill_blank', 'sentence': 'Me gusta la _____.', 'options': ['comida', 'correr', 'azul'], 'correct': 'comida', 'translation': 'I like the food.'},
        ],
        'level_2': [
            {'type': 'grammar', 'prompt': 'How do you say "I am happy" in Spanish?', 'answer': 'estoy feliz', 'explanation': 'Use "estoy" for temporary states'},
            {'type': 'grammar', 'prompt': 'What is the Spanish word for "beautiful" (feminine)?', 'answer': 'bella', 'explanation': 'Adjectives must match gender'},
            {'type': 'translation', 'english': 'The red car', 'translation': 'el carro rojo', 'explanation': 'Adjectives come after nouns in Spanish'},
            {'type': 'fill_blank', 'sentence': 'Yo _____ estudiante.', 'options': ['soy', 'estoy', 'tengo'], 'correct': 'soy', 'translation': 'I am a student.'},
            {'type': 'fill_blank', 'sentence': '¿_____ años tienes?', 'options': ['Cuántos', 'Cuándo', 'Dónde'], 'correct': 'Cuántos', 'translation': 'How old are you?'},
            {'type': 'grammar', 'prompt': 'How do you say "I have a book" in Spanish?', 'answer': 'tengo un libro', 'explanation': 'Use "tengo" for possession'},
            {'type': 'translation', 'english': 'My sister is tall', 'translation': 'mi hermana es alta', 'explanation': 'Use "es" for permanent characteristics'},
            {'type': 'grammar', 'prompt': 'What is the plural of "niño" (boy)?', 'answer': 'niños', 'explanation': 'Add -s for masculine plurals'},
        ],
        'level_3': [
            {'type': 'conversation', 'prompt': 'How do you ask someone their name politely?', 'answer': '¿cómo te llamas?', 'alternative': '¿cuál es tu nombre?'},
            {'type': 'conversation', 'prompt': 'How do you say "I am from India"?', 'answer': 'soy de india', 'alternative': 'vengo de india'},
            {'type': 'story_completion', 'context': 'María goes to a restaurant', 'prompt': 'Complete: "Buenos días, ¿qué _____ hoy?"', 'answer': 'quiere', 'translation': 'Good morning, what do you want today?'},
            {'type': 'conversation', 'prompt': 'How do you say "Where is the bathroom?"', 'answer': '¿dónde está el baño?', 'alternative': '¿dónde queda el baño?'},
            {'type': 'conversation', 'prompt': 'How do you ask "How much does it cost?"', 'answer': '¿cuánto cuesta?', 'alternative': '¿cuál es el precio?'},
            {'type': 'story_completion', 'context': 'At a café', 'prompt': 'Complete: "Me gustaría un _____, por favor."', 'answer': 'café', 'translation': 'I would like a coffee, please.'},
            {'type': 'conversation', 'prompt': 'How do you say "Nice to meet you"?', 'answer': 'mucho gusto', 'alternative': 'encantado de conocerte'},
        ]
    },
    'fr': {
        'level_1': [
            {'type': 'vocabulary', 'word': 'hello', 'context': 'A greeting when you meet someone', 'translation': 'bonjour', 'audio_text': 'bon-ZHOOR'},
            {'type': 'vocabulary', 'word': 'goodbye', 'context': 'A farewell when you leave', 'translation': 'au revoir', 'audio_text': 'oh ruh-VWAHR'},
            {'type': 'vocabulary', 'word': 'thank you', 'context': 'Expression of gratitude', 'translation': 'merci', 'audio_text': 'mer-SEE'},
            {'type': 'vocabulary', 'word': 'water', 'context': 'A clear liquid we drink', 'translation': 'eau', 'audio_text': 'OH'},
            {'type': 'vocabulary', 'word': 'food', 'context': 'What we eat to survive', 'translation': 'nourriture', 'audio_text': 'noor-ree-TOOR'},
            {'type': 'vocabulary', 'word': 'house', 'context': 'A place where people live', 'translation': 'maison', 'audio_text': 'meh-ZOHN'},
            {'type': 'vocabulary', 'word': 'friend', 'context': 'Someone you like and trust', 'translation': 'ami', 'audio_text': 'ah-MEE'},
            {'type': 'vocabulary', 'word': 'family', 'context': 'Your relatives', 'translation': 'famille', 'audio_text': 'fah-MEEL'},
            {'type': 'fill_blank', 'sentence': 'Comment _____ vous?', 'options': ['allez', 'mangez', 'dormez'], 'correct': 'allez', 'translation': 'How are you?'},
            {'type': 'fill_blank', 'sentence': 'Je _____ français.', 'options': ['parle', 'mange', 'dors'], 'correct': 'parle', 'translation': 'I speak French.'},
        ],
        'level_2': [
            {'type': 'grammar', 'prompt': 'How do you say "I am" in French?', 'answer': 'je suis', 'explanation': 'Use "je suis" for permanent states'},
            {'type': 'translation', 'english': 'The house', 'translation': 'la maison', 'explanation': 'House is feminine in French'},
            {'type': 'grammar', 'prompt': 'How do you say "I have" in French?', 'answer': 'j\'ai', 'explanation': 'Use "j\'ai" for possession'},
            {'type': 'fill_blank', 'sentence': 'Elle _____ belle.', 'options': ['est', 'a', 'va'], 'correct': 'est', 'translation': 'She is beautiful.'},
            {'type': 'fill_blank', 'sentence': 'Nous _____ français.', 'options': ['parlons', 'mangeons', 'allons'], 'correct': 'parlons', 'translation': 'We speak French.'},
            {'type': 'grammar', 'prompt': 'How do you say "I am going" in French?', 'answer': 'je vais', 'explanation': 'Use "je vais" for immediate future'},
            {'type': 'translation', 'english': 'The red book', 'translation': 'le livre rouge', 'explanation': 'Adjectives usually come after nouns'},
        ],
        'level_3': [
            {'type': 'conversation', 'prompt': 'How do you ask "What is your name?"', 'answer': 'comment vous appelez-vous?', 'alternative': 'quel est votre nom?'},
            {'type': 'conversation', 'prompt': 'How do you say "I am from France"?', 'answer': 'je viens de france', 'alternative': 'je suis de france'},
            {'type': 'conversation', 'prompt': 'How do you ask "Where is the station?"', 'answer': 'où est la gare?', 'alternative': 'où se trouve la gare?'},
            {'type': 'conversation', 'prompt': 'How do you say "I would like"?', 'answer': 'je voudrais', 'alternative': 'j\'aimerais'},
            {'type': 'story_completion', 'context': 'At a café', 'prompt': 'Complete: "Je voudrais un _____, s\'il vous plaît."', 'answer': 'café', 'translation': 'I would like a coffee, please.'},
            {'type': 'conversation', 'prompt': 'How do you say "Excuse me"?', 'answer': 'excusez-moi', 'alternative': 'pardon'},
        ]
    },
    'de': {
        'level_1': [
            {'type': 'vocabulary', 'word': 'hello', 'context': 'A greeting when you meet someone', 'translation': 'hallo', 'audio_text': 'HAH-loh'},
            {'type': 'vocabulary', 'word': 'goodbye', 'context': 'A farewell when you leave', 'translation': 'auf wiedersehen', 'audio_text': 'owf VEE-der-zayn'},
            {'type': 'vocabulary', 'word': 'thank you', 'context': 'Expression of gratitude', 'translation': 'danke', 'audio_text': 'DAHN-kuh'},
            {'type': 'vocabulary', 'word': 'water', 'context': 'A clear liquid we drink', 'translation': 'wasser', 'audio_text': 'VAH-ser'},
            {'type': 'vocabulary', 'word': 'food', 'context': 'What we eat to survive', 'translation': 'essen', 'audio_text': 'EH-sen'},
            {'type': 'vocabulary', 'word': 'house', 'context': 'A place where people live', 'translation': 'haus', 'audio_text': 'HOWS'},
            {'type': 'vocabulary', 'word': 'friend', 'context': 'Someone you like and trust', 'translation': 'freund', 'audio_text': 'FROYNT'},
            {'type': 'vocabulary', 'word': 'family', 'context': 'Your relatives', 'translation': 'familie', 'audio_text': 'fah-MEE-lee-eh'},
            {'type': 'fill_blank', 'sentence': 'Wie _____ du?', 'options': ['heißt', 'bist', 'gehst'], 'correct': 'heißt', 'translation': 'What is your name?'},
            {'type': 'fill_blank', 'sentence': 'Ich _____ Deutsch.', 'options': ['spreche', 'esse', 'gehe'], 'correct': 'spreche', 'translation': 'I speak German.'},
        ],
        'level_2': [
            {'type': 'grammar', 'prompt': 'How do you say "I am" in German?', 'answer': 'ich bin', 'explanation': 'Use "ich bin" for identity'},
            {'type': 'translation', 'english': 'The house', 'translation': 'das haus', 'explanation': 'House is neuter in German'},
            {'type': 'grammar', 'prompt': 'How do you say "I have" in German?', 'answer': 'ich habe', 'explanation': 'Use "ich habe" for possession'},
            {'type': 'fill_blank', 'sentence': 'Sie _____ schön.', 'options': ['ist', 'hat', 'geht'], 'correct': 'ist', 'translation': 'She is beautiful.'},
            {'type': 'fill_blank', 'sentence': 'Wir _____ nach Hause.', 'options': ['gehen', 'sind', 'haben'], 'correct': 'gehen', 'translation': 'We go home.'},
            {'type': 'grammar', 'prompt': 'How do you say "I can" in German?', 'answer': 'ich kann', 'explanation': 'Use "ich kann" for ability'},
            {'type': 'translation', 'english': 'The big dog', 'translation': 'der große hund', 'explanation': 'Adjectives come before nouns'},
        ],
        'level_3': [
            {'type': 'conversation', 'prompt': 'How do you ask "How are you?"', 'answer': 'wie geht es dir?', 'alternative': 'wie geht es ihnen?'},
            {'type': 'conversation', 'prompt': 'How do you say "I am from Germany"?', 'answer': 'ich komme aus deutschland', 'alternative': 'ich bin aus deutschland'},
            {'type': 'conversation', 'prompt': 'How do you ask "Where is the train station?"', 'answer': 'wo ist der bahnhof?', 'alternative': 'wo befindet sich der bahnhof?'},
            {'type': 'conversation', 'prompt': 'How do you say "I would like"?', 'answer': 'ich möchte', 'alternative': 'ich hätte gern'},
            {'type': 'story_completion', 'context': 'At a restaurant', 'prompt': 'Complete: "Ich möchte ein _____, bitte."', 'answer': 'bier', 'translation': 'I would like a beer, please.'},
            {'type': 'conversation', 'prompt': 'How do you say "Please" in German?', 'answer': 'bitte', 'alternative': 'bitte schön'},
        ]
    }
}

# Language codes and names
language_codes = {
    'spanish': 'es',
    'french': 'fr', 
    'german': 'de'
}

language_names = {
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German'
}

# Initialize session state with improved structure
def initialize_session_state():
    if 'current_level' not in st.session_state:
        st.session_state.current_level = 1
    if 'current_language' not in st.session_state:
        st.session_state.current_language = None
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    # if 'level_progress' not in st.session_state:
    #     st.session_state.level_progress = {1: 0, 2: 0, 3: 0}  # Track questions completed per level
    # if 'level_unlocked' not in st.session_state:
    #     st.session_state.level_unlocked = {1: True, 2: False, 3: False}
    if 'level_progress' not in st.session_state:
        st.session_state.level_progress = {
            'es': {1: 0, 2: 0, 3: 0},
            'fr': {1: 0, 2: 0, 3: 0}, 
            'de': {1: 0, 2: 0, 3: 0}
        }
    if 'level_unlocked' not in st.session_state:
        st.session_state.level_unlocked = {
            'es': {1: True, 2: False, 3: False},
            'fr': {1: True, 2: False, 3: False},
            'de': {1: True, 2: False, 3: False}
        }
    if 'current_questions' not in st.session_state:
        st.session_state.current_questions = []
    if 'question_types' not in st.session_state:
        st.session_state.question_types = []
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = None
    if 'speech_input' not in st.session_state:
        st.session_state.speech_input = ""
    if 'question_answered' not in st.session_state:
        st.session_state.question_answered = False

@st.cache_resource
def initialize_tts_engine():
    """Simplified TTS engine initialization"""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        return engine
    except:
        return None

def text_to_speech_real(text, language='en'):
    """Simplified TTS with browser fallback"""
    try:
        st.info(f"🔊 Speaking: {text}")
        
        # Use browser TTS
        audio_html = f"""
        <script>
        if ('speechSynthesis' in window) {{
            var utterance = new SpeechSynthesisUtterance("{text}");
            utterance.lang = "{get_speech_lang_code(language)}";
            utterance.rate = 0.8;
            window.speechSynthesis.speak(utterance);
        }}
        </script>
        """
        components.html(audio_html, height=0)
        st.success("✅ Audio played!")
        
    except Exception as e:
        st.write(f"🔊 Read aloud: {text}")

def get_speech_lang_code(language):
    """Get proper language codes for browser speech synthesis"""
    lang_codes = {
        'es': 'es-ES',  # Spanish
        'fr': 'fr-FR',  # French
        'de': 'de-DE',  # German
        'en': 'en-US'   # English
    }
    return lang_codes.get(language, 'en-US')

def speech_to_text_real():
    """Fixed Speech-to-Text with proper fallback"""
    st.write("🎤 Speech Input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Option 1: Voice Input")
        # Improved browser speech recognition
        if st.button("🎤 Start Recording", key="voice_btn"):
            speech_html = f"""
            <div style="padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
                <button onclick="startSpeech()" style="padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 5px;">🎤 Click to Speak</button>
                <div id="result" style="margin-top: 10px; font-weight: bold;"></div>
                <div id="status" style="margin-top: 5px; color: #666;"></div>
            </div>
            <script>
            function startSpeech() {{
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    const recognition = new SpeechRecognition();
                    
                    recognition.continuous = false;
                    recognition.interimResults = false;
                    recognition.lang = '{get_speech_lang_code(st.session_state.get("current_language", "en"))}';
                    
                    document.getElementById('status').innerHTML = '🎤 Listening...';
                    
                    recognition.onresult = function(event) {{
                        const transcript = event.results[0][0].transcript;
                        document.getElementById('result').innerHTML = 'You said: "' + transcript + '"';
                        document.getElementById('status').innerHTML = '✅ Recording complete!';
                        
                        // Store result in a way Streamlit can access (simplified approach)
                        console.log('Speech result:', transcript);
                    }};
                    
                    recognition.onerror = function(event) {{
                        document.getElementById('status').innerHTML = '❌ Error: ' + event.error;
                    }};
                    
                    recognition.onend = function() {{
                        document.getElementById('status').innerHTML = '🔴 Recording stopped';
                    }};
                    
                    recognition.start();
                }} else {{
                    document.getElementById('result').innerHTML = '❌ Speech recognition not supported in this browser';
                }}
            }}
            </script>
            """
            components.html(speech_html, height=150)
    
    with col2:
        st.write("Option 2: Text Input")
        # Text input fallback (primary method)
        user_input = st.text_input(
            "Type your answer:", 
            key=f"text_input_{st.session_state.current_question_index}",
            placeholder="Enter your answer here..."
            )
        
        if user_input:
            st.session_state.speech_input = user_input
            return user_input.lower().strip()
    
    # Return any existing input
    return st.session_state.speech_input.lower().strip() if st.session_state.speech_input else None

def shuffle_questions(level, language_code):
    """Shuffle questions for the current level with validation"""
    questions = sample_prompts.get(language_code, {}).get(f'level_{level}', [])
    
    if not questions:
        st.error(f"No questions found for {language_names.get(language_code, 'Unknown')} Level {level}")
        return []
    
    shuffled = questions.copy()
    random.shuffle(shuffled)
    return shuffled

def check_level_completion(level):
    required_correct = 5
    current_lang = st.session_state.current_language
    
    if st.session_state.level_progress[current_lang][level] >= required_correct:
        if level < 3:
            st.session_state.level_unlocked[current_lang][level + 1] = True
        return True
    return False

def add_to_chat_history(speaker, message, language='en'):
    """Add message to chat history"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.chat_history.append({
        'timestamp': timestamp,
        'speaker': speaker,
        'message': message,
        'language': language
    })

def run_vocabulary_question(prompt, target_language):
    """Handle vocabulary questions"""
    word = prompt['word']
    context = prompt['context']
    correct_translation = prompt['translation']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"*English Word:* {word}")
        st.write(f"*Context:* {context}")
        
        if st.button("🔊 Listen to pronunciation", key=f"vocab_listen_{st.session_state.current_question_index}"):
            text_to_speech_real(f"The word {word} in {language_names[target_language]} is {correct_translation}", target_language)
    
    with col2:
        st.write(f"*Translate to {language_names[target_language]}:*")
        
        # Get user input (speech or text)
        user_input = speech_to_text_real()
        
        if user_input and st.button("✅ Check Answer", key=f"vocab_check_{st.session_state.current_question_index}") and not st.session_state.question_answered:
            st.session_state.question_answered = True
            add_to_chat_history("You", user_input)
            
            if user_input == correct_translation.lower():
                st.success("🎉 Correct!")
                st.session_state.score += 1
                #st.session_state.level_progress[st.session_state.current_level] += 1
                current_lang = st.session_state.current_language
                st.session_state.level_progress[current_lang][st.session_state.current_level] += 1
                text_to_speech_real("Correct! Well done!", target_language)
                return True
            else:
                st.error(f"❌ Incorrect. The correct answer is: *{correct_translation}*")
                text_to_speech_real(f"Incorrect. The correct answer is {correct_translation}", target_language)
                return False
    
    return None

def run_fill_blank_question(prompt, target_language):
    """Handle fill-in-the-blank questions"""
    sentence = prompt['sentence']
    options = prompt['options']
    correct = prompt['correct']
    translation = prompt.get('translation', '')
    
    st.write(f"*Complete the sentence:*")
    st.write(f"{sentence}")
    if translation:
        st.write(f"Translation: {translation}")
    
    # Randomize options
    shuffled_options = options.copy()
    random.shuffle(shuffled_options)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔊 Listen to sentence", key=f"blank_listen_{st.session_state.current_question_index}"):
            text_to_speech_real(sentence, target_language)
    
    with col2:
        selected_option = st.radio("Choose the correct word:", shuffled_options, key=f"blank_radio_{st.session_state.current_question_index}")
        
        if st.button("✅ Submit Answer", key=f"blank_submit_{st.session_state.current_question_index}") and not st.session_state.question_answered:
            st.session_state.question_answered = True
            add_to_chat_history("You", selected_option)
            
            if selected_option == correct:
                st.success("🎉 Correct!")
                st.session_state.score += 1
                current_lang = st.session_state.current_language
                st.session_state.level_progress[current_lang][st.session_state.current_level] += 1
                text_to_speech_real("Correct! Great job!", target_language)
                return True
            else:
                st.error(f"❌ Incorrect. The correct answer is: *{correct}*")
                text_to_speech_real(f"Incorrect. The correct answer is {correct}", target_language)
                return False
    
    return None

def run_grammar_question(prompt, target_language):
    """Handle grammar questions - FIXED VERSION"""
    question = prompt['prompt']
    correct_answer = prompt['answer']
    explanation = prompt.get('explanation', '')
    
    st.write(f"*Question:* {question}")
    if explanation:
        st.info(f"💡 *Tip:* {explanation}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔊 Listen to question", key=f"grammar_listen_{st.session_state.current_question_index}"):
            text_to_speech_real(question, target_language)
    
    with col2:
        user_input = speech_to_text_real()
        
        if user_input and st.button("✅ Check Answer", key=f"grammar_check_{st.session_state.current_question_index}") and not st.session_state.question_answered:
            st.session_state.question_answered = True
            add_to_chat_history("You", user_input)
            
            # More flexible answer checking
            user_clean = user_input.lower().strip()
            correct_clean = correct_answer.lower().strip()
            
            if correct_clean in user_clean or user_clean == correct_clean:
                st.success("🎉 Correct!")
                st.session_state.score += 1

                # st.session_state.level_progress[st.session_state.current_level] += 1
                current_lang = st.session_state.current_language
                st.session_state.level_progress[current_lang][st.session_state.current_level] += 1
                text_to_speech_real("Excellent! That's correct!", target_language)
                return True
            else:
                st.error(f"❌ Incorrect. The correct answer is: *{correct_answer}*")
                text_to_speech_real(f"Incorrect. The correct answer is {correct_answer}", target_language)
                return False
    
    return None

def run_translation_question(prompt, target_language):
    """Handle translation questions - FIXED VERSION"""
    english_text = prompt['english']
    correct_translation = prompt['translation']
    explanation = prompt.get('explanation', '')
    
    st.write(f"*Translate to {language_names[target_language]}:*")
    st.write(f"*English:* {english_text}")
    if explanation:
        st.info(f"💡 *Note:* {explanation}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔊 Listen to English", key=f"trans_listen_{st.session_state.current_question_index}"):
            text_to_speech_real(english_text, 'en')
    
    with col2:
        user_input = speech_to_text_real()
        
        if user_input and st.button("✅ Check Translation", key=f"trans_check_{st.session_state.current_question_index}") and not st.session_state.question_answered:
            st.session_state.question_answered = True
            add_to_chat_history("You", user_input)
            
            # More flexible translation checking
            user_clean = user_input.lower().strip()
            correct_clean = correct_translation.lower().strip()
            
            if correct_clean in user_clean or user_clean == correct_clean:
                st.success("🎉 Correct!")
                st.session_state.score += 1
                current_lang = st.session_state.current_language
                st.session_state.level_progress[current_lang][st.session_state.current_level] += 1
                text_to_speech_real("Perfect translation!", target_language)
                return True
            else:
                st.error(f"❌ Incorrect. The correct translation is: *{correct_translation}*")
                text_to_speech_real(f"Incorrect. The correct translation is {correct_translation}", target_language)
                return False
    
    return None

def run_conversation_question(prompt, target_language):
    """Handle conversation questions"""
    question = prompt['prompt']
    correct_answer = prompt['answer']
    alternative = prompt.get('alternative', '')
    
    st.write(f"*Conversation Practice:*")
    st.write(f"{question}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔊 Listen to question", key=f"conv_listen_{st.session_state.current_question_index}"):
            text_to_speech_real(question, 'en')
    
    with col2:
        user_input = speech_to_text_real()
        
        if user_input and st.button("✅ Check Answer", key=f"conv_check_{st.session_state.current_question_index}") and not st.session_state.question_answered:
            st.session_state.question_answered = True
            add_to_chat_history("You", user_input)
            
            user_clean = user_input.lower().strip()
            correct_clean = correct_answer.lower().strip()
            alt_clean = alternative.lower().strip() if alternative else ""
            
            if correct_clean in user_clean or user_clean == correct_clean or (alt_clean and alt_clean in user_clean):
                st.success("🎉 Great conversation skills!")
                st.session_state.score += 1
                #st.session_state.level_progress[st.session_state.current_level] += 1
                current_lang = st.session_state.current_language
                st.session_state.level_progress[current_lang][st.session_state.current_level] += 1
                text_to_speech_real("Excellent! You're speaking like a native!", target_language)
                return True
            else:
                st.error(f"❌ Try again. Suggested answer: *{correct_answer}*")
                if alternative:
                    st.info(f"Alternative: *{alternative}*")
                text_to_speech_real(f"Try again. The answer is {correct_answer}", target_language)
                return False
    
    return None

def run_story_completion_question(prompt, target_language):
    """Handle story completion questions"""
    context = prompt['context']
    question = prompt['prompt']
    correct_answer = prompt['answer']
    translation = prompt.get('translation', '')
    
    st.write(f"*Story Context:* {context}")
    st.write(f"*Complete the dialogue:*")
    st.write(f"{question}")
    if translation:
        st.write(f"Translation: {translation}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔊 Listen to dialogue", key=f"story_listen_{st.session_state.current_question_index}"):
            text_to_speech_real(question, target_language)
    
    with col2:
        user_input = speech_to_text_real()
        
        if user_input and st.button("✅ Complete Story", key=f"story_check_{st.session_state.current_question_index}") and not st.session_state.question_answered:
            st.session_state.question_answered = True
            add_to_chat_history("You", user_input)
            
            user_clean = user_input.lower().strip()
            correct_clean = correct_answer.lower().strip()
            
            if correct_clean in user_clean or user_clean == correct_clean:
                st.success("🎉 Perfect story completion!")
                st.session_state.score += 1

                #st.session_state.level_progress[st.session_state.current_level] += 1
                current_lang = st.session_state.current_language
                st.session_state.level_progress[current_lang][st.session_state.current_level] += 1
                text_to_speech_real("Wonderful storytelling!", target_language)
                return True
            else:
                st.error(f"❌ Not quite right. The answer is: *{correct_answer}*")
                text_to_speech_real(f"Not quite right. The answer is {correct_answer}", target_language)
                return False
    
    return None

def run_question(prompt, target_language):
    """Route question to appropriate handler based on type"""
    question_type = prompt.get('type', 'vocabulary')
    
    if question_type == 'vocabulary':
        return run_vocabulary_question(prompt, target_language)
    elif question_type == 'fill_blank':
        return run_fill_blank_question(prompt, target_language)
    elif question_type == 'grammar':
        return run_grammar_question(prompt, target_language)
    elif question_type == 'translation':
        return run_translation_question(prompt, target_language)
    elif question_type == 'conversation':
        return run_conversation_question(prompt, target_language)
    elif question_type == 'story_completion':
        return run_story_completion_question(prompt, target_language)
    else:
        st.error(f"Unknown question type: {question_type}")
        return None

def display_progress():
    """Display user progress and achievements"""
    st.sidebar.markdown("## 📊 Your Progress")
    
    # Overall score
    if st.session_state.total_questions > 0:
        accuracy = (st.session_state.score / st.session_state.total_questions) * 100
        st.sidebar.metric("Overall Accuracy", f"{accuracy:.1f}%", f"{st.session_state.score}/{st.session_state.total_questions}")
    
    # Level progress
    for level in [1, 2, 3]:
        current_lang = st.session_state.current_language
        progress = st.session_state.level_progress[current_lang][level]
        unlocked = st.session_state.level_unlocked[current_lang][level]
        
        if unlocked:
            st.sidebar.progress(min(progress / 5, 1.0), text=f"Level {level}: {progress}/5 ⭐")
        else:
            st.sidebar.write(f"🔒 Level {level}: Locked")
    
    # Achievements
    st.sidebar.markdown("## 🏆 Achievements")
    achievements = []
    
    if st.session_state.score >= 5:
        achievements.append("🌟 First Steps")
    if st.session_state.score >= 10:
        achievements.append("🔥 Getting Hot")
    if st.session_state.score >= 20:
        achievements.append("💎 Language Master")
    if st.session_state.current_language and st.session_state.level_unlocked[st.session_state.current_language][3]:
         achievements.append("🎓 Advanced Learner")

def show_chat_history():
    """Display chat history in sidebar"""
    if st.session_state.chat_history:
        st.sidebar.markdown("## 💬 Recent Activity")
        # Show last 5 interactions
        for chat in st.session_state.chat_history[-5:]:
            st.sidebar.write(f"{chat['speaker']}: {chat['message']}")

def main():
    """Main application function with futuristic sci-fi UI"""
    initialize_session_state()
    
    # Futuristic Sci-Fi CSS styling
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
        
        /* Global futuristic styling */
        .stApp {
            background: radial-gradient(ellipse at center, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #00ffff;
            font-family: 'Rajdhani', sans-serif;
        }
        
        /* Animated background particles */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
        
        .particle {
            position: absolute;
            width: 2px;
            height: 2px;
            background: #00ffff;
            animation: float 6s ease-in-out infinite;
            opacity: 0.7;
        }
        
        .particle:nth-child(2n) {
            background: #ff00ff;
            animation-delay: -2s;
            animation-duration: 8s;
        }
        
        .particle:nth-child(3n) {
            background: #ffff00;
            animation-delay: -4s;
            animation-duration: 10s;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.7; }
            50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
        }
        
        /* Main header with holographic effect */
        .main-header {
            background: linear-gradient(135deg, 
                rgba(0,255,255,0.1) 0%, 
                rgba(255,0,255,0.1) 25%,
                rgba(0,255,0,0.1) 50%,
                rgba(255,255,0,0.1) 75%,
                rgba(0,255,255,0.1) 100%);
            border: 2px solid transparent;
            background-clip: padding-box;
            position: relative;
            padding: 3rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            text-align: center;
            color: #00ffff;
            box-shadow: 
                0 0 30px rgba(0,255,255,0.3),
                inset 0 0 30px rgba(0,255,255,0.1);
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00, #00ff00);
            border-radius: 20px;
            z-index: -1;
            animation: rainbow-border 3s linear infinite;
        }
        
        @keyframes rainbow-border {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .main-header h1 {
            font-family: 'Orbitron', monospace;
            font-size: 4rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
            text-shadow: 
                0 0 10px #00ffff,
                0 0 20px #00ffff,
                0 0 30px #00ffff;
            animation: glow-pulse 2s ease-in-out infinite alternate;
        }
        
        .main-header h3 {
            font-size: 1.4rem;
            opacity: 0.9;
            font-weight: 400;
            text-shadow: 0 0 10px rgba(0,255,255,0.5);
            letter-spacing: 2px;
        }
        
        @keyframes glow-pulse {
            from { text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff; }
            to { text-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #00ffff; }
        }
        
        /* Welcome section with matrix-style background */
        .welcome-section {
            background: linear-gradient(135deg, 
                rgba(0,0,0,0.8) 0%, 
                rgba(26,26,46,0.9) 100%);
            border: 1px solid rgba(0,255,255,0.3);
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: 
                0 8px 32px rgba(0,255,255,0.1),
                inset 0 1px 0 rgba(255,255,255,0.1);
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .welcome-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent, 
                rgba(0,255,255,0.1), 
                transparent);
            animation: scan-line 3s linear infinite;
        }
        
        @keyframes scan-line {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        /* Feature cards with holographic styling */
        .feature-card {
            background: linear-gradient(135deg, 
                rgba(0,0,0,0.7) 0%, 
                rgba(26,26,46,0.8) 100%);
            border: 1px solid rgba(0,255,255,0.4);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            position: relative;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0,255,255,0.1);
        }
        
        .feature-card:hover {
            transform: translateY(-8px) scale(1.02);
            border-color: #00ffff;
            box-shadow: 
                0 20px 40px rgba(0,255,255,0.2),
                0 0 20px rgba(0,255,255,0.3);
        }
        
        .feature-card h4 {
            color: #00ffff;
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            text-shadow: 0 0 10px rgba(0,255,255,0.5);
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }
        
        .feature-card p {
            color: #a0a0a0;
            line-height: 1.6;
            font-size: 1.1rem;
        }
        
        /* Question type cards with neon effects */
        .question-card {
            background: rgba(0,0,0,0.8);
            border: 2px solid;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 1.5rem;
            position: relative;
            transition: all 0.4s ease;
            font-family: 'Rajdhani', sans-serif;
            overflow: hidden;
        }
        
        .question-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
            transform: translateX(-100%);
            transition: transform 0.6s;
        }
        
        .question-card:hover::before {
            transform: translateX(100%);
        }
        
        .question-card:hover {
            transform: scale(1.05) rotateY(5deg);
            box-shadow: 0 0 30px currentColor;
        }
        
        .question-card {
            border-color: #ffff00;
            color: #ffff00;
            text-shadow: 0 0 10px #ffff00;
        }
        
        .question-card.grammar {
            border-color: #ff00ff;
            color: #ff00ff;
            text-shadow: 0 0 10px #ff00ff;
        }
        
        .question-card.conversation {
            border-color: #00ff00;
            color: #00ff00;
            text-shadow: 0 0 10px #00ff00;
        }
        
        .question-card h3 {
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        
        /* Subscription section with cyberpunk styling */
        .subscription-section {
            background: linear-gradient(135deg, 
                rgba(26,26,46,0.9) 0%, 
                rgba(22,33,62,0.9) 100%);
            border: 1px solid rgba(0,255,255,0.3);
            color: #00ffff;
            padding: 3rem;
            border-radius: 20px;
            margin-top: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .subscription-section::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0,255,255,0.05) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .plan-card {
            background: rgba(0,0,0,0.6);
            border: 1px solid rgba(0,255,255,0.3);
            padding: 2rem;
            border-radius: 12px;
            backdrop-filter: blur(15px);
            position: relative;
            z-index: 1;
            transition: all 0.4s ease;
        }
        
        .plan-card:hover {
            border-color: #00ffff;
            box-shadow: 0 0 30px rgba(0,255,255,0.3);
            transform: translateY(-5px);
        }
        
        .plan-card.premium {
            background: linear-gradient(135deg, rgba(255,0,255,0.1), rgba(255,255,0,0.1));
            border: 2px solid #ff00ff;
            transform: scale(1.05);
            animation: premium-glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes premium-glow {
            from { box-shadow: 0 0 20px rgba(255,0,255,0.3); }
            to { box-shadow: 0 0 40px rgba(255,0,255,0.6), 0 0 60px rgba(255,255,0,0.3); }
        }
        
        /* Contact section with terminal styling */
        .contact-section {
            background: linear-gradient(135deg, rgba(0,0,0,0.9), rgba(26,26,46,0.9));
            border: 1px solid #00ff00;
            color: #00ff00;
            padding: 2.5rem;
            border-radius: 15px;
            text-align: center;
            margin-top: 2rem;
            font-family: 'Rajdhani', monospace;
            box-shadow: 0 0 20px rgba(0,255,0,0.2);
        }
        
        .contact-link {
            display: inline-block;
            background: rgba(0,255,0,0.1);
            border: 1px solid #00ff00;
            padding: 1rem 2rem;
            margin: 0.5rem;
            border-radius: 25px;
            text-decoration: none;
            color: #00ff00;
            transition: all 0.3s ease;
            font-family: 'Orbitron', monospace;
            font-weight: 600;
            position: relative;
            overflow: hidden;
        }
        
        .contact-link::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: radial-gradient(circle, rgba(0,255,0,0.3) 0%, transparent 70%);
            transition: all 0.3s ease;
            transform: translate(-50%, -50%);
        }
        
        .contact-link:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .contact-link:hover {
            background: rgba(0,255,0,0.2);
            box-shadow: 0 0 20px rgba(0,255,0,0.4);
            transform: translateY(-3px);
            text-shadow: 0 0 10px #00ff00;
        }
        
        /* VR Button with advanced holographic effect */
        .vr-button {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 1000;
            background: linear-gradient(135deg, rgba(102,51,238,0.8), rgba(168,85,247,0.8));
            border: 2px solid #ff00ff;
            color: #ff00ff;
            padding: 20px 25px;
            border-radius: 50px;
            font-size: 18px;
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.4s ease;
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 0 10px #ff00ff;
            box-shadow: 
                0 8px 25px rgba(255,0,255,0.3),
                0 0 20px rgba(255,0,255,0.2);
            animation: vr-float 3s ease-in-out infinite;
        }
        
        .vr-button:hover {
            transform: translateY(-5px) scale(1.1);
            box-shadow: 
                0 15px 35px rgba(255,0,255,0.4),
                0 0 30px rgba(255,0,255,0.4);
            background: linear-gradient(135deg, rgba(255,0,255,0.2), rgba(255,255,0,0.2));
        }
        
        @keyframes vr-float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        /* Learning session styling */
        .question-header {
            background: linear-gradient(135deg, 
                rgba(0,255,255,0.1) 0%, 
                rgba(255,0,255,0.1) 100%);
            border: 1px solid rgba(0,255,255,0.5);
            color: #00ffff;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 1.5rem;
            text-align: center;
            font-family: 'Orbitron', monospace;
            box-shadow: 0 0 20px rgba(0,255,255,0.2);
        }
        
        .progress-container {
            background: rgba(0,0,0,0.8);
            border: 1px solid rgba(0,255,255,0.3);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            backdrop-filter: blur(10px);
        }
        
        /* Custom progress bar */
        .stProgress .st-bo {
            background: linear-gradient(90deg, #00ffff, #ff00ff, #ffff00) !important;
            height: 8px !important;
            border-radius: 10px !important;
        }
        
        /* Level buttons with matrix effect */
        .level-button {
            margin-bottom: 0.8rem;
            font-family: 'Rajdhani', sans-serif;
        }
        
        /* Streamlit button customization */
        .stButton > button {
            background: linear-gradient(135deg, rgba(0,0,0,0.8), rgba(26,26,46,0.8)) !important;
            border: 1px solid rgba(0,255,255,0.5) !important;
            color: #00ffff !important;
            font-family: 'Rajdhani', sans-serif !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        
        .stButton > button:hover {
            border-color: #00ffff !important;
            box-shadow: 0 0 20px rgba(0,255,255,0.3) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            background: rgba(0,0,0,0.8) !important;
            border: 1px solid rgba(0,255,255,0.3) !important;
            color: #00ffff !important;
        }
        
        /* Matrix rain effect background */
        .matrix-rain {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -2;
            opacity: 0.1;
        }
        
        /* Animations */
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .animate-slide-up {
            animation: slideInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .animate-fade-in {
            animation: fadeIn 1s ease-in;
        }
        
        /* Terminal text effect */
        .terminal-text {
            font-family: 'Courier New', monospace;
            color: #00ff00;
            text-shadow: 0 0 5px #00ff00;
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(0,0,0,0.5);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #00ffff, #ff00ff);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(45deg, #ff00ff, #ffff00);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Add animated background particles
    st.markdown("""
    <div class="particles">
        <div class="particle" style="top: 10%; left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="top: 20%; left: 80%; animation-delay: 1s;"></div>
        <div class="particle" style="top: 80%; left: 20%; animation-delay: 2s;"></div>
        <div class="particle" style="top: 60%; left: 70%; animation-delay: 3s;"></div>
        <div class="particle" style="top: 30%; left: 40%; animation-delay: 4s;"></div>
        <div class="particle" style="top: 70%; left: 60%; animation-delay: 5s;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Futuristic Header
    st.markdown("""
    <div class="main-header animate-slide-up">
        <h1>⚡ CORTEX TALK</h1>
        <h3>ADVANCED AI LANGUAGE MATRIX •  LEARNING PROTOCOL</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Sidebar with cyberpunk design
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; 
                    background: linear-gradient(135deg, rgba(0,255,255,0.1), rgba(255,0,255,0.1)); 
                    border: 1px solid rgba(0,255,255,0.3);
                    border-radius: 12px; margin-bottom: 1.5rem; color: #00ffff;
                    box-shadow: 0 0 20px rgba(0,255,255,0.2);">
            <h2 style="margin: 0; font-family: 'Orbitron', monospace; text-shadow: 0 0 10px #00ffff;">🌐 LANGUAGE HUB</h2>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;"> LANGUAGE INTERFACE</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Language selection with futuristic styling
        selected_language = st.selectbox(
            "◦ SELECT TARGET LANGUAGE PROTOCOL:",
            ["[STANDBY MODE]", "SPANISH", "FRENCH", "GERMAN"],
            key="language_selector"
        )
        
        if selected_language != "[STANDBY MODE]":
            st.session_state.current_language = language_codes[selected_language.lower()]
            
            # Enhanced level selection with matrix styling
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(255,0,255,0.1), rgba(255,255,0,0.1)); 
                        border: 1px solid rgba(255,0,255,0.3);
                        color: #ff00ff; padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0; text-align: center;
                        box-shadow: 0 0 15px rgba(255,0,255,0.2);">
                <h3 style="margin: 0; font-family: 'Orbitron', monospace; text-shadow: 0 0 10px #ff00ff;">📊 NEURAL PROGRESSION</h3>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">COGNITIVE ENHANCEMENT LEVELS</p>
            </div>
            """, unsafe_allow_html=True)
            
            for level in [1, 2, 3]:
                current_lang = st.session_state.current_language
                if st.session_state.level_unlocked[current_lang][level]:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button(f"⚡ LEVEL {level} - ONLINE", key=f"level_{level}", use_container_width=True):
                            st.session_state.current_level = level
                            st.session_state.current_question_index = 0
                            st.session_state.current_questions = shuffle_questions(level, st.session_state.current_language)
                            st.session_state.question_answered = False
                            st.rerun()
                    with col2:
                        st.markdown("🟢")
                else:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.button(f"🔒 LEVEL {level} - LOCKED", disabled=True, use_container_width=True)
                    with col2:
                        st.markdown("🔴")
            
            display_progress()
            show_chat_history()
    
    # Main content area
    if not st.session_state.current_language:
        # Futuristic Welcome screen
        st.markdown("""
        <div class="welcome-section animate-slide-up">
            <h2 style="text-align: center; color: #00ffff; margin-bottom: 2rem; font-family: 'Orbitron', monospace;">
                🚀  LANGUAGE INTERFACE INITIALIZED
            </h2>
            <p style="text-align: center; color: #a0a0a0; font-size: 1.1rem; line-height: 1.6;">
                Welcome to the future of language learning. Our advanced AI neural network adapts to your learning patterns, 
                providing personalized cognitive enhancement through quantum-powered language protocols.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced features section with sci-fi styling
        st.markdown("### ⚡ SYSTEM CAPABILITIES")
        
        features = [
            ("🧠", " ADAPTATION", "Advanced AI that learns your patterns and optimizes training protocols"),
            ("🎯", " TARGETING", "Precision-focused skill development with real-time neural feedback"),
            ("🔊", " AUDIO", "Voice synthesis and recognition with phonetic analysis systems"),
            ("📊", "COGNITIVE METRICS", "Advanced analytics tracking your neural pathway development"),
            ("🏆", "ACHIEVEMENT", "Gamified progression system with unlock-based advancement protocols")
        ]
        
        for icon, title, description in features:
            st.markdown(f"""
            <div class="feature-card animate-fade-in">
                <h4>{icon} {title}</h4>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced question types with cyberpunk styling
        st.markdown("### 🎮 TRAINING MODULES")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="question-card">
                <h3>💾 VOCABULARY CORE</h3>
                <p>• Neural word mapping<br>
                • Phonetic synthesis<br>
                • Memory bank expansion</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="question-card grammar">
                <h3>🔗 SYNTAX MATRIX</h3>
                <p>• Grammar protocol training<br>
                • Structural optimization<br>
                • Pattern recognition</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="question-card conversation">
                <h3>💬 DIALOGUE ENGINE</h3>
                <p>• Real-world simulation<br>
                • Contextual processing<br>
                • Interactive scenarios</p>
            </div>
            """, unsafe_allow_html=True)

        # Futuristic getting started section
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0,255,0,0.1), rgba(0,255,255,0.1)); 
                    border: 1px solid rgba(0,255,0,0.3);
                    color: #00ff00; padding: 3rem; border-radius: 20px; text-align: center; margin: 2rem 0;
                    box-shadow: 0 0 30px rgba(0,255,0,0.2);">
            <h3 style="font-family: 'Orbitron', monospace; text-shadow: 0 0 15px #00ff00;">🔋 SYSTEM ACTIVATION PROTOCOL</h3>
            <p style="font-size: 1.2rem; margin-bottom: 2rem; line-height: 1.6;">
                Initialize your neural learning matrix and join the cognitive enhancement program
            </p>
            <div style="background: rgba(0,0,0,0.3); padding: 2rem; border-radius: 12px; 
                        border: 1px solid rgba(0,255,0,0.2); margin-top: 1.5rem;">
                <strong style="color: #00ffff;">ACTIVATION SEQUENCE:</strong><br><br>
                <span class="terminal-text">
                > SELECT_LANGUAGE_PROTOCOL<br>
                > INITIALIZE_LEVEL_01<br>
                > ENABLE_VOICE_SYNTHESIS<br>
                > START_COGNITIVE_ENHANCEMENT
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Cyberpunk subscription section
        st.markdown("""
        <div class="subscription-section">
            <h2 style="text-align: center; margin-bottom: 2rem; font-family: 'Orbitron', monospace; 
                       text-shadow: 0 0 15px #00ffff;">💎 ACCESS LEVEL SELECTION</h2>
            <p style="text-align: center; margin-bottom: 2rem; opacity: 0.8;">Choose your neural enhancement package</p>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="plan-card">
                <h3 style="text-align: center; color: #ffff00; font-family: 'Orbitron', monospace;">🌐 BASIC PROTOCOL</h3>
                <div style="text-align: center; font-size: 2.5rem; margin: 1.5rem 0; color: #ffff00;">FREE ACCESS</div>
            """, unsafe_allow_html=True)
            
            for feature in SUBSCRIPTION_PLANS["Free"]['features']:
                st.markdown(f"🔹 {feature}")
            
            if st.button("ACTIVATE BASIC PROTOCOL", use_container_width=True, key="free_plan"):
                st.success("🔋 BASIC PROTOCOL ACTIVATED! Neural matrix ready for initialization! ⚡")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="plan-card premium">
                <h3 style="text-align: center; color: #ff00ff; font-family: 'Orbitron', monospace;">⚡ PREMIUM NEURAL</h3>
                <div style="text-align: center; font-size: 2.5rem; margin: 1.5rem 0; color: #ff00ff;">$9.99/CYCLE</div>
            """, unsafe_allow_html=True)
            
            for feature in SUBSCRIPTION_PLANS["Premium"]['features']:
                st.markdown(f"🔸 {feature}")
            
            if st.button("UPGRADE TO PREMIUM NEURAL", use_container_width=True, key="premium_plan"):
                st.success("🚀 INITIATING QUANTUM PAYMENT PROTOCOL...")
                st.balloons()
            
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Futuristic contact section
        st.markdown("""
        <div class="contact-section">
            <h2 style="font-family: 'Orbitron', monospace;">📡  CONTACT</h2>
            <p style="margin-bottom: 2rem;">Connect to our communication channels</p>
            <div style="margin-top: 2rem;">
                 <a href="tel:+918919453489" class="contact-link">
                        📞 LINE — +44 7776619604
                    </a>   
                <a href="mailto:abdul99.rc@gmail.com" class="contact-link">
                    📧 NEURAL.SUPPORT
                </a>
               <a href="https://www.instagram.com/cor.textalk?igsh=MmVzMjYydW5tejht" class="contact-link">
                    🌐 QUANTUM.INSTA
                </a>
                <a href="https://discord.gg/cortexai" class="contact-link">
                    💬 AI.COLLECTIVE
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Advanced VR button with holographic effect
        st.markdown("""
            <button class="vr-button" onclick="alert('🎮 VIRTUAL REALITY NEURAL INTERFACE\\n\\nQuantum VR learning protocols coming online...\\nPrepare for full immersion cognitive enhancement!')">
                🎮 VR.NEURAL
            </button>
        """, unsafe_allow_html=True)
                
    elif not st.session_state.current_questions:
        # Enhanced language selection screen
        lang_name = language_names[st.session_state.current_language]
        st.markdown(f"""
        <div class="question-header">
            <h2 style="font-family: 'Orbitron', monospace;">🎯 CORTEXTALK: {lang_name.upper()}</h2>
            <p>Select training level  to begin cognitive enhancement!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced level requirements with matrix styling
        st.markdown("""
        <div style="background: rgba(0,0,0,0.8); border: 1px solid rgba(0,255,255,0.3);
                    padding: 2.5rem; border-radius: 15px; box-shadow: 0 0 20px rgba(0,255,255,0.1);">
            <h3 style="color: #00ffff; margin-bottom: 2rem; font-family: 'Orbitron', monospace; text-shadow: 0 0 10px #00ffff;">
                📋 NEURAL ENHANCEMENT PROTOCOLS
            </h3>
        """, unsafe_allow_html=True)
        
        levels_info = [
            ("1", "🔰 INITIATE", "Basic neural pathway mapping", "Complete 5 protocols to unlock Level 2"),
            ("2", "⚡ ENHANCED", "Advanced cognitive processing", "Complete 5 protocols to unlock Level 3"),
            ("3", "🧠 MASTER", "Maximum neural efficiency", "Achieve cognitive mastery")
        ]
        
        for level, title, desc, req in levels_info:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(0,255,255,0.05), rgba(255,0,255,0.05)); 
                        border: 1px solid rgba(0,255,255,0.3);
                        padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
                <h4 style="margin: 0; color: #00ffff; font-family: 'Orbitron', monospace;">
                    LEVEL {level}: {title}
                </h4>
                <p style="margin: 0.8rem 0; color: #a0a0a0; line-height: 1.6;">{desc}</p>
                <small style="color: #ffff00; font-family: 'Courier New', monospace;">
                    ⚡ REQUIREMENT: {req}
                </small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        # Enhanced active learning session
        if st.session_state.current_question_index < len(st.session_state.current_questions):
            current_prompt = st.session_state.current_questions[st.session_state.current_question_index]
            
            # Enhanced question header
            lang_name = language_names[st.session_state.current_language]
            st.markdown(f"""
            <div class="question-header">
                <h2 style="font-family: 'Orbitron', monospace;">🎯 {lang_name.upper()} NEURAL LINK - LEVEL {st.session_state.current_level}</h2>
                <p>PROTOCOL {st.session_state.current_question_index + 1} OF {len(st.session_state.current_questions)} | STATUS: ACTIVE</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced progress section
            st.markdown('<div class="progress-container">', unsafe_allow_html=True)
            progress = (st.session_state.current_question_index) / len(st.session_state.current_questions)
            st.progress(progress)
            
            # Question type indicator with enhanced styling
            question_type = current_prompt.get('type', 'vocabulary').replace('_', ' ').title()
            st.markdown(f"""
            <div style="text-align: center; margin: 1.5rem 0;">
                <span style="background: linear-gradient(135deg, rgba(0,255,255,0.2), rgba(255,0,255,0.2)); 
                            border: 1px solid rgba(0,255,255,0.5);
                            color: #00ffff; padding: 0.8rem 2rem; border-radius: 25px; 
                            font-weight: bold; font-family: 'Orbitron', monospace;
                            text-shadow: 0 0 10px #00ffff; box-shadow: 0 0 15px rgba(0,255,255,0.2);">
                    🔬 {question_type.upper()} PROTOCOL
                </span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Run the question
            result = run_question(current_prompt, st.session_state.current_language)
            
            # Enhanced navigation buttons
            st.markdown('<div style="margin-top: 3rem;">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("⏪ PREVIOUS ", disabled=st.session_state.current_question_index == 0, 
                           use_container_width=True, key="prev_btn"):
                    if st.session_state.current_question_index > 0:
                        st.session_state.current_question_index -= 1
                        st.session_state.question_answered = False
                        st.rerun()
            
            with col2:
                if st.session_state.question_answered:
                    if st.button("⏩ NEXT ", use_container_width=True, key="next_btn"):
                        st.session_state.current_question_index += 1
                        st.session_state.total_questions += 1
                        st.session_state.question_answered = False
                        
                        # Check level completion
                        if check_level_completion(st.session_state.current_level):
                            st.balloons()
                            st.success(f"🎉 LEVEL {st.session_state.current_level} COMPLETED! Neural pathway enhanced! Next level unlocked!")
                        
                        st.rerun()
            
            with col3:
                if st.button("🔄 RESTART NEURAL LINK", use_container_width=True, key="restart_btn"):
                    st.session_state.current_question_index = 0
                    st.session_state.current_questions = shuffle_questions(st.session_state.current_level, st.session_state.current_language)
                    st.session_state.question_answered = False
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            # Enhanced session completed screen
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(0,255,0,0.1), rgba(0,255,255,0.1)); 
                        border: 2px solid #00ff00;
                        color: #00ff00; padding: 4rem; border-radius: 25px; text-align: center; margin-bottom: 2rem;
                        box-shadow: 0 0 40px rgba(0,255,0,0.3); position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; 
                            background: repeating-linear-gradient(90deg, transparent, rgba(0,255,0,0.1) 2px, transparent 4px);
                            animation: scan-complete 2s linear infinite;"></div>
                <h1 style="font-size: 4rem; margin-bottom: 1rem; font-family: 'Orbitron', monospace; 
                           text-shadow: 0 0 20px #00ff00;">⚡</h1>
                <h2 style="font-family: 'Orbitron', monospace; text-shadow: 0 0 15px #00ff00;">
                    NEURAL SESSION COMPLETE
                </h2>
                <p style="font-size: 1.3rem; margin-top: 1rem;">Cognitive enhancement protocol successfully executed!</p>
            </div>
            
            <style>
            @keyframes scan-complete {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }
            </style>
            """, unsafe_allow_html=True)
            
            accuracy = (st.session_state.score / st.session_state.total_questions) * 100 if st.session_state.total_questions > 0 else 0
            
            # Enhanced session summary with holographic stats
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(0,255,255,0.1), rgba(255,0,255,0.1)); 
                            border: 1px solid #00ffff;
                            color: #00ffff; padding: 2.5rem; border-radius: 15px; text-align: center;
                            box-shadow: 0 0 25px rgba(0,255,255,0.2);">
                    <h2 style="font-size: 3rem; margin: 0; font-family: 'Orbitron', monospace; 
                               text-shadow: 0 0 15px #00ffff;">{len(st.session_state.current_questions)}</h2>
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">PROTOCOLS EXECUTED</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(255,0,255,0.1), rgba(255,255,0,0.1)); 
                            border: 1px solid #ff00ff;
                            color: #ff00ff; padding: 2.5rem; border-radius: 15px; text-align: center;
                            box-shadow: 0 0 25px rgba(255,0,255,0.2);">
                    <h2 style="font-size: 3rem; margin: 0; font-family: 'Orbitron', monospace; 
                               text-shadow: 0 0 15px #ff00ff;">{st.session_state.score}/{st.session_state.total_questions}</h2>
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">NEURAL SCORE</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(255,255,0,0.1), rgba(0,255,0,0.1)); 
                            border: 1px solid #ffff00;
                            color: #ffff00; padding: 2.5rem; border-radius: 15px; text-align: center;
                            box-shadow: 0 0 25px rgba(255,255,0,0.2);">
                    <h2 style="font-size: 3rem; margin: 0; font-family: 'Orbitron', monospace; 
                               text-shadow: 0 0 15px #ffff00;">{accuracy:.1f}%</h2>
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">EFFICIENCY RATE</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Enhanced action buttons
            st.markdown('<div style="margin-top: 3rem;">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 REPEAT NEURAL TRAINING", use_container_width=True, key="practice_again"):
                    st.session_state.current_question_index = 0
                    st.session_state.current_questions = shuffle_questions(st.session_state.current_level, st.session_state.current_language)
                    st.session_state.question_answered = False
                    st.rerun()
            
            with col2:
                current_lang = st.session_state.current_language
                if st.session_state.level_unlocked.get(st.session_state.current_level + 1, False):
                    if st.button("⚡ ADVANCE NEURAL LEVEL", use_container_width=True, key="next_level"):
                        st.session_state.current_level += 1
                        st.session_state.current_question_index = 0
                        st.session_state.current_questions = shuffle_questions(st.session_state.current_level, st.session_state.current_language)
                        st.session_state.question_answered = False
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
