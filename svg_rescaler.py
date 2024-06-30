import xml.etree.ElementTree as ET
import sys
import re

# Register namespaces to ensure they are preserved in the output
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

def scale_svg_path(svg_file, output_file, scale_factor):
    tree = ET.parse(svg_file)
    root = tree.getroot()

    def scale_coord(coord):
        numbers = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", coord)
        scaled_numbers = [str(float(number) * scale_factor) for number in numbers]
        scaled_coord = re.sub(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", lambda match: scaled_numbers.pop(0), coord, count=len(numbers))
        return scaled_coord

    for path in root.findall('.//{http://www.w3.org/2000/svg}path'):
        d_attr = path.get('d')
        if d_attr:
            commands = re.split('([A-Za-z])', d_attr)[1:]
            scaled_commands = []
            for i in range(0, len(commands), 2):
                command = commands[i] + scale_coord(commands[i + 1])
                scaled_commands.append(command)
            path.set('d', ''.join(scaled_commands))

    # Write the modified tree to the output file without using default_namespace
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python scale_svg.py <input_svg> <output_svg> <scale_factor>")
        sys.exit(1)
    input_svg = sys.argv[1]
    output_svg = sys.argv[2]
    scale_factor = float(sys.argv[3])
    scale_svg_path(input_svg, output_svg, scale_factor)
