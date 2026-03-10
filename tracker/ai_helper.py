import os
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def generate_question(topic, role, difficulty):
    aptitude_topics = [
        'Permutation & Combination', 'Ratio & Proportion', 'Time Speed Distance',
        'Boats & Streams', 'Profit & Loss', 'Time & Work', 'Age Problems',
        'Percentages', 'Simple & Compound Interest', 'Number Series'
    ]

    if topic in aptitude_topics:
        prompt = f"""
Generate 1 aptitude MCQ question for the topic: {topic}
Difficulty: {difficulty}

Format your response EXACTLY like this:
Question: [question text with numbers]
A) [option A]
B) [option B]
C) [option C]
D) [option D]
Answer: [correct option letter]
Explanation: [brief explanation of solution]
Hint: [solving approach in one line]
"""
    else:
        prompt = f"""
Generate 1 interview question for:
- Role: {role}
- Topic: {topic}
- Difficulty: {difficulty}

Format your response as:
Question: [the question]
Hint: [a small hint]
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def analyze_answer(question, answer):
    prompt = f"""
You are an expert interviewer. Analyze this answer:

Question: {question}
Candidate's Answer: {answer}

Provide:
1. Score out of 10
2. What was good
3. What needs improvement
4. Model answer in 2-3 lines
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def generate_mock_interview(role, num_questions, topics):
    prompt = f"""
Generate {num_questions} interview questions for a {role} interview.
Topics to cover: {', '.join(topics) if topics else 'Mixed topics including technical and behavioral'}.

Mix difficulty levels. Include both technical and behavioral questions.

Return ONLY a JSON array like this:
[
    {{"question": "question text here", "topic": "topic name", "difficulty": "Easy/Medium/Hard", "type": "technical/behavioral"}},
    ...
]
Return only the JSON array, nothing else.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    import json
    try:
        content = response.choices[0].message.content
        start = content.find('[')
        end = content.rfind(']') + 1
        return json.loads(content[start:end])
    except:
        return [{"question": "Tell me about yourself", "topic": "Behavioral", "difficulty": "Easy", "type": "behavioral"}]


def generate_aptitude_mcq(topic, difficulty, num=5):
    prompt = f"""
Generate {num} aptitude MCQ questions for topic: {topic}
Difficulty: {difficulty}

Return ONLY a JSON array, no other text:
[
  {{
    "question": "question text with numbers",
    "options": {{"A": "option1", "B": "option2", "C": "option3", "D": "option4"}},
    "answer": "A",
    "explanation": "step by step solution",
    "hint": "key formula or approach"
  }}
]
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    import json
    try:
        content = response.choices[0].message.content
        start = content.find('[')
        end = content.rfind(']') + 1
        return json.loads(content[start:end])
    except:
        return []
