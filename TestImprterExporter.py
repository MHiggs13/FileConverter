from ImporterExporter import ImporterExporter
import csv
import os


class TestImporterExporter():

    def testReadCSVEqualsReturnedCSV(self):
        """ test that when a csv is read the list of lists read is what is
        expected to be read from the actual csv file """
        fileName = 'imports/exampleMH.csv'
        impExp = ImporterExporter()
        result = impExp.readCSV(fileName)

        expected = []
        with open(fileName) as f:
            reader = csv.reader(f)

            for row in reader:
                # append a list of tags/values to a list (list of lists)
                expected.append(row)
            f.close()

        assert(result == expected)

    def testIntTidyValue(self):
        """ test that when an integer value is passed it is returned with no
        values missing """
        value = "1234567890"
        impExp = ImporterExporter()
        result = impExp.tidyValue(value)

        expected = int(value)
        assert(result == expected)

    def testZeroIntTidyValue(self):
        """ test that when an integer value (but there is a preceding 0)
        is passed it is returned with no value missing """
        value = "001234"
        impExp = ImporterExporter()
        result = impExp.tidyValue(value)

        expected = int(value)
        assert(result == expected)

    def testAlphaTidyValue(self):
        """ Test that when an alphabetic value is passed, it is returned
        with no values missing """
        value = "This is a alpha value"
        impExp = ImporterExporter()
        result = impExp.tidyValue(value)

        expected = value

        assert(result == expected)

    def testNegStripCurrencySign(self):
        """ Test that the pound sign can be stripped from a negative decimal 
        number """
        value = "-£405.01"
        impExp = ImporterExporter()
        result = impExp.stripCurrencySign(value)

        expected = -405.01

        assert(result == expected)

    def testStripCurrencySign(self):
        """ Test that the dollar sign can be stripped from a 2 digit number 
        with no decimal point"""
        value = "$60"
        impExp = ImporterExporter()
        result = impExp.stripCurrencySign(value)

        expected = 60

        assert(result == expected)

    def testExportFileName(self):
        """ Tests that the json file created is named the same as the csv file
        that was used as basis for the json file. """
        value = "imports/test.csv"
        impExp = ImporterExporter()
        impExp.work(value, 'csv', 'json')
        result = os.path.exists("exports/test.json")

        assert(result)
