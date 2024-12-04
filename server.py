import http.server
import os

class case_no_file(object):
    ''' File or directory does not exist. '''

    def test(self, handler):
        return not os.path.exists(handler.full_path)
    
    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))
    
class case_existing_file(object):
    ''' File exists. '''

    def test(self, handler):
        return os.path.exists(handler.full_path)
    
    def act(self, handler):
        handler.handle_file(handler.full_path)

class case_always_fail(object):
    ''' Base case if nothing else worked. '''

    def test(self, handler):
        return True
    
    def act(self, handler):
        raise ServerException("Unkown object '{0}'".format(handler.path))

class ServerException(Exception):
    """Custom exception to represent server-related errors."""
    def __init__(self, message):
        super().__init__(message)


class RequestHandler(http.server.BaseHTTPRequestHandler):
    '''Handle HTTP requests by returning a fixed "page"'''
    
    # page to send back.
#     Page = '''\
# <html>
# <body>
# <table>
# <tr> <td>Header</td> <td>Value</td> </tr>
# <tr> <td>Date and time</td> <td>{date_time}</td> </tr>
# <tr> <td>Client host</td> <td>{client_host}</td> </tr>
# <tr> <td>Client port</td> <td>{client_port}s</td> </tr>
# <tr> <td>Command</td> <td>{command}</td> </tr>
# <tr> <td>Path</td> <td>{path}</td> </tr>
# </table>
# </body>
# </html>
# '''

    # error page
    Error_Page = '''\
<html>
<body>
<h1>Error accessing {path}</h1>
<p>{msg}</p>
</body>
</html>
'''

    # handle a GET request.
    def do_GET(self):
        try:
            # figure out what exactly is being requested
            self.full_path = os.getcwd() + self.path

            # figure out how to handle it
            for case in self.Cases:
                handler = case()
                if handler.test(self):
                    handler.act(self)
                    break
        
        # handle errors
        except Exception as msg:
            self.handle_error(msg)

    def handle_file(self, full_path):
        try:
            with open(full_path, "rb") as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(self.path, msg)

    # def create_page(self):
    #     values = {
    #         "date_time": self.date_time_string(),
    #         "client_host": self.client_address[0],
    #         "client_port": self.client_address[1],
    #         "command": self.command,
    #         "path": self.path
    #     }

    #     page = self.Page.format(**values).encode("utf-8")
    #     return page

    # def send_page(self, page):
    #     self.send_response(200)
    #     self.send_header("Content-type", "text/html")
    #     self.send_header("Content-length", str(len(page)))
    #     self.end_headers()
    #     self.wfile.write(page)

    # send actual content
    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    # handle unknown objects
    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content, 404)

#----------------------------------------------------------------------

if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = http.server.HTTPServer(serverAddress, RequestHandler)
    print("Serving on port 8080...")
    server.serve_forever()
