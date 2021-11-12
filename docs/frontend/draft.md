# TEI cataloguing mapping

## Identification

| TEI | API | Status | Required to remove toggle |
| :--- | :--- |:--- |:--- |
| msIdentifier/idno | identifiers |
| msIdentifier/idno | ReferenceNumber |
| msIdentifier/altIdentifier | identifiers |
| msIdentifier/altIdentifier type="Sierra" | Sierra identifier | Done | yes
| msIdentifier/altIdentifier type="accession" | Accession identifier |
| msIdentifier/altIdentifier type="former" | Former identifier |

## Description

| TEI | API | Status | Required for toggle |
| :--- | :--- |:--- |:--- |
| publicationStmt/idno type="msID" | title | Done | yes
| mscontents/summary | description | Done | yes
| textLang | languages | Done | yes
| msItem/textLang | languages | Done | yes
| msItem/locus | description | | yes
| msItem/author | contributor | Done | yes
| msItem/title type="original" | title | Done | yes
| msItem/incipit | notes /[begins]/ | waiting for reindex | yes
| msItem/incipit/locus | notes /[begins]/ | waiting for reindex | yes
| msItem/explicit | notes /[ends]/ | waiting for reindex | yes
| msItem/explicit/locus | notes /[ends]/ | waiting for reindex | yes
| msItem/colophon | notes /[colophon]/ | waiting for reindex | yes
| msItem/colophon/locus | notes /[colophon]/ | waiting for reindex | yes
| history/origin/origPlace | production | Done | yes
| history/origin/origDate | production | Done | yes
| history/provenance | notes \[ownership\] | 
| history/acquisition | notes \[acquisition\] |
| physDesc/handDesc/handNote | contributor | Done | yes
| physDesc/objectDesc/object/support | physicalDescription | in progress| yes
| physDesc/objectDesc/object/extent |physicalDescription | in progress | yes
| handDesc | notes \[hand\] |


## Notes

| TEI | API | Status | Required for toggle |
| :--- | :--- |:--- |:--- |
| additional/adminInfo/recordHist/source | notes \[source\] | | 

## Access Conditions?

| TEI | API |
| :--- | :--- |
|  |  |

