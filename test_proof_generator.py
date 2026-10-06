from src.executor.proof_generator import generate_proof


print("===================================")
print("PROOF GENERATOR TESTS")
print("===================================")


# -----------------------------------
# TEST 1 — AVERAGE
# -----------------------------------

print("\nTEST 1 — AVERAGE")

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
}

proof = generate_proof(plan)

print(proof)

assert 'df = tables["sales"].copy()' in proof

assert (
    "df['revenue'].dropna().mean()"
    in proof
)

assert "print(answer)" in proof

print("TEST 1 PASSED")


# -----------------------------------
# TEST 2 — FILTER + AVERAGE
# -----------------------------------

print("\nTEST 2 — FILTER + AVERAGE")

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "category": "Electronics"
    }
}

proof = generate_proof(plan)

print(proof)

assert (
    "df['category'] == 'Electronics'"
    in proof
)

assert (
    "df['revenue'].dropna().mean()"
    in proof
)

print("TEST 2 PASSED")


# -----------------------------------
# TEST 3 — COUNT
# -----------------------------------

print("\nTEST 3 — COUNT")

plan = {
    "status": "answerable",
    "operation": "count",
    "table": "sales",
    "column": "product",
}

proof = generate_proof(plan)

print(proof)

assert (
    "df['product'].count()"
    in proof
)

print("TEST 3 PASSED")


# -----------------------------------
# TEST 4 — SUM
# -----------------------------------

print("\nTEST 4 — SUM")

plan = {
    "status": "answerable",
    "operation": "sum",
    "table": "sales",
    "column": "revenue",
}

proof = generate_proof(plan)

print(proof)

assert (
    "df['revenue'].dropna().sum()"
    in proof
)

print("TEST 4 PASSED")


# -----------------------------------
# TEST 5 — MIN
# -----------------------------------

print("\nTEST 5 — MIN")

plan = {
    "status": "answerable",
    "operation": "min",
    "table": "sales",
    "column": "revenue",
}

proof = generate_proof(plan)

print(proof)

assert (
    "df['revenue'].dropna().min()"
    in proof
)

print("TEST 5 PASSED")


# -----------------------------------
# TEST 6 — MAX
# -----------------------------------

print("\nTEST 6 — MAX")

plan = {
    "status": "answerable",
    "operation": "max",
    "table": "sales",
    "column": "revenue",
}

proof = generate_proof(plan)

print(proof)

assert (
    "df['revenue'].dropna().max()"
    in proof
)

print("TEST 6 PASSED")


# -----------------------------------
# TEST 7 — CANNOT DETERMINE
# -----------------------------------

print("\nTEST 7 — CANNOT DETERMINE")

plan = {
    "status": "cannot_determine",
    "reason": "No matching data."
}

try:

    generate_proof(plan)

    assert False, "Expected ValueError"

except ValueError as exc:

    print(exc)

    assert (
        "Proof can only be generated for an answerable plan."
        in str(exc)
    )

print("TEST 7 PASSED")


# -----------------------------------
# TEST 8 — UNSUPPORTED OPERATION
# -----------------------------------

print("\nTEST 8 — UNSUPPORTED OPERATION")

plan = {
    "status": "answerable",
    "operation": "median",
    "table": "sales",
    "column": "revenue",
}

try:

    generate_proof(plan)

    assert False, "Expected ValueError"

except ValueError as exc:

    print(exc)

    assert (
        "is not supported yet."
        in str(exc)
    )

print("TEST 8 PASSED")


# -----------------------------------
# FINAL RESULT
# -----------------------------------

print("\n===================================")
print("ALL PROOF GENERATOR TESTS PASSED")
print("===================================")