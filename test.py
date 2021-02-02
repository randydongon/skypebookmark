from skpy import Skype
from getpass import getpass
import re
sk = Skype('katranjikamote@gmail.com', getpass())


gcid = sk.chats.recent()

# for x in gcid:
#     if re.findall('19', x):
#         print(x)

id = '19:c7c4deb4e8d0454baaca2fedaaac35da@thread.skype'

ch = sk.chats.chat(id)

messages = ch.getMsgs()

for msg in messages:
    print(msg)


# 19:e47755a127014fcdb39a1cafea48bf7c@thread.skype
# 19:ca5a16a9ae6546a188ba3475dc9a4f8c@thread.skype
# 19:8cc8f25c4edc4184a2d74dcc3a64b693@thread.skype
# 19:4bd5b85988d940e9a36e4b07b174eb4a@thread.skype
# 19:c7c4deb4e8d0454baaca2fedaaac35da@thread.skype
