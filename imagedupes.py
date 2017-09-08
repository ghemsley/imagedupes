#!/usr/bin/python3

def getImagePaths(__dirPath):
    "Creates a list of image paths within a given directory"

    import os

    __filePathList = []

    print("Searching for duplicate images...")
    for __root, __dirs, __files in os.walk(__dirPath, followlinks=True):
        for __file in __files:
            if str(__file).endswith(".jpg") or str(__file).endswith(".jpeg") or str(__file).endswith(".png"):
                __filePathList.append(os.path.join(__root, __file))
    return __filePathList

def generateHashDict(__imagePathList):

    from PIL import Image
    from imagehash import phash

    __imageHashDict = {}
    __image = None

    for __imagePath in __imagePathList:
        print("Hashing " + str(__imagePath))
        __image = Image.open(__imagePath)
        __imageHashDict[__imagePath] = phash(__image)
        __image.close

    return __imageHashDict


def compareHashes(__imageHashDict):

    __reverseMultiDict = {}
    __duplicateListOfSets = {}
    __duplicateListOfLists = []

    for __key, __value in __imageHashDict.items():
        __reverseMultiDict.setdefault(__value, set()).add(__key)
    __duplicateListOfSets = [__values for __key, __values in __reverseMultiDict.items() if len(__values) > 1]
    for __i in range(0, len(__duplicateListOfSets)):
        __duplicateListOfLists.append(list(__duplicateListOfSets[__i]))
    return __duplicateListOfLists

def storeDuplicates(__duplicateListOfLists):

    from PIL import Image

    __imageList = []

    for __i in range(0, len(__duplicateListOfLists)):
        for __j in range(0, len(__duplicateListOfLists[__i])):
            print("Found duplicate: " + str(__duplicateListOfLists[__i][__j]))
            __imageList.append(__duplicateListOfLists[__i][__j])
    return __imageList

def displayImage(__imageList):

    import webbrowser

    for __image in __imageList:
        webbrowser.open(__image)

def main():

    from argparse import ArgumentParser
    from sys import exit

    __parser = ArgumentParser()
    __parser.add_argument("-d", "--directory", help="Directory to search for images")
    __args = __parser.parse_args()

    if __args.directory is not None:
        displayImage(storeDuplicates(compareHashes(generateHashDict(getImagePaths(__args.directory)))))
    else:
        displayImage(storeDuplicates(compareHashes(generateHashDict(getImagePaths(os.path.curdir)))))
    exit()

main()
