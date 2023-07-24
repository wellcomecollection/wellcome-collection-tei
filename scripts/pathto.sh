# Show the full XPath from document root to the target node(s) in all TEI documents within the working directory
#
# Requires XMLStarlet
#
# Usage example:
# sh pathto.sh '//t:acquisition
#
# prints a list of results including:
#...
# ./Greek/MS_MSL_112.xml
# TEI/teiHeader/fileDesc/sourceDesc/msDesc/history/acquisition
# ./Greek/MS_354.xml
# TEI/teiHeader/fileDesc/sourceDesc/msDesc/history/acquisition
# TEI/teiHeader/fileDesc/sourceDesc/msDesc/msPart/history/acquisition
# TEI/teiHeader/fileDesc/sourceDesc/msDesc/msPart/history/acquisition
# ...

find . -name '*xml'  -not -path '*Templates*' -not -path '*.idea*' -not -path '*docs*' | xargs -J % xml sel -B -I -T -N 't=http://www.tei-c.org/ns/1.0' -t -f -n -m $1 -m 'ancestor::*' -v 'name()' -o '/'  -b -v "name()" -n '%' 2>/dev/null