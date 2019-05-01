# coding: cp1251

import sys
import time
import random
import gzip
import shutil
from pathlib import Path

fileDir = "e:\\test\\logs"
fileNameTemplate = "testLog"
sizeThreshold = 2048 * 5 # 1 kibibytes

def genOnegin( ):
    gen1 = [ "� �����", "�� �����", "������ ��", "������", "�������", 
    "�����", "�������", "�������", "������", "�� �����?", "������ ��" ]

    gen2 = [ "������", "��������", "�����", "�������", "������",
    "��������", "������", "������", "������", "�������"]

    gen3 = [ "���������", "��������", "�������", "�������", "��������",
    "�������", "��������", "��������", "�������", "������"]

    gen4 = [ "������ ����", "��� ��������", "�� ��������", "� ���� ������", "��� ����������",
    "� ���� ������", "��-�� ����", "� ���� ����", "� ������ ������", "�� ������"]

    gen5 = [ "������� ��", "�������� ��", "������ ������", "������ �����",
    "�������� ��", "��� �����", "���� ������", "�� �������", "�������� ��"]

    gen6 = [ "����������", "����������", "������������", "�����������",
    "���������", "� ����������", "������ ���", "��� �� ������", "�����������"]

    gen7 = [ "�������", "�������", "�������", "��������", "��������",
    "��������", "��������", "�������", "�������", "���������"]

    gen8 = [ "�����", "������", "������", "������", 
    "������", "�����", "�����", "����", "������", "����"]

    gen9 = [ "������", "������", "������", "������", "�������",
    "������", "�� ����", "� ����", "�������", "������"]

    gen10 = [ "�������", "��������", "�����", "�������",
    "�������", "�������", "���� ��", "��������", "������"]

    phraze = ""
    phraze += random.choice( gen1  ) + " "
    phraze += random.choice( gen2  ) + " "
    phraze += random.choice( gen3  ) + ": "
    phraze += random.choice( gen4  ) + " "
    phraze += random.choice( gen5  ) + ", "
    phraze += "��� "
    phraze += random.choice( gen6  ) + " "
    phraze += random.choice( gen7  ) + ", "
    phraze += "��� "
    phraze += random.choice( gen8  ) + " "
    phraze += random.choice( gen9  ) + " "
    phraze += random.choice( gen10 ) + " "
    return phraze

def genPanaRu():
    phrazes = [
    "��, ����! ��� ���? ����� ���� ������� � ����.",
    "���� ��� ����! ���� � ��� ���� ����� ���!",
    "� ����� ��� ��� �� ������? ��, �� ��������� ���������!",
    "��� ������ ��� ����� � ���� ������ ����.",
    "���-����? ���� �����. ���� ������ ��� ����!",
    "��, �����! ����� ���� ��� ���� (����) � ������!",
    "��, ���� ����, ������ ����� ���, ����� ����.",
    "����: ��� �� ��� ����, ���� ���� ���� ����." ]
    return random.choice( phrazes )

def genPanaEn():
    phrazes = [
    "The quick brown fox jumps over the lazy dog.",
    "Jackdaws love my big sphinx of quartz.",
    "The five boxing wizards jump quickly." ]
    return random.choice( phrazes )

def genBlaBla():
    listOfWords = ( "spam", "bla", "eggs", "foo", "bar", "stoo", "snitzel",
                    "ice cream", "sour cream", "potato", "toast", "baz" )
    return random.choice( listOfWords )

def generateMessage( number ):

    newLine = "{0}: line {1:04d}: ".format( time.strftime("%c"), number )
    if number % 3 == 0:
        newLine += genPanaRu()
    elif number % 5 == 0:
        newLine += genPanaEn()
    elif number % 7 == 0:
        newLine += genOnegin()
    else:
        newLine += genBlaBla()
    return newLine

def main( argv ) :
    iters = 10
    if len( argv ) > 1 and (argv[1]).isnumeric():
        iters = int(argv[1])

    random.seed()

    filePath = "{0}\\{1}.log".format( fileDir, fileNameTemplate )

    if Path( filePath ).exists():
        logFile = open( filePath, "a" )
    else:
        logFile = open( filePath, "w" )

    # search for files by mask and if exists, continue counter
    # \warning template for globbing must be compatible with one that is used
    # for gzipFileName file name creation! see below
    gzipFiles = [ x.name for x in list( Path( fileDir ).glob( "{0}.*.gz".format( fileNameTemplate ) ) ) ]
    # gzipFiles.sort() not needed
    gzipFileNameCounter = len(gzipFiles) != 0 and int( (gzipFiles[-1].split('.'))[-2] ) + 1 or 0

    for it in range( iters ):

        if ((50/iters) > ((it*100/iters)%10) ) or ( ((it*100/iters)%10) > 10 - (50/iters)): # MAGIC
            print("|", sep='', end="", flush=True ) # print progress in console

        newLine = generateMessage( it )

        logFile.write( newLine + '\n' )
        logFile.flush()

        if logFile.tell() > sizeThreshold: # if more, gzip old and truncate new

            logFile.close()
            gzipFileName = "{0}.{1:04d}.gz".format( filePath, gzipFileNameCounter )
            with open( filePath, "rb" ) as inFile:
                with gzip.open( gzipFileName, "wb" ) as gzFile:
                    shutil.copyfileobj( inFile, gzFile )
            gzipFileNameCounter += 1
            logFile = open( filePath, "w" )
            #logFile.truncate()
        else:
            time.sleep( 0.6 )

    logFile.close()
    print( '' )

if __name__ == "__main__" :
    main( sys.argv )

