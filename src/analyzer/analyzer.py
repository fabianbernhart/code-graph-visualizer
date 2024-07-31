class CoedAnalyzer():

    def __init__(self, path: str):
        self.path = path


def analyze_code(directory):
    analyzer = CodeAnalyzer()
    for root, _, files in os.walk(directory):
        for file in files:
            print(file)
            # if re.match(r".*\.py$", file) and re.match(r".*__init__$", file) is None:
            #     with open(os.path.join(root, file), 'r') as f:
            #         tree = ast.parse(f.read(), filename=file)
            #         analyzer.visit(tree)
    return analyzer.graph
