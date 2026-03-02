import unittest
from soal1_aritmatika import parse_expression
from soal2_suhu import convert_temp, classify_temp
from soal3_bilangan import decimal_to_base, base_to_decimal
from soal_bonus_ip import prefix_to_mask

class TestModularCalculator(unittest.TestCase):
    
    def test_soal1_arithmetic(self):
        res, _ = parse_expression("5 + 3 * 2 - 4 / 2")
        self.assertEqual(res, 9.0)

    def test_soal2_temperature(self):
        self.assertAlmostEqual(convert_temp(25, 'C', 'F'), 77.0)
        self.assertEqual(classify_temp(25), "Normal")

    def test_soal3_base_conversion(self):
        res, _ = decimal_to_base(45, 2)
        self.assertEqual(res, "101101")
        res, _ = base_to_decimal("FF", 16)
        self.assertEqual(res, 255)

    def test_bonus_ip(self):
        self.assertEqual(prefix_to_mask(24), "255.255.255.0")

if __name__ == '__main__':
    unittest.main()