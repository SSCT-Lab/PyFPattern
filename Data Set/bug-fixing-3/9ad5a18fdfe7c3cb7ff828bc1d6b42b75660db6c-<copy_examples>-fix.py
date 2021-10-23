def copy_examples(examples_dir, destination_dir):
    'Copy the examples directory in the documentation.\n\n    Prettify files by extracting the docstrings written in Markdown.\n    '
    pathlib.Path(destination_dir).mkdir(exist_ok=True)
    for file in os.listdir(examples_dir):
        if (not file.endswith('.py')):
            continue
        module_path = os.path.join(examples_dir, file)
        (docstring, starting_line) = get_module_docstring(module_path)
        destination_file = os.path.join(destination_dir, (file[:(- 2)] + 'md'))
        with open(destination_file, 'w+', encoding='utf-8') as f_out, open(os.path.join(examples_dir, file), 'r+', encoding='utf-8') as f_in:
            f_out.write((docstring + '\n\n'))
            for _ in range(starting_line):
                next(f_in)
            f_out.write('```python\n')
            line = next(f_in)
            if (line != '\n'):
                f_out.write(line)
            for line in f_in:
                f_out.write(line)
            f_out.write('```')