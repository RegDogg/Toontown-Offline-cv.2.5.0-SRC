# Embedded file name: toontown.toonbase.TTOffStart
import collections
collections.namedtuple = lambda *x: tuple
import _gamedata
from panda3d.core import loadPrcFileData
for i, config in enumerate(_gamedata.CONFIG):
    loadPrcFileData('Packaged Config Page #%d' % i, config)

from panda3d.core import StringStream
dcStream = StringStream(_gamedata.DC)
from direct.distributed import ConnectionRepository
import types

class ConnectionRepository_override(ConnectionRepository.ConnectionRepository):

    def readDCFile(self, dcFileNames = None):
        """
        Reads in the dc files listed in dcFileNames, or if
        dcFileNames is None, reads in all of the dc files listed in
        the Config.prc file.
        """
        dcFile = self.getDcFile()
        dcFile.clear()
        self.dclassesByName = {}
        self.dclassesByNumber = {}
        self.hashVal = 0
        if isinstance(dcFileNames, types.StringTypes):
            dcFileNames = [dcFileNames]
        dcImports = {}
        readResult = dcFile.read(dcStream)
        if not readResult:
            self.notify.error('Could not read dc file.')
        self.hashVal = dcFile.getHash()
        for n in range(dcFile.getNumImportModules()):
            moduleName = dcFile.getImportModule(n)[:]
            suffix = moduleName.split('/')
            moduleName = suffix[0]
            suffix = suffix[1:]
            if self.dcSuffix in suffix:
                moduleName += self.dcSuffix
            elif self.dcSuffix == 'UD' and 'AI' in suffix:
                moduleName += 'AI'
            importSymbols = []
            for i in range(dcFile.getNumImportSymbols(n)):
                symbolName = dcFile.getImportSymbol(n, i)
                suffix = symbolName.split('/')
                symbolName = suffix[0]
                suffix = suffix[1:]
                if self.dcSuffix in suffix:
                    symbolName += self.dcSuffix
                elif self.dcSuffix == 'UD' and 'AI' in suffix:
                    symbolName += 'AI'
                importSymbols.append(symbolName)

            self.importModule(dcImports, moduleName, importSymbols)

        for i in range(dcFile.getNumClasses()):
            dclass = dcFile.getClass(i)
            number = dclass.getNumber()
            className = dclass.getName() + self.dcSuffix
            classDef = dcImports.get(className)
            if classDef is None and self.dcSuffix == 'UD':
                className = dclass.getName() + 'AI'
                classDef = dcImports.get(className)
            if classDef == None:
                className = dclass.getName()
                classDef = dcImports.get(className)
            if classDef is None:
                self.notify.debug('No class definition for %s.' % className)
            else:
                if type(classDef) == types.ModuleType:
                    if not hasattr(classDef, className):
                        self.notify.warning('Module %s does not define class %s.' % (className, className))
                        continue
                    classDef = getattr(classDef, className)
                if type(classDef) != types.ClassType and type(classDef) != types.TypeType:
                    self.notify.error('Symbol %s is not a class name.' % className)
                else:
                    dclass.setClassDef(classDef)
            self.dclassesByName[className] = dclass
            if number >= 0:
                self.dclassesByNumber[number] = dclass

        if self.hasOwnerView():
            ownerDcSuffix = self.dcSuffix + 'OV'
            ownerImportSymbols = {}
            for n in range(dcFile.getNumImportModules()):
                moduleName = dcFile.getImportModule(n)
                suffix = moduleName.split('/')
                moduleName = suffix[0]
                suffix = suffix[1:]
                if ownerDcSuffix in suffix:
                    moduleName = moduleName + ownerDcSuffix
                importSymbols = []
                for i in range(dcFile.getNumImportSymbols(n)):
                    symbolName = dcFile.getImportSymbol(n, i)
                    suffix = symbolName.split('/')
                    symbolName = suffix[0]
                    suffix = suffix[1:]
                    if ownerDcSuffix in suffix:
                        symbolName += ownerDcSuffix
                    importSymbols.append(symbolName)
                    ownerImportSymbols[symbolName] = None

                self.importModule(dcImports, moduleName, importSymbols)

            for i in range(dcFile.getNumClasses()):
                dclass = dcFile.getClass(i)
                if dclass.getName() + ownerDcSuffix in ownerImportSymbols:
                    number = dclass.getNumber()
                    className = dclass.getName() + ownerDcSuffix
                    classDef = dcImports.get(className)
                    if classDef is None:
                        self.notify.error('No class definition for %s.' % className)
                    else:
                        if type(classDef) == types.ModuleType:
                            if not hasattr(classDef, className):
                                self.notify.error('Module %s does not define class %s.' % (className, className))
                            classDef = getattr(classDef, className)
                        dclass.setOwnerClassDef(classDef)
                        self.dclassesByName[className] = dclass

        return


ConnectionRepository.ConnectionRepository = ConnectionRepository_override
import toontown.toonbase.ToontownStart