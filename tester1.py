import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Label, Checkbutton, IntVar

class RestaurantGraph:
    # Inisiasi graph dengan library networkx
    # serta inisiasi list bahan yang harus dihindari
    def __init__(self):
        self.graph = nx.Graph()
        self.avoided_ingredients = []  

    # Menambahkan node restoran ke dalam graph
    def add_restaurant(self, name, menu):
        self.graph.add_node(name, menu=menu)

    # Menambahkan edge antar restoran ke dalam graph
    def add_edge(self, restaurant1, restaurant2, distance):
        self.graph.add_edge(restaurant1, restaurant2, weight=distance)

    # Mengatur bahan yang harus dihindari berdasarkan diet
    def set_diets(self, selected_diets):
        # Daftar bahan yang harus dihindari berdasarkan diet
        diets = {
            'vegetarian': ['meat', 'seafood'],
            'vegan': ["animal products"],
            'pescatarian': ['meat'],
            'gluten-free': ['flour'],
            'lactose-free': ['milk', 'cheese', 'yogurt', 'butter', 'cream', 'dairy'],
            'low-carb': ['rice', 'potatoes', 'bread', 'pasta'],
            'nut-free': ['peanuts', 'almonds', 'cashews', 'walnuts'],
            'keto': ['rice', 'potatoes', 'bread', 'pasta', 'sugar', 'fruits', 'legumes', 'grains'],
        }
        
        self.avoided_ingredients = []
        for diet in selected_diets:
            self.avoided_ingredients.extend(diets.get(diet, []))

    # Mengatur bahan yang harus dihindari berdasarkan input pengguna
    def set_custom_avoided_ingredients(self, custom_ingredients):
        # Mengatur agar input menjadi lowercase dan memisahkan tiap bahan dengan koma
        self.avoided_ingredients += [ingredient.strip().lower() for ingredient in custom_ingredients.split(',')]

    # Mengembalikan daftar restoran yang lolos filtering
    def filter_restaurants(self):
        filtered_restaurants = []
        for restaurant in self.graph.nodes:
            menu = self.graph.nodes[restaurant].get('menu', {})
            menu_ingredients = menu.get('Ingredients', [])

            # Mengecek apakah restoran mengandung bahan yang harus dihindari
            if not any(ingredient in self.avoided_ingredients for ingredient in map(str.lower, menu_ingredients)):
                filtered_restaurants.append(restaurant)

        return filtered_restaurants
    
    # Awalan aplikasi berupa landing page
    def run_application(self):
        landing_root = tk.Tk()
        landing_root.title("DietNav - Welcome")
        #landing_root.geometry("600x400")
        landing_root.attributes('-fullscreen', True)
        landing_root.configure(background='#dbe2ef')
        def toggle_fullscreen(event=None):
            state = not landing_root.attributes("-fullscreen")
            landing_root.attributes("-fullscreen", state)
            return "break"
        landing_root.bind("<F11>", toggle_fullscreen)
        
        welcome_label = Label(landing_root, text="Welcome to DietNav!", font=("Helvetica", 36, "bold"), background='#dbe2ef')
        welcome_label.pack(pady=40)

        description_label = Label(landing_root, text="DietNav is an application to help you find restaurants based on your dietary preferences.", font=("Helvetica", 16), background='#dbe2ef')
        description_label.pack(pady=20)

        continue_button = Button(landing_root, text="Continue", font=("Helvetica", 14, "bold"), command=landing_root.destroy, bg="#4CAF50", fg="white", padx=20, pady=10)
        continue_button.pack(pady=40)

        landing_root.mainloop()
    
    # Menengahkan window tkinter
    def center_window(self, root):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        x = (screen_width/2) - (root.winfo_width() / 2)
        y = (screen_height/2) - (root.winfo_height() / 2)
        
        root.geometry("+%d+%d" % (x, y))

    # Menampilkan menu restoran yang lolos filtering
    def display_filtered_menus(self):
        root = tk.Tk()
        root.title("Restaurant Filter")
        root.attributes('-fullscreen', True)
        #root.geometry("1280x720")
        root.update_idletasks()
        self.center_window(root)
        root.configure(background='#dbe2ef')
        def toggle_fullscreen(event=None):
            state = not root.attributes("-fullscreen")
            root.attributes("-fullscreen", state)
            return "break"
        root.bind("<F11>", toggle_fullscreen)

        root.resizable(width=True, height=True)
        
        # Daftar diet yang dapat dipilih dengan checkbox di window tkinter
        diets = ['vegetarian', 'vegan', 'pescatarian', 'gluten-free', 'lactose-free', 'low-carb', 'nut-free', 'keto']
        diet_checkboxes = {}
        
        # membuat frame untuk menampilkan checkbox
        frames = [tk.Frame(root, background='#dbe3ef') for _ in range((len(diets) + 2) // 3)]
        for i, frame in enumerate(frames):
            frame.grid(row=i, column=2, columnspan=2)
            root.grid_rowconfigure(i, weight=1)
            
            root.grid_columnconfigure(i%3, weight=1)
        
        # membuat checkbox untuk setiap diet
        for i, diet in enumerate(diets):
            var = tk.IntVar()
            checkbox = tk.Checkbutton(frames[i//3], text=diet, variable=var, width=10)
            checkbox.configure(background='#dbe2ef')
            checkbox.grid(row=0, column=i%3)
            frames[i//3].grid_columnconfigure(i%3, weight=1)
            #root.grid_columnconfigure(i%3, weight=1) 
            diet_checkboxes[diet] = var
        
        custom_label = tk.Label(root, text="Enter custom avoided ingredients (comma-separated):")
        custom_label.configure(background='#dbe2ef')
        custom_label.grid(row=len(frames), column=0, columnspan=6, sticky='ew')
        
        custom_entry = Entry(root)
        custom_entry.configure(width=48)
        custom_entry.grid(row=len(diets)//3+2, column=0, columnspan=6)
        
        # membuat button untuk update diet
        def update_diets():
            selected_diets = [diet for diet, var in diet_checkboxes.items() if var.get()]
            self.set_diets(selected_diets)
            custom_ingredients = custom_entry.get()
            self.set_custom_avoided_ingredients(custom_ingredients)
            display_menus() 
        
        update_button = Button(root, text="Update Diets", command=update_diets)
        update_button.grid(row=len(diets)//3+3, column=0, columnspan=6)
        
        # membuat frame untuk menampilkan menu
        for i in range(6):
            root.grid_columnconfigure(i, weight=1)

        # membuat scrolled text untuk menampilkan menu
        text_widget = scrolledtext.ScrolledText(root, width=40, height=20)
        text_widget.configure(background='#F9F7F7', height=25)
        text_widget.grid(row=len(diets)//3+4, column=0, columnspan=6, sticky='ew')
        
        # membuat button untuk menampilkan menu
        def display_menus():
            nonlocal text_widget
            text_widget.delete(1.0, tk.END)
            filtered_restaurants = restaurant_graph.filter_restaurants()
            home_node = 'Home'

            # Create a list of tuples containing restaurant and its distance to the Home node
            distances = [(restaurant, nx.astar_path_length(restaurant_graph.graph, home_node, restaurant, heuristic=heuristic)) for restaurant in filtered_restaurants]

            # Sort the list by distance
            distances.sort(key=lambda x: x[1])

            for restaurant, distance in distances:
                menu = restaurant_graph.graph.nodes[restaurant].get('menu', {})
                filtered_dishes = []

                for dish, dish_info in menu.items():
                    dish_ingredients = dish_info.get('Ingredients', [])
                    # Mengecek apakah restoran mengandung bahan yang harus dihindari
                    if not any(ingredient in restaurant_graph.avoided_ingredients for ingredient in map(str.lower, dish_ingredients)):
                        filtered_dishes.append((dish, dish_info))

                if filtered_dishes:
                    # Display the restaurant name and distance
                    text_widget.insert(tk.END, f"Restaurant {restaurant} (Distance: {distance} meters):\n")
                    for dish, dish_info in filtered_dishes:
                        price = dish_info.get('Price', 'N/A')
                        text_widget.insert(tk.END, f"  {dish}, Price: {price}\n")

        root.mainloop()
    
    # Menggambar graph menggunakan Matplotlib
    def draw_graph(self):
        pos = nx.shell_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, font_weight='bold')
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.show()
        
# Inisiasi graph
restaurant_graph = RestaurantGraph()

# Menambahkan node restoran beserta menu dan bahan
restaurant_graph.add_restaurant('Tombo Luwe', {
    'Tahu Bacem': {"Price": 13000, "Ingredients": ["Tofu", "Palm Sugar", "Coriander", "Galangal"]},
    'Tempe Bacem': {"Price": 14000, "Ingredients": ["Tempe", "Palm Sugar", "Coriander", "Galangal"]},
    'Eggplant Dish': {"Price": 15000, "Ingredients": ["Eggplant", "Garlic", "Soy Sauce", "Chili"]},
    'Urap': {"Price": 14000, "Ingredients": ["Vegetables", "Coconut", "Spices", "Lime Leaves"]}
})

restaurant_graph.add_restaurant('Pakar Nasi Uduk', {
    'Nasi Uduk': {"Price": 10000, "Ingredients": ["Rice", "Coconut Milk", "Spices"]},
    'Tempe Penyet': {"Price": 12000, "Ingredients": ["Fried Tempe", "Spices", "Sambal", "Cucumber"]},
    'Ayam Goreng': {"Price": 16000, "Ingredients": ["Chicken", "Spices", "Lime Leaves", "Sweet Soy Sauce", "Meat", "Animal Products"]}
})

restaurant_graph.add_restaurant('Penyetan Mbak Lis', {
    'Ayam Penyet': {"Price": 15000, "Ingredients": ["Chicken", "Spices", "Meat", "Animal Products"]},
    'Grilled Chicken': {"Price": 18000, "Ingredients": ["Chicken", "Lemon", "Herbs", "Meat", "Animal Products"]},
    'Grilled Egg': {"Price": 12000, "Ingredients": ["Egg", "Salt", "Pepper", "Herbs", "Animal Products"]}
})

restaurant_graph.add_restaurant('Warung Kane', {
    'Pizza Mie': {"Price": 17000, "Ingredients": ["Instant Noodles", "Tomato Sauce", "Cheese", "Toppings", "Dairy", "Animal Products"]},
    'Bandeng Presto': {"Price": 20000, "Ingredients": ["Milkfish", "Spices", "Coconut Milk", "Turmeric", "Seafood", "Animal Products"]},
    'Ayam Katsu': {"Price": 18000, "Ingredients": ["Chicken", "Bread Crumbs", "Egg", "Cabbage", "Meat", "Animal Products", "flour"]}

})

restaurant_graph.add_restaurant('J-One', {
    'Nasi Goreng': {"Price": 10000, "Ingredients": ["Rice", "Vegetables", "Egg", "Soy Sauce", "Animal Products"]},
    'Sambal Goreng Ati': {"Price": 16000, "Ingredients": ["Chicken Liver", "Chili", "Coconut Milk", "Meat", "Animal Products"]},
    'Omelette': {"Price": 12000, "Ingredients": ["Eggs", "Milk", "Cheese", "Vegetables", "Animal Products", "Dairy"]}
})

restaurant_graph.add_restaurant('Warung Kampus', {
    'Grilled Sausages': {"Price": 16000, "Ingredients": ["Sausages", "Mustard", "Ketchup", "Herbs", "Meat", "Animal Products"]},
    'Katsu Ikan': {"Price": 16000, "Ingredients": ["Fish", "Bread Crumbs", "Egg", "Cabbage", "Seafood", "Animal Products", "flour"]},
    'Tahu Petis': {"Price": 14000, "Ingredients": ["Tofu", "Shrimp Paste", "Palm Sugar", "Chilies"]},
    'Ayam Rempah': {"Price": 17000, "Ingredients": ["Chicken", "Spices", "Coconut Milk", "Lime Leaves", "Meat", "Animal Products"]}
})

restaurant_graph.add_restaurant('Deles', {
    'Nasi Goreng': {"Price": 10000, "Ingredients": ["Rice", "Vegetables", "Egg", "Soy Sauce", "Animal Products"]},
    'Sate Ayam': {"Price": 15000, "Ingredients": ["Chicken", "Soy Sauce", "Peanut", "Peanut Sauce", "Cucumber", "Meat", "Animal Products"]},
    'Siomay': {"Price": 17000, "Ingredients": ["Fish", "Shrimp", "Tofu", "Peanut", "Peanut Sauce", "Seafood", "Animal Products", "flour"]},
    'Soto Ayam': {"Price": 14000, "Ingredients": ["Chicken", "Turmeric", "Lime Leaves", "Rice Noodle", "Meat", "Animal Products"]}
})

restaurant_graph.add_restaurant('Gobar', {
    'Gurame Bakar': {"Price": 25000, "Ingredients": ["Fish", "Gurame Fish", "Spices", "Sweet Soy Sauce", "Lime", "Seafood", "Animal Products"]},
    'Patin Bakar': {"Price": 19000, "Ingredients": ["Fish","Patin Fish", "Spices", "Sweet Soy Sauce", "Lime", "Seafood", "Animal Products"]},
    'Lele Bakar': {"Price": 13000, "Ingredients": ["Fish","Catfish", "Spices", "Sweet Soy Sauce", "Lime", "Seafood", "Animal Products"]}
})

restaurant_graph.add_restaurant('KFC Mulyosari', {
    'Hot Wings': {"Price": 15000, "Ingredients": ["Chicken", "Hot Sauce", "Butter", "Celery", "Meat", "Animal Products", "flour"]},
    'Chicken Popcorn': {"Price": 16000, "Ingredients": ["Chicken", "Flour", "Spices", "Meat", "Animal Products", "flour"]},
    'Chicken Strips': {"Price": 17000, "Ingredients": ["Chicken", "Flour", "Spices", "Meat", "Animal Products", "flour"]},
    'Chicken Burger': {"Price": 18000, "Ingredients": ["Chicken", "Bread", "Lettuce", "Tomato", "Meat", "Animal Products", "flour"]},
    'Extra Crispy Chicken': {"Price": 17000, "Ingredients": ["Chicken", "Crispy Coating", "Spices", "Dipping Sauce", "Meat", "Animal Products", "flour"]}
})

restaurant_graph.add_restaurant('Mie Ayam Nusantara', {
    'Mie Ayam': {"Price": 12000, "Ingredients": ["Egg Noodles", "Chicken", "Vegetables", "Soy Sauce", "Meat", "Animal Products", "flour"]},
})

restaurant_graph.add_restaurant('Geprek Joder Ka Dhani', {
    'Ayam Geprek': {"Price": 16000, "Ingredients": ["Chicken", "Chili Paste", "Tomato", "Spices", "Meat", "Animal Products", "flour"]},
    'Cumi Geprek': {"Price": 17000, "Ingredients": ["Calamari", "Chili Paste", "Tomato", "Spices", "Meat", "Animal Products" , "flour"]},
})

restaurant_graph.add_restaurant('Mie Gacoan Manyar', {
    'Mie Hompimpa': {"Price": 16000, "Ingredients": ["Egg Noodles", "Chicken", "Vegetables", "Special Sauce", "Meat", "Animal Products", "flour"]},
})
  
# Menambahkan edge antar restoran beserta jaraknya
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

# Menambahkan fungsi heuristik untuk A* search
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

# Eksekusi program
restaurant_graph.run_application()
restaurant_graph.display_filtered_menus()

# Menampilkan graph
# restaurant_graph.draw_graph()