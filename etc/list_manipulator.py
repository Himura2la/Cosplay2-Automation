rejected = """

""".split("\n")

accepted = """

""".split("\n")

promo_eligible = set(rejected) - set(accepted)

print("\n".join(sorted(promo_eligible)))
print(f"Rejected: {len(rejected)}")
print(f"Accepted: {len(accepted)}")
print(f"Total: {len(promo_eligible)}")
