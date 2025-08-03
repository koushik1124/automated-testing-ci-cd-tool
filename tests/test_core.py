import unittest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.main import process_data, validate_input

class TestCoreFunctions(unittest.TestCase):
    
    def test_process_data_valid(self):
        """Test processing valid data."""
        sample_data = {"name": "Test Sample", "value": 42}
        result = process_data(sample_data)
        self.assertEqual(result["status"], "success")
        self.assertIn("processed_value", result)
    
    def test_process_data_invalid(self):
        """Test processing invalid data."""
        sample_data = {"name": "", "value": -1}
        with self.assertRaises(ValueError):
            process_data(sample_data)
    
    def test_validate_input_valid(self):
        """Test validating valid input."""
        sample_data = {"name": "Test Sample", "value": 42}
        self.assertTrue(validate_input(sample_data))
    
    def test_validate_input_invalid(self):
        """Test validating invalid input."""
        sample_data = {"name": "", "value": -1}
        self.assertFalse(validate_input(sample_data))

if __name__ == "__main__":
    unittest.main()
