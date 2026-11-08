"""Unit tests for verifiable-agent-trace-attestor."""
import unittest
from verifiable_agent_trace_attestor.attestor import VerifiableAgentTraceAttestor


class TestVerifiableAgentTraceAttestor(unittest.TestCase):
    def test_merkle_root_and_verification(self):
        att = VerifiableAgentTraceAttestor()
        h0 = att.record_step("step 0")
        h1 = att.record_step("step 1")
        h2 = att.record_step("step 2")
        h3 = att.record_step("step 3")

        root = att.compute_merkle_root()
        self.assertTrue(len(root) > 0)

        proof = att.generate_proof(2)
        self.assertTrue(att.verify_proof(h2, proof, root))
        # Tampered leaf should fail
        self.assertFalse(att.verify_proof("fake_hash", proof, root))
