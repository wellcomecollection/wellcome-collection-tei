# Print the XML nodes corresponding to the given XPath expression in all TEI documents
#
# Requires XMLStarlet
#
# Usage example:
# sh teigrep.sh '//t:objectDesc[@form="scroll"]//t:layout[@writtenLines="177"]'
#
# prints:
# ./Ethiopian/Ethiopian_20.xml
#  <layout xmlns="http://www.tei-c.org/ns/1.0" writtenLines="177">
#    177 lines in black and red ink.
#  </layout>
#

find . -name '*xml'  -not -path '*Templates*' -not -path '*.idea*' -not -path '*docs*'| xargs -J % xml sel -B -I -N 't=http://www.tei-c.org/ns/1.0' -t -i "$1" -f -n -c "$1" '%' 2>/dev/null
