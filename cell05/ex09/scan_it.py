import sys
import re

if len(sys.argv) != 3:
    print("none")
else:
    keyword = sys.argv[1]
    text = sys.argv[2]
    match = re.findall(re.escape(keyword),text)
    if not match:
        print("none")
    else:
        print(len(match))
        
