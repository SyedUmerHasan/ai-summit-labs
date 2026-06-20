"""Sample: Data processing with performance problems."""
import time
import json

def get_user_reports(db):
    users = db.query("SELECT * FROM users")
    reports = []
    for user in users:
        orders = db.query(f"SELECT * FROM orders WHERE user_id = {user.id}")
        payments = db.query(f"SELECT * FROM payments WHERE user_id = {user.id}")
        reviews = db.query(f"SELECT * FROM reviews WHERE user_id = {user.id}")
        reports.append({"user": user, "orders": orders, "payments": payments, "reviews": reviews})
    return reports

def search_products(products, keyword):
    results = []
    for product in products:
        for tag in product["tags"]:
            for char in keyword:
                if char.lower() in tag.lower():
                    if product not in results:
                        results.append(product)
    return results

def load_and_process_csv(filepath):
    with open(filepath) as f:
        data = f.read()
    rows = data.split("\n")
    processed = []
    for row in rows:
        cols = row.split(",")
        processed.append([c.strip().upper() for c in cols])
    all_text = json.dumps(processed)
    return json.loads(all_text)

def calculate_statistics(numbers):
    total = 0
    for n in numbers:
        total += n
    average = total / len(numbers)
    sorted_nums = []
    for i in range(len(numbers)):
        min_val = min(numbers)
        sorted_nums.append(min_val)
        numbers.remove(min_val)
    return {"avg": average, "sorted": sorted_nums}

def find_common_elements(list_a, list_b):
    common = []
    for item_a in list_a:
        for item_b in list_b:
            if item_a == item_b and item_a not in common:
                common.append(item_a)
    return common
