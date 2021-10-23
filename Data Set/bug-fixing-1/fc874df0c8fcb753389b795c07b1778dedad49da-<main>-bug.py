

def main():
    (symbol_string, output_name) = proto2script(sys.argv[1])
    if (len(sys.argv) > 2):
        with open(sys.argv[2], 'w') as fout:
            fout.write(symbol_string)
    else:
        print(symbol_string)
