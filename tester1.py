import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Label

class RestaurantGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_restaurant(self, name, menu):
        self.graph.add_node(name, menu=menu)

    def add_edge(self, restaurant1, restaurant2, distance):
        self.graph.add_edge(restaurant1, restaurant2, weight=distance)

    def filter_restaurants(self, avoid_ingredients):
        filtered_restaurants = []
        for restaurant in self.graph.nodes:
            menu = self.graph.nodes[restaurant].get('menu', {})
            menu_ingredients = menu.get('Ingredients', [])

            if not any(ingredient in avoid_ingredients for ingredient in menu_ingredients):
                filtered_restaurants.append(restaurant)

        return filtered_restaurants

    def display_filtered_menus(self, avoid_ingredients):
        # Create a tkinter window
        root = tk.Tk()
        root.title("Filtered Menus")

        # Make the window resizable
        root.resizable(width=True, height=True)

        # Create a label and entry widget for user input
        label = Label(root, text="Enter ingredients to avoid (comma-separated):")
        label.pack()
        avoid_ingredients_entry = Entry(root)
        avoid_ingredients_entry.pack()

        # Create a scrolled text widget
        text_widget = scrolledtext.ScrolledText(root, width=40, height=20)
        text_widget.pack(fill=tk.BOTH, expand=True)

        def display_menus():
            nonlocal text_widget
            text_widget.delete(1.0, tk.END)  # Clear previous content
            avoid_ingredients = avoid_ingredients_entry.get().split(', ')
            filtered_restaurants = self.filter_restaurants(avoid_ingredients)

            for restaurant in filtered_restaurants:
                menu = self.graph.nodes[restaurant].get('menu', {})
                filtered_dishes = []

                for dish, dish_info in menu.items():
                    dish_ingredients = dish_info.get('Ingredients', [])
                    if not any(ingredient in avoid_ingredients for ingredient in dish_ingredients):
                        filtered_dishes.append((dish, dish_info))

                if filtered_dishes:
                    text_widget.insert(tk.END, f"Restaurant {restaurant} Menu:\n")
                    for dish, dish_info in filtered_dishes:
                        price = dish_info.get('Price', 'N/A')
                        text_widget.insert(tk.END, f"  {dish}, Price: {price}\n")

                    # Display the distance using A*
                    try:
                        shortest_path = nx.astar_path(self.graph, source=restaurant, target='Home', heuristic=heuristic, weight='weight')
                        shortest_distance = nx.astar_path_length(self.graph, source=restaurant, target='Home', heuristic=heuristic, weight='weight')
                        reversed_shortest_path = shortest_path[::-1]
                        text_widget.insert(tk.END, f"Shortest path from Home to {restaurant} using A*: {reversed_shortest_path}\n")
                        text_widget.insert(tk.END, f"Shortest distance: {shortest_distance}\n\n")

                    except nx.NetworkXNoPath:
                        text_widget.insert(tk.END, f"No path from Home to {restaurant}\n\n")

        # Create a button to trigger the display
        display_button = Button(root, text="Display Menus", command=display_menus)
        display_button.pack()

        # Run the tkinter main loop
        root.mainloop()

    def draw_graph(self):
        pos = nx.shell_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, font_weight='bold')
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.show()

restaurant_graph = RestaurantGraph()

# Add restaurants to the graph with updated menu representation
restaurant_graph.add_restaurant('Tombo Luwe', {
    'Tahu Bacem': {"Price": 13000, "Ingredients": ["Tofu", "Palm Sugar", "Coriander", "Galangal"]},
    'Tempe Bacem': {"Price": 14000, "Ingredients": ["Tempe", "Palm Sugar", "Coriander", "Galangal"]},
    'Eggplant Dish': {"Price": 15000, "Ingredients": ["Eggplant", "Garlic", "Soy Sauce", "Chili"]},
    'Urap': {"Price": 14000, "Ingredients": ["Vegetables", "Grated Coconut", "Spices", "Lime Leaves"]}
})

restaurant_graph.add_restaurant('Pakar Nasi Uduk', {
    'Nasi Uduk': {"Price": 10000, "Ingredients": ["Rice", "Coconut Milk", "Spices"]},
    'Tempe Penyet': {"Price": 12000, "Ingredients": ["Fried Tempe", "Spices", "Sambal", "Cucumber"]},
    'Ayam Goreng': {"Price": 16000, "Ingredients": ["Chicken", "Spices", "Lime Leaves", "Sweet Soy Sauce"]}
})

restaurant_graph.add_restaurant('Penyetan Mbak Lis', {
    'Ayam Penyet': {"Price": 15000, "Ingredients": ["Chicken", "Spices"]},
    'Grilled Chicken': {"Price": 18000, "Ingredients": ["Chicken", "Lemon", "Herbs"]},
    'Grilled Egg': {"Price": 12000, "Ingredients": ["Egg", "Salt", "Pepper", "Herbs"]}
})

restaurant_graph.add_restaurant('Warung Kane', {
    'Pizza Mie': {"Price": 17000, "Ingredients": ["Instant Noodles", "Tomato Sauce", "Cheese", "Toppings"]},
    'Bandeng Presto': {"Price": 20000, "Ingredients": ["Milkfish", "Spices", "Coconut Milk", "Turmeric"]},
    'Ayam Katsu': {"Price": 18000, "Ingredients": ["Chicken", "Bread Crumbs", "Egg", "Cabbage"]}

})

restaurant_graph.add_restaurant('J-One', {
    'Nasi Goreng': {"Price": 10000, "Ingredients": ["Rice", "Vegetables", "Egg", "Soy Sauce"]},
    'Sambal Goreng Ati': {"Price": 16000, "Ingredients": ["Chicken Liver", "Chili", "Coconut Milk"]},
    'Omelette': {"Price": 12000, "Ingredients": ["Eggs", "Milk", "Cheese", "Vegetables"]}
})

restaurant_graph.add_restaurant('Warung Kampus', {
    'Grilled Sausages': {"Price": 16000, "Ingredients": ["Sausages", "Mustard", "Ketchup", "Herbs"]},
    'Katsu Ikan': {"Price": 16000, "Ingredients": ["Fish", "Bread Crumbs", "Egg", "Cabbage"]},
    'Tahu Petis': {"Price": 14000, "Ingredients": ["Tofu", "Shrimp Paste", "Palm Sugar", "Chilies"]},
    'Ayam Rempah': {"Price": 17000, "Ingredients": ["Chicken", "Spices", "Coconut Milk", "Lime Leaves"]}
})

restaurant_graph.add_restaurant('Deles', {
    'Nasi Goreng': {"Price": 10000, "Ingredients": ["Rice", "Vegetables", "Egg", "Soy Sauce"]},
    'Sate Ayam': {"Price": 15000, "Ingredients": ["Chicken", "Soy Sauce", "Peanut", "Peanut Sauce", "Cucumber"]},
    'Siomay': {"Price": 17000, "Ingredients": ["Fish", "Shrimp", "Tofu", "Peanut", "Peanut Sauce"]},
    'Soto Ayam': {"Price": 14000, "Ingredients": ["Chicken", "Turmeric", "Lime Leaves", "Rice Noodle"]}
})

restaurant_graph.add_restaurant('Gobar', {
    'Gurame Bakar': {"Price": 25000, "Ingredients": ["Fish", "Gurame Fish", "Spices", "Sweet Soy Sauce", "Lime"]},
    'Patin Bakar': {"Price": 19000, "Ingredients": ["Fish","Patin Fish", "Spices", "Sweet Soy Sauce", "Lime"]},
    'Lele Bakar': {"Price": 13000, "Ingredients": ["Fish","Catfish", "Spices", "Sweet Soy Sauce", "Lime"]}
})

restaurant_graph.add_restaurant('KFC Mulyosari', {
    'Hot Wings': {"Price": 15000, "Ingredients": ["Chicken", "Hot Sauce", "Butter", "Celery"]},
    'Chicken Popcorn': {"Price": 16000, "Ingredients": ["Chicken", "Flour", "Spices"]},
    'Chicken Strips': {"Price": 17000, "Ingredients": ["Chicken", "Flour", "Spices"]},
    'Chicken Burger': {"Price": 18000, "Ingredients": ["Chicken", "Bread", "Lettuce", "Tomato"]},
    'Extra Crispy Chicken': {"Price": 17000, "Ingredients": ["Chicken", "Crispy Coating", "Spices", "Dipping Sauce"]}
})

restaurant_graph.add_restaurant('Mie Ayam Nusantara', {
    'Mie Ayam': {"Price": 12000, "Ingredients": ["Egg Noodles", "Chicken", "Vegetables", "Soy Sauce"]}
})

restaurant_graph.add_restaurant('Geprek Joder Ka Dhani', {
    'Ayam Geprek': {"Price": 16000, "Ingredients": ["Chicken", "Chili Paste", "Tomato", "Spices"]},
    'Cumi Geprek': {"Price": 17000, "Ingredients": ["Calamari", "Chili Paste", "Tomato", "Spices"]}
})

restaurant_graph.add_restaurant('Mie Gacoan Manyar', {
    'Mie Hompimpa': {"Price": 16000, "Ingredients": ["Egg Noodles", "Chicken", "Vegetables", "Special Sauce"]}
})

# Add edges with specified distances    

restaurant_graph.add_edge('Home', 'Gobar', 3500)
restaurant_graph.add_edge('Home', 'Tombo Luwe', 400)
restaurant_graph.add_edge('Home', 'J-One', 500)
restaurant_graph.add_edge('Home', 'Deles', 1500)
restaurant_graph.add_edge('Home', 'Mie Ayam Nusantara', 1900)
restaurant_graph.add_edge('Home', 'Mie Gacoan Manyar', 3800)
restaurant_graph.add_edge('J-One', 'Warung Kampus', 240)
restaurant_graph.add_edge('Tombo Luwe', 'Pakar Nasi Uduk', 550)
restaurant_graph.add_edge('Pakar Nasi Uduk', 'Penyetan Mbak Lis', 40)
restaurant_graph.add_edge('Pakar Nasi Uduk', 'Warung Kane', 300)
restaurant_graph.add_edge('Warung Kane', 'Gobar', 2700)
restaurant_graph.add_edge('Pakar Nasi Uduk', 'Gobar', 2800)
restaurant_graph.add_edge('Gobar', 'KFC Mulyosari', 1200)
restaurant_graph.add_edge('Gobar', 'Mie Gacoan Manyar', 4000)
restaurant_graph.add_edge('Mie Gacoan Manyar', 'Geprek Joder Ka Dhani', 2000)
restaurant_graph.add_edge('Geprek Joder Ka Dhani', 'Mie Ayam Nusantara', 130)
restaurant_graph.add_edge('Geprek Joder Ka Dhani', 'Deles', 1200)

def heuristic(node1, node2):
    match node1:
        case 'Tombo Luwe':
            return 162
        case 'Pakar Nasi Uduk':
            return 603
        case 'Penyetan Mbak Lis':
            return 610
        case 'Warung Kane':
            return 519
        case 'J-One':
            return 288
        case 'Warung Kampus':
            return 404
        case 'Deles':
            return 1493
        case 'Gobar':
            return 2051
        case 'KFC Mulyosari':
            return 2477
        case 'Mie Ayam Nusantara':
            return 1310
        case 'Geprek Joder Ka Dhani':
            return 1359
        case 'Mie Gacoan Manyar':
            return 2903
        case 'Home':
            return 0


# Display menus from restaurants that do not contain the specified ingredients to avoid
# Add ingredients to avoid
avoid_ingredients = []
restaurant_graph.display_filtered_menus(avoid_ingredients)

# Draw the graph using Matplotlib
restaurant_graph.draw_graph()
