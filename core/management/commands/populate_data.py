from django.core.management.base import BaseCommand
from core.models import Faculty, LogisticsSession, EnrollmentFee, CurriculumPhase, CurriculumSection, PracticumProject

class Command(BaseCommand):
    help = 'Populate database with initial data from original frontend design'

    def handle(self, *args, **options):
        self.stdout.write('Populating database with initial data...')

        # Clear existing data
        Faculty.objects.all().delete()
        LogisticsSession.objects.all().delete()
        EnrollmentFee.objects.all().delete()
        CurriculumPhase.objects.all().delete()
        PracticumProject.objects.all().delete()

        # Populate Faculty
        self.stdout.write('Creating faculty...')
        faculty_data = [
            {
                'name': 'Puvvada Sai Pridhvi Raj',
                'initials': 'PR',
                'title': 'Lead AI Engineer',
                'bio': 'Expert in building and deploying production-grade LLM architectures and RAG pipelines.',
                'linkedin': '',
                'skills': 'Transformers, NLP, Agentic AI Orchestration, RAG, LLMs'
            },
            {
                'name': 'Ramrohith Gadi',
                'initials': 'RG',
                'title': 'AI Lead Engineer',
                'bio': 'Specialist in hybrid architectures combining robust Backend systems with Generative AI implementation.',
                'linkedin': '',
                'skills': 'AI Orchestration, Backend Engineering, FastAPI, Gen AI Implementation, System Design'
            },
            {
                'name': 'Narendra Golla',
                'initials': 'NG',
                'title': 'Senior AI Engineer',
                'bio': 'Engineering expert focusing on specialized Generative AI solutions and distributed systems architecture.',
                'linkedin': '',
                'skills': 'Gen AI Engineering, Distributed Systems, Agentic Swarms, Scalable Backend, Prompt Eng'
            }
        ]

        for data in faculty_data:
            Faculty.objects.create(**data)

        # Populate Logistics Sessions
        self.stdout.write('Creating logistics sessions...')
        logistics_data = [
            {
                'title': 'Saturday Technical Deep Dive',
                'description': 'Rigorous architectural theory focusing on Transformer mechanics and attention logic.',
                'order': 1
            },
            {
                'title': 'Sunday Implementation Lab',
                'description': 'Code-intensive lab sessions focusing on RAG optimization and Agentic state management.',
                'order': 2
            }
        ]

        for data in logistics_data:
            LogisticsSession.objects.create(**data)

        # Populate Enrollment Fee
        self.stdout.write('Creating enrollment fee...')
        EnrollmentFee.objects.create(
            currency_inr=50000,
            currency_usd=600,
            details='1-on-1 GenAI Expert Mentorship, 8 Graded Production Assignments, 4 Production-Grade Capstones'
        )

        # Populate Curriculum Phases
        self.stdout.write('Creating curriculum phases...')
        curriculum_data = [
            {
                'title': 'GenAI Infrastructure & Python Execution Engine',
                'order': 1,
                'description': 'Develop a thread-safe, asynchronous batch processor that bypasses the GIL for CPU-intensive tokenization tasks.',
                'sections': [
                    {
                        'name': 'Python for LLM Services',
                        'topics': 'Data Structures for Token Streams, High-Level OOP for Model Pipelines, Exception Handling in Model Invocations'
                    },
                    {
                        'name': 'Execution Optimization',
                        'topics': 'Global Interpreter Lock (GIL) & Memory Management, Thread/Process Pool Executors for Heavy Inference, Asyncio for High-Throughput GenAI APIs'
                    },
                    {
                        'name': 'Performance Patterns',
                        'topics': 'Decorators for LLM Tracing, Generators for Streaming Text Outputs, Memory Leak Prevention in Long-Running Agents'
                    }
                ]
            },
            {
                'title': 'Productionizing GenAI: FastAPI Specialization',
                'order': 2,
                'description': '',
                'sections': []
            },
            {
                'title': 'Vector Theory & Semantic Intelligence',
                'order': 3,
                'description': '',
                'sections': []
            },
            {
                'title': 'Transformer Architecture & LLM Mechanics',
                'order': 4,
                'description': '',
                'sections': []
            },
            {
                'title': 'RAG Engineering & Advanced Retrieval',
                'order': 5,
                'description': '',
                'sections': []
            },
            {
                'title': 'RAG Evaluation & Efficiency Protocols',
                'order': 6,
                'description': '',
                'sections': []
            },
            {
                'title': 'Fine-Tuning & PyTorch Specialization',
                'order': 7,
                'description': '',
                'sections': []
            },
            {
                'title': 'Agentic AI & LangGraph Orchestration',
                'order': 8,
                'description': '',
                'sections': []
            }
        ]

        for phase_data in curriculum_data:
            sections = phase_data.pop('sections')
            phase = CurriculumPhase.objects.create(**phase_data)

            for section_data in sections:
                CurriculumSection.objects.create(phase=phase, **section_data)

        # Populate Practicum Projects
        self.stdout.write('Creating practicum projects...')
        projects_data = [
            {
                'title': 'Enterprise Hybrid RAG System',
                'icon': '🔍',
                'description': 'Advanced document intelligence system featuring semantic indexing, hybrid retrieval with reranking, and rigorous automated evaluation metrics for generation faithfulness.',
                'tags': 'ChromaDB, Hybrid Search, RAGAS',
                'order': 1
            },
            {
                'title': 'ShopGenie: Personalized Commerce Agent',
                'icon': '🛍️',
                'description': 'An autonomous commerce assistant that researches products, compares real-time pricing, and manages virtual carts using sophisticated tool-calling and web-search capabilities.',
                'tags': 'LangChain Tools, Tavily Search, Function Calling',
                'order': 2
            },
            {
                'title': 'Capstone: Collaborative Multi-Agent',
                'icon': '📡',
                'description': 'Architecting a supervisor-worker hierarchy for complex problem decomposition, persistent state management, and real-time observability via the Model Context Protocol (MCP).',
                'tags': 'LangGraph, Stateful Graphs, Langfuse',
                'order': 3
            },
            {
                'title': 'Grocery Management Agentic System',
                'icon': '🛒',
                'description': 'A multi-agent swarm system designed to manage real-time inventory, handle grocery logistics, and orchestrate restocking through autonomous coordination nodes.',
                'tags': 'Pydantic AI, Swarm Logic, Async Pipelines',
                'order': 4
            }
        ]

        for data in projects_data:
            PracticumProject.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully populated database with initial data!'))
        self.stdout.write(f'Created {Faculty.objects.count()} faculty members')
        self.stdout.write(f'Created {LogisticsSession.objects.count()} logistics sessions')
        self.stdout.write(f'Created {EnrollmentFee.objects.count()} enrollment fee entries')
        self.stdout.write(f'Created {CurriculumPhase.objects.count()} curriculum phases')
        self.stdout.write(f'Created {CurriculumSection.objects.count()} curriculum sections')
        self.stdout.write(f'Created {PracticumProject.objects.count()} practicum projects')