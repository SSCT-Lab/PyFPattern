@skipIf((sys.platform == 'win32'), 'Named pipes are Unix-only.')
def test_file_from_named_pipe_response(self):
    with tempfile.TemporaryDirectory() as temp_dir:
        pipe_file = os.path.join(temp_dir, 'named_pipe')
        os.mkfifo(pipe_file)
        pipe_for_read = os.open(pipe_file, (os.O_RDONLY | os.O_NONBLOCK))
        with open(pipe_file, 'wb') as pipe_for_write:
            pipe_for_write.write(b'binary content')
        response = FileResponse(os.fdopen(pipe_for_read, mode='rb'))
        self.assertEqual(list(response), [b'binary content'])
        response.close()
        self.assertFalse(response.has_header('Content-Length'))