#!/usr/bin/python3

def checkHashAlgorithmChoice(__algorithmString):

    from sys import exit
    __acceptableChoices = ['dhash', 'dhash_vertical', 'average_hash', 'phash', 'phash_simple', 'whash']
    if __algorithmString not in __acceptableChoices:
        print("Error: please choose a valid hash algorithm")
        exit()

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

def generateHashDict(__imagePathList, __hashAlgorithm):

    from PIL import Image
    from imagehash import dhash
    from imagehash import dhash_vertical
    from imagehash import average_hash
    from imagehash import phash
    from imagehash import phash_simple
    from imagehash import whash

    __imageHashDict = {}
    __image = None

    for __imagePath in __imagePathList:
        print("Hashing " + str(__imagePath))
        __image = Image.open(__imagePath)
        if __hashAlgorithm == 'dhash':
            __imageHashDict[__imagePath] = dhash(__image)
        elif __hashAlgorithm == 'dhash_vertical':
            __imageHashDict[__imagePath] = dhash_vertical(__image)
        elif __hashAlgorithm == 'average_hash':
            __imageHashDict[__imagePath] = average_hash(__image)
        elif __hashAlgorithm == 'phash':
            __imageHashDict[__imagePath] = phash(__image)
        elif __hashAlgorithm == 'phash_simple':
            __imageHashDict[__imagePath] = phash_simple(__image)
        elif __hashAlgorithm == 'whash':
            __imageHashDict[__imagePath] = whash(__image)
        elif __hashAlgorithm == None:
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
    __parser.add_argument("-a", "--algorithm", type=str, help="Specify a hash algorithm to use. Acceptable inputs:\n'dhash' (horizontal difference hash),\n'dhash_vertical',\n'average_hash',\n'phash' (perceptual hash),\n'phash_simple',\n'whash' (wavelet hash)")
    __args = __parser.parse_args()

    if __args.algorithm is not None:
        checkHashAlgorithmChoice(__args.algorithm)
    if __args.directory is not None:
        displayImage(storeDuplicates(compareHashes(generateHashDict(getImagePaths(__args.directory), __args.algorithm))))
    else:
        displayImage(storeDuplicates(compareHashes(generateHashDict(getImagePaths(os.path.curdir), __args.algorithm))))
    exit()

main()
