# Return all TEI files that have a node matching the given XPath expression
#
# Requires XMLStarlet
#
# Usage example:
# sh teigrepl.sh '//t:objectDesc[@form="scroll"]'
#
# prints:
# ./Hebrew/Hebrew_B_1.xml
# ./Batak/Batak_330890.xml
# ./Ethiopian/Ethiopian_10.xml
# ./Ethiopian/Ethiopian_3.xml
# ./Ethiopian/Ethiopian_20.xml
# ./Ethiopian/Ethiopian_22.xml
#
find . -name '*xml'  -not -path '*Templates*' -not -path '*.idea*' -not -path '*docs*'| xargs -J % xml sel -N 't=http://www.tei-c.org/ns/1.0' -t -i $1 -f -n '%' 2>/dev/null
