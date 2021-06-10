<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:output method="xml" indent="yes" encoding="utf-8"/>
       
    
    <xsl:template match="/">
        <xsl:processing-instruction name="xml-model">href="https://raw.githubusercontent.com/bodleian/consolidated-tei-schema/master/msdesc.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"</xsl:processing-instruction>
        <TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="">
            
            <teiHeader>
                
                <fileDesc>
                    
                    <titleStmt>
                        <title></title>
                        <title type="collection">Wellcome Collection</title>
                        <respStmt xml:id="">
                            <resp when="">Cataloguer</resp>
                            <persName><!-- Insert name --></persName>
                        </respStmt>
                        <respStmt xml:id="">
                            <resp when="">TEI Encoder</resp>
                            <persName><xsl:value-of select="/DScribeDatabase/DScribeRecord/Modifier"/></persName>
                        </respStmt>
                        <!-- Add another <respStmt> for every resp -->
                    </titleStmt>
                    
                    <publicationStmt>
                        <publisher>Wellcome Collection</publisher>
                        <idno>UkLW</idno>
                        <address>
                            <orgName type="institution">Wellcome Collection</orgName>
                            <street>215 Euston Rd</street>
                            <settlement>London</settlement>
                            <postCode>NW1 2BE</postCode>
                        </address>
                        <distributor>
                            <email>library@wellcome.ac.uk</email>
                        </distributor>
                        <idno type="msID"><xsl:value-of select="/DScribeDatabase/DScribeRecord/RefNo"/></idno>
                        <idno type="catalogue"></idno>
                    </publicationStmt>
                    
                    <sourceDesc>
                        
                        <msDesc>
                            
                            <msIdentifier>
                                <country>United Kingdom</country>
                                <settlement>London</settlement>
                                <institution>Wellcome Collection</institution>
                                <repository>Wellcome Library</repository>
                                <idno type="shelfmark"><xsl:value-of select="/DScribeDatabase/DScribeRecord/RefNo"/></idno>
                                <!-- Use <altIdentifier> if former or alternative <idno> is available -->
                                <altIdentifier type="">
                                    <idno><xsl:value-of select="/DScribeDatabase/DScribeRecord/AltRefNo"/></idno>
                                </altIdentifier>
                            </msIdentifier>
                            
                            <msContents>
                                
                                <summary><xsl:value-of select="/DScribeDatabase/DScribeRecord/Description"/></summary>
                                
                                
                                <textLang mainLang=""><xsl:value-of select="/DScribeDatabase/DScribeRecord/Language"/><!-- Use if only one language in manuscript --> <!-- Enter BCP 47 language code as attribute value and full language name here --> </textLang>
                                
                                <msItem n="" xml:id="">
                                    
                                    <author key=""><xsl:value-of select="/DScribeDatabase/DScribeRecord/CreatorName"/><!-- Insert viaf code as attribute value, if available, and enter author name here --></author>
                                    <title key=""><xsl:value-of select="/DScribeDatabase/DScribeRecord/Title"/></title>
                                    
                                    <!-- Use as needed, or delete -->
                                    <textLang mainLang=""><!-- Enter BCP 47 language code as attribute value and full language name here --></textLang>
                                    <textLang otherLangs=""><!-- Enter BCP 47 language code as attribute value and full language name here --></textLang>
                                    
                                    <incipit><!-- insert --> <locus></locus>
                                        <!-- Use <note> to add general comment -->
                                    </incipit>
                                    <explicit><!-- insert --> <locus></locus>
                                        <!-- Use <note> to add general comment -->
                                    </explicit>
                                    <colophon><!-- insert --> <locus></locus>
                                        <!-- Use <note> to add general comment -->
                                    </colophon>
                                    
                                    <filiation><!-- insert --></filiation>
                                    <note><!-- insert --></note>
                                    
                                    
                                </msItem>
                                
                                <!-- Add <msItem> as needed, adding the @n and @xml:id attributes  -->
                                
                            </msContents>
                            
                            <physDesc>
                                <!-- Insert and delete as needed -->
                                <objectDesc form="">
                                    
                                    <supportDesc material="">
                                        
                                        <support><!-- Insert prose description --></support>
                                        <extent><xsl:value-of select="/DScribeDatabase/DScribeRecord/Extent"/>
                                            <dimensions unit="" type=""><!-- Add if available -->
                                                <dim type="diameter"></dim>
                                                <dim type="length"></dim>
                                                <!-- Add or delete dimensions as needed -->
                                            </dimensions>
                                        </extent>
                                        
                                        <foliation>
                                            <!-- Use to record information about the system of numbering folia in the manuscript, if applicable -->
                                        </foliation>
                                        
                                        <collation>
                                            <formula><!-- Use to record the quire structure of the manuscript, if available --></formula>
                                            <signatures><!-- Use to record quire signatures, if available --></signatures>
                                        </collation>
                                        
                                    </supportDesc>
                                    
                                    <layoutDesc>
                                        
                                        <layout writtenLines="">
                                            <!-- Add description or further elements -->                                        
                                        </layout>
                                        
                                    </layoutDesc> 
                                    
                                </objectDesc>
                                
                                <handDesc>
                                    <!-- Add or delete <handNote> elements as needed -->
                                    <handNote scope=""></handNote>
                                </handDesc>
                                
                                <decoDesc>
                                    <decoNote></decoNote>
                                </decoDesc>
                                
                                <additions>
                                    <p></p>
                                </additions>
                                
                                <bindingDesc>
                                    <binding>
                                        <p></p>
                                    </binding>
                                </bindingDesc>
                                
                            </physDesc>
                            
                            <history>
                                <origin>
                                    <origPlace>
                                        <country><!-- insert --></country>,
                                        <region><!-- insert --></region>,
                                        <settlement><!-- insert --></settlement>,
                                        <orgName><!-- insert --></orgName>
                                    </origPlace>
                                    <origDate calendar=""><xsl:value-of select="/DScribeDatabase/DScribeRecord/Date"/></origDate>
                                    <!-- use additional origPlace and origDate elements if necessary -->
                                </origin>
                                <provenance notBefore="" notAfter=""><!-- insert, otherwise delete --></provenance>
                                <!-- use additional provenance elements if necessary -->
                                <acquisition><xsl:value-of select="/DScribeDatabase/DScribeRecord/Acquisition"/></acquisition>
                            </history>
                            
                            <additional>
                                <adminInfo>
                                    <recordHist>
                                        <source>
                                            <!-- insert text, if relevant -->
                                            <bibl><!-- insert if necesary --></bibl>
                                            <!-- Might include link to catalogue source -->
                                            <!--<listBibl>
                              <bibl> </bibl>
                           </listBibl>-->
                                        </source>
                                    </recordHist>
                                    <availability status=""><p><xsl:value-of select="/DScribeDatabase/DScribeRecord/AccessConditions"/></p></availability> 
                                </adminInfo>
                                <!-- Enter bibliographical info, if needed -->
                                <listBibl>
                                    <!-- a number of listBibl elements can be nested inside an outer listBibl if required -->
                                    <head><!-- use to provide a heading if required, otherwise delete --></head>
                                    <bibl><!-- insert bibliography, links to online resource, etc., otherwise delete--></bibl>
                                </listBibl>
                                
                            </additional>
                            
                        </msDesc>
                        
                    </sourceDesc>
                    
                </fileDesc>
                
                <!-- Use the following to record subject headings, if needed -->
                <encodingDesc>
                    <classDecl>
                        <taxonomy xml:id="LCSH">
                            <bibl>
                                <ref target="http://id.loc.gov/authorities/about.html#lcsh">Library of Congress Subject Headings</ref>
                            </bibl>
                        </taxonomy>
                        <taxonomy xml:id="MeSH">
                            <bibl>
                                <ref target="">MeSH</ref>
                            </bibl>
                        </taxonomy>
                    </classDecl>
                </encodingDesc>
                <profileDesc>
                    <textClass>
                        <keywords scheme="#LCSH">
                            <list>
                                <item facs="">
                                    <term ref="subject_"></term>
                                </item>
                            </list>
                        </keywords>
                        <keywords scheme="#MeSH">
                            <list>
                                <item facs="">
                                    <term ref="subject_"></term>
                                </item>
                            </list>
                        </keywords>
                    </textClass>
                </profileDesc>    
                
                <revisionDesc>
                    <change when=""><!-- Make an entry to record the creation of the file, and then a new <change> for every later edit --></change>
                    
                </revisionDesc>
                
            </teiHeader>    
            
            <facsimile>
                <surface></surface>
                
            </facsimile>    
            
            <text>
                <body>
                    <p></p>
                    <!-- For future full transcription -->
                </body>
                
            </text>    
            
        </TEI>
    </xsl:template>
</xsl:stylesheet>