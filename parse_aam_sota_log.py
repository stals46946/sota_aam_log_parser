import sys
import xml.dom.minidom as minidom

def pretty_xml(xml_string):
    #print(f"DEBUG: {xml_string}")
    dom = minidom.parseString(xml_string)
    return dom.toprettyxml(indent="  ")

def starts_with_xml(s):
    s = s.lstrip()  # remove leading whitespace
    return "<?xml" in s

def contains_end_of_xml(s):
    s = s.lstrip()  # remove leading whitespace
    return "</S:Envelope>" in s
  
def index_of_start_xml(s):
    s = s.lstrip()  # remove leading whitespace
    return s.find("<?xml")

#</S:Envelope>
def index_of_end_xml(s):
    s = s.lstrip()  # remove leading whitespace
    tok1=s.find("</S:Envelope>")
    tok2=s.find("</soapenv:Envelope>")
    if tok1>-1:
       tok1+=len("</S:Envelope>")
    if tok2>-1:
       tok2+=len("</soapenv:Envelope>") 
    return max(tok1,tok2)      
    #return s.find("</S:Envelope>")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        return

    filename = sys.argv[1]
    in_xml=False
    with open(filename, "r") as f:
        found_start=False
        found_end=False
        xml_string=""
        for line in f:
          line = line.rstrip("\n")
          #print(f"READING line: {line}")
          start_pos=index_of_start_xml(line)
          end_pos=index_of_end_xml(line)

          # if end_pos==-1 and start_pos==-1 and in_xml==False:
          #   print(f"skipping line: {line}")

          #print(f"{line}, {start_pos}, {end_pos}")
          if start_pos>=0:
            found_start=True
            in_xml=True
          else:
            start_pos=0
            found_start=False
            #print(line[start_pos:])
          found_end=False
          if (end_pos>=0):
            found_end=True
            #in_xml=False
          #print(f"DEBUG: {found_start}, {found_end}, {in_xml}, {start_pos}, {end_pos}")
          if found_start and found_end:
             #print(line[start_pos:end_pos])
            in_xml=False
            xml_string+=line[start_pos:end_pos]
            print(pretty_xml(xml_string))
            xml_string=""

          if (found_start or in_xml) and not found_end:
             #print(line[start_pos:])
             xml_string+=line[start_pos:]
          if not found_start and in_xml and not found_end:
             #print(line)
             xml_string+=line
          if not found_start and in_xml and found_end:
            #print(line[:end_pos])
            #print("GOT HERE")
            in_xml=False
            xml_string+=line[:end_pos]
            #pretty_xml(xml_string)
            #print(xml_string)
            print(pretty_xml(xml_string))
            #print(f"TEST: {xml_string}:")
            #pretty_xml(xml_string)
            xml_string=""







if __name__ == "__main__":
    main()

#print("DONE")