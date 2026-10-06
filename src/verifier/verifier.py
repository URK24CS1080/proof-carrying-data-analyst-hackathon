import io
from contextlib import redirect_stdout

import pandas as pd

from .result_comparator import compare_results


def verify_proof(
    proof_code: str,
    expected_result,
    tables: dict[str, pd.DataFrame],
) -> dict:
    """
    Execute generated proof code and compare its result
    with the expected executor result.

    The proof must store its final result in the variable
    'answer' and print it.
    """

    if not isinstance(proof_code, str):
        return {
            "status": "verification_failed",
            "executed": False,
            "matched": False,
            "answer": None,
            "reason": "Proof code must be a string.",
        }

    if not proof_code.strip():
        return {
            "status": "verification_failed",
            "executed": False,
            "matched": False,
            "answer": None,
            "reason": "Proof code is empty.",
        }

    if not isinstance(tables, dict):
        return {
            "status": "verification_failed",
            "executed": False,
            "matched": False,
            "answer": None,
            "reason": "Tables must be provided as a dictionary.",
        }

    namespace = {
        "tables": tables,
        "pd": pd,
    }

    output = io.StringIO()

    try:
        with redirect_stdout(output):
            exec(
                proof_code,
                {
                    "__builtins__": __builtins__,
                },
                namespace,
            )

        if "answer" not in namespace:
            return {
                "status": "verification_failed",
                "executed": True,
                "matched": False,
                "answer": None,
                "reason": (
                    "Proof executed successfully but did not "
                    "produce an 'answer' variable."
                ),
            }

        proof_result = namespace["answer"]

        comparison = compare_results(
            expected_result,
            proof_result,
        )

        if comparison["matched"]:
            return {
                "status": "verified",
                "executed": True,
                "matched": True,
                "answer": proof_result,
                "reason": "Proof result matches executor result.",
            }

        return {
            "status": "verification_failed",
            "executed": True,
            "matched": False,
            "answer": proof_result,
            "reason": comparison["reason"],
        }

    except Exception as exc:
        return {
            "status": "verification_failed",
            "executed": False,
            "matched": False,
            "answer": None,
            "reason": f"Proof execution failed: {exc}",
        }