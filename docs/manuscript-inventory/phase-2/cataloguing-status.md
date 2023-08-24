---
description: >-
  This section details the considerations involved in determining whether an
  item is catalogued and available in TEI.
---

# Cataloguing status

### Overview

Cataloguing information about a manuscript item can be dispersed across a number of sources, ranging from printed catalogues to digital management systems. A main aim of manuscript inventory, in keeping with the [SPECTRUM standard set out by Collections Trust](https://collectionstrust.org.uk/resource/inventory-the-spectrum-standard/), is to develop a centralised register of uncatalogued manuscripts that may in turn be submitted for [cataloguing prioritisation](http://127.0.0.1:5000/o/-LumfFcEMKx4gYXKAZTQ/s/-MaCyZe0q1CUexeaRgr6-887967055/).

For this purpose, the 'Add Manuscript' function in Quickbase presents the following question and drop-down menu:



<figure><img src="../../.gitbook/assets/Screenshot 2023-07-26 at 18.06.39.png" alt=""><figcaption></figcaption></figure>



While the responses in turn require further responses, possibly even different workflows, the main two considerations we need to record are:

* Whether the item is catalogued.
* If yes, whether it is catalogued in TEI.

### Whether an item is catalogued

There can be several ways of identifying whether an item is catalogued in some way or the other. Any shelfmark or numbering system, either on the item itself or its housing, indicates that some form of cataloguing may have happened.&#x20;

If there is enough contextual information about the item available while assessing it in the Stacks, it might be possible to check sources such as Sierra, Calm, printed catalogues, or TEI.&#x20;

> For instance, if the item is labelled MS Thai 40, it is relevant to check the printed catalogue of Thai manuscripts, Sierra, and the TEI repository.

If further research is required, or the item itself is unwieldy or fragile, it is safe to record it as 'TBD' and undertake further research at one's desk.

#### What is 'catalogued' in this context?

For the purposes of manuscript inventory, 'catalogued' simply means that we have a minimum viable description available for the item. The backlog of uncatalogued and/or less catalogued manuscripts at Wellcome Collection is such that we are mainly aiming for a quantitative approach to cover holes.

### Whether an item is available in TEI

If there is any indication that the manuscript is catalogued, the next step is to interrogate the [TEI GitHub repository](https://github.com/wellcomecollection/wellcome-collection-tei). This can be done by running a search in the repository as a whole, or taking a more granular look through the collections-based repositories. Especially relevant TEI elements for identification are \<msIdentifier>, \<summary>, and \<physDesc>.

If any enhancements or inaccuriaces appear to be present in the TEI file, please record this in the 'Metadata work required' box on Quickbase.

<mark style="background-color:orange;">\[AP - ADD NOTE ABOUT THE NEXT BOX (WHERE IS THIS CATALOGUED)]</mark>

