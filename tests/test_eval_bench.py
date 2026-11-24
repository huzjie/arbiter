# -*- coding: utf-8 -*-
import unittest

from arbiter.eval.bench import bench_skill_sweep


class TestBench(unittest.TestCase):
    def test_sweep_rows(self):
        rows = bench_skill_sweep(steps=3)
        self.assertEqual(len(rows), 4)
        self.assertIn("skill", rows[0])
        self.assertIn("avg_cost_saved", rows[0])


if __name__ == "__main__":
    unittest.main()
