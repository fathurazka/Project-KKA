import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext

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
        filtered_restaurants = self.filter_restaurants(avoid_ingredients)

        # Create a tkinter window
        root = tk.Tk()
        root.title("Filtered Menus")

        # Make the window resizable
        root.resizable(width=True, height=True)

        # Create a scrolled text widget
        text_widget = scrolledtext.ScrolledText(root, width=40, height=20)
        text_widget.pack(fill=tk.BOTH, expand=True)

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
                    shortest_path = nx.astar_path(self.graph, source='Home', target=restaurant, heuristic=None, weight='weight')
                    shortest_distance = nx.astar_path_length(self.graph, source='Home', target=restaurant, heuristic=None, weight='weight')
                    text_widget.insert(tk.END, f"Shortest path from Home to {restaurant} using A*: {shortest_path}\n")
                    text_widget.insert(tk.END, f"Shortest distance: {shortest_distance}\n\n")
                except nx.NetworkXNoPath:
                    text_widget.insert(tk.END, f"No path from Home to {restaurant}\n\n")

        # Run the tkinter main loop
        root.mainloop()

    def draw_graph(self):
        pos = nx.shell_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, font_weight='bold')
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.show()

# Example Usage:
restaurant_graph = RestaurantGraph()

# Add restaurants to the graph with updated menu representation
restaurant_graph.add_restaurant('A', {
    'Burger': {"Price": 5000, "Ingredients": ["Meat", "Bread", "Lettuce", "Cucumber"]},
    'Pizza': {"Price": 6000, "Ingredients": ["Dough", "Tomato Sauce", "Cheese", "Pepperoni"]},
    'Pasta': {"Price": 7000, "Ingredients": ["Pasta", "Tomato Sauce", "Meat", "Cheese"]}
})

restaurant_graph.add_restaurant('B', {
    'Fried Rice': {"Price": 4500, "Ingredients": ["Rice", "Vegetables", "Egg", "Soy Sauce"]},
    'Fried Noodle': {"Price": 4800, "Ingredients": ["Noodle", "Vegetables", "Chicken", "Soy Sauce"]}
})

restaurant_graph.add_restaurant('C', {
    'Crispy Chicken': {"Price": 8000, "Ingredients": ["Chicken", "Flour", "Spices"]},
    'Peking Duck': {"Price": 10000, "Ingredients": ["Duck", "Flour", "Hoisin Sauce", "Cucumber"]}
})

restaurant_graph.add_restaurant('D', {
    'Grilled Fish': {"Price": 9000, "Ingredients": ["Fish", "Lemon", "Herbs", "Olive Oil"]},
    'Butter Crab': {"Price": 12000, "Ingredients": ["Crab", "Butter", "Garlic", "Herbs"]}
})

restaurant_graph.add_restaurant('Home', {})  # 'Home' with an empty menu

# Add edges with specified distances    
restaurant_graph.add_edge('A', 'B', 5)
restaurant_graph.add_edge('A', 'C', 8)
restaurant_graph.add_edge('A', 'D', 10)
restaurant_graph.add_edge('B', 'C', 4)
restaurant_graph.add_edge('B', 'D', 7)
restaurant_graph.add_edge('C', 'D', 6)
restaurant_graph.add_edge('Home', 'B', 5)
restaurant_graph.add_edge('Home', 'C', 7)

# Display menus from restaurants that do not contain the specified ingredients to avoid
avoid_ingredients = ['Cucumber', 'Cheese']
restaurant_graph.display_filtered_menus(avoid_ingredients)

# Draw the graph using Matplotlib
restaurant_graph.draw_graph()
