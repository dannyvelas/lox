import sys


def defineVisitor(file, base_name, types):
    file.write("  interface Visitor<R> {\n")

    for type in types:
        type_name = type.split(":")[0].strip()
        file.write(
            f"    R visit{type_name}{base_name}({type_name} {base_name.lower()});\n")

    file.write("  }\n")


def defineType(file, base_name, class_name, field_list):
    file.write(f" static class {class_name} extends {base_name} {{\n"
               f"    {class_name}({field_list}) {{\n")
    fields = field_list.split(", ")

    # store values in each field
    for field in fields:
        name = field.split(" ")[1]
        file.write(f"      this.{name} = {name};\n")
    file.write("    }\n\n")

    # visitor pattern
    file.write("\n"
               "    @Override\n"
               "    <R> R accept(Visitor<R> visitor) {\n"
               f"      return visitor.visit{class_name}{base_name}(this);\n"
               "    }\n")

    # declare fields
    for field in fields:
        file.write(f"    final {field};\n")
    file.write("  }\n")


def defineAst(output_dir, base_name, types):
    path = output_dir + base_name + ".java"
    with open(path, "w") as file:
        file.write("package lox;\n\n"
                   "import java.util.List;\n\n"
                   "abstract class " + base_name + " {\n")

        defineVisitor(file, base_name, types)
        for type in types:
            class_name = type.split(":")[0].strip()
            fields = type.split(":")[1].strip()
            defineType(file, base_name, class_name, fields)

        file.write("\n"
                   "  abstract <R> R accept(Visitor<R> visitor);\n"
                   "}\n")


if len(sys.argv) != 2:
    print('Usage: generate_ast <dir>')

output_dir = sys.argv[1]
defineAst(output_dir, "Expr", ["Binary : Expr left, Token operator, Expr right",
                               "Grouping : Expr expression",
                               "Literal : Object value",
                               "Unary : Token operator, Expr right"])
