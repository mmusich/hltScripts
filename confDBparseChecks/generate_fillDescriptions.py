import re
import sys
import os

def parse_parameters(filename):
    parameters = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            match = re.search(r'get(Untracked)?Parameter<(.+?)>\("(.+?)"(?:, (.+?))?\)', line)
            if match:
                untracked = bool(match.group(1))
                param_type = match.group(2)
                param_name = match.group(3)
                default_value = match.group(4) if match.group(4) else None

                parameters.append((param_name, param_type, default_value, untracked))

    return parameters

def generate_class_name(filename):
    # Extract the base name without extension
    base_name = os.path.splitext(os.path.basename(filename))[0]
    return base_name

def generate_class_name2(filename):
    # Extract the base name without extension
    base_name = os.path.splitext(os.path.basename(filename))[0]
    # Convert to CamelCase
    class_name = ''.join(word.capitalize() for word in base_name.split('_'))
    return class_name

def generate_fillDescriptions(class_name, parameters):
    description_lines = []
    description_lines.append(f"void {class_name}::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {{")
    description_lines.append("  edm::ParameterSetDescription desc;")

    for param in parameters:
        param_name, param_type, default_value, untracked = param

        if untracked:
            param_call = f'desc.addUntracked<{param_type}>("{param_name}"'
        else:
            param_call = f'desc.add<{param_type}>("{param_name}"'

        if default_value is not None:
            param_call += f', {default_value}'

        param_call += ");"
        description_lines.append(f"  {param_call}")

    description_lines.append('  descriptions.addWithDefaultLabel(desc);')
    description_lines.append("}")

    return "\n".join(description_lines)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_fillDescriptions.py <path_to_plugin_file>")
        sys.exit(1)

    plugin_filename = sys.argv[1]
    parameters = parse_parameters(plugin_filename)
    class_name = generate_class_name(plugin_filename)
    fill_descriptions_code = generate_fillDescriptions(class_name, parameters)

    print(fill_descriptions_code)
