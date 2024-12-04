from datetime import datetime

# Print the correct Content-Type header
print("Content-Type: text/html")  # Content-type header for HTML
print()  # Blank line separating headers from body content

# Print the HTML content with the current date and time
print("<html><body><p>Generated {0}</p></body></html>".format(datetime.now()))
