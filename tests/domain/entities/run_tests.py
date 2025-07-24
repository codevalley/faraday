"""Run domain entity tests directly without loading the full test suite."""

import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Import the test modules
from tests.domain.entities.test_thought import *
from tests.domain.entities.test_semantic_entry import *
from tests.domain.entities.test_user import *
from tests.domain.entities.test_search_query import *

if __name__ == '__main__':
    unittest.main()