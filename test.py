import re

pattern = r"(\w{3})(_|-)(\d{8})(_|-)(\d{6})(\w*)"
string = "IMG_20230101_123456"

match = re.match(pattern, string)
if match:
    print("Pattern matched!")
    print("Match object:", match)
    print("Matched groups:", match.groups())
    print("Start position:", match.start())
    print("End position:", match.end())
    print("Span:", match.span())
else:
    print("No match found.")