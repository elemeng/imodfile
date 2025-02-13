import argparse
from imodfile import parse_imod, write_imod


def apply_operations(points, operations):
    """
    Apply coordinate operations to a list of points.

    Args:
        points (list of tuple): List of (x, y, z) coordinates.
        operations (dict): Dictionary of operations to apply.

    Returns:
        list of tuple: List of modified (x, y, z) coordinates.
    """
    for i, (x, y, z) in enumerate(points):
        if "add" in operations:
            x += operations["add"]
            y += operations["add"]
            z += operations["add"]
        if "subtract" in operations:
            x -= operations["subtract"]
            y -= operations["subtract"]
            z -= operations["subtract"]
        if "multiply" in operations:
            x *= operations["multiply"]
            y *= operations["multiply"]
            z *= operations["multiply"]
        if "divide" in operations:
            x /= operations["divide"]
            y /= operations["divide"]
            z /= operations["divide"]
        points[i] = (x, y, z)
    return points


def convert(input_file, output_file, operations):
    """
    Convert an IMOD file and apply coordinate operations.

    Args:
        input_file (str): Path to the input IMOD file.
        output_file (str): Path to the output IMOD file.
        operations (dict): Dictionary of operations to apply.
    """
    try:
        model = parse_imod(input_file)
    except Exception as e:
        print(f"Error parsing IMOD file: {e}")
        return

    for obj in model.objects:
        for contour in obj.contours:
            contour.points = apply_operations(contour.points, operations)

    try:
        write_imod(model, output_file)
    except Exception as e:
        print(f"Error writing IMOD file: {e}")


def convert_to_starfile(input_file, output_file, operations):
    """
    Convert an IMOD file to a Relion starfile and apply coordinate operations.

    Args:
        input_file (str): Path to the input IMOD file.
        output_file (str): Path to the output starfile.
        operations (dict): Dictionary of operations to apply.
    """
    try:
        model = parse_imod(input_file)
    except Exception as e:
        print(f"Error parsing IMOD file: {e}")
        return

    try:
        with open(output_file, "w") as f:
            f.write("\ndata_\n\nloop_\n")
            f.write("_rlnCoordinateX #1\n")
            f.write("_rlnCoordinateY #2\n")
            f.write("_rlnCoordinateZ #3\n")

            for obj in model.objects:
                for contour in obj.contours:
                    contour.points = apply_operations(contour.points, operations)
                    for point in contour.points:
                        f.write(f"{point[0]} {point[1]} {point[2]}\n")
    except Exception as e:
        print(f"Error writing starfile: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert IMOD files and apply coordinate operations."
    )
    parser.add_argument("input_file", type=str, help="Path to the input file.")
    parser.add_argument("output_file", type=str, help="Path to the output file.")
    parser.add_argument(
        "--add", type=float, help="Add constant to coordinates.", default=0
    )
    parser.add_argument(
        "--subtract", type=float, help="Subtract constant from coordinates.", default=0
    )
    parser.add_argument(
        "--multiply", type=float, help="Multiply coordinates by constant.", default=1
    )
    parser.add_argument(
        "--divide", type=float, help="Divide coordinates by constant.", default=1
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["mod", "star"],
        default="mod",
        help="Output file format: 'mod' or 'star'.",
    )

    args = parser.parse_args()

    operations = {
        "add": args.add,
        "subtract": args.subtract,
        "multiply": args.multiply,
        "divide": args.divide,
    }

    if args.format == "mod":
        convert(args.input_file, args.output_file, operations)
    elif args.format == "star":
        convert_to_starfile(args.input_file, args.output_file, operations)
