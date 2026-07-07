"""
Seed command to populate the database with demo data.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import SchoolInfo, Announcement, SchoolEvent
from teachers.models import Teacher
from students.models import Student
from academics.models import Subject, AcademicSession, Result
from accounts.models import UserProfile
from news.models import NewsPost
from gallery.models import GalleryCategory
import datetime


class Command(BaseCommand):
    help = 'Seed the database with initial demo data for LGEA Staff School Portal'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🏫 Seeding LGEA Staff School Portal...'))

        # ── School Info ──────────────────────────────────────────────────────
        info, _ = SchoolInfo.objects.get_or_create(pk=1)
        info.name = "L.G.E.A STAFF SCHOOL, KEFFI"
        info.tagline = "Nurturing Excellence in Every Child"
        info.address = "No. 1 School Road, Keffi, Nasarawa State, Nigeria"
        info.phone = "+234 813 456 7890"
        info.email = "info@lgeastaffschoolkeffi.edu.ng"
        info.established_year = "1985"
        info.about = (
            "L.G.E.A Staff School, Keffi is a government-owned primary school located in "
            "Keffi Local Government Area of Nasarawa State, Nigeria. Established in 1985, "
            "the school has been at the forefront of quality primary education, producing "
            "well-rounded graduates who go on to succeed in various fields. The school is "
            "managed by the Local Government Education Authority (L.G.E.A) and adheres to "
            "national educational standards set by the Universal Basic Education Commission (UBEC)."
        )
        info.vision = (
            "To be the leading primary school in Nasarawa State, producing academically "
            "excellent, morally upright, and socially responsible citizens."
        )
        info.mission = (
            "To provide a safe, inclusive, and stimulating learning environment where "
            "every child is given the opportunity to discover and develop their full potential "
            "through quality education, character formation, and extracurricular activities."
        )
        info.save()
        self.stdout.write('  ✔ School information updated')

        # ── Academic Session ─────────────────────────────────────────────────
        session, _ = AcademicSession.objects.get_or_create(
            session='2024/2025', term='Third',
            defaults={
                'start_date': datetime.date(2025, 4, 14),
                'end_date': datetime.date(2025, 7, 18),
                'is_current': True,
            }
        )
        self.stdout.write('  ✔ Academic session created')

        # ── Announcements ────────────────────────────────────────────────────
        announcements = [
            ('Third Term Begins April 14, 2025', 'All students are expected to resume on Monday, April 14, 2025 for the commencement of the Third Term. Parents should ensure fees are paid promptly.', 'high'),
            ('PTA Meeting — May 10, 2025', 'The Parent-Teacher Association meeting is scheduled for Saturday, May 10, 2025 at 10:00 AM. All parents are strongly encouraged to attend.', 'normal'),
            ('Annual Sports Day — June 6, 2025', 'The school Annual Sports Day will hold on Friday, June 6, 2025. Students should come with their house colours. Parents are welcome!', 'normal'),
            ('End of Year Examination — July 7–11, 2025', 'Third Term examinations will commence on July 7, 2025. Students should prepare adequately.', 'urgent'),
            ('Admission for 2025/2026 Now Open', 'Applications for admission into Nursery 1 and Primary 1 for the 2025/2026 academic session are now open. Visit the school office or apply online.', 'high'),
        ]
        for title, content, priority in announcements:
            Announcement.objects.get_or_create(title=title, defaults={'content': content, 'priority': priority})
        self.stdout.write('  ✔ Announcements created')

        # ── School Events ────────────────────────────────────────────────────
        events = [
            ('Annual Sports Day', 'The school annual inter-house sports competition featuring running, long jump, field events, and cultural dances.', datetime.date(2025, 6, 6), None, 'School Sports Field'),
            ('Parent-Teacher Meeting', 'Quarterly meeting between parents and teachers to discuss student progress and school development.', datetime.date(2025, 5, 10), None, 'School Hall'),
            ('End of Year Examination', 'Third Term examinations for all classes from Nursery 1 to Primary 6.', datetime.date(2025, 7, 7), datetime.date(2025, 7, 11), 'All Classrooms'),
            ('Prize Giving Day', 'Annual prize giving and valedictory ceremony for graduating Primary 6 students.', datetime.date(2025, 7, 18), None, 'School Hall'),
            ('Independence Day Celebration', 'School celebration of Nigeria\'s Independence Day with cultural dances and performances.', datetime.date(2025, 10, 1), None, 'School Assembly Ground'),
        ]
        for title, desc, start, end, loc in events:
            SchoolEvent.objects.get_or_create(title=title, start_date=start, defaults={
                'description': desc, 'end_date': end, 'location': loc
            })
        self.stdout.write('  ✔ School events created')

        # ── Admin User ───────────────────────────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@lgeastaffschoolkeffi.edu.ng',
                password='Admin@2025!',
                first_name='School',
                last_name='Administrator'
            )
            UserProfile.objects.create(user=admin, role='admin')
            self.stdout.write('  ✔ Admin user created (username: admin, password: Admin@2025!)')
        else:
            self.stdout.write('  ℹ Admin user already exists')

        # ── Teachers ─────────────────────────────────────────────────────────
        teachers_data = [
            ('Mrs. Simiatu', 'Raji', 'A.', 'Head Teacher', 'Administration', 'B.Ed', True, True, True, 0),
            ('Mr. Emmanuel', 'Okafor', 'Chukwu', 'Deputy Head Teacher', 'Administration', 'B.Ed', True, True, True, 1),
            ('Mrs. Aisha', 'Suleiman', 'Mohammed', 'Primary 6 Class Teacher', 'Upper Primary', 'NCE', False, True, True, 2),
            ('Mr. Usman', 'Yusuf', 'Garba', 'Primary 5 Class Teacher', 'Upper Primary', 'NCE', False, True, True, 3),
            ('Mrs. Grace', 'Adeyemi', 'Olawale', 'Primary 4 Class Teacher', 'Middle Primary', 'B.Ed', False, True, True, 4),
            ('Mr. John', 'Danladi', 'Musa', 'Primary 3 Class Teacher', 'Middle Primary', 'NCE', False, True, True, 5),
            ('Mrs. Blessing', 'Okeke', 'Eze', 'Primary 2 Class Teacher', 'Lower Primary', 'NCE', False, True, True, 6),
            ('Miss Hauwa', 'Abdullahi', 'Bello', 'Primary 1 Class Teacher', 'Lower Primary', 'NCE', False, True, True, 7),
            ('Mrs. Nkechi', 'Obi', 'Ikenna', 'Nursery Teacher', 'Nursery', 'NCE', False, True, True, 8),
            ('Mr. Sadiq', 'Abubakar', 'Hassan', 'ICT Teacher', 'Information Technology', 'B.Sc', False, True, True, 9),
            ('Mr. Peter', 'Atiku', '', 'School Bursar', 'Administration', 'B.Sc', True, False, False, 10),
            ('Mrs. Amina', 'Kwato', '', 'School Secretary', 'Administration', 'HND', True, False, False, 11),
        ]
        for first, last, middle, position, dept, qual, is_mgmt, is_active, is_teaching, order in teachers_data:
            Teacher.objects.get_or_create(
                first_name=first, last_name=last,
                defaults={
                    'middle_name': middle, 'position': position, 'department': dept,
                    'qualification': qual, 'is_management': is_mgmt, 'is_active': is_active,
                    'is_teaching': is_teaching, 'order': order,
                    'phone': '+234 800 000 0000', 'email': f"{first.lower().replace('mrs. ', '').replace('mr. ', '').replace('miss ', '')}.{last.lower()}@lgeastaffschoolkeffi.edu.ng"
                }
            )
        self.stdout.write('  ✔ Teachers created')

        # ── Subjects ─────────────────────────────────────────────────────────
        core_subjects = ['Mathematics', 'English Language', 'Basic Science', 'Social Studies',
                         'Civic Education', 'Christian Religious Studies', 'Islamic Religious Studies',
                         'Agricultural Science', 'Physical & Health Education', 'Cultural & Creative Arts',
                         'Computer Studies', 'Hausa Language', 'Yoruba Language']
        classes = ['Nursery 1', 'Nursery 2', 'Primary 1', 'Primary 2', 'Primary 3',
                   'Primary 4', 'Primary 5', 'Primary 6']
        nursery_subjects = ['Number Work', 'Literacy', 'Rhymes & Songs', 'Arts & Craft',
                            'Physical Education', 'Social Habit']
        for cls in classes:
            if 'Nursery' in cls:
                subj_list = nursery_subjects
            elif cls in ['Primary 1', 'Primary 2', 'Primary 3']:
                subj_list = core_subjects[:8]
            else:
                subj_list = core_subjects
            for subj in subj_list:
                cls_parts = cls.split()
                cls_code = f"{cls_parts[0][:3].upper()}{cls_parts[1] if len(cls_parts) > 1 else ''}"
                code = f"{cls_code}{subj[:3].upper()}"
                Subject.objects.get_or_create(
                    name=subj, class_level=cls,
                    defaults={'code': code[:10]}
                )
        self.stdout.write('  ✔ Subjects created')

        # ── Students ─────────────────────────────────────────────────────────
        students_data = [
            ('Ahmed', 'Musa', 'Bello', 'M', '2015-03-12', 'Primary 6', 'Mr. Bello Musa', '+234 803 111 1111'),
            ('Fatima', 'Abubakar', 'Sani', 'F', '2015-07-25', 'Primary 6', 'Mr. Abubakar Sani', '+234 803 222 2222'),
            ('Chukwuemeka', 'Okafor', 'Eze', 'M', '2016-01-18', 'Primary 5', 'Mr. Okafor Eze', '+234 803 333 3333'),
            ('Ngozi', 'Adeyemi', 'Olawale', 'F', '2016-09-05', 'Primary 5', 'Dr. Adeyemi Olawale', '+234 803 444 4444'),
            ('Ibrahim', 'Yusuf', 'Garba', 'M', '2017-04-22', 'Primary 4', 'Mr. Yusuf Garba', '+234 803 555 5555'),
            ('Blessing', 'Nwosu', 'Chisom', 'F', '2017-11-30', 'Primary 4', 'Mrs. Nwosu Chisom', '+234 803 666 6666'),
            ('Usman', 'Danladi', 'Mohammed', 'M', '2018-06-14', 'Primary 3', 'Mr. Danladi Mohammed', '+234 803 777 7777'),
            ('Amina', 'Hassan', 'Kwato', 'F', '2018-02-08', 'Primary 3', 'Mr. Hassan Kwato', '+234 803 888 8888'),
            ('Emmanuel', 'Okeke', 'Nkechi', 'M', '2019-08-19', 'Primary 2', 'Mr. Okeke Nkechi', '+234 803 999 9999'),
            ('Hauwa', 'Abdullahi', 'Bello', 'F', '2019-12-03', 'Primary 1', 'Mr. Abdullahi Bello', '+234 803 000 0000'),
        ]
        for first, last, middle, gender, dob, cls, parent, phone in students_data:
            Student.objects.get_or_create(
                first_name=first, last_name=last,
                defaults={
                    'middle_name': middle, 'gender': gender,
                    'date_of_birth': datetime.date.fromisoformat(dob),
                    'current_class': cls, 'parent_name': parent,
                    'parent_phone': phone, 'home_address': 'Keffi, Nasarawa State, Nigeria'
                }
            )
        self.stdout.write('  ✔ Students created')

        # ── News Posts ───────────────────────────────────────────────────────
        news_items = [
            ('School Wins State Academic Excellence Award 2024',
             'We are proud to announce that L.G.E.A Staff School, Keffi has won the State Academic Excellence Award for outstanding performance in the 2024 Primary School Leaving Examination.',
             'achievement', True),
            ('New Computer Laboratory Commissioned',
             'The school\'s newly equipped computer laboratory has been commissioned by the Local Government Education Authority. The lab features 20 modern computers for student use.',
             'news', False),
            ('Admission for 2025/2026 Session Open',
             'Applications for admission into Nursery 1 and Primary 1 for the 2025/2026 academic session are now open. Interested parents should visit the school office or apply online.',
             'announcement', True),
            ('Annual Sports Day Results',
             'Red House emerged champion at the 2024 Annual Inter-House Sports Competition with 85 points. Blue House came second with 72 points, Green House third with 68 points.',
             'event', False),
            ('Primary 6 Students Excel in NABTEB Mock',
             'Twenty-five Primary 6 students participated in the NABTEB mock examination, with 90% scoring above average in Mathematics and English Language.',
             'achievement', False),
        ]
        for title, content, category, featured in news_items:
            NewsPost.objects.get_or_create(
                title=title,
                defaults={'content': content, 'category': category, 'is_featured': featured, 'is_published': True}
            )
        self.stdout.write('  ✔ News posts created')

        # ── Gallery Categories ───────────────────────────────────────────────
        gallery_cats = [
            ('Sports & Athletics', 'sports-athletics', 'Sports events and athletic competitions'),
            ('Academic Activities', 'academic-activities', 'Classroom and academic activities'),
            ('Cultural Events', 'cultural-events', 'Cultural dances, drama, and performances'),
            ('School Facilities', 'school-facilities', 'School buildings and facilities'),
        ]
        for name, slug, desc in gallery_cats:
            GalleryCategory.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
        self.stdout.write('  ✔ Gallery categories created')

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write(self.style.WARNING('\n🔐 Login Credentials:'))
        self.stdout.write('   Admin:   username=admin  password=Admin@2025!')
        self.stdout.write('   Access the admin panel at: http://127.0.0.1:8000/admin/')
        self.stdout.write('   View the portal at:        http://127.0.0.1:8000/')
