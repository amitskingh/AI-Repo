def read_lines():
    print("Reading Line 1 at start")
    yield "Line 1"
    print("Reading Line 2")
    yield "Line 2"
    print("Reading Line 3")
    yield "Line 3"


if __name__ == "__main__":
    for line in read_lines():
        print(line)
