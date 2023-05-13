# This is a sample Python script.
import openai

openai.api_key = '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'
PREV = """Answer the new question as sales man as if he was talking to the client, 
       if those are the only restaurant you know your answer should include only one restaurant name from the list (Include resturant name in your answer)
       ** provide me with an answer that takes into account the customer's order history, 
       including the specific restaurant type on each day. 
       If the customer has expressed a preference for certain items on a particular day,
       please take that into consideration and provide recommendations accordingly.
       Today's Date 5.12.2023 Friday"""
RESTURANT1 = """restaurant name 'American' : 
                Appetizers
Spinach and Artichoke Dip: Creamy spinach and artichoke dip served with tortilla chips $9.99.
Fried Calamari: Lightly breaded and fried calamari served with marinara sauce $12.99.
Bruschetta: Toasted baguette slices topped with diced tomatoes, fresh basil, garlic, and olive oil  $7.99.

Entrees
Grilled Ribeye: 12-ounce ribeye steak grilled to your liking and served with roasted vegetables and mashed potatoes $24.99.
Lobster Linguine: Linguine pasta tossed in a creamy lobster sauce with chunks of fresh lobster meat $29.99.
Chicken Marsala: Sauteed chicken breasts in a marsala wine sauce served with roasted potatoes and asparagus $18.99.

Sandwiches
Classic Cheeseburger: A juicy beef patty topped with American cheese, lettuce, tomato, and onion on a brioche bun $11.99.
Grilled Chicken Sandwich: Grilled chicken breast topped with avocado, bacon, lettuce, tomato, and mayo on a ciabatta roll $13.99.
Veggie Wrap: Grilled zucchini, squash, red pepper, and onion wrapped in a flour tortilla with hummus and feta cheese $10.99.

Desserts
New York Cheesecake: Classic cheesecake with a graham cracker crust and raspberry sauce  $7.99.
Chocolate Lava Cake: Warm chocolate cake with a melted chocolate center and vanilla ice cream $8.99.
Tiramisu: Layers of espresso-soaked ladyfingers and mascarpone cheese dusted with cocoa powder $6.99."""
RESTURANT2 = """ restaurant name 'Asian'
Appetizers
- Egg Rolls: Crispy fried rolls filled with ground pork, vegetables, and spices, served with sweet and sour sauce 5.99$.
- Edamame: Steamed soybeans with sea salt, served hot 4.99$.
- Gyoza: Pan-fried or steamed dumplings filled with ground pork and vegetables, served with soy sauce and sesame oil 6.99$.

Soups
- Miso Soup: Traditional Japanese soup made with fermented soybean paste, tofu, seaweed, and scallions 3.99$.
- Tom Yum Soup: Spicy and sour Thai soup with shrimp, lemongrass, galangal, and lime juice 5.99$.
- Pho: Vietnamese noodle soup with beef or chicken, rice noodles, bean sprouts, and herbs 9.99$.

Entrees
- Pad Thai: Classic Thai stir-fried rice noodles with shrimp, chicken, egg, tofu, bean sprouts, and peanuts 12.99$.
- General Tso's Chicken: Crispy fried chicken with a sweet and spicy sauce, served with steamed broccoli and rice 14.99$.
- Sushi Platter: Assortment of fresh sushi rolls with raw fish, avocado, cucumber, and pickled ginger, served with soy sauce and wasabi 18.99$.

Desserts
- Mango Sticky Rice: Sweet and creamy coconut milk rice pudding served with fresh mango slices 6.99$.
- Green Tea Ice Cream: Smooth and creamy ice cream with a delicate green tea flavor 4.99$.
- Mochi: Soft and chewy rice cakes filled with sweet red bean paste or ice cream, served with whipped cream and fruit 5.99$.
"""
RESTURANT3 = """restaurant name 'Morcoo'
Appetizers
- Harira: Traditional Moroccan soup made with tomatoes, lentils, chickpeas, and spices 4.99$.
- Briouat: Crispy fried phyllo dough filled with spiced ground meat or vegetables, served with harissa sauce 6.99$.
- Zaalouk: Roasted eggplant and tomato salad with garlic, cumin, and paprika, served with bread 5.99$.

Entrees
- Tagine: Slow-cooked stew made with meat or vegetables, preserved lemon, olives, and spices, served with couscous or bread 16.99$.
- Couscous: Steamed semolina grains with a variety of vegetables and meat or fish, served with harissa sauce 14.99$.
- Bastilla: Sweet and savory pastry made with layers of phyllo dough, spiced chicken or pigeon, almonds, and cinnamon, topped with powdered sugar and cinnamon 12.99$.

Desserts
- Moroccan Mint Tea: Traditional sweet and minty green tea, served with small cookies 2.99$.
- M'hancha: Sweet pastry filled with almond paste, orange blossom water, and cinnamon, shaped into a coiled snake 6.99$.
- Halwa Shebakia: Sesame seed and honey cookies, fried and soaked in a sweet syrup, served with almonds and tea 4.99$."""

client_that_love_asain_in_friday = """\nclient : John Doe age 58 History:
                    keywords :
                    1) Vegtrain
                    2) Spicy
                    3) Chip
                    Orders History : 
Order 1:
Restaurant: American
Day: Sunday
Date: May 21, 2023
Dishes:
Grilled Ribeye: $24.99
Classic Cheeseburger: $11.99
New York Cheesecake: $7.99
Total price: $44.97

Order 2:
Restaurant: Asian
Day: Friday
Date: June 2, 2023
Dishes:
Edamame: $4.99
Tom Yum Soup: $5.99
Sushi Platter: $18.99
Total price: $29.97

Order 3:
Restaurant: American
Day: Thursday
Date: May 18, 2023
Dishes:
Bruschetta: $7.99
Lobster Linguine: $29.99
New York Cheesecake: $7.99
Total price: $45.97

Order 4:
Restaurant: American
Day: Monday
Date: May 15, 2023
Dishes:
Fried Calamari: $12.99
Grilled Ribeye: $24.99
Chocolate Lava Cake: $8.99
Total price: $46.97

Order 5:
Restaurant: American
Day: Wednesday
Date: May 17, 2023
Dishes:
Spinach and Artichoke Dip: $9.99
Classic Cheeseburger: $11.99
Tiramisu: $6.99
Total price: $28.97

Order 6:
Restaurant: Asian
Day: Friday
Date: June 9, 2023
Dishes:
Gyoza: $6.99
General Tso's Chicken: $14.99
Total price: $21.98

Order 7:
Restaurant: American
Day: Monday
Date: May 8, 2023
Dishes:
Grilled Chicken Sandwich: $13.99
Veggie Wrap: $10.99
Chocolate Lava Cake: $8.99
Total price: $33.97

Order 8:
Restaurant: American
Day: Saturday
Date: May 20, 2023
Dishes:
Chicken Marsala: $18.99
Fried Calamari: $12.99
Bruschetta: $7.99
Mango Sticky Rice: $6.99
Total price: $46.96

Order 9:
Restaurant: Asian
Day: Friday
Date: May 12, 2023
Dishes:
Egg Rolls: $5.99
Pad Thai: $12.99
Total price: $18.98"""
#client_that_used_to_love_asian_and_now_love_italian =

def askGPT(text, conv):
    message = f"Conversation history:{' '.join(conv)}\nQuestion: {text} " \
              f"relevant for client)\nAnswer: "
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        temperature=0.6,
        max_tokens=500,
    )
    conv.append(response.choices[0].text)



if __name__ == '__main__':
    conversation_history = [PREV, RESTURANT1, RESTURANT2, RESTURANT3,
                            client_that_love_asain_in_friday]  # Initialize conversation history as empty list
    while True:
        question = input("What is your question?\n")
        conversation_history.append(question)
        askGPT(question, conversation_history)
        print(conversation_history[-1])
