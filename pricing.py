import json




MINIMUM_GUESTS = 100
VEG_PRICE = 150
NON_VEG_PRICE = 200
MIXED_PRICE = 250
DISCOUNT_THRESHOLD = 500
DISCOUNT_MULTIPLIER = 0.9

def calculate_quote(guest_count, food_preference):
    discount = False
    if not isinstance(guest_count, int):
        return {"error": "Guest count needs to be an integer"}
    if guest_count < MINIMUM_GUESTS:
        return {"error": "Minimum Number of Guests is 100"}
        
    else:
        if food_preference == "veg":
            price = VEG_PRICE
        elif food_preference == "non-veg":
            price = NON_VEG_PRICE
        elif food_preference == "mixed":
            price = MIXED_PRICE
        else:
            return {"error": "Food Preference is not available"}
        sub_total = price * guest_count
        total = sub_total
        if guest_count >= DISCOUNT_THRESHOLD:
            discount = True
            total = sub_total * DISCOUNT_MULTIPLIER

        quote = {"price_per_plate": price, "guest_count": guest_count, "sub_total": sub_total, "discount_applied": discount, "total": total}
        return quote