import ast
import os
import re

import networkx as nx
import matplotlib.pyplot as plt
from networkx import DiGraph

from src.utils import log


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.current_class = None
        self.current_function = None

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.graph.add_node(self.current_class, type='class')
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        function_name = node.name
        if self.current_class:
            function_name = f"{self.current_class}.{function_name}"
        self.graph.add_node(function_name, type='function')
        if self.current_function:
            self.graph.add_edge(self.current_function, function_name)
        elif self.current_class:
            self.graph.add_edge(self.current_class, function_name)
        self.current_function = function_name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
            if self.current_function:
                self.graph.add_edge(self.current_function, function_name)
        elif isinstance(node.func, ast.Attribute):
            function_name = f"{node.func.value.id}.{node.func.attr}"
            if self.current_function:
                self.graph.add_edge(self.current_function, function_name)
        self.generic_visit(node)


def analyze_code(directory):
    analyzer = CodeAnalyzer()
    for root, _, files in os.walk(directory):
        for file in files:

            if re.match(r".*\.py$", file) and re.match(r".*__init__$", file) is None:
                with open(os.path.join(root, file), 'r') as f:
                    tree = ast.parse(f.read(), filename=file)
                    analyzer.visit(tree)
    return analyzer.graph


def draw_graph(graph, file_path):

    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(12, 12))
    node_colors = ['skyblue' if node_data.get('type', None) == 'class' else 'lightgreen' for _, node_data in
                   graph.nodes(data=True)]
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color=node_colors, font_size=10, font_weight="bold",
            edge_color="gray")
    plt.title("Class and Function Communication")
    plt.savefig(file_path)
    plt.close()


def main():
    directory = "./src"  # Set your project directory path
    graph: DiGraph = analyze_code(directory)

    file_path: str = "analyze_result/code_analyze_communication.png"
    draw_graph(graph, file_path)
    print(f"Graph saved as {file_path}")


if __name__ == "__main__":
    main()
