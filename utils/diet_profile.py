class DietProfile:
    def __init__(self, dietary_preference, allergies):
        self.dietary_preference = dietary_preference
        self.allergies = [allergen.strip().lower() for allergen in allergies]
        self.non_veg_ingredients = ['chicken', 'beef', 'pork', 'lamb', 'fish', 'shrimp', 'bacon', 'turkey', 'duck']
        self.non_vegan_ingredients = ['chicken', 'beef', 'pork', 'lamb', 'fish', 'shrimp', 'bacon', 'turkey', 'duck', 'milk', 'cheese', 'butter', 'eggs', 'honey']

    def set_dietary_preference(self, dietary_preference):
        self.dietary_preference = dietary_preference
    
    def set_allergies(self, allergies):
        self.allergies = [allergen.strip().lower() for allergen in allergies]

    def find_allergen(self, user_ingredients):
        allergens_found = [allergen for allergen in self.allergies if allergen in user_ingredients]
        return allergens_found
    
    def check_diet(self, user_ingredients):
        if self.dietary_preference == "Vegan":
            non_vegan_found = [ingredient for ingredient in user_ingredients if ingredient in self.non_vegan_ingredients]
            return non_vegan_found
        elif self.dietary_preference == "Vegetarian":
            non_veg_found = [ingredient for ingredient in user_ingredients if ingredient in self.non_veg_ingredients]
            return non_veg_found