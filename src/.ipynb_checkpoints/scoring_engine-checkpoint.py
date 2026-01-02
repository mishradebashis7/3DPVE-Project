import numpy as np

class PatentValueEngine:
    """
    The 3D-PVE Core Scoring System.
    """
    def __init__(self):
        # Default State
        self.alpha = 0.6
        self.beta = 0.4
        self.mode = "Heuristic (Default)"

    def set_model_mode(self, mode, custom_weights=None):
        """
        Switch between Heuristic and Data-Driven modes.
        Allows passing custom weights from the ML module in the future.
        """
        if mode == 'Heuristic':
            self.alpha = 0.6
            self.beta = 0.4
            self.mode = "Heuristic"
            
        elif mode == 'ML_Optimized':
            # In a real scenario, these could be loaded from a saved model file.
            # For the prototype, we use the hypothetical 'optimized' values.
            if custom_weights:
                self.alpha = custom_weights['alpha']
                self.beta = custom_weights['beta']
            else:
                self.alpha = 0.82 
                self.beta = 0.15
            self.mode = "ML_Optimized"

    def calculate_legal_score(self, event_type):
        if event_type in ['Revocation', 'Lapse']: return 0.0
        elif event_type in ['Opposition (Survived)', 'Appeal (Survived)']: return 1.5
        else: return 1.0

    def calculate_economic_score(self, family_size, years_active):
        # USES CURRENT ALPHA/BETA
        term1 = self.alpha * np.log(1 + family_size)
        term2 = self.beta * years_active
        return term1 + term2

    def calculate_tech_score(self, diversity_factor):
        # Simple simulation of entropy scaling
        return 0.0 if diversity_factor == 0 else diversity_factor * 2.5

    def get_composite_score(self, s_leg, s_eco, s_tech):
        return s_leg * s_eco * s_tech