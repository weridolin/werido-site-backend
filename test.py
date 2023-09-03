import re
commit_content = """message:xxx
author:xxx"""
message,author = re.findall(r"message:(.*)\nauthor:(.*)",commit_content)[0]
print(message,author)