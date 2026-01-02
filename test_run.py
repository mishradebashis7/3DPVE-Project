from src.scoring_engine import PatentValueEngine

# Initialize engine
engine = PatentValueEngine()

# Simulated Patent Data
# Scenario: A patent that survived opposition, has 10 family members, 
# active for 5 years, and cited across 4 diverse fields (0.25 prob each).

s_leg = engine.calculate_legal_score('Opposition') # Should be 1.5 [cite: 24]
s_eco = engine.calculate_economic_score(family_size=10, years_active=5) 
s_tech = engine.calculate_tech_score([0.25, 0.25, 0.25, 0.25]) # High entropy

v_cp = engine.get_composite_score(s_leg, s_eco, s_tech)

print(f"Legal Score (S_leg): {s_leg}")
print(f"Economic Score (S_eco): {s_eco:.2f}")
print(f"Tech Score (S_tech): {s_tech:.2f}")
print(f"FINAL 3D-PVE SCORE (V_cp): {v_cp:.2f}")