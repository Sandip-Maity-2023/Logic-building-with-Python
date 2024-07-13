def print_10th_line(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 10:
                print(lines[9].strip())
            else:
                print("The file contains less than 10 lines")
    except FileNotFoundError:
        print(f"The file {filename} does not exist")

print_10th_line('file.txt')
