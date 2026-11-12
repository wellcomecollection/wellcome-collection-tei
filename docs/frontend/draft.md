# TEI cataloguing mapping

## Identification

| TEI | API | Status | Required to remove toggle |
| :--- | :--- |:--- |:--- |
| msIdentifier/idno | identifiers |
| msIdentifier/idno | ReferenceNumber | Done |
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
| msItem/locus | notes [locus] | Done | yes
| msItem/author | contributor | Done | yes
| msItem/title type="original" | title | Done | yes
| msItem/title | alternativeTitles | Done | 
| msItem/incipit | notes /[begins]/ | Done | yes
| msItem/incipit/locus | notes /[begins]/ | Done | yes
| msItem/explicit | notes /[ends]/ |Done | yes
| msItem/explicit/locus | notes /[ends]/ | Done | yes
| msItem/colophon | notes /[colophon]/ | Done | yes
| msItem/colophon/locus | notes /[colophon]/ | Done | yes
| history/origin/origPlace | production | Done | yes
| history/origin/origDate | production | Done | yes
| history/provenance | notes \[ownership\] | Done |
| history/acquisition | notes \[acquisition\] | Done |
| physDesc/handDesc/handNote | contributor | Done | yes
| physDesc/objectDesc/object/support | physicalDescription | Done| yes
| physDesc/objectDesc/object/extent |physicalDescription | Done | yes
| physDesc/objectDesc/supportDesc/support/watermark | physicalDescription | Done |
| physDesc/objectDesc/supportDesc/condition | notes \[condition\] | Done |
| physDesc/objectDesc/supportDesc/collation | notes \[collation\] | Done |
| physDesc/objectDesc/supportDesc/foliation | notes \[foliation\] | Done |
| physDesc/objectDesc/layoutDesc/layout | notes \[layout\] | Done |
| physDesc/handDesc/handNote | notes \[hand\] | Done |
| physDesc/handDesc/handNote/@script | notes \[hand\] | Done |
| physDesc/decoDesc/decoNote | notes \[decoration\] | Done |
| physDesc/bindingDesc | notes \[binding detail\] | Done |
| msItem/filiation | notes \[filiation\] | Done |
| profileDesc/keywords |subjects | Done | |


## Notes

| TEI | API | Status | Required for toggle |
| :--- | :--- |:--- |:--- |
| additional/adminInfo/recordHist/source | notes \[source\] | | 
| additional/adminInfo/custodialHist | notes \[custodial\] | | 

## HTML snippets

| TEI | API | Status | 
| :--- | :--- | :--- |
| <p> | Format as separate paragrahps  | Done |
| <list> | Format as list | |

