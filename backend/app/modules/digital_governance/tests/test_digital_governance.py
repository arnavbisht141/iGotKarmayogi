import json
import unittest
from app.core.database import SessionLocal
from app.models.models import Course, Assessment, Question, Lesson, Skill, CourseSkill

class TestDigitalGovernanceCurriculum(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = SessionLocal()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_01_course_metadata(self):
        course = self.db.query(Course).filter(
            Course.title == "Digital Governance, Cyber Defense & Public Digital Architecture"
        ).first()
        self.assertIsNotNone(course, "Course not found in database")
        self.assertEqual(course.category, "Digital Governance")
        self.assertEqual(course.organization, "National e-Governance Division (NeGD) & CERT-In")
        self.assertEqual(course.difficulty, "intermediate")
        self.assertEqual(course.rating, 4.96)
        self.assertEqual(len(course.modules), 5, f"Expected 5 modules, found {len(course.modules)}")

    def test_02_modules_and_in_lesson_activities(self):
        course = self.db.query(Course).filter(
            Course.title == "Digital Governance, Cyber Defense & Public Digital Architecture"
        ).first()
        self.assertIsNotNone(course)

        total_lessons = 0
        for module in course.modules:
            self.assertGreaterEqual(len(module.lessons), 2, f"Module {module.title} has fewer than 2 lessons")
            for lesson in module.lessons:
                total_lessons += 1
                self.assertIsNotNone(lesson.activity_question, f"Lesson {lesson.title} missing activity question")
                options = json.loads(lesson.activity_options_json)
                self.assertEqual(len(options), 4, f"Lesson {lesson.title} options must have 4 choices")
                self.assertTrue(0 <= lesson.activity_correct_option < 4)
                self.assertTrue(len(lesson.activity_explanation) > 15)

        self.assertEqual(total_lessons, 10, f"Expected exactly 10 lessons across 5 modules, got {total_lessons}")

    def test_03_certification_assessment_and_15_questions(self):
        course = self.db.query(Course).filter(
            Course.title == "Digital Governance, Cyber Defense & Public Digital Architecture"
        ).first()
        self.assertIsNotNone(course)

        assessment = self.db.query(Assessment).filter(Assessment.course_id == course.id).first()
        self.assertIsNotNone(assessment, "Assessment record missing")
        self.assertEqual(assessment.time_limit_minutes, 30)
        self.assertEqual(assessment.pass_threshold_percent, 70.0)
        self.assertEqual(len(assessment.questions), 15, f"Expected 15 questions, found {len(assessment.questions)}")

        # Validate all 15 questions
        for idx, q in enumerate(assessment.questions, start=1):
            self.assertEqual(q.order, idx)
            self.assertGreater(len(q.text), 20)
            opts = json.loads(q.options_json)
            self.assertEqual(len(opts), 4, f"Question {idx} must have 4 options")
            self.assertTrue(0 <= q.correct_option_index < 4)
            self.assertGreater(len(q.explanation), 20)

    def test_04_skills_association(self):
        course = self.db.query(Course).filter(
            Course.title == "Digital Governance, Cyber Defense & Public Digital Architecture"
        ).first()
        self.assertIsNotNone(course)

        expected_skills = {
            "Critical Infrastructure Cyber Defense & CERT-In Compliance",
            "Data Privacy Compliance & DPDP Act 2023",
            "Public Key Infrastructure (PKI) & Digital Signatures",
            "Government Cloud Architecture & MeghRaj Strategy",
            "Digital Public Infrastructure (DPI) & India Stack"
        }

        linked_skills = {cs.skill.name for cs in course.course_skills if cs.skill}
        self.assertTrue(expected_skills.issubset(linked_skills), f"Missing skills: {expected_skills - linked_skills}")

if __name__ == "__main__":
    unittest.main()

