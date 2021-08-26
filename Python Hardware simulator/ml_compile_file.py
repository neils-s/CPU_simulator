import ml_assembler
import sys

def readAssemblyFile(assemblyFile:str,verbose:bool)->list[str]:
    """Reads in the contents of the specified file."""
    returnList:list[str]=[]
    fileReader=None
    try:
        if verbose:
            print("\nOpening file ",assemblyFile,"\nLines read:")
        fileReader=open(assemblyFile,'r')
        while True:
            line=fileReader.readline()
            if not line: # stop if we've reached the end of the file
                break
            returnList.append(line)
            if verbose:
                print("  ",line)
    except Exception as e:
        print("Error reading specified file.")
        if verbose:
            print("Error details",e)
    finally:
        if fileReader != None:
            fileReader.close()
        if verbose:
            print("Finished reading file.")
    return returnList

def writeBinaryFile(binaryFile:str,binaryCode:list[str],verbose:bool)->bool:
    """Writes the binary data to a file."""
    success:bool=True
    fileWriter=None
    try:
        if verbose:
            print("\nWriting file ",binaryFile)
        fileWriter=open(binaryFile,'w')
        fileWriter.writelines(binaryCode)
    except Exception as e:
        print("Error writing output file.")
        if verbose:
            print("Error details",e)
    finally:
        if fileWriter!=None:
            fileWriter.close()
        if verbose:
            print("Finished writing binary file.")
    return success

def compile(assemblyCode:list[str],verbose:bool,theAssembler:ml_assembler.assembler)->list[str]:
        """The complete parser and compiler.  This converts lines of assembler code (with labels) to binary code."""
        if verbose:
            print("\nStripping extraneous whitespace...")
        linesOfCodeWithoutWhitespace = theAssembler.cleanWhiteSpace(assemblyCode)
        if verbose:
            for line in linesOfCodeWithoutWhitespace:
                print("  ",line)

        if verbose:
            print("\nConverting explicit labels...")
        linesOfCodeWithoutExplicitLabels = theAssembler.symbolHandler1_ExplicitLabels(linesOfCodeWithoutWhitespace)
        if verbose:
            print("Assembly code without explicit labels:")
            for line in linesOfCodeWithoutExplicitLabels:
                print("  ",line)
            print("Symbol table:")
            for key,value in theAssembler.symbolTable:
                print("  ",key," : ",value)

        if verbose:
            print("\nRemoving line labels...")
        linesOfCodeWithoutLineLabels=theAssembler.symbolHandler2_LinesLabels(linesOfCodeWithoutExplicitLabels)
        if verbose:
            print("Assembly code without explicit line labels:")
            for line in linesOfCodeWithoutLineLabels:
                print("  ",line)
            print("Symbol table:")
            for key,value in theAssembler.symbolTable:
                print("  ",key," : ",value)

        if verbose:
            print("\nReplacing labels with values in assembly language code...")
        linesOfCodeWithoutAnyLabels=theAssembler.symbolHandler3_ReplaceSymbols(linesOfCodeWithoutLineLabels)
        if verbose:
            print("Assembly code with labels replaced:")
            for line in linesOfCodeWithoutAnyLabels:
                print("  ",line)

        if verbose:
            print("Converting explicit assembly language code to binary...")
        linesOfBinary=theAssembler.parseToBinary(linesOfCodeWithoutAnyLabels)
        if verbose:
            print("Binary code:")
            for line in linesOfBinary:
                print("  ",line)
        
        if verbose:
            print("Compilation complete")
        return linesOfBinary

def main(argv):
    if len(sys.argv)<2:
        print("The compiler requires 2 arguments.  The first is the source file containing assembly code, and the second is the name of the file to be created to hold binary code.")
        sys.exit(1)
    if len(sys.argv)>2:
        print("Only the first 2 arguments will be used.")

    assemblyFile:str = argv[0]
    binaryFile:str = argv[1]
    verbose:bool = True
    theAssembler=ml_assembler.assembler()

    assemblyCode:list[str] = readAssemblyFile(assemblyFile,verbose)
    binaryCode:list[str] = compile(assemblyCode,verbose,theAssembler)
    success:bool = writeBinaryFile(binaryFile,binaryCode,verbose)
    if success:
        return 0
    return 1

if __name__=="__main__":
    sys.exit(main(sys.argv[1:]))

