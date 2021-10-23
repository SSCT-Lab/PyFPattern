def nested_view(request):
    '\n    A view that uses test client to call another view.\n    '
    setup_test_environment()
    c = Client()
    c.get('/no_template_view/')
    return render(request, 'base.html', {
        'nested': 'yes',
    })