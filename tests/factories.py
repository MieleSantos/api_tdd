def product_data_sucess():
    return {
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


def products_data_sucess():
    return [
        {"name": "Iphone 14 Pro Max", "quantity": 10, "price": "8.500", "status": True},
        {"name": "Iphone 13 Pro Max", "quantity": 4, "price": " 5.500", "status": True},
        {"name": "Iphone 12 Pro Max", "quantity": 1, "price": "6.500", "status": True},
        {"name": "Iphone 11 Pro Max", "quantity": 2, "price": "3.500", "status": True},
    ]


def product_data_raises():
    return {"name": "Iphone 14 Pro Max", "quantity": 10, "price": "8.500"}
