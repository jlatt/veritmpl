if __name__ == '__main__':
    import os
    import sys
    import unittest


    sys.path.insert(0, '.')
    file_dir = os.path.dirname(__file__)
    def gen_test_suites():
        for entry in os.listdir(file_dir):
            if entry.endswith('_tests.py'):
                module_name = entry.rsplit('.', 1)[0]
                module = __import__(module_name)
                yield unittest.defaultTestLoader.loadTestsFromModule(module)
    all_suite = unittest.TestSuite(gen_test_suites())
    unittest.TextTestRunner(verbosity=2).run(all_suite)
