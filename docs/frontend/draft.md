# TEI cataloguing mapping

## Identification

| TEI | API |
| :--- | :--- |
| msIdentifier/idno | identifiers |
| msIdentifier/idno | ReferenceNumber |
| msIdentifier/altIdentifier | identifiers |
| msIdentifier/altIdentifier type="Sierra" | Sierra identifier |
| msIdentifier/altIdentifier type="accession" | Accession identifier |
| msIdentifier/altIdentifier type="former" | Former identifier |

## Description

| TEI | API |
| :--- | :--- |
| publicationStmt/idno type="msID" | title |
| mscontents/summary | description |
| textLang | languages |
| msItem/textLang | languages |
| msItem/locus | description |
| msItem/author | contributor |
| msItem/title type="original" | title |
| msItem/incipit | notes /[begins]/ |
| msItem/incipit/locus | notes /[begins]/ |
| msItem/explicit | notes /[ends]/ |
| msItem/explicit/locus | notes /[ends]/ |
| msItem/colophon | notes /[colophon]/ |
| msItem/colophon/locus | notes /[colophon]/ |
| history/origin/origPlace | production |
| history/origin/origDate | production |
| history/provenance | notes \[ownership\] |
| history/acquisition | notes \[acquisition\] |
| physDesc/handDesc/handNote | contributor |
| physDesc/objectDesc/object/support | ? |
| physDesc/objectDesc/object/extent | ? |
| handDesc | notes \[hand\] |


## Notes

| TEI | API |
| :--- | :--- |
| additional/adminInfo/recordHist/source | notes \[source\] |

## Access Conditions?

| TEI | API |
| :--- | :--- |
|  |  |

