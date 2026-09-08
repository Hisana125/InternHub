from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from internships.models import Internship


class Command(BaseCommand):
    help = "Seeds realistic college internship openings for demonstrations and evaluation."

    def handle(self, *args, **options):
        today = timezone.now().date()

        sample_internships = [
            {
                'title': 'Python & Django Backend Intern',
                'company_name': 'InApp Information Technologies',
                'description': 'Join our web development engineering team to build scalable RESTful APIs, manage MySQL databases, and develop backend microservices using Python and Django. Interns will work alongside senior software engineers on live enterprise products.',
                'location': 'Kochi, Kerala',
                'duration': '3 Months',
                'stipend': '₹15,000 / month',
                'skills_required': 'Python, Django, MySQL, REST API, Git',
                'application_deadline': today + timedelta(days=30),
            },
            {
                'title': 'Full Stack Web Developer Intern',
                'company_name': 'UST Global',
                'description': 'Looking for proactive computer science and applications students to work on responsive frontend interfaces and backend integration. You will be responsible for creating modern UI components and integrating backend services.',
                'location': 'Thiruvananthapuram, Kerala',
                'duration': '6 Months',
                'stipend': '₹18,000 / month',
                'skills_required': 'HTML5, CSS3, JavaScript, Django, PostgreSQL',
                'application_deadline': today + timedelta(days=45),
            },
            {
                'title': 'Data Science & Machine Learning Intern',
                'company_name': 'Tata Consultancy Services (TCS)',
                'description': 'Assist data science teams in data collection, cleaning, feature engineering, and training predictive machine learning models using Scikit-Learn, Pandas, and TensorFlow for business intelligence applications.',
                'location': 'Bangalore, Karnataka',
                'duration': '4 Months',
                'stipend': '₹22,000 / month',
                'skills_required': 'Python, Pandas, NumPy, Scikit-Learn, SQL',
                'application_deadline': today + timedelta(days=25),
            },
            {
                'title': 'Cyber Security & Network Defense Intern',
                'company_name': 'CyberTech Solutions',
                'description': 'Participate in vulnerability assessments, security log analysis, and penetration testing simulation exercises. Learn standard cybersecurity protocols, firewall configuration, and compliance audit frameworks.',
                'location': 'Kochi, Kerala',
                'duration': '3 Months',
                'stipend': '₹14,000 / month',
                'skills_required': 'Linux, Network Security, Ethical Hacking, Wireshark',
                'application_deadline': today + timedelta(days=40),
            },
            {
                'title': 'Cloud & DevOps Engineering Intern',
                'company_name': 'Cognizant Technology Solutions',
                'description': 'Work with cloud infrastructure automation, Docker containerization, CI/CD pipeline deployment, and AWS cloud service management under the guidance of certified DevOps architects.',
                'location': 'Chennai, Tamil Nadu',
                'duration': '6 Months',
                'stipend': '₹20,000 / month',
                'skills_required': 'AWS, Docker, CI/CD, Git, Linux, Bash',
                'application_deadline': today + timedelta(days=60),
            },
            {
                'title': 'Flutter Mobile App Development Intern',
                'company_name': 'AppForge Studio',
                'description': 'Develop cross-platform Android and iOS mobile applications using Google Flutter framework and Dart. Integrate push notifications, offline caching, and REST APIs.',
                'location': 'Calicut, Kerala',
                'duration': '3 Months',
                'stipend': '₹12,000 / month',
                'skills_required': 'Flutter, Dart, Mobile UI, Firebase, REST APIs',
                'application_deadline': today + timedelta(days=35),
            },
            {
                'title': 'UI/UX Design & Frontend Intern',
                'company_name': 'Zoho Corporation',
                'description': 'Create user journeys, wireframes, and interactive mockups in Figma, and convert design systems into clean semantic HTML5, CSS3, and JavaScript components.',
                'location': 'Tenkasi, Tamil Nadu',
                'duration': '4 Months',
                'stipend': '₹16,000 / month',
                'skills_required': 'Figma, UI/UX, CSS Grid, Responsive Design, JavaScript',
                'application_deadline': today + timedelta(days=50),
            },
        ]

        created_count = 0
        for item in sample_internships:
            internship, created = Internship.objects.get_or_create(
                title=item['title'],
                company_name=item['company_name'],
                defaults=item
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"+ Created: {internship.title} at {internship.company_name}"))
            else:
                self.stdout.write(f"- Already exists: {internship.title}")

        self.stdout.write(self.style.SUCCESS(f"\nSuccessfully seeded {created_count} new internships!"))
