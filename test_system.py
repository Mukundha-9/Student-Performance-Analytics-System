# ==============================================================================
# Automated System Verification Test Suite
# Tests NumPy statistical math, Pandas CRUD, Matplotlib exports, and Flask endpoints
# ==============================================================================
import unittest
import os
import pandas as pd
import numpy as np
from config import SUBJECTS, DEFAULT_CSV_PATH, REPORTS_DIR
import sample_data
import data_manager
import analytics
import visualizer
import generate_report
from app import app


class TestStudentAnalyticsSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = sample_data.generate_sample_dataset(n_students=60, seed=42)

    def test_01_dataset_integrity(self):
        self.assertFalse(self.df.empty)
        self.assertIn('Student_ID', self.df.columns)
        self.assertIn('Name', self.df.columns)
        self.assertIn('Attendance', self.df.columns)
        for sub in SUBJECTS:
            self.assertIn(sub, self.df.columns)
        self.assertIn('Percentage', self.df.columns)
        self.assertIn('Grade', self.df.columns)
        self.assertIn('Status', self.df.columns)

    def test_02_numpy_overall_stats(self):
        stats = analytics.compute_overall_statistics(self.df)
        self.assertEqual(stats['total_students'], len(self.df))
        self.assertTrue(0 <= stats['mean_percentage'] <= 100)
        self.assertTrue(stats['min_percentage'] <= stats['max_percentage'])
        self.assertTrue(0 <= stats['q1'] <= stats['q2'] <= stats['q3'] <= 100)
        self.assertIn('topper', stats)

    def test_03_numpy_correlation_and_regression(self):
        corr = analytics.compute_attendance_correlation(self.df)
        self.assertTrue(-1.0 <= corr['r'] <= 1.0)
        self.assertTrue(0.0 <= corr['r_squared'] <= 1.0)
        self.assertIn('Percentage =', corr['equation'])

    def test_04_pandas_crud(self):
        df_copy = self.df.copy()
        new_student = {
            'Student_ID': 'TEST-999',
            'Name': 'Test Student',
            'Gender': 'Male',
            'Branch': 'Computer Science & Engineering',
            'Semester': 'Semester 4',
            'Attendance': 95.0,
            'Mathematics': 85.0,
            'Physics': 90.0,
            'Python_Programming': 95.0,
            'Data_Structures': 88.0,
            'English': 92.0
        }
        updated_df, ok, msg = data_manager.add_student(df_copy, new_student)
        self.assertTrue(ok)
        self.assertEqual(len(updated_df), len(df_copy) + 1)

        # Update
        updated_df2, ok2, _ = data_manager.update_student(updated_df, 'TEST-999', {'Attendance': 98.0})
        self.assertTrue(ok2)

        # Delete
        final_df, ok3, _ = data_manager.delete_student(updated_df2, 'TEST-999')
        self.assertTrue(ok3)
        self.assertEqual(len(final_df), len(df_copy))

    def test_05_matplotlib_visualizations(self):
        files = visualizer.save_all_visualizations(self.df)
        self.assertEqual(len(files), 7)
        for f in files:
            self.assertTrue(os.path.exists(f))
            self.assertGreater(os.path.getsize(f), 5000)

    def test_06_report_generation(self):
        report_path = generate_report.generate_academic_report(self.df)
        self.assertTrue(os.path.exists(report_path))
        with open(report_path, 'r', encoding='utf-8') as f:
            text = f.read()
        self.assertIn('ADITYA UNIVERSITY', text)
        self.assertIn('KALYANAM MUKUNDHA', text)

    def test_07_flask_api_endpoints(self):
        client = app.test_client()
        res = client.get('/api/summary')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('overall', data)
        self.assertIn('subject_stats', data)

        res2 = client.get('/api/students?page=1&page_size=5')
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(len(res2.get_json()['records']), 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
