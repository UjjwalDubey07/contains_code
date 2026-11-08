from graphviz import Digraph

# Create a directed graph for the food chain
food_chain = Digraph(comment='Simple Food Chain', format='png')

# Add node attributes to make it look nicer
food_chain.attr('node', shape='ellipse', style='filled', color='lightgrey')

# Define the relationships (The arrows point in the direction of energy flow)
# Grass -> Rabbit -> Fox -> Lion
# Also Grass -> Grasshopper -> Bird -> Fox
food_chain.edge('Sun', 'Grass')
food_chain.edge('Grass', 'Rabbit')
food_chain.ge('Grass', 'Grasshopper')
food_chain.edge('Rabbit', 'Fox')
food_chain.edge('Grasshopper', 'Bird')
food_chain.edge('Bird', 'Fox')
food_chain.edge('Fox', 'Lion')

# Render the graph
# This will save as 'foodchain.png' and try to open it automatically
food_chain.render('foodchain', view=True)

print("Food chain diagram generated as 'foodchain.png'!")
