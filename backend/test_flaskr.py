import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:1234@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "What is the project name?", "answer": "trivia", "category": 1, "difficulty": 1}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["categories"])
        self.assertTrue(data["currentCategory"])

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_question_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": "World Cup"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]),2)
        self.assertTrue(data["totalQustions"],2)
        self.assertTrue(data["currentCategory"])

    def test_get_question_search_without_results(self):
            res = self.client().post("/questions", json={"searchTerm": "qwertyuytr"})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["questions"],[])
            self.assertEqual(data["totalQustions"],0)
            self.assertTrue(data["currentCategory"])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()