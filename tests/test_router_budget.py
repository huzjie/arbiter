# -*- coding: utf-8 -*-
import unittest

from arbiter.router.base import Tier
from arbiter.router.budget import BudgetRouter
from arbiter.budget.account import BudgetAccount
from arbiter.deciders.mock import MockDecider
from arbiter.intents import INTENT_IDS


class TestBudgetRouter(unittest.TestCase):
    def test_budget_exhausted_stops_escalation(self):
        budget = BudgetAccount(max_cost=1)  # 只够 decider，不够 reasoner
        r = BudgetRouter([
            Tier("decider", MockDecider(skill=0.1), cost=1, latency_ms=5, threshold=0.85),
            Tier("reasoner", MockDecider(skill=1.0), cost=100, latency_ms=200),
        ], budget).route("随便说说", INTENT_IDS)
        self.assertEqual(r.tier, "decider")  # 预算耗尽，不再升级


if __name__ == "__main__":
    unittest.main()
