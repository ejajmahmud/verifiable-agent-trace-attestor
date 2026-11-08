"""Core Verifiable Agent Trace Attestor implementation."""
import hashlib
from typing import List, Dict, Tuple, Optional, Any


class VerifiableAgentTraceAttestor:
    def __init__(self):
        self.leaves: List[str] = []

    def _hash(self, data: str) -> str:
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def record_step(self, step_data: str) -> str:
        h = self._hash(step_data)
        self.leaves.append(h)
        return h

    def compute_merkle_root(self) -> str:
        if not self.leaves:
            return ""
        current_level = list(self.leaves)
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i+1] if i + 1 < len(current_level) else left
                combined = self._hash(left + right)
                next_level.append(combined)
            current_level = next_level
        return current_level[0]

    def generate_proof(self, leaf_index: int) -> List[Tuple[str, str]]:
        """Returns list of (sibling_hash, direction) for inclusion proof."""
        if leaf_index < 0 or leaf_index >= len(self.leaves):
            return []

        proof: List[Tuple[str, str]] = []
        current_level = list(self.leaves)
        idx = leaf_index

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i+1] if i + 1 < len(current_level) else left
                combined = self._hash(left + right)
                next_level.append(combined)

            sibling_idx = idx + 1 if idx % 2 == 0 else idx - 1
            if sibling_idx < len(current_level):
                direction = "right" if idx % 2 == 0 else "left"
                proof.append((current_level[sibling_idx], direction))
            else:
                proof.append((current_level[idx], "right"))

            idx //= 2
            current_level = next_level

        return proof

    def verify_proof(self, leaf_hash: str, proof: List[Tuple[str, str]], root_hash: str) -> bool:
        curr = leaf_hash
        for sibling, direction in proof:
            if direction == "right":
                curr = self._hash(curr + sibling)
            else:
                curr = self._hash(sibling + curr)
        return curr == root_hash
