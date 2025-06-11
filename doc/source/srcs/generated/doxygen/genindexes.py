import xml.etree.ElementTree as ET





tree = ET.parse('xml/index.xml')
root = tree.getroot()


formats={
"file":".. doxygenfile:: %s",
"class":".. doxygenclass:: %s",
}

parsers={
"file":lambda s: s.replace("__","_"),
"class":lambda s: s.replace("class","").replace("__","_")
}

filenames={
"file":"file.rst",
"class":"class.rst",
}

filecontents={
"file":"Files",
"class":"Classes",
}
for key in formats:
    filecontents[key]+= "\n"
    filecontents[key]+= "================"
    filecontents[key]+= "\n\n"


matched={}

for child in root:
    matched[child.attrib["kind"]]=False
    for key in formats:
        if key==child.attrib["kind"]:
            matched[key]=True
            filecontents[key]+= formats[key] % parsers[key](child.attrib["refid"])
            filecontents[key]+= "\n"
    print(child.tag, child.attrib)

print(matched)
for key in formats:
    with open(filenames[key], "w") as f:
        f.write(filecontents[key])