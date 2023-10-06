from bb.utils import richprint


def test_str_print():
    richprint.str_print("Hello, world!", "bold white")
    # The output should be "Hello, world!" in bold white style.


def test_table():
    header_args = {"name": "Name", "age": "Age", "gender": "Gender"}
    value_args = [
        {"name": "Alice", "age": 25, "gender": "Female"},
        {"name": "Bob", "age": 30, "gender": "Male"},
        {"name": "Charlie", "age": 35, "gender": "Male"},
    ]
    table = richprint.table(header_args, value_args, True)
    # The output should be a table with the given header and values.
