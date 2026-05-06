# LexiRumah 3.0.1

  

**CLDF Metadata**: [cldf-metadata.json](./cldf-metadata.json)

  

**Sources**: [sources.bib](./sources.bib)

  

A lexical database of Lesser Sunda languages

  

property | value

 --- | ---

[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF Wordlist](http://cldf.clld.org/v1.0/terms.rdf#Wordlist)

[dc:creator](http://purl.org/dc/terms/creator) | <ol><li>Owen Edwards</li><li>Gereon A. Kaiping</li><li>Marian Klamer</li></ol>

[dc:bibliographicCitation](http://purl.org/dc/terms/bibliographicCitation) | Kaiping, Gereon A., Owen Edwards, and Marian Klamer (eds.). 2019. LexiRumah 3.0.1. Leiden: Leiden University Centre for Linguistics. (Available online at https://lexirumah.model-ling.eu/)

[dc:format](http://purl.org/dc/terms/format) | <ol><li>http://concepticon.clld.org/contributions/Klamer-2018-607</li></ol>

[dc:identifier](http://purl.org/dc/terms/identifier) | https://lexirumah.model-ling.eu

[dcat:accessURL](http://www.w3.org/ns/dcat#accessURL) | https://gituhb.com/lessersunda/lexirumah-data

[dc:license](http://purl.org/dc/terms/license) | http://creativecommons.org/licenses/by/4.0/

[dc:publisher](http://purl.org/dc/terms/publisher) | Leiden University Centre for Linguistics

[prov:wasDerivedFrom](http://www.w3.org/ns/prov#wasDerivedFrom) | <ol><li><a href="https://github.com/concepticon/concepticon-data/tree/v2.5.0">Concepticon  v2.5.0</a></li></ol>

special:contact | m.a.f.klamer@hum.leidenuniv.nl

special:domain | lexirumah.model-ling.eu

special:license_icon | cc-by.png

special:license_name | Creative Commons Attribution 4.0 International License

special:publisher_place | Leiden, The Netherlands

special:publisher_url | http://www.universiteitleiden.nl/en/humanities/leiden-university-centre-for-linguistics

[rdf:id](http://www.w3.org/1999/02/22-rdf-syntax-ns#id) | lexirumah

[rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type) | http://www.w3.org/ns/dcat#Distribution

  

  

## <a name="table-formscsv"></a>Table [forms.csv](./forms.csv)

  

property | value

 --- | ---

[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF FormTable](http://cldf.clld.org/v1.0/terms.rdf#FormTable)

  

  

### Columns

  

Name/Property | Datatype | Description

 --- | --- | --- 

[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_-]+` | Primary key

[Lect_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string`<br>Regex: `[a-zA-Z0-9_-]+` | References [lects.csv::ID](#table-lectscsv)

[Concept_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string`<br>Regex: `[a-zA-Z0-9_-]+` | References [concepts.csv::ID](#table-conceptscsv)

[Form_according_to_Source](http://cldf.clld.org/v1.0/terms.rdf#value) | `string` | 

[Form](http://cldf.clld.org/v1.0/terms.rdf#form) | `string` | 

`Local_Orthography` | `string` | 

[Segments](http://cldf.clld.org/v1.0/terms.rdf#segments) | list of `string` (separated by ` `) | 

[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 

[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)

  

## <a name="table-missingformscsv"></a>Table [missing_forms.csv](./missing_forms.csv)

  

property | value

 --- | ---

[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ValueTable](http://cldf.clld.org/v1.0/terms.rdf#ValueTable)

  

  

### Columns

  

Name/Property | Datatype | Description

 --- | --- | --- 

[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_-]+` | Primary key

[Lect_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string`<br>Regex: `[a-zA-Z0-9_-]+` | References [lects.csv::ID](#table-lectscsv)

[Concept_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string`<br>Regex: `[a-zA-Z0-9_\-]+` | References [concepts.csv::ID](#table-conceptscsv)

[Form_according_to_Source](http://cldf.clld.org/v1.0/terms.rdf#value) | `string` | 

[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 

[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)

  

## <a name="table-lectscsv"></a>Table [lects.csv](./lects.csv)

  

property | value

 --- | ---

[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF LanguageTable](http://cldf.clld.org/v1.0/terms.rdf#LanguageTable)

[dc:extent](http://purl.org/dc/terms/extent) | 180

  

  

### Columns

  

Name/Property | Datatype | Description

 --- | --- | --- 

[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_-]+` | Primary key

[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 

[Family](http://glottolog.org/glottolog/family) | `string` | 

[Latitude](http://cldf.clld.org/v1.0/terms.rdf#latitude) | `decimal`<br>&ge; -90<br>&le; 90 | 

[Longitude](http://cldf.clld.org/v1.0/terms.rdf#longitude) | `decimal`<br>&ge; -180<br>&le; 180 | 

`Region` | `string` | 

[Glottocode](http://cldf.clld.org/v1.0/terms.rdf#glottocode) | `string`<br>Regex: `[a-z0-9]{4}[1-9][0-9]{3}` | 

[Iso](http://cldf.clld.org/v1.0/terms.rdf#iso639P3code) | `string`<br>Regex: `[a-z]{3}` | 

`Culture` | `string` | 

[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 

`Orthography` | list of `string` (separated by `:`) | 

[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 

[Macroarea](http://cldf.clld.org/v1.0/terms.rdf#macroarea) | `string` | 

  

## <a name="table-conceptscsv"></a>Table [concepts.csv](./concepts.csv)

  

property | value

 --- | ---

[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ParameterTable](http://cldf.clld.org/v1.0/terms.rdf#ParameterTable)

  

  

### Columns

  

Name/Property | Datatype | Description

 --- | --- | --- 

[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_-]+` | Primary key

[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 

[English](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 

`Indonesian` | `string` | 

`Semantic_Field` | `string` | 

`Elicitation_Notes` | `string` | 

`Core_Set` | `boolean` | 

[Concepticon_ID](http://cldf.clld.org/v1.0/terms.rdf#concepticonReference) | `string`<br>Regex: `[0-9]+` | 

`Comment` | `string` | 

  

## <a name="table-cognatescsv"></a>Table [cognates.csv](./cognates.csv)

  

property | value

 --- | ---

[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF CognateTable](http://cldf.clld.org/v1.0/terms.rdf#CognateTable)

  

  

### Columns

  

Name/Property | Datatype | Description

 --- | --- | --- 

[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_-]+` | Primary key

[Form_ID](http://cldf.clld.org/v1.0/terms.rdf#formReference) | `string`<br>Regex: `[a-zA-Z0-9_-]+` | References [forms.csv::ID](#table-formscsv)

[Cognateset_ID](http://cldf.clld.org/v1.0/terms.rdf#cognatesetReference) | `string`<br>Regex: `[a-zA-Z0-9_-]+` | 

[Alignment](http://cldf.clld.org/v1.0/terms.rdf#alignment) | list of `string` (separated by ` `) | 

[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)

  

## <a name="table-borrowingscsv"></a>Table [borrowings.csv](./borrowings.csv)

  

property | value

 --- | ---

[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF BorrowingTable](http://cldf.clld.org/v1.0/terms.rdf#BorrowingTable)

  

  

### Columns

  

Name/Property | Datatype | Description

 --- | --- | --- 

[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_-]+` | Primary key

[Form_ID_Target](http://cldf.clld.org/v1.0/terms.rdf#targetFormReference) | `string`<br>Regex: `[a-zA-Z0-9_-]+` | References [forms.csv::ID](#table-formscsv)

[Form_ID_Source](http://cldf.clld.org/v1.0/terms.rdf#sourceFormReference) | `string`<br>Regex: `[a-zA-Z0-9_-]+` | References [forms.csv::ID](#table-formscsv)

[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 

[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)

[Status](http://wold.clld.org/terms#borrowed_status) | `integer` |