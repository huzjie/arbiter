# -*- coding: utf-8 -*-
import unittest

from arbiter.budget.account import BudgetAccount


class TestBudgetAccount(unittest.TestCase):
    def test_can_afford(self):
        b = BudgetAccount(max_cost=100)
        self.assertTrue(b.can_afford(50, 10))
        b.charge(50, 10)
        self.assertFalse(b.can_afford(60, 10))

    def test_reset(self):
        b = BudgetAccount(max_cost=10)
        b.charge(5, 1)
        b.reset()
        self.assertEqual(b.spent_cost, 0.0)


if __name__ == "__main__":
    unittest.main()
