import os


class MsgFile:

    @classmethod
    def done_replace(cls):
        try:
            file = open('donereplace.txt')
            if file:
                return True
            else:
                return False
        except FileNotFoundError as e:
            return False

    @classmethod
    def find_file(cls, basedir='/', filename='msg.py'):
        for dirname, dirs, files in os.walk(basedir):
            if filename in files:
                yield os.path.join(dirname, filename)

    @classmethod
    def replaceMsg(cls, file_to_replace, file_found):

        print('File found at: ', file_to_replace)

        val_input = input("\nTo replace msg.py, Press 1 or 0 to exit: ")

        if file_found and val_input == '1' and file_to_replace:
            # return
            if file_to_replace:
                dir_list = file_to_replace.split('/')
                if 'skpy' in dir_list:
                    index = dir_list.index('skpy')
                    print(index, dir_list[index+1])
                    if dir_list[index+1] == 'msg.py':
                        with open(file_to_replace, 'rt') as old_file:
                            old_data = old_file.read()
                            char_index = old_data.find('def uriObject')
                            old_file.close()
                            if old_data[char_index: char_index+13] == 'def uriObject':
                                with open('msg.py', 'rt') as file:
                                    data = file.read()

                                    file.close()
                                    with open(file_to_replace, 'wt') as new_file:
                                        new_file.write(data)
                                        new_file.close()

                                    with open('donereplace.txt', 'wt') as done_file:
                                        done_file.write("Done replace msg.py")
                                        done_file.close()

                                print("Successfully replace with new msg file!!!")
                                return True
                            else:
                                print(
                                    'Error: when trying to replace old msg to new msg.py')
                                return False
