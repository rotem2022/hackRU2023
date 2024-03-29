""" Module that contains the methods for the server side functionality of the chat application"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from main import askGPT

'''PREV = """Answer the new question as sales man as if he was talking to the client, 
       if those are the only restaurant you know your answer should include only one restaurant name from the list (Include resturant name in your answer)
       ** provide me with an answer that takes into account the customer's order history, 
       including the specific restaurant type on each day. 
       Give extra priority if the customer has expressed a preference for certain restaurant on a particular day of the week,
       Your answer should be up to 20 words
       Today's Date 5.12.2023 Friday"""'''
PREV = """Answer the new question as sales man as if he was talking to the client, 
       if those are the only restaurant you know your answer should include only one restaurant name from the list (Include resturant name in your answer)
       ** provide me with an answer that takes into account the customer's order history, 
       including the specific restaurant type on each day. 
       If the customer has expressed a preference for certain items on a particular day,
       please take that into consideration and provide recommendations accordingly.
       Give extra priority to recent ordered from restaurants
       Your answer should be up to 20 words
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
client_that_used_to_love_asian_and_now_love_morocoo = """\nclient : John Doe age 58 History:
                    keywords :
                    1) Tajin
                    2) Spicy
                    3) Shushi
                    Orders History : 
Order 1:
Restaurant: Asian
Day: Sunday
Date: May 21, 2021
Dishes:
Grilled Ribeye: $24.99
Classic Cheeseburger: $11.99
New York Cheesecake: $7.99
Total price: $44.97

Order 2:
Restaurant: Asian
Day: Friday
Date: June 2, 2021
Dishes:
Edamame: $4.99
Tom Yum Soup: $5.99
Sushi Platter: $18.99
Total price: $29.97

Order 3:
Restaurant: American
Day: Thursday
Date: May 18, 2022
Dishes:
Bruschetta: $7.99
Lobster Linguine: $29.99
New York Cheesecake: $7.99
Total price: $45.97

Order 4:
Restaurant: Asian
Day: Friday
Date: June 9, 2022
Dishes:
Gyoza: $6.99
General Tso's Chicken: $14.99
Total price: $21.98

Order 5:
Restaurant: Asian
Day: Friday
Date: May 12, 2022
Dishes:
Egg Rolls: $5.99
Pad Thai: $12.99
Total price: $18.98

Order 6:
Restaurant: Morcoo
Day: Friday
Date: May 10, 2023
Dishes:
Harira: $4.99
Tagine: $16.99
M'hancha: $6.99
Total price: $28.97

Order 7:
Restaurant: Morcoo
Day: Sunday
Date: May 23, 2023
Dishes:
Briouat: $6.99
Couscous: $14.99
Halwa Shebakia: $4.99
Moroccan Mint Tea: $2.99
Total price: $30.96

"""
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
conversation_history = [PREV, RESTURANT1, RESTURANT2, RESTURANT3,
                        client_that_used_to_love_asian_and_now_love_morocoo]
""" We'll be using TCP sockets over UDP sockets, so we import AF_NET(Internet address family for IPv4) and SOCK_STREAM(connection oriented TCP)"""

"""
clients: Dictionary that contains the client's names
addresses: Dictionary that stores incoming (new) client's addresses
HOST: 
PORT: Port number for this process
BUFFSIZE: Maximum buffer size that a client can send at a time
ADDR: tuple containing socket address(IP address, PORT number)
SERVER: socket object that represents the server
bind is used to map the server object to a IP address and PORT number(socket address)
"""

clients = {}
addresses = {}
HOST = '127.0.0.1'
PORT = 5545
BUFFSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

"""
The below function that will listen and accept all incoming connections.
The accept method returns a socket object that can be used to communicate wuth the client, and the socket address of the client.
The send method id used to send an inital greeeting message to the client.
Then store the address of the client in the dictionary addresses
A seperate thread is created to handle this client.
"""


def acceptIncomingConnections():
    while True:
        client, clientAddress = SERVER.accept()
        print("%s:%s has connected." % clientAddress)
        client.send(bytes("Welcome to Bite Wise, type your name and press enter!", "utf8"))
        addresses[client] = clientAddress
        Thread(target=handleClient, args=(client,)).start()


def split_string_in_half(s):
    words = s.split()
    halfway_point = len(words) // 2
    first_half = ' '.join(words[:halfway_point])
    second_half = ' '.join(words[halfway_point:])
    first_half += "\n"
    second_half += "\n"
    return first_half, second_half


"""
The below function will handle all communication to and from a client
The chat name of the client is obtained 
Unless the client sends the exit message, he is allowed to chat, else, he is removed from the chat
and some cleanup is done to remove his/her information.
"""


def handleClient(client):
    name = client.recv(BUFFSIZE).decode("utf8")
    client.send(bytes("Welcome %s, type 'exit' to exit the chat" % name, 'utf8'))
    msg = '%s has joined the chat' % name
    broadcast(bytes(msg, 'utf8'))
    clients[client] = name
    while True:
        msg = client.recv(BUFFSIZE)
        askGPT(msg, conversation_history)
        if msg != bytes("'exit'", "utf8"):
            broadcast(msg, name + ": ")
            # broadcast(conversation_history[-1].encode('ascii'), "Bite Wise: ")
            broadcast(bytes(conversation_history[-1], 'utf8'), "Bite Wise: ")

        # else:
        #     client.send(bytes("'exit'", "utf8"))
        #     client.close()
        #     del clients[client]
        #     broadcast(bytes("%s has left the chat." % name, "utf8"))
        #     break


"""
The below function will broadcast a message to all clients in the chat.
"""


def broadcast(msg, prefix=""):
    for client in clients:
        client.send(bytes(prefix, 'utf8') + msg)


if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for a new connection...")
    ACCEPT_THREAD = Thread(target=acceptIncomingConnections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
