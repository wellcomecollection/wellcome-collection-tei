<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
    
    <!-- ========================================================= -->
    <!-- GLOBAL VARIABLES (DEFENSIVE, XSLT 1.0 SAFE)               -->
    <!-- ========================================================= -->
    
    <!-- AltRefNo (raw) -->
    <xsl:variable name="altrefno-raw">
        <xsl:value-of select="normalize-space(//AltRefNo[1])"/>
    </xsl:variable>
    
    <!-- AltRefNo as xml:id-safe -->
    <xsl:variable name="altrefno-id">
        <xsl:choose>
            <xsl:when test="string-length($altrefno-raw) &gt; 0">
                <xsl:value-of
                    select="
                    translate(
                    $altrefno-raw,
                    ' ./:\&#x9;&#xA;&#xD;',
                    '_______________'
                    )"/>
            </xsl:when>
            <xsl:otherwise/>
        </xsl:choose>
    </xsl:variable>
    
    <!-- Creator (raw) -->
    <xsl:variable name="creator-raw">
        <xsl:value-of select="normalize-space(/DScribeRecord/Creator)"/>
    </xsl:variable>
    
    <!-- Creator xml:id (Surnamei → IS) -->
    <xsl:variable name="creator-id">
        <xsl:choose>
            <xsl:when test="string-length($creator-raw) &gt; 0">
                <xsl:value-of
                    select="concat(
                    '',
                    translate(
                    substring($creator-raw, string-length($creator-raw), 1),
                    'abcdefghijklmnopqrstuvwxyz',
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                    ),
                    translate(
                    substring($creator-raw, 1, 1),
                    'abcdefghijklmnopqrstuvwxyz',
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                    )
                    )"/>
            </xsl:when>
            <xsl:otherwise/>
        </xsl:choose>
    </xsl:variable>
    
    <!-- Created date from dd/mm/yyyy to yyyy-mm-dd-->
    <xsl:variable name="created-iso">
        <xsl:choose>
            <xsl:when test="string-length(normalize-space(//Created[1])) = 10">
                <xsl:value-of select="
                    concat(
                    substring(//Created[1], 7, 4), '-', 
                    substring(//Created[1], 4, 2), '-', 
                    substring(//Created[1], 1, 2)
                    )
                    "/>
            </xsl:when>
            <xsl:otherwise/>
        </xsl:choose>
    </xsl:variable>
    
    
    <!-- ========================================================= -->
    <!-- ROOT TEMPLATE                                             -->
    <!-- ========================================================= -->
    
    <xsl:template match="/">
        
        <xsl:processing-instruction name="xml-model">
            href="https://raw.githubusercontent.com/bodleian/consolidated-tei-schema/master/msdesc.rng"
            type="application/xml"
            schematypens="http://relaxng.org/ns/structure/1.0"
        </xsl:processing-instruction>
        
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            
            <!-- TEI xml:id -->
            <xsl:attribute name="xml:id">
                <xsl:value-of select="$altrefno-id"/>
            </xsl:attribute>
            
            <teiHeader>
                <fileDesc>
                    
                    <!-- ================= TITLE STATEMENT ================= -->
                    
                    <titleStmt>
                        <title><xsl:value-of select="$altrefno-id"/></title>
                        <title type="collection">Wellcome Collection</title>
                        
                        <respStmt xml:id="SM">
                            <resp when="1973">Cataloguer</resp>
                            <persName>S. A. J. Moorat</persName>
                        </respStmt>
                        
                        <xsl:if test="string-length($creator-raw) &gt; 0">
                            <respStmt>
                                <xsl:attribute name="xml:id">
                                    <xsl:value-of select="$creator-id"/>
                                </xsl:attribute>
                                
                                <resp when="{$created-iso}">Calm encoder</resp>
                                
                                <persName>
                                    <xsl:value-of select="$creator-raw"/>
                                </persName>
                            </respStmt>
                        </xsl:if>
                    </titleStmt>
                    
                    <!-- ================= PUBLICATION ================= -->
                    
                    <publicationStmt>
                        <publisher>Wellcome Collection</publisher>
                        <idno>UkLW</idno>
                        <address>
                            <orgName>Wellcome Collection</orgName>
                            <street>215 Euston Rd</street>
                            <settlement>London</settlement>
                            <postCode>NW1 2BE</postCode>
                        </address>
                        <distributor>
                            <email>library@wellcome.org</email>
                        </distributor>
                        <idno type="msID">
                            <xsl:value-of select="/DScribeRecord/AltRefNo"/>
                        </idno>
                    </publicationStmt>
                    
                    <!-- ================= SOURCE ================= -->
                    
                    <sourceDesc>
                        <msDesc>
                            <msIdentifier>
                                <country>United Kingdom</country>
                                <settlement>London</settlement>
                                <institution>Wellcome Collection</institution>
                                <repository>Wellcome Library</repository>
                                <idno type="shelfmark">
                                    <xsl:value-of select="/DScribeRecord/AltRefNo"/>
                                </idno>
                                <altIdentifier type="CalmRef">
                                    <idno><xsl:value-of select="/DScribeRecord/RefNo"/></idno>
                                </altIdentifier>
                                <xsl:for-each select="/DScribeRecord/AccNo">
                                    <altIdentifier type="accession">
                                        <idno>
                                            <xsl:value-of select="."/>
                                        </idno>
                                    </altIdentifier>
                                </xsl:for-each> 
                                <xsl:for-each select="/DScribeRecord/OtherNumber">
                                    <altIdentifier type="other">
                                        <idno>
                                            <xsl:value-of select="."/>
                                        </idno>
                                    </altIdentifier>
                                </xsl:for-each>    
                                <xsl:for-each select="/DScribeRecord/PreviousNumbers">
                                    <altIdentifier type="previous">
                                        <idno>
                                            <xsl:value-of select="."/>
                                        </idno>
                                    </altIdentifier>
                                </xsl:for-each>
                                <altIdentifier type="CalmID">
                                    <idno><xsl:value-of select="/DScribeRecord/RecordID"/></idno>
                                </altIdentifier>
                            </msIdentifier>
                            
                            <msContents>
                                <summary>
                                    <xsl:apply-templates select="/DScribeRecord/Description/node()"/>
                                </summary>
                                
                                <textLang mainLang="" source="IANA"><xsl:value-of select="/DScribeRecord/Language"/></textLang>
                                
                                <msItem n="1">
                                    <xsl:attribute name="xml:id">
                                        <xsl:value-of select="concat($altrefno-id, '_1')"/>
                                    </xsl:attribute>
                                    
                                    <xsl:for-each select="/DScribeRecord/CreatorName">
                                        <author>
                                            <xsl:value-of select="."/>
                                        </author>
                                    </xsl:for-each>
                                    
                                    <title type="original">
                                        <xsl:value-of select="/DScribeRecord/Title"/>
                                    </title>
                                    <title type="standard">
                                        <xsl:value-of select="/DScribeRecord/Alternative_Title"/></title>
                                    
                                    <xsl:for-each select="/DScribeRecord/Language">
                                        <textLang mainLang="" source="IANA">
                                            <xsl:value-of select="."/>
                                        </textLang>
                                    </xsl:for-each>
                                    
                                   <filiation>
                                       <xsl:value-of select="/DScribeRecord/AdminHistory"/>
                                   </filiation>
                                    <filiation>
                                        <xsl:value-of select="/DScribeRecord/Notes"/>
                                    </filiation>                                    
                                </msItem>
                                
                            </msContents>
                            
                            <physDesc>
                                <objectDesc form="codex">
                                    <supportDesc material=""><xsl:value-of select="/DScribeRecord/Extent"/>
                                    <extent><xsl:value-of select="/DScribeRecord/UserWrapped6"/>
                                        <dimensions type="leaf" unit="cm">
                                            <dim type="width"></dim>
                                            <dim type="length"></dim>
                                        </dimensions>
                                        <dimensions type="written" unit="cm">
                                            <dim type="width"></dim>
                                            <dim type="length"></dim>
                                        </dimensions>
                                    </extent>
                                    
                                        <foliation><!-- delete if not required --></foliation>
                                        
                                        <collation>
                                            <xsl:value-of select="/DScribeDatabase/DScribeRecord/Arrangement"/>
                                        </collation>
                                        
                                        <condition><p><xsl:value-of select="/DScribeDatabase/DScribeRecord/UserWrapped6"/></p>
                                            <p><xsl:value-of select="/DScribeRecord/Condition"/></p>
                                            <p><xsl:value-of select="/DScribeRecord/ConditionNote"/></p>
                                            <p><xsl:value-of select="/DScribeRecord/UserWrapped2"/></p>
                                        </condition>
                                        <support>
                                            <watermark><!-- delete if not required --></watermark>
                                        </support>
                                    </supportDesc>
                                    
                                    <layoutDesc>
                                        <layout writtenLines=""><!-- delete if not required -->
                                            <note><!-- add in info about rulings --></note>
                                        </layout>
                                    </layoutDesc>
                                    
                                </objectDesc>
                                
                                <handDesc><!-- delete if not required -->
                                    <handNote scribe="sole"><!-- delete if not required --></handNote>
                                    <handNote script=""><!-- delete if not required --></handNote>
                                </handDesc>
                                
                                <decoDesc><!-- delete if not required -->
                                    <decoNote type="marginal"><!-- delete if not required --></decoNote>    
                                    <decoNote type="illustration"><!-- delete if not required --></decoNote>
                                </decoDesc>
                                
                                <additions>
                                    <!-- delete if not required -->
                                </additions>
                                
                                <bindingDesc>
                                    <binding>
                                        <p><xsl:value-of select="/DScribeRecord/UserWrapped6"/></p>
                                    </binding>
                                </bindingDesc>
                            </physDesc>
                            
                            <history>
                                <origin>
                                    <origDate>
                                        <xsl:value-of select="/DScribeRecord/Date"/>
                                    </origDate>
                                </origin>
                                <provenance><xsl:value-of select="/DScribeRecord/CustodialHistory"/></provenance>
                                <xsl:for-each select="/DScribeRecord/Acquisition">
                                    <acquisition>
                                        <xsl:value-of select="."/>
                                    </acquisition>
                                </xsl:for-each>
                                <xsl:for-each select="/DScribeRecord/Accruals">
                                    <acquisition type="accrual">
                                        <xsl:value-of select="."/>                                   
                                    </acquisition>
                                </xsl:for-each>
                            </history>
                            
                            
                            <!-- ================= RECORD ADMIN ================= -->     
                            
                            <additional>
                                <adminInfo>
                                    <recordHist>
                                        <source>
                                            <bibl>
                                                <title>Catalogue of Western Manuscripts on Medicine and Science in the Wellcome Historical Medical Library</title>
                                                <author>S. A. J. Moorat</author>
                                                <placeName>London</placeName>
                                                <publisher>Wellcome Institute for the History of Medicine</publisher>
                                                <date>1962-1973</date>  
                                            </bibl>
                                        </source>
                                    </recordHist>
                                    
                                    <availability status="">
                                        <p><xsl:value-of select="/DScribeRecord/AccessConditions"/></p>
                                    </availability>
                                    <availability><licence><xsl:value-of select="/DScribeRecord/Copyright"/></licence></availability>
                                    <custodialHist>
                                        <custEvent type="Cataloguing">Manuscripts in CALM were exported and transformed into TEI as part of the Wellcome Collection Transformation Programme 2026.</custEvent>
                                        <custEvent type="cataloguing"><xsl:value-of select="/DScribeRecord/UserWrapped4"/></custEvent>
                                        <custEvent type="exhibition"><xsl:value-of select="/DScribeRecord/Usage"/></custEvent>
                                        <custEvent type="digitised">Digitised: <xsl:value-of select="/DScribeRecord/Digitised"/></custEvent>
                                    </custodialHist>
                                                                           
                                </adminInfo>
                                
                                <surrogates><xsl:value-of select="/DScribeRecord/Copies"/></surrogates>
                                <surrogates><xsl:value-of select="/DScribeRecord/Originals"/></surrogates>
                                
                                <listBibl>
                                    <bibl><xsl:value-of select="/DScribeRecord/PublnNote"/></bibl>
                                </listBibl>
                                <listBibl>
                                    <bibl><xsl:value-of select="/DScribeRecord/RelatedMaterial"/></bibl>
                                </listBibl>
                                <listBibl>
                                    <bibl>
                                        <title><!-- delete if not required --></title>
                                        <author><!-- delete if not required --></author>
                                        <date><!-- delete if not required --></date>
                                        <placeName><!-- delete if not required --></placeName>
                                        <publisher><!-- delete if not required --></publisher>
                                        <abbr><!-- delete if not required --></abbr>
                                        <note><!-- delete if not required --></note>
                                    </bibl>
                                </listBibl>
                            </additional>
                        </msDesc>
                    </sourceDesc>
                    
                </fileDesc>
 
                <!-- ================= SUBJECTS ================= -->    
                
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
                                <xsl:for-each select="/DScribeRecord/Subject">
                                    <item facs="">
                                        <term ref="subject_">
                                            <p>
                                                <xsl:value-of select="."/>
                                            </p>
                                        </term>
                                    </item>
                                </xsl:for-each>
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
                    <change when="2026-05-05" who="Victoria Sloyan">Transformed Calm xml export to TEI xml file using a transformation scenario</change>
                    <change when="" who="">Manual edits following automated Calm-TEI transformation</change>
                </revisionDesc>
                
            </teiHeader>
            
            <text>
                <body>
                    <p></p>
                </body>
            </text>
            
        </TEI>
    </xsl:template>
 
 <!--- template for HTML list tags -->
    <xsl:template match="list">
        <list xmlns="http://www.tei-c.org/ns/1.0" rend="bulleted">
            <xsl:apply-templates/>
        </list>
    </xsl:template>
    
    <xsl:template match="item">
        <item xmlns="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates/>
        </item>
    </xsl:template>
    
    <xsl:template match="p">
        <p xmlns="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    
</xsl:stylesheet>