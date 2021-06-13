import ml_assembler as asssemb
import pytest

def test_assemblyLanguage_initializeWithoutError():
    thisAssemblyLanguageInstance:asssemb.assemblyLanguage = asssemb.assemblyLanguage()
    assert thisAssemblyLanguageInstance != None

