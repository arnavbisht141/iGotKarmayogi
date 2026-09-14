import unittest
from app.modules.digital_governance.services.scenario_service import (
    ScenarioRepository, ScenarioSessionManager
)

class TestDigitalGovernanceScenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ScenarioRepository.initialize_scenarios()

    def test_01_all_five_domains_represented(self):
        scenarios = ScenarioRepository.list_scenarios()
        self.assertEqual(len(scenarios), 5, f"Expected 5 scenarios, got {len(scenarios)}")
        domains = {s.domain for s in scenarios}
        expected_domains = {
            "Cybersecurity",
            "Data Privacy",
            "Digital Signatures",
            "Government Cloud",
            "Digital Public Infrastructure"
        }
        self.assertEqual(domains, expected_domains)

    def test_02_scenario_session_lifecycle_and_branching(self):
        # Start session on Treasury Ransomware
        session = ScenarioSessionManager.start_session("dg-sec-01-ransomware-treasury")
        self.assertIsNotNone(session.session_id)
        self.assertEqual(session.current_question.id, "s1_q1_containment")
        self.assertEqual(session.compliance_score, 50)

        # Step 1: Optimal network isolation
        res1 = ScenarioSessionManager.submit_answer(session.session_id, "s1_q1_opt_a")
        self.assertFalse(res1.is_terminal)
        self.assertEqual(res1.compliance_score, 80)
        self.assertEqual(res1.next_question.id, "s1_q2_certin")

        # Step 2: Optimal CERT-In 6-hour reporting
        res2 = ScenarioSessionManager.submit_answer(session.session_id, "s1_q2_opt_a")
        self.assertFalse(res2.is_terminal)
        self.assertEqual(res2.compliance_score, 100)
        self.assertEqual(res2.next_question.id, "s1_q3_recovery")

        # Step 3: Optimal air-gap recovery and Section 65B certification
        res3 = ScenarioSessionManager.submit_answer(session.session_id, "s1_q3_opt_a")
        self.assertTrue(res3.is_terminal)
        self.assertEqual(res3.compliance_score, 100)
        self.assertIsNotNone(res3.session_summary)
        self.assertTrue(res3.session_summary.resolved_satisfactorily)
        self.assertEqual(len(res3.session_summary.decision_trail), 3)

    def test_03_suboptimal_path_handling(self):
        # Start session on Data Privacy Cloud Breach
        session = ScenarioSessionManager.start_session("dg-priv-02-dbt-cloud-breach")
        
        # Select suboptimal choice in step 1 (ignoring breach)
        res1 = ScenarioSessionManager.submit_answer(session.session_id, "s2_q1_opt_b")
        self.assertFalse(res1.is_terminal)
        self.assertEqual(res1.compliance_score, 15)  # 50 - 35
        self.assertFalse(res1.selected_option.is_optimal)

    def test_04_session_summary_retrieval(self):
        session = ScenarioSessionManager.start_session("dg-pki-03-gem-tender-dispute")
        res1 = ScenarioSessionManager.submit_answer(session.session_id, "s3_q1_opt_a")
        res2 = ScenarioSessionManager.submit_answer(session.session_id, "s3_q2_opt_a")
        res3 = ScenarioSessionManager.submit_answer(session.session_id, "s3_q3_opt_a")
        self.assertTrue(res3.is_terminal)

        summary = ScenarioSessionManager.get_session_summary(session.session_id)
        self.assertIsNotNone(summary)
        self.assertEqual(summary.scenario_id, "dg-pki-03-gem-tender-dispute")
        self.assertEqual(summary.total_steps, 3)
        self.assertEqual(summary.optimal_steps, 3)

if __name__ == "__main__":
    unittest.main()
