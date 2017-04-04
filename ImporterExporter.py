import csv
import json
from collections import OrderedDict
import re


class InFileTypeException(Exception):
    """ Exception to say what went wrong with the in file type """
    pass


class OutFileTypeException(Exception):
    """ Exception to say what went wrong with the out file type """
    pass


class ImporterExporter(object):
    """ Manages importing of data from different files.
    Formats currently supported: CSV
    """
    currentInTypes = ['csv']
    currentOutTypes = ['json']

    def __init__(self):
        pass

    def readCSV(self, fileName):
        """ read the csv file and convert it to a string """
        tempCSV = []
        with open(fileName) as f:
            reader = csv.reader(f)

            for row in reader:
                # append a list of tags/values to a list (list of lists)
                tempCSV.append(row)
        f.close()
        return tempCSV

    def writeCSVtoJSON(self, fileName, readIn):
        """ write the contents of readIn out to a JSON file, fileName will
        be used as the name of the file with the .xxx removed and replace by
        .json
        - Currently relies on the data being in the csv in the order that it
        is to be stored in the json file"""
        jsonObjects = []
        for listItem in readIn:
            # ignore first listItem as this is the headings
            if readIn.index(listItem) > 0:
                # use OrderedDict because dict is unordered
                data = OrderedDict()
                modData = OrderedDict()
                modList = []

                for value in listItem:
                    # only add to dict if not the first row(headings)
                    index = listItem.index(value)

                    # pick out row heading
                    heading = str(readIn[0][index])

                    if 'modifier' not in heading:
                        # create dict entries with first row of csv(headings)
                        data[heading] = self.tidyValue(value)
                    else:
                        if 'name' in heading:
                            modData["name"] = self.tidyValue(value)
                        else:
                            # add price to modifier dict
                            modData["price"] = self.tidyValue(value)

                            # add modifier dict to list of modifiers
                            modList.append(modData)

                            # reset modifier dict
                            modData = OrderedDict()

                data["modifiers"] = modList
                jsonObjects.append(data)

        with open(fileName, 'w') as outFile:
            outFile.write("[")
            count = 0   # count the number of objects to place comma

            for obj in jsonObjects:
                json.dump(obj, outFile, indent=4)
                if count < len(jsonObjects)-1:
                    # only place comma if not last obj
                    count += 1
                    outFile.write(","+"\n")
            outFile.write("]")

    def tidyValue(self, val):
        """ tidies the passed in value so that the correct type will be
        returned - string for non numeric characters, float for currency
        and int for integers, otherwise what was received is returned """
        alphaPattern = '([A-Z]+|[a-z]+)'
        integerPattern = '([0-9]+)'
        currencyPattern = '(\-?[£$€][0-9]+(\.[0-9]+)?)'
        if re.match(alphaPattern, val) is not None:
            return val
        elif re.match(integerPattern, val) is not None:
            return int(val)
        elif re.match(currencyPattern, val) is not None:
            return self.stripCurrencySign(val)
        else:
            # if val does not match a pattern return what was received
            return val

    def stripCurrencySign(self, val):
        """ Removes the currency sign that prepends a number and returns a
        float
        if the number to be returned does not match the format of a decimal
        number, -999999 is returned as an error"""
        decimalChars = '-0123456789.'
        decimalPattern = '(\-?[0-9]+(\.[0-9]+)?)'
        number = ''
        for c in val:
            if c not in decimalChars:
                pass
            else:
                number += c

        if re.match(decimalPattern, number) is not None:
            return float(number)
        else:
            return -999999

    def work(self, fileName, inType, outType):
        """ reads in a file of fileName that is of format inType.
        Then converts that to the outType. """
        if inType in self.currentInTypes:
            if outType in self.currentOutTypes:
                # read files in, using inType as the format
                if inType == self.currentInTypes[0]:
                    # index 0 is for csv file imports
                    readIn = self.readCSV(fileName)

                    if outType == self.currentOutTypes[0]:
                        # convert csv to JSON, use the csv filename as json file name
                        filePattern = '\/([a-z]|[A-Z]|[0-9])+.csv'
                        foundPattern = re.search(filePattern, fileName)
                        if foundPattern is not None:
                            # if pattern is found remove csv from end and append json
                            temp = foundPattern.group(0)[0:-3]
                            jsonFileName = "exports" + temp + "json"
                            self.writeCSVtoJSON(jsonFileName, readIn)
                        else:
                            raise OutFileTypeException('The export file type was ' +
                                           'incorrect, please specify one of the following: {}'.format(self.currentOutTypes))

            else:
                raise OutFileTypeException('The export file type was ' +
                                           'incorrect, please specify one of the following: {}'.format(self.currentOutTypes))
        else:
            raise InFileTypeException('The import file type was incorrect' +
                'please specify one of the following: {}'.format(self.currentInTypes))


if __name__ == "__main__":
    i = ImporterExporter()
    i.work('imports/exampleMH.csv', 'csv', 'json')
