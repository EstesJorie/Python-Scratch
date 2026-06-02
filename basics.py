import pydantic
from typing import List, Optional

ver = pydantic.__version__  # prints install version
if ver.startswith("2."):
    print("[INFO] Pydantic version 2.x is installed.")
else:
    raise ImportError(
        "Pydantic version 2.x is required. Please upgrade your pydantic version."
    )


class User(pydantic.BaseModel):
    id: int
    name: str = "John Doe"  # set default value


user = User(id="123")  # create an instance of User with only id

print(user.id)

print(user.model_fields_set)  # prints the fields that were set during initialization
user2 = User(id=456, name="Alice")  # create another instance of User with id and name
print(
    user2.model_fields_set
)  # prints the fields that were set during initialization for user2

print(user.model_dump())  # prints the dictionary representation of the user instance
print(user.model_dump_json())  # prints the JSON representation of the user instance
print(user.model_json_schema())  # prints the JSON schema of the User model


class Food(pydantic.BaseModel):
    name: str
    price: float
    ingredients: Optional[List[str]] = (
        None  # set default value to None for optional field
    )


class Restaurant(pydantic.BaseModel):
    name: str
    location: str
    foods: List[
        Food
    ]  # list of Food items in the restaurant's menu, uses Food model as the type for the items in the list


restaurant = Restaurant(
    name="Subshop",
    location="123 Main St",
    foods=[
        Food(
            name="Burger", price=9.99, ingredients=["Bun", "Patty", "Lettuce", "Tomato"]
        ),
        Food(
            name="Pizza",
            price=14.99,
            ingredients=["Dough", "Tomato Sauce", "Cheese", "Pepperoni"],
        ),
        Food(name="Salad", price=7.99),
    ],
)

for food in restaurant.foods:
    print(f"Food: {food.name}, Price: £{food.price}")
print(restaurant.model_dump())

print(
    restaurant.foods[2].ingredients
)  # prints None since ingredients is optional and not provided for the Salad food item
