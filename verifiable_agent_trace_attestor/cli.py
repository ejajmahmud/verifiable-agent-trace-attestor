"""CLI for verifiable-agent-trace-attestor."""
import sys
import argparse
from .attestor import VerifiableAgentTraceAttestor


def main():
    parser = argparse.ArgumentParser(description="Verifiable Agent Trace Attestor CLI")
    parser.add_argument("--demo", action="store_true", help="Run Merkle trace attestation demo")
    args = parser.parse_args()

    if args.demo:
        attestor = VerifiableAgentTraceAttestor()
        h0 = attestor.record_step("Turn 1: Read config.json")
        h1 = attestor.record_step("Turn 2: Execute safe test suite")
        h2 = attestor.record_step("Turn 3: Commit code modifications")

        root = attestor.compute_merkle_root()
        print(f"[+] Merkle Root Hash: {root}")

        proof = attestor.generate_proof(1)
        valid = attestor.verify_proof(h1, proof, root)
        print(f"[+] Proof Verification for Turn 2: {valid} (Cryptographically attested!)")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
