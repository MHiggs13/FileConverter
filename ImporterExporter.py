import csv
import json
from collections import OrderedDict


class InFileTypeException(Exception):
    """ Exception to say what went wrong with the in file type """
    # todo make the exception class smarter (make it do stuff)
    pass


class OutFileTypeException(Exception):
    """ Exception to say what went wrong with the out file type """
    # todo make the exception class smarter (make it do stuff)
    pass


class Importer(object):
    """ Manages importing of data from different files.
    Formats currently supported: CSV
    """
    currentInTypes = ['csv']
    currentOutTypes = ['json']

    def __init__(self):
        pass

    def readCSV(self, fileName):
        """ read the csv file and convert it to a string """
        # todo should this be converted to an array first or is string ok
        # todo might be able to do a conversion straight to JSON but
        # this would possibly not be very future friendly for other formats
        tempCSV = []
        with open('imports/example.csv') as f:
            reader = csv.reader(f)

            for row in reader:
                # append a list of tags/values to a list (list of lists)
                tempCSV.append(row)
        f.close()
        return tempCSV

    def writeJSON(self, fileName, readIn):
        """ write the contents of readIn out to a JSON file, fileName will
        be used as the name of the file with the .xxx removed and replace by
        .json
        - Currently relies on the data being in the csv in the order that it
        is to be stored in the json file"""
        # todo put information like above in documentation
        jsonObjects = []
        # todo come up with away to avoid using 3 for loops
        # loop through all list of readIn (besides the first list)
        for listItem in readIn:
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
                        data[heading] = value
                    else:
                        if 'name' in heading:
                            modData["name"] = value
                        else:
                            modData["price"] = value
                            modList.append(modData)
                data["modifiers"] = modList
                jsonObjects.append(data)

        with open('exports/example.json', 'w') as outFile:
            outFile.write("[")
            count = 0   # count the number of objects to place comma

            for obj in jsonObjects:
                json.dump(obj, outFile, indent=4)
                if count < len(jsonObjects)-1:
                    # only place comma if not last obj
                    count += 1
                    outFile.write(","+"\n")
            outFile.write("]")

    def work(self, fileName, inType, outType):
        """ reads in a file of fileName that is of format inType.
        Then converts that to the outType. """
        if inType in self.currentInTypes:
            if outType in self.currentOutTypes:
                # both file types are in the import and export file types

                # read files in, using inType as the format
                if inType == self.currentInTypes[0]:
                    # index 0 is for csv file imports
                    readIn = self.readCSV(fileName)
                    # todo catch an exception???

                # todo do some special validation to allow certain combination
                # todo i.e. csv to json but maybe there is xml too but csv
                # todo can't be converted to xml
                # write files out, using outType as the format
                if outType == self.currentOutTypes[0]:
                    # todo think about how converting other files to json would work
                    # todo it wouldn't really, csv to json is different from x to json
                    self.writeJSON(fileName, readIn)

            else:
                raise OutFileTypeException('The export file type was ' +
                                           'incorrect, please specify one of the following: {}'.format(self.currentOutTypes))
        else:
            raise InFileTypeException('The import file type was incorrect' +
                'please specify one of the following: {}'.format(self.currentInTypes))


i = Importer()
i.work('imports/example.csv', 'csv', 'json')
