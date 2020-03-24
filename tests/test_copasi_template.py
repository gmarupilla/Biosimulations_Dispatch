import unittest
from biosimulations_dispatch.sbatch.templates.copasi_template import CopasiTemplate, template_string as ts


class TestCopasiTemplate(unittest.TestCase):
    """Test for the class Copasi Template"""
    def test_fill_values(self):
        """Test for fill values for SLURM sbatch manager"""

        value_dict1 = {
            'id': '2134254',
            'tempDir': '/usr/copasi/12345321/2134254',
            'jobhookURL': 'https://localhost:5000/simulations',
            'owner': '12345321'
        }
        value_dict2 = {
            'id': '213741',
            'tempDir': '/usr/copasi/123478952/213741',
            'jobhookURL': 'https://localhost:5000/simulations',
            'owner': '123478952'
        }
        value_dict3 = {
            'id': '213854',
            'tempDir': '/usr/copasi/12387452/213854',
            'jobhookURL': 'https://localhost:5000/simulations',
            'owner': '12387452'
        }
        value_dict4 = {
            'id': '216958',
            'tempDir': '/usr/copasi/123485412/216958',
            'jobhookURL': 'https://localhost:5000/simulations',
            'owner': '123485412'
        }

        test_template_string1 = ts.format(**value_dict1)
        test_template_string2 = ts.format(**value_dict2)
        test_template_string3 = ts.format(**value_dict3)
        test_template_string4 = ts.format(**value_dict4)

        copasi_test1 = CopasiTemplate().fill_values(value_dict1)
        copasi_test2 = CopasiTemplate().fill_values(value_dict2)
        copasi_test3 = CopasiTemplate().fill_values(value_dict3)
        copasi_test4 = CopasiTemplate().fill_values(value_dict4)

        self.assertEqual(test_template_string1, copasi_test1)
        self.assertEqual(test_template_string2, copasi_test2)
        self.assertEqual(test_template_string3, copasi_test3)
        self.assertEqual(test_template_string4, copasi_test4)


if __name__ == "__main__":
    unittest.main()
