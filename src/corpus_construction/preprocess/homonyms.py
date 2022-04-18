import json
import xml.etree.ElementTree as ET


def extract_homonyms(filename):
    homonym_list = {}

    tree = ET.parse(filename)
    root = tree.getroot()
    for synonym in root:
        # extract a list of all the english literals
        litertal_list_en = []
        synonym_en = synonym.find(".//SYNONYM[@{http://www.w3.org/XML/1998/namespace}lang='en']")
        if synonym_en is not None:
            for litertal in synonym_en:
                litertal_list_en.append(litertal.text)
        else:
            # if there are not english literals, there is no use in processing further
            break

        # extract a list of all the slovenian usages
        usage_sl_list = []
        usage_sl = synonym.findall(".//USAGE[@{http://www.w3.org/XML/1998/namespace}lang='sl']")
        if usage_sl is not None:
            for usage in usage_sl:
                usage_sl_list.append(usage.text)

        # extract a list of all the english usages
        usage_en_list = []
        usage_en = synonym.findall(".//USAGE[@{http://www.w3.org/XML/1998/namespace}lang='en']")
        if usage_en is not None:
            for usage in usage_en:
                usage_en_list.append(usage.text)

        # extract a list of all the slovenian definitions
        defin_sl_list = []
        defin_sl = synonym.findall(".//DEF[@{http://www.w3.org/XML/1998/namespace}lang='sl']")
        if defin_sl is not None:
            for defin in defin_sl:
                defin_sl_list.append(defin.text)

        # extract a list of all the english definitions
        defin_en_list = []
        defin_en = synonym.findall(".//DEF[@{http://www.w3.org/XML/1998/namespace}lang='en']")
        if defin_en is not None:
            for defin in defin_en:
                defin_en_list.append(defin.text)

        synonym_sl = synonym.find(".//SYNONYM[@{http://www.w3.org/XML/1998/namespace}lang='sl']")
        if synonym_sl is not None:
            for litertal in synonym_sl:
                # check an entry for homonym is already in the dictonary
                if litertal.text in homonym_list.keys():
                    homonym_list[litertal.text].litertal_list.update(litertal_list_en)
                    homonym_list[litertal.text].usage_sl_list.update(usage_sl_list)
                    homonym_list[litertal.text].usage_en_list.update(usage_en_list)
                    homonym_list[litertal.text].defin_sl_list.update(defin_sl_list)
                    homonym_list[litertal.text].defin_en_list.update(defin_en_list)
                    homonym_list[litertal.text].counter += 1
                else:
                    homonym_list[litertal.text] = HomonymEntry(litertal.text, litertal_list_en, usage_sl_list, usage_en_list, defin_sl_list,
                                                               defin_en_list)

    return homonym_list


def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)

    return obj


def convert_homonym_json(homonym_list, filename):
    json_str = json.dumps([homonym_list[i].__dict__ for i in homonym_list], default=serialize_sets, indent=2)

    with open(filename, "w") as outfile:
        outfile.write(json_str)


class HomonymEntry:
    def __init__(self, homonym, litertal_list, usage_sl_list, usage_en_list, defin_sl_list, defin_en_list):
        self.homonym = homonym
        self.litertal_list = set(litertal_list)
        self.usage_sl_list = set(usage_sl_list)
        self.usage_en_list = set(usage_en_list)
        self.defin_sl_list = set(defin_sl_list)
        self.defin_en_list = set(defin_en_list)
        self.counter = 1


if __name__ == '__main__':
    homonym_list = extract_homonyms('../../../data/slownet/slownet-2015-05-07.xml')
    convert_homonym_json(homonym_list, 'homonyms.json')
