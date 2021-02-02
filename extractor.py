import xlsxwriter
import re


# from progress.spinner import Spinner
# xlsxwriter
# workbook = xlsxwriter.Workbook('gcmsgs.xlsx')

def allgchistory(sk, gcid):
    filename = getfilename()
    workbook = getworkbook(filename)  # workbook

    ln = len(gcid)
    history = True

    recentprevious = messageoptions()

    for x in gcid:
        if ln <= 0:
            workbook.close()
            history = False
            print("Group chat history successfully extracted.")
            break
        else:
            ln -= 1

        if re.findall('19', x):
            ch = sk.chats.chat(x)

            sheetname = cleanstring(gcid[x].topic)  # remove special characters

            worksheet = workbook.add_worksheet(sheetname)

            if recentprevious == '1':
                msg(sheetname)
                getrecentmsgs(ch, sk, worksheet, history)
            elif recentprevious == '3':
                msg(sheetname)
                getMsgs(ch, sk, worksheet, history)
            elif recentprevious == '6':
                getAllBookmark(ch, sk, worksheet, history)
                # getRecentBookmark(ch, sk, worksheet, history)

    workbook.close()
    print(f'{filename} GC History successfully retrieved!')
    # uploadfile('./docs/', filename+'.xlsx')


def removeHtmlTag(raw_txt):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_txt)
    return cleantext.strip()


def singlegchistory(sk, gcid, id):

    filename = getfilename()
    workbook = getworkbook(filename)  # generate workbook

    ch = sk.chats.chat(id)
    history = True

    recentprevious = messageoptions()

    sheetname = cleanstring(gcid[id.strip()].topic)

    worksheet = workbook.add_worksheet(sheetname)

    msg(sheetname)

    if recentprevious == '1':
        getrecentmsgs(ch, sk, worksheet, history)
    elif recentprevious == '3':
        getMsgs(ch, sk, worksheet, history)
    elif recentprevious == '6':
        # getRecentBookmark(ch, sk, worksheet, history)
        getAllBookmark(ch, sk, worksheet, history)

    workbook.close()
    print(f'{filename} GC History successfully retrieved!')


def getworkbook(filename):
    doc = './docs/'

    workbook = xlsxwriter.Workbook(doc + filename + '.xlsx')
    return workbook


def getMsgs(ch, sk, worksheet, history):
    from animatecursor import CursorAnimation
    spin = CursorAnimation()

    col = 0
    row = 0
    outer = False
    msglist = []
    spin.start()

    worksheet.write(row, col, 'Datetime')
    worksheet.write(row, col+1, 'Sent by')
    worksheet.write(row, col+2, 'Message')
    row = 1

    while history:

        gcmsgs = ch.getMsgs()

        for ms in gcmsgs:

            if re.findall('HistoryDisclosedUpdate', ms.type):  #
                print(ms.type)
                print(ms.history)
                history = False
                outer = ms.history

                break

            else:
                if sk.contacts[ms.userId]:
                    msglist.append(ms)

        if outer:
            spin.stop()
            break

    msglist.reverse()
    for ms in msglist:
        worksheet.write(row, col, str(ms.time))
        worksheet.write(row, col + 1, sk.contacts[ms.userId].name.first)
        worksheet.write(row, col + 2, removeHtmlTag(ms.content))
        row += 1

    spin.stop()


def msg(cleanString):
    print(f"Extracting: {cleanString} Chat History...")


def cleanstring(strval):
    cleanString = re.sub('\W+', ' ', strval)
    if len(cleanString) > 30:
        cleanString = cleanString[:30]

    content = cleanString.encode('utf-8').decode('utf8')
    return content


def getfilename():
    filename = input("Enter File name: ")
    return filename


def getallrecentmsgs():
    print("all recent gc msgs")


def getrecentmsgs(ch, sk, worksheet, history):
    from animatecursor import CursorAnimation
    spin = CursorAnimation()

    col = 0
    row = 0
    outer = False
    msglist = []

    spin.start()

    gcmsgs = ch.getMsgs()

    worksheet.write(row, col, 'Datetime')
    worksheet.write(row, col+1, 'Sent by')
    worksheet.write(row, col+2, 'Message')
    row = 1

    for ms in gcmsgs:

        if sk.contacts[ms.userId]:
            msglist.append(ms)

    msglist.reverse()
    for ms in msglist:
        worksheet.write(row, col, str(ms.time))
        worksheet.write(row, col + 1, sk.contacts[ms.userId].name.first)
        worksheet.write(row, col + 2, removeHtmlTag(ms.content))
        row += 1
    history = False

    spin.stop()


def messageoptions():
    val = input(
        "\nPress 1 recent messages only\nPress 3 from start to precent messages\nPress 6 Bookmark messages: ")
    if val:
        return val


def fromuser(str_val):
    text = str_val.split('/')

    text = re.sub(r"8:.*?", '', text[-1:][0])
    return text


def userid(str_val):
    text = re.sub(r"8:.*?", '', str_val)

    return text


def getRecentBookmark(ch, sk, worksheet, history):
    from animatecursor import CursorAnimation
    spin = CursorAnimation()

    col = 0
    row = 0

    worksheet.write(row, col, 'Datetime')
    worksheet.write(row, col+1, 'Sent by')
    worksheet.write(row, col+2, 'Message')
    row = 1

    spin.start()

    messages = ch.getBookMark()

    msglist = []
    for msg in messages:
        msglist.append(msg)

    msglist.reverse()

    for msg in msglist:

        try:
            if msg['properties']:
                if msg['properties']['poll']:
                    name = sk.contacts[fromuser(msg['from'])].name.first
                    worksheet.write(row, col, msg['originalarrivaltime'])
                    worksheet.write(row, col + 1, name)
                    worksheet.write(
                        row, col + 2, removeHtmlTag(msg['content']))
                    row += 1

        except KeyError as e:
            print(e)

    history = False

    spin.stop()


def plain(str_val):
    text = re.sub(r"</?(e|ss|quote|legacyquote)\b.*?>", "", str_val)
    text = re.sub(r"</?b\b.*?>", "*", text)
    text = re.sub(r"</?i\b.*?>", "_", text)
    text = re.sub(r"</?s\b.*?>", "~", text)
    text = re.sub(r"</?pre\b.*?>", "{code}", text)
    text = re.sub(r"""<a\b.*?href="(.*?)">.*?</a>""", r"\1", text)
    text = re.sub(r"""<at\b.*?id="8:(.*?)">.*?</at>""", r"@\1", text)
    text = (text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
            .replace("&quot;", "\"").replace("&apos;", "'"))
    return text


def getAllBookmark(ch, sk, worksheet, history):

    from animatecursor import CursorAnimation
    spin = CursorAnimation()

    col = 0
    row = 0

    spin.start()

    msglist = []

    worksheet.write(row, col, 'Datetime')
    worksheet.write(row, col+1, 'Sent by')
    worksheet.write(row, col+2, 'Message')
    row = 1

    while history:
        messages = ch.getMsgs()
        for msg in messages:

            msglist.append(msg)

            if re.findall('HistoryDisclosedUpdate', msg.type):  #
                print(msg.type)
                print(msg.history)
                history = False
                outer = msg.history

                break

            # print(removeHtmlTag(msg['content']))
    msglist.reverse()

    if len(msglist) > 0:
        for msg in msglist:

            try:
                if msg.bookmark:
                    if msg.bookmark['poll']:
                        name = sk.contacts[msg.userId].name.first
                        worksheet.write(row, col, str(msg.time))
                        worksheet.write(row, col + 1, name)
                        worksheet.write(
                            row, col + 2, removeHtmlTag(msg.content))
                        row += 1

            except KeyError as e:
                pass

    spin.stop()


# for msg in messages:
#     try:
#         if msg.bookmark:
#             if msg.bookmark['poll']:
#                 print(msg.content)
#                 print(msg.bookmark)
#     except KeyError as e:
#         pass
