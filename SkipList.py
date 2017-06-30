import os

class SkipList:
    def __init__(self):
        self.TheSkipList = []

        if os.path.isfile('SkipList.txt'):
            fd = open('SkipList.txt', 'r')
            Lines = fd.readlines()
            fd.close()
            for line in Lines:
                self.TheSkipList.append(line.strip('\n'))

    def GetSkipList(self):
        return self.TheSkipList