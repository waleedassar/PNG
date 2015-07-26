import os,sys,time,struct
import zlib


#And Vice Versa
def LittleToBigEndian(IntX):
    if IntX == 0:
        return 0
    StrX = struct.pack("L",IntX)
    if len(StrX) != 4:
        return 0
    NewStrX = ""
    NewStrX += StrX[3]
    NewStrX += StrX[2]
    NewStrX += StrX[1]
    NewStrX += StrX[0]
    NewIntX = (struct.unpack("L",NewStrX))[0]
    return NewIntX


if len(sys.argv) != 2:
    print "Usage: ParsePNG.py input.png\r\n"
    sys.exit(-1)

inF = sys.argv[1]

if os.path.exists(inF)==False or \
   os.path.getsize(inF)==0:
    print "File does not exist or empty\r\n"
    sys.exit(-2)

LenF = os.path.getsize(inF)


if LenF <= 8:
    print "File is too small\r\n"
    sys.exit(-3)

fIn = open(inF,"rb")
fCon = fIn.read()
fIn.close()

ix = 0
Magic = fCon[0:8]

ix = 8

if Magic == "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a":
    print "PNG Magic found"
First = True
NumOfChunks = 0
IDAT_All = ""

while ix < LenF:
    LenChunk = 0
    sChunkType = ""
    ChunkData = ""
    CRC = 0
    if ix + 8 < LenF:
        sLenChunk = fCon[ix:ix+4]
        ix += 4
        LenChunk_bg = (struct.unpack("L",sLenChunk))[0]
        LenChunk = LittleToBigEndian(LenChunk_bg)
        print hex(LenChunk)
        sChunkType = fCon[ix:ix+4]
        print sChunkType
        #--------------IHDR-----------------------------
        if sChunkType == "IHDR" and First == False:
            print "Warning: IHDR Chunk is not the first chunk"
        else:
            First = False
        if sChunkType[0].isupper()==True:
            print "***Critical***"
        else:
            print "***Ancillary***"
        if sChunkType[1].isupper()==True:
            print "***Public***"
        else:
            print "***Private***"
        if sChunkType[2].isupper()==False:
            print "Warning: Abnormal Chunk (Does not comply to specifications)"
        #--------------------------------------------------
        ix += 4
    if ix + LenChunk < LenF:
        ChunkData = fCon[ix:ix+LenChunk]
        ix += LenChunk
        if sChunkType == "IDAT":
            IDAT_All += ChunkData
        print ChunkData
    if ix + 4 <= LenF:
        sCRC = fCon[ix:ix+4]
        ix += 4
        CRC = (struct.unpack("L",sCRC))[0]
        CRC = LittleToBigEndian(CRC)#Convert to Network-Order
        print "Embedded CRC: " + str(hex(CRC))

        TempDataForCRC = sChunkType + ChunkData
        CRC_calc = (zlib.crc32(TempDataForCRC)) & 0xFFFFFFFF
        print "Calculated CRC: " + str(hex(CRC_calc))
        if CRC_calc != CRC:
            print "Warning: CRC for current chunk does not match"
        if ix == LenF:
            print "End of PNG"
            break
    NumOfChunks += 1

print "Finished parsing " + str(NumOfChunks+1) + " Chunks"
sys.exit(0)

    
