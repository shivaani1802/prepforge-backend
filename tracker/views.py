from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Topic, Question, UserProgress
from .serializers import TopicSerializer, QuestionSerializer, UserProgressSerializer
from .ai_helper import generate_question, analyze_answer, generate_mock_interview, generate_aptitude_mcq

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer

@api_view(['POST'])
def generate_ai_question(request):
    topic = request.data.get('topic', 'Arrays')
    role = request.data.get('role', 'SDE')
    difficulty = request.data.get('difficulty', 'Easy')
    question = generate_question(topic, role, difficulty)
    return Response({'question': question})

@api_view(['POST'])
def analyze_ai_answer(request):
    question = request.data.get('question', '')
    answer = request.data.get('answer', '')
    feedback = analyze_answer(question, answer)
    return Response({'feedback': feedback})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_progress(request):
    topic_name = request.data.get('topic')
    score = request.data.get('score', 0)
    try:
        topic = Topic.objects.get(name=topic_name)
        progress, created = UserProgress.objects.update_or_create(
            user=request.user,
            topic=topic,
            defaults={'score': score, 'completed': score >= 5}
        )
        return Response({'message': 'Progress saved!'})
    except Topic.DoesNotExist:
        return Response({'error': 'Topic not found'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_progress(request):
    progress = UserProgress.objects.filter(user=request.user)
    data = []
    for p in progress:
        data.append({
            'topic': p.topic.name,
            'score': p.score,
            'completed': p.completed,
            'attempted_at': p.attempted_at,
        })
    return Response(data)

@api_view(['POST'])
def mock_interview(request):
    role = request.data.get('role', 'SDE')
    num_questions = request.data.get('num_questions', 5)
    topics = request.data.get('topics', [])
    questions = generate_mock_interview(role, num_questions, topics)
    return Response({'questions': questions})

@api_view(['GET'])
def hot_topics(request):
    data = {
        'trending': [
            {'topic': 'Dynamic Programming', 'frequency': 95, 'difficulty': 'Hard', 'role': 'SDE'},
            {'topic': 'System Design', 'frequency': 92, 'difficulty': 'Hard', 'role': 'SDE'},
            {'topic': 'Arrays & Strings', 'frequency': 90, 'difficulty': 'Easy', 'role': 'SDE'},
            {'topic': 'SQL Joins', 'frequency': 88, 'difficulty': 'Medium', 'role': 'DA'},
            {'topic': 'Trees & Graphs', 'frequency': 85, 'difficulty': 'Medium', 'role': 'SDE'},
            {'topic': 'Product Metrics', 'frequency': 83, 'difficulty': 'Medium', 'role': 'PM'},
             
        ],
    
        'companies': {
            'Google': [
                'Design a URL shortener like bit.ly',
                'Find the longest substring without repeating characters',
                'Design Google Search autocomplete',
                'Implement LRU Cache',
                'Find all permutations of a string',
            ],
            'Amazon': [
                'Tell me about a time you showed leadership (Leadership Principles)',
                "Design Amazon's recommendation system",
                'Two Sum problem variations',
                'Design a parking lot system',
                'Serialize and deserialize a binary tree',
            ],
            'Microsoft': [
                'Reverse a linked list',
                'Design a chat application like Teams',
                'Find the median of two sorted arrays',
                'Implement a stack using queues',
                'Design an elevator system',
            ],
            'Meta': [
                'Design Facebook News Feed',
                'Clone a graph',
                'Design Instagram Stories',
                'Find connected components in a graph',
                'Design a notification system',
            ],
        },
        'most_asked': [
            {'question': 'Two Sum', 'company': 'Google, Amazon, Meta', 'difficulty': 'Easy', 'topic': 'Arrays'},
            {'question': 'Reverse a Linked List', 'company': 'Microsoft, Amazon', 'difficulty': 'Easy', 'topic': 'Linked Lists'},
            {'question': 'LRU Cache', 'company': 'Google, Meta', 'difficulty': 'Medium', 'topic': 'Design'},
            {'question': 'Binary Tree Level Order Traversal', 'company': 'Amazon, Microsoft', 'difficulty': 'Medium', 'topic': 'Trees'},
            {'question': 'Design a URL Shortener', 'company': 'Google, Amazon', 'difficulty': 'Hard', 'topic': 'System Design'},
            {'question': 'Tell me about yourself', 'company': 'All Companies', 'difficulty': 'Easy', 'topic': 'Behavioral'},
            {'question': 'Longest Palindromic Substring', 'company': 'Amazon, Meta', 'difficulty': 'Medium', 'topic': 'Strings'},
            {'question': 'Design Twitter', 'company': 'Meta, Google', 'difficulty': 'Hard', 'topic': 'System Design'},
        ]
    }
    
    return Response(data)
@api_view(['POST'])
def generate_aptitude_question(request):
        topic = request.data.get('topic', 'Ratio & Proportion')
        difficulty = request.data.get('difficulty', 'Medium')
        num = request.data.get('num', 5)
        questions = generate_aptitude_mcq(topic, difficulty, num)
        return Response({'questions': questions})

