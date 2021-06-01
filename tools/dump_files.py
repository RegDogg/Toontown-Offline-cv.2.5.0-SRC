# This is the following script I used to Dump all the Frozen Modules in Toontown Offline cv.2.5.0
# Requires Immunity Debugger
import immlib

DESC = 'PyCommand to dump frozen python modules'
PYTHONMAGIC = '\x03\xF3\x0D\x0A\x00\x00\x00\x00' # Change this value according to the version of python used. The value given here is for Python 2.7

'''
Run this pycommand when all frozen modules are loaded.
This will dump each frozen module in a .pyc file in 
immunity debugger installation directory
'''

def main(args):
    imm = immlib.Debugger()
    addr = imm.getAddress('PyImport_FrozenModules')
    structAddr = imm.readLong(addr)

    while True:
        ptrToName = imm.readLong(structAddr)
        ptrToCode = imm.readLong(structAddr + 4)
        sizeOfCode = imm.readLong(structAddr + 8)
        structAddr += 12

        # The array is terminated by a structure whose members are null
        if ptrToName == 0 and ptrToCode == 0 and sizeOfCode == 0:
            break

        if sizeOfCode > 0 and sizeOfCode < 2147483647:            
            moduleName = imm.readString(ptrToName)
            moduleCode = imm.readMemory(ptrToCode, sizeOfCode)

            # You can change the output path here
            open(moduleName + '.pyc', 'wb').write(PYTHONMAGIC + moduleCode) 

    return '[*] Frozen modules dumped'
