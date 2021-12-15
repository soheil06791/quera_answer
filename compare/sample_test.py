import unittest
from solution import compare
print(compare)

class Test(unittest.TestCase):

	def test_upper_1(self):
		self.assertEqual('las', compare('ali', 'salib'))

	def test_upper_2(self):
		self.assertEqual('Both strings are empty!', compare('nima', 'amin'))



if __name__ == '__main__':
    unittest.main()
