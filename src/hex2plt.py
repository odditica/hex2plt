from sys import argv;
import math;
import os;
import struct;

def waitForKey():
  try:
      os.system('pause'); 
  except ImportError:
      os.system('read -p "Press any key to continue"');

def allowChars(string, chars):
    tempString = string;
    buildString = "";
    for x in range(0, len(tempString)):
        contains = 0;
        for y in range(0, len(chars)):
            if (tempString[x] == chars[y]):
                contains = 1;
                break;
        if (contains):
            buildString += tempString[x];
    return buildString;

def write16BitUIntToFile(file, num):
    file.write(struct.pack('>H', num));

print("\n╔════════════╗ | made by blokatt in 2016");
print("║hex2plt v1.0║ | blokatt.net");
print("╚════════════╝ | @blokatt\n");
print("");

if (len(argv) == 1):
    print("No input file!");
    waitForKey();
    quit();

script, inputFilename = argv;

try:
    if (inputFilename.endswith(".pal")):
        print("File is already in .pal format!");
        quit();
    file = open(inputFilename);
except:
    print("Couldn't open input file!");
    waitForKey();
    quit();

print("Input file: " + inputFilename);
content = file.read();
file.close();
content = allowChars(content, "0123456789ABCDEFabcdef").upper();
colorCount = math.floor(len(content) / 6);
print("Detected " + str(colorCount) + " colours.\n" + "=" * 10);
extensionLength = len(os.path.splitext(os.path.basename(inputFilename))[1]);
fileNameNoPath = os.path.splitext(os.path.basename(inputFilename))[0];

###pal
outputFilename = inputFilename[:-extensionLength] + ".pal";
outputFile = open(outputFilename, 'w');
outputFile.write("JASC-PAL\n");
outputFile.write("0100\n");
outputFile.write(str(colorCount) + "\n");
for x in range(0, colorCount):
    for y in range(0, 3):
        outputFile.write(str(int("0x" + content[(x * 6 + y * 2):(x * 6 + y * 2) + 2], 0)) + " ");
    outputFile.write("\n");    
outputFile.close();
print("PAL: " + outputFilename);

###paint.net
outputFilename = inputFilename[:-extensionLength] + "_pn.txt";
outputFile = open(outputFilename, 'w');
for x in range(0, colorCount):
    outputFile.write("FF");  
    for y in range(0, 3):
        outputFile.write(content[(x * 6 + y * 2):(x * 6 + y * 2) + 2]);
    outputFile.write("\n");    
outputFile.close();
print("Paint.NET (.txt): " + outputFilename);

###photoshop
outputFilename = inputFilename[:-extensionLength] + ".aco";
outputFile = open(outputFilename, "wb");

#version 1
write16BitUIntToFile(outputFile, 1);
write16BitUIntToFile(outputFile, colorCount);
for x in range(0, colorCount):
    write16BitUIntToFile(outputFile, 0);
    for y in range(0, 3):
        write16BitUIntToFile(outputFile, math.ceil(65535 * int("0x" + content[(x * 6 + y * 2):(x * 6 + y * 2) + 2], 0) / 255));
    write16BitUIntToFile(outputFile, 0);
#version 2
write16BitUIntToFile(outputFile, 2);
write16BitUIntToFile(outputFile, colorCount);
for x in range(0, colorCount):
    write16BitUIntToFile(outputFile, 0);
    for y in range(0, 3):
        write16BitUIntToFile(outputFile, math.ceil(65535 * int("0x" + content[(x * 6 + y * 2):(x * 6 + y * 2) + 2], 0) / 255));
    write16BitUIntToFile(outputFile, 0);
    write16BitUIntToFile(outputFile, 0);
    write16BitUIntToFile(outputFile, 0);
outputFile.close();
print("Photoshop (.aco): " + outputFilename);

###gimp
outputFilename = inputFilename[:-extensionLength] + ".gpl";
outputFile = open(outputFilename, 'w');
outputFile.write("GIMP Palette\nName: " + fileNameNoPath + "\nColumns: 3\n");
for x in range(0, colorCount):
    for y in range(0, 3):
        outputFile.write(str(int("0x" + content[(x * 6 + y * 2):(x * 6 + y * 2) + 2], 0)) + " ");
    outputFile.write("\n");    
outputFile.close();  
print("Gimp (.gpl): " + outputFilename);
print("\nAll done.");
waitForKey();


