#!/usr/bin/env python


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    sum = 0
    for a in args:
      sum += int(a)
    return str(sum)


def subtract(*args):
    result = int(args[0]) - int(args[1])
    return str(result)


def multiply(*args):
    result = int(args[0]) * int(args[1])

    return str(result)


def divide(*args):
    try:
        result = int(args[0]) / int(args[1])
        return str(result)
    except ZeroDivisionError:
        return 'Error! Divide by zero'


def index_page():
    body = ['<h1>Here is how to use this page...</h1>', '<ul>']
    body.append('/add/1/2 == 1+2</ul>')
    body.append('<ul>/subtract/10/5 == 10-5</ul>')
    body.append('<ul>/multiply2/2 == 2x2</ul>')
    body.append('<ul>/divide/10/5 == 10/5</ul>')
    return '\n'.join(body)


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
        '': index_page
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError

        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()