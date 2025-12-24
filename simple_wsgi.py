message = b"Hello, World!"


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")

    print(environ.get("QUERY_STRING", ""))

    if method == "POST":
        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            content_length = 0

        if content_length > 0:
            print(
                environ["wsgi.input"].read(content_length).decode("utf-8")
            )

    status = "200 OK"
    headers = [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(message)))
    ]

    start_response(status, headers)
    return [message]