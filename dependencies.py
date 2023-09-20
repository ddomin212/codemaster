import os

from graphviz import Digraph


def get_dependencies():
    print(os.listdir("/home/dan/Documents/bnb_ai"))


def create_chart():
    # Create a Digraph object
    dot = Digraph(
        format="pdf"
    )  # You can specify the output format (e.g., 'png', 'pdf', 'svg', etc.)

    # Define nodes
    dot.node("A")
    dot.node("B")
    dot.node("C")

    # Define edges to represent dependencies
    dot.edge("A", "B")
    dot.edge("B", "C")
    dot.edge("A", "C")

    # Customize node appearance
    dot.node("A", color="blue", shape="ellipse")
    dot.node("B", color="green", shape="box")
    dot.node("C", color="red", shape="diamond")

    # Render and save the graph as an image
    dot.render("dependency_graph")

    dot.view()
