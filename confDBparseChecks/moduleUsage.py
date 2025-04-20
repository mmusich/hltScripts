import ast
import sys
from collections import defaultdict

class ModuleUsageAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.producers = set()
        self.usage_counts = defaultdict(int)

    def visit_Assign(self, node):
        # Check for: process.moduleLabel = cms.EDProducer(...)
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
            cms_type = node.value.func.attr
            if cms_type == 'EDProducer':
                for target in node.targets:
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                        if target.value.id == 'process':
                            label = target.attr
                            self.producers.add(label)
                            self.usage_counts[label] += 1  # Declaration counts as 1 use
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Catch all references to process.<something>
        if isinstance(node.value, ast.Name) and node.value.id == 'process':
            label = node.attr
            self.usage_counts[label] += 1
        self.generic_visit(node)

def find_unused_producers(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read(), filename=file_path)

    analyzer = ModuleUsageAnalyzer()
    analyzer.visit(tree)

    for label in analyzer.producers:
        print(label)
    
    unused = sorted([
        label for label in analyzer.producers
        if analyzer.usage_counts[label] == 1  # Only defined once
    ])

    print("\n=== Possibly Unused EDProducers (Declared but not referenced again) ===")
    for label in unused:
        print(label)

    print(f"\nTotal EDProducers: {len(analyzer.producers)}")
    print(f"Possibly unused: {len(unused)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python find_unused_producers.py fullHLTConfig_dumped.py")
        sys.exit(1)
    find_unused_producers(sys.argv[1])
