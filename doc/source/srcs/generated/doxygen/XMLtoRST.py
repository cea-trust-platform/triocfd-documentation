import xml.etree.ElementTree as ET







def print_class(index_elem):
    tree = ET.parse('xml/%s.xml' % index_elem.get("refid"))
    root = tree.getroot()
    doc=root[0]
    rst=""
    has_base=False
    has_deriv=False
    is_template=False
    my_type="Class"
    if doc.find("templateparamlist")!=None:
        print("is template")
        is_template=True
        my_type="Template"
    
    elem_name=doc.find("compoundname")
        
    my_name=elem_name.text
    rst += (".. _{my_type} {my_name}:".format(my_type=my_type, my_name=my_name)) + "\n\n"
    title="{my_name}".format(my_type=my_type, my_name=my_name)
    rst += title + "\n" + "-" * len(title) + "\n"
    
    list_elem_base=doc.findall("basecompoundref")
    if len(list_elem_base)>0:
        rst += "\n.. dropdown:: Inherits from:\n\n"
        has_base=True
        for child in list_elem_base:                
                
            base_type="Class"
            base_name=child.text
            tparams=""
            if "<" in child.text:
                base_type="Template"
                base_name=child.text[:child.text.index("<")]
                tparams=child.text[child.text.index("<"):]
            rst += " "*4 + "- {prot} : :ref:`{base_type} {name}` {tparams}".format(prot=child.get("prot"),name=base_name, base_type=base_type,tparams=tparams)
            rst+="\n"
        rst+="\n\n"
        
        
    list_elem_deriv=doc.findall("derivedcompoundref")
    if len(list_elem_deriv)>0:
        rst += "\n.. dropdown:: Inherited by:\n\n"
        has_deriv=True
        for child in list_elem_deriv:                
                
            tparams=""
            deriv_type="Class"
            deriv_name=child.text
            if "<" in child.text:
                deriv_type="Template"
                deriv_name=child.text[:child.text.index("<")]
                tparams=child.text[child.text.index("<"):]
            rst += " "*4 + "- {prot} : :ref:`{deriv_type} {name}` {tparams}".format(prot=child.get("prot"),name=deriv_name, deriv_type=deriv_type,tparams=tparams)
            rst+="\n"
        rst+="\n\n"
        
    #  for child in root[0]:                
            
        #  if child.tag=="briefdescription":
            #  rst += "\n\nSummary: "
            #  for para in child:
                #  rst += para.text or ""
                #  rst += "\n\n"
            
        #  if child.tag=="detaileddescription":
            #  rst += "\n\nDescription:\n\n"
            #  for para in child:
                #  rst += para.text or ""
                #  rst += "\n\n"
    #  print(rst)
    return(rst)








tree = ET.parse('xml/index.xml')
root = tree.getroot()


formats={
#  "file":".. doxygenfile:: %s",
"class":".. doxygenclass:: %s",
}

parsers={
"file":lambda s: s.replace("__","_"),
"class":lambda s: s.replace("class","").replace("__","_")
}

printers={
"file":lambda ie: "",
"class":print_class
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
            filecontents[key] += printers[key](child)
            filecontents[key] += "\n\n"
    #  print(child.tag, child.attrib)

print(matched)
for key in formats:
    with open(filenames[key], "w") as f:
        f.write(filecontents[key])