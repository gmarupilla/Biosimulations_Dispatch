import unittest
from biosimulations_dispatch.sbatch.templates.vcell_template import VCellTemplate, template_string as ts


class TestVcellTemplate(unittest.TestCase):
    """Test for the class VCELL Template"""
    def test_fill_values(self):
        """Test for fill values for SLURM sbatch manager"""

        value_dict1 = {
            'id': '2134254',
            'tempDir': '/usr/vcell/12345321/2134254',
            'jobhookURL': 'https://localhost:5000/simulations',
            'owner': '12345321'
        }
        value_dict2 = {
            'id': '213741',
            'tempDir': '/usr/vcell/123478952/213741',
            'jobhookURL': 'https://localhost:5000/simulations',
            'owner': '123478952'
        }
        value_dict3 = {
            'id': '213854',
            'tempDir': '/usr/vcell/12387452/213854',
            'jobhookURL': 'https://localhost:5000/simulations',
            'owner': '12387452'
        }
        value_dict4 = {
            'id': '216958',
            'tempDir': '/usr/vcell/123485412/216958',
            'jobhookURL': 'https://localhost:5000/simulations',
            'owner': '123485412'
        }

        test_template_string1 = ts.format(**value_dict1)
        test_template_string2 = ts.format(**value_dict2)
        test_template_string3 = ts.format(**value_dict3)
        test_template_string4 = ts.format(**value_dict4)

        vcell_test1 = VCellTemplate().fill_values(value_dict1)
        vcell_test2 = VCellTemplate().fill_values(value_dict2)
        vcell_test3 = VCellTemplate().fill_values(value_dict3)
        vcell_test4 = VCellTemplate().fill_values(value_dict4)

        self.assertEqual(test_template_string1, vcell_test1)
        self.assertEqual(test_template_string2, vcell_test2)
        self.assertEqual(test_template_string3, vcell_test3)
        self.assertEqual(test_template_string4, vcell_test4)
