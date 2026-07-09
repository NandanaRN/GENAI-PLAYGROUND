import random
import re
import torch
import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# =====================================================================
# 1. LOCAL HARDWARE & ENGINE CONFIGURATION
# =====================================================================
MODEL_ID = 'HuggingFaceTB/SmolLM2-135M-Instruct'

print("Checking local system configuration...")
if torch.cuda.is_available():
    print(f"GPU detected: {torch.cuda.get_device_name(0)}. Running on hardware acceleration.")
    device_map = 'auto'
    torch_dtype = torch.float16
else:
    print("No GPU detected. Running on CPU engine. (Optimized with ultra-fast SmolLM2)")
    device_map = 'cpu'
    torch_dtype = torch.float32

print(f"Loading open-source brain model: {MODEL_ID}")
print("Loading model weights...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch_dtype,
    device_map=device_map
)

generator = pipeline(
    'text-generation',
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=150,  
    temperature=0.7,
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id
)

print('🧠 Local Interview Model is loaded and ready!')

# =====================================================================
# 2. INTERVIEW QUESTION BANK
# =====================================================================
QUESTION_BANK = {
    'Python Developer': [
        'Explain the difference between a list and a tuple in Python.',
        'What are Python decorators and how do you use them?',
        'Explain the concept of generators in Python with an example.',
        'What is the difference between deep copy and shallow copy?',
        'How does Python GIL affect multithreading?'
    ],
    'Data Science': [
        'What is the difference between supervised and unsupervised learning?',
        'Explain overfitting and how to prevent it.',
        'What is cross-validation and why is it important?',
        'Explain the bias-variance tradeoff.'
    ],
    'Web Developer': [
        'Explain the difference between HTTP and HTTPS.',
        'What is REST API and what are its principles?',
        'Explain the event loop in JavaScript.',
        'What is the difference between SQL and NoSQL databases?'
    ],
    'HR / Behavioral': [
        'Tell me about yourself and your background.',
        'Describe a situation where you handled a conflict with a teammate.',
        'What is your greatest strength and weakness?',
        'Tell me about a time you failed and what you learned from it.'
    ],
    'Machine Learning Engineer': [
        'Explain the difference between batch and online learning.',
        'How do you deploy a machine learning model to production?',
        'What is model drift and how do you monitor it.',
        'Explain the transformer architecture briefly.'
    ]
}

# =====================================================================
# 3. CORE PROCESSING LOGIC
# =====================================================================
def generate_response(prompt, max_tokens=150):
    try:
        output = generator(prompt, max_new_tokens=max_tokens, truncation=True)
        full_text = output[0]['generated_text']
        response = full_text[len(prompt):].strip()
        return response
    except Exception as e:
        return f'[Model processing error: {str(e)}]'

def get_next_question(role, used_questions):
    all_questions = QUESTION_BANK.get(role, QUESTION_BANK['HR / Behavioral'])
    remaining = [q for q in all_questions if q not in used_questions]
    if not remaining:
        return None
    return random.choice(remaining)

def evaluate_answer(question, answer, role):
    messages = [
        {
            "role": "system", 
            "content": f"You are an expert technical interviewer and supportive career coach for {role} positions. Evaluate the candidate's answer strictly but keep your tone helpful."
        },
        {
            "role": "user", 
            "content": (
                f"Interview Question: {question}\n\n"
                f"Candidate Answer: {answer}\n\n"
                f"Evaluate this answer exactly with this structure:\n"
                f"1. SCORE: X/10\n"
                f"2. STRENGTHS: What the candidate did well\n"
                f"3. WEAKNESSES: What was missing or incorrect\n"
                f"4. IDEAL ANSWER: Key points a strong answer should include\n"
                f"5. TIP: One specific improvement suggestion"
            )
        }
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    return generate_response(prompt, max_tokens=150)

def teach_concept(question, role):
    """Custom coaching function when a user explicitly states they don't know the answer."""
    messages = [
        {
            "role": "system", 
            "content": f"You are an encouraging mentor and technical coach training someone for a {role} role. Explain concepts simply and cleanly."
        },
        {
            "role": "user", 
            "content": f"I don't know the answer to this interview question: '{question}'. Can you explain it to me simply so I can learn it?"
        }
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    return generate_response(prompt, max_tokens=150)

def new_state():
    return {
        'phase': 'role_selection',
        'role': None,
        'used_questions': [],
        'current_question': None,
        'score_total': 0,
        'questions_done': 0,
        'max_questions': 5
    }

def _summary(state):
    done = state['questions_done']
    total = state['score_total']
    avg = total / max(done, 1)
    if avg >= 8:
        verdict = 'Excellent performance! You are well-prepared!'
    elif avg >= 6:
        verdict = 'Good effort! Review weak areas and keep practicing.'
    else:
        verdict = 'Keep studying - review the ideal answers above and try again.'
    return (
        f'**Interview Complete!**\n\n'
        f'**Final Score: {total}/{done * 10}** (Average: {avg:.1f}/10)\n\n'
        f'{verdict}\n\nType **restart** to start a new interview.'
    )

def chat(user_message, history, state):
    if state is None:
        state = new_state()

    response = ''
    phase = state['phase']
    roles = list(QUESTION_BANK.keys())
    msg = user_message.strip()

    if phase == 'role_selection':
        selected_role = None
        if msg.isdigit():
            idx = int(msg) - 1
            if 0 <= idx < len(roles):
                selected_role = roles[idx]
        else:
            for role in roles:
                if msg.lower() in role.lower() or role.lower() in msg.lower():
                    selected_role = role
                    break

        if selected_role:
            state['role'] = selected_role
            state['phase'] = 'interviewing'
            question = get_next_question(selected_role, state['used_questions'])
            state['current_question'] = question
            state['used_questions'].append(question)
            response = (
                f'Great! Starting your **{selected_role}** interview.\n\n'
                f'I will ask you {state["max_questions"]} questions and give feedback after each.\n\n'
                f'---\n\n**Question 1/{state["max_questions"]}:**\n\n'
                f'{question}\n\nTake your time and type your answer below. (If you don\'t know it, just type "I don\'t know" and I will help you!)'
            )
        else:
            role_list = '\n'.join([f'{i+1}. {r}' for i, r in enumerate(roles)])
            response = f'Please type a number or role name:\n{role_list}'

    elif phase == 'interviewing':
        # Check if the user is explicitly asking for help or doesn't know
        dont_know_keywords = ["don't know", "dont know", "no idea", "skip", "clueless", "help me", "not sure"]
        is_clueless = any(keyword in msg.lower() for keyword in dont_know_keywords)
        
        if is_clueless:
            state['questions_done'] += 1
            q_num = state['questions_done']
            
            # Coach mode trigger
            explanation = teach_concept(state['current_question'], state['role'])
            response = (
                f'**No worries at all! That\'s exactly why we are practicing.** 👍\n\n'
                f'Here is a simple breakdown of the concept:\n\n{explanation}\n\n'
                f'**Did you understand this explanation?**\n\n'
                f'---\n'
            )
            # Give a free baseline passing point for engaging with the learning material
            state['score_total'] += 5 
            
            # queue next question
            if state['questions_done'] < state['max_questions']:
                next_q = get_next_question(state['role'], state['used_questions'])
                if next_q:
                    state['current_question'] = next_q
                    state['used_questions'].append(next_q)
                    response += (
                        f'Let\'s try the next one!\n\n'
                        f'**Question {q_num + 1}/{state["max_questions"]}:**\n\n'
                        f'{next_q}\n\nType your answer below.'
                    )
                else:
                    state['phase'] = 'completed'
                    response += _summary(state)
            else:
                state['phase'] = 'completed'
                response += _summary(state)
                
        elif len(msg) < 10:
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": "Please give a more detailed answer or type 'I don't know' so I can explain it to you!"})
            return history, '', state
        else:
            state['questions_done'] += 1
            q_num = state['questions_done']
            feedback = evaluate_answer(state['current_question'], msg, state['role'])
            score_match = re.search(r'(\d+)\s*/\s*10', feedback)
            if score_match:
                state['score_total'] += int(score_match.group(1))
            else:
                state['score_total'] += 7

            response = f'**Feedback for Question {q_num}:**\n\n{feedback}\n\n---\n'

            if state['questions_done'] < state['max_questions']:
                next_q = get_next_question(state['role'], state['used_questions'])
                if next_q:
                    state['current_question'] = next_q
                    state['used_questions'].append(next_q)
                    response += (
                        f'**Question {q_num + 1}/{state["max_questions"]}:**\n\n'
                        f'{next_q}\n\nType your answer below.'
                    )
                else:
                    state['phase'] = 'completed'
                    response += _summary(state)
            else:
                state['phase'] = 'completed'
                response += _summary(state)

    elif phase == 'completed':
        if 'restart' in msg.lower():
            state = new_state()
            role_list = '\n'.join([f'{i+1}. {r}' for i, r in enumerate(roles)])
            response = f'New Interview Session!\n\nChoose your role:\n{role_list}'
        else:
            response = 'Interview complete. Type **restart** to begin a new session.'

    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": response})
    return history, state

def start_session():
    state = new_state()
    roles = list(QUESTION_BANK.keys())
    role_list = '\n'.join([f'{i+1}. {r}' for i, r in enumerate(roles)])
    welcome = (
        'Welcome to your personal AI Interview Coach!\n\n'
        'I will ask you 5 interview questions and give detailed feedback on each answer. '
        'If you run into an answer you don\'t know, just type **"I don\'t know"** and I will explain the concept to help you learn.\n\n'
        '**Choose your interview role by typing the number:**\n\n'
        + role_list
    )
    history = [{"role": "assistant", "content": welcome}]
    return history, state

# =====================================================================
# 4. INTERFACE LAYOUT (Gradio 6.0+ Compliant)
# =====================================================================
css = """
.gradio-container { max-width: 860px; margin: auto; }
footer { display: none !important; }
"""

with gr.Blocks(title='AI Interview Coach') as demo:

    gr.HTML("""
        <div style='text-align:center; padding: 10px 0'>
            <h1 style='font-size:2em; margin:0'>🤖 AI Interview Coach</h1>
            <p style='color:#666; margin:4px 0'>Practice interviews with an encouraging local mentor | Fast CPU Mode</p>
        </div>
    """)

    state = gr.State(None)
    chatbot = gr.Chatbot(label='Interview Session', height=500) 

    with gr.Row():
        msg = gr.Textbox(
            placeholder='Type your answer here, or say "I don\'t know" for assistance...',
            label='', scale=5, lines=2
        )
        send_btn = gr.Button('Send', scale=1, variant='primary')

    with gr.Row():
        restart_btn = gr.Button('New Interview', scale=1)
        clear_btn = gr.Button('Clear Chat', scale=1)

    def respond(message, history, state):
        if not message.strip():
            return history, '', state
        history, state = chat(message, history, state)
        return history, '', state

    def restart(state):
        history, state = start_session()
        return history, '', state

    msg.submit(respond, [msg, chatbot, state], [chatbot, msg, state])
    send_btn.click(respond, [msg, chatbot, state], [chatbot, msg, state])
    restart_btn.click(restart, [state], [chatbot, msg, state])
    clear_btn.click(lambda: ([], ''), outputs=[chatbot, msg])
    demo.load(restart, [state], [chatbot, msg, state])

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1", 
        server_port=None,  # <-- Changing this to None fixes the blocked port error permanently!
        share=False,
        theme=gr.themes.Soft(),
        css=css
    )
    