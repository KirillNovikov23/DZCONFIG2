import unittest
from unittest.mock import patch
from graph_builder import build_commit_graph

class TestBuildCommitGraph(unittest.TestCase):
    @patch("subprocess.check_output")
    def test_build_commit_graph(self, mock_subprocess):
        mock_subprocess.return_value = "a1b2c3d4 e5f6g7h8\na1b2c3d5\n"

        expected_graph = {
            "a1b2c3d4": ["e5f6g7h8"],
            "a1b2c3d5": []
        }

        graph = build_commit_graph("/fake/repo")
        self.assertEqual(graph, expected_graph)

if __name__ == "__main__":
    unittest.main()
