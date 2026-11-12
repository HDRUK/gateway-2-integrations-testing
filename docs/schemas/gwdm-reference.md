---
title: GWDM field reference
description: Every field in the Gateway Working Data Model, by version and by block.
tags:
  - reference
  - schemas
  - gwdm
---

<!-- GENERATED FILE — do not edit by hand.
     Regenerate with: python3 docs/examples/gwdm_reference.py
     Source: docs/examples/fields-gwdm-*.tsv -->

# GWDM field reference

**Applies to:** GWDM 2.0 · 2.1 · 2.2

Every field in the Gateway Working Data Model, grouped by top-level block.
This page is **generated** from the schemas themselves, so it does not drift
from the model the way a hand-written list would.

!!! info "Where the full field descriptions live"
    This page gives you the shape: path, type, whether it is required, the
    permitted values, and which GWDM version introduced it. For the complete
    prose description of each field, see the generated schema documentation at
    [hdruk.github.io/schemata](https://hdruk.github.io/schemata/), which is
    built from the Pydantic models directly.

    Descriptions below are truncated to one line. Where they disagree with
    `schemata`, `schemata` is right and this page is stale — please
    [raise an issue](https://github.com/HDRUK/gateway-2-integrations-testing/issues).

## Before you read the tables

Three conventions decide whether your metadata survives the round trip. They
are explained in full on [The GWDM explained](gwdm.md); in brief:

- **Fields marked 🔒 are written by the Gateway API** and overwrite whatever
  you send. Do not compute them.
- **Fields marked ⁂ are delimited strings**, not arrays — a list is joined
  with `;,;` into a single string.
- **`-1` means "unknown"** in numeric fields, not zero.

## Field counts

| Version | Fields | Blocks | Source |
|---|---|---|---|
| GWDM 2.0 | 149 | 11 | `GWDM/2.0/schema.json` |
| GWDM 2.1 | 169 | 15 | `GWDM/2.1/schema.json` |
| GWDM 2.2 | 172 | 15 | **projected: GWDM 2.1 + 3 DUO paths** |

=== "GWDM 2.0"

    ??? note "`required` — 9 fields"

        Identity and versioning. **Written by the Gateway API — see the warning below.**

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `required` 🔒 | Required | ✓ |  | 2.0 | Required metadata needed for the GWDM |
        | `required.gatewayId` 🔒 | string | ✓ |  | 2.0 | Associated identifier (number) that is the BigInt key in our SQL database for the dataset version associate… |
        | `required.gatewayPid` 🔒 | string | ✓ |  | 2.0 | A unique persistent identifier for the metadata version. This is a 128-bit unique identifiers, as 32 hexade… |
        | `required.issued` 🔒 | string | ✓ |  | 2.0 | Datetime stamp of when this metadata version was initially issued |
        | `required.modified` 🔒 | string | ✓ |  | 2.0 | Datetime stamp of when this metadata was last modified |
        | `required.revisions` 🔒 | array | ✓ |  | 2.0 | A list of persistent identifiers and version numbers for previous versions of metadata for this dataset |
        | `required.revisions[].url` | Url\|null | ✓ |  | 2.0 | Some url with a reference to the record of a previous version of this dataset |
        | `required.revisions[].version` | string | ✓ |  | 2.0 | Version number used for previous version of this dataset |
        | `required.version` | string | ✓ |  | 2.0 | Dataset metadata version |

    ??? note "`summary` — 17 fields"

        Title, description, keywords, publisher, population size. The block search relies on most.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `summary` | Summary | ✓ |  | 2.0 | Summary of metadata describing key pieces of information. |
        | `summary.abstract` | LongAbstractText | ✓ |  | 2.0 | Longer abstract detailing the dataset. |
        | `summary.contactPoint` | string\|null |  |  | 2.0 | email of a person who can be the main contact point of this dataset |
        | `summary.controlledKeywords` | CommaSeparatedValues\|null |  |  | 2.0 | Keywords that have been filtered and limited |
        | `summary.datasetSubType` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Placeholder for dataset sub-type |
        | `summary.datasetType` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | What type of dataset is this? |
        | `summary.description` | LongDescription\|null |  |  | 2.0 | Longer description of the dataset in detail |
        | `summary.doiName` | Doi\|null |  |  | 2.0 | DOI associated to this dataset |
        | `summary.inPipeline` | Pipeline\|null |  | `Available, Not available` | 2.0 | Indicate whether this dataset is currently available for Researchers to request access. |
        | `summary.keywords` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Comma separated key words associated to this dataset. |
        | `summary.populationSize` | integer\|null |  |  | 2.0 | Summary population size of the cohort |
        | `summary.publisher` 🔒 | Organisation\|null |  |  | 2.0 | Link to details about the publisher of this dataset |
        | `summary.publisher.gatewayId` | string\|null |  |  | 2.0 | Identifier on the gateway |
        | `summary.publisher.name` | Name\|null |  |  | 2.0 | Name of the organisation |
        | `summary.publisher.rorId` | string\|null |  |  | 2.0 | The Research Organization Registry (ROR) for the organisation, if applicable |
        | `summary.shortTitle` | ShortTitle\|null |  |  | 2.0 | A shorter descriptive title of the dataset |
        | `summary.title` | TwoHundredFiftyFiveCharacters | ✓ |  | 2.0 | The main title of the dataset |

    ??? note "`coverage` — 6 fields"

        Geographic, temporal and demographic reach of the cohort.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `coverage` | Coverage\|null |  |  | 2.0 | This information includes attributes for geographical and temporal coverage, cohort details etc. to enable… |
        | `coverage.datasetCompleteness` | Url\|null |  |  | 2.0 | The URL where a Researcher can learn more about the completeness of the dataset. |
        | `coverage.followUp` | FollowupV2\|null |  | `0 - 6 Months, 6 - 12 Months, 1 - 10 Years, > 10 Years, Unknown, Continuous, Other, null` | 2.0 | If known, what is the typical time span that a patient appears in the dataset (follow up period) |
        | `coverage.pathway` | LongDescription\|null |  |  | 2.0 | Please indicate if the dataset is representative of the patient pathway and any limitations the dataset may… |
        | `coverage.spatial` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | The geographical area covered by the dataset. It is recommended that links are to entries in a well-maintai… |
        | `coverage.typicalAgeRange` | AgeRange\|null |  |  | 2.0 | Please indicate the age range in whole years of participants in the dataset. Please provide range in the fo… |

    ??? note "`provenance` — 12 fields"

        Where the data came from and how often it is refreshed.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `provenance` | Provenance\|null |  |  | 2.0 | Provenance information allows researchers to understand data within the context of its origins and can be a… |
        | `provenance.origin` | Origin\|null |  |  | 2.0 |  |
        | `provenance.origin.collectionSituation` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please indicate the setting(s) where data was collected. Multiple settings may be provided |
        | `provenance.origin.imageContrast` | Ternary\|null |  | `Yes, No, Not stated` | 2.0 | Indicate whether usage of imaging contrast is captured within the dataset. |
        | `provenance.origin.purpose` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please indicate the purpose(s) that the dataset was collected. |
        | `provenance.origin.source` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please indicate the source of the data extraction |
        | `provenance.temporal` | object | ✓ |  | 2.0 |  |
        | `provenance.temporal.accrualPeriodicity` | PeriodicityV2 | ✓ |  | 2.0 | Please indicate the frequency of distribution release. If a dataset is distributed regularly please choose… |
        | `provenance.temporal.distributionReleaseDate` | string\|string\|null |  |  | 2.0 | Date of the latest release of the dataset. If this is a regular release i.e. quarterly, or this is a static… |
        | `provenance.temporal.endDate` | string\|string\|null |  |  | 2.0 | The end of the time period that the dataset provides coverage for. If the dataset is “Continuous” and has n… |
        | `provenance.temporal.startDate` | string\|string\|null |  |  | 2.0 | The start of the time period that the dataset provides coverage for. If there are multiple cohorts in the d… |
        | `provenance.temporal.timeLag` | TimeLagV2 | ✓ |  | 2.0 | Please indicate the typical time-lag between an event and the data for that event appearing in the dataset |

    ??? note "`accessibility` — 22 fields"

        Access rights, formats, standards and usage conditions. Required.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `accessibility` | Accessibility | ✓ |  | 2.0 | Accessibility information allows researchers to understand access, usage, limitations, formats, standards a… |
        | `accessibility.access` | Access | ✓ |  | 2.0 | This section includes information about data access |
        | `accessibility.access.accessRequestCost` ⁂ | LongDescription\|null |  |  | 2.0 | Please provide link(s) to a webpage detailing the commercial model for processing data access requests for… |
        | `accessibility.access.accessRights` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please provide details for the data access rights |
        | `accessibility.access.accessService` | LongDescription\|null |  |  | 2.0 | Please provide a brief description of the data access services that are available including: environment th… |
        | `accessibility.access.accessServiceCategory` | CommaSeparatedValues\|null |  |  | 2.0 | Where access to data come from: TRE/SED, direct access, open acccess, varies based on project. |
        | `accessibility.access.dataController` | LongDescription\|null |  |  | 2.0 | Data Controller means a person/entity who (either alone or jointly or in common with other persons/entities… |
        | `accessibility.access.dataProcessor` | LongDescription\|null |  |  | 2.0 | A Data Processor, in relation to any Data Subject data, specifically personal data, means any person/entity… |
        | `accessibility.access.deliveryLeadTime` | DeliveryLeadTimeV2\|null |  | `Less than 1 week, 1-2 weeks, 2-4 weeks, 1-2 months, 2-6 months, More than 6 months, Variable, Not applicable, Other` | 2.0 | Please provide an indication of the typical processing times based on the types of requests typically recei… |
        | `accessibility.access.jurisdiction` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please use country code from ISO 3166-1 country codes and the associated ISO 3166-2 for regions, cities, st… |
        | `accessibility.formatAndStandards` | FormatAndStandards\|null |  |  | 2.0 | Section includes technical attributes for language vocabularies, sizes etc. and gives researchers facts abo… |
        | `accessibility.formatAndStandards.conformsTo` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | What the vocabulary conforms to. |
        | `accessibility.formatAndStandards.formats` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Format(s) the dataset can be made available in |
        | `accessibility.formatAndStandards.languages` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Language code(s) of the language of the dataset metadata and underlying data is made available. |
        | `accessibility.formatAndStandards.vocabularyEncodingSchemes` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Code value of the ontology vocabulary encoding |
        | `accessibility.usage` | Usage\|null |  |  | 2.0 | This section includes information about how the data can be used and how it is currently being used |
        | `accessibility.usage.dataUseLimitation` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please provide an indication of consent permissions for datasets and/or materials, and relates to the purpo… |
        | `accessibility.usage.dataUseRequirement` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please indicate fit here are any additional conditions set for use if any, multiple requirements may be pro… |
        | `accessibility.usage.resourceCreator` | Organisation\|null |  |  | 2.0 | Please provide the text that you would like included as part of any citation that credits this dataset. Thi… |
        | `accessibility.usage.resourceCreator.gatewayId` | string\|null |  |  | 2.0 | Identifier on the gateway |
        | `accessibility.usage.resourceCreator.name` ⁂ | Name\|null |  |  | 2.0 | Name of the organisation |
        | `accessibility.usage.resourceCreator.rorId` | string\|null |  |  | 2.0 | The Research Organization Registry (ROR) for the organisation, if applicable |

    ??? note "`linkage` — 27 fields"

        Relationships to other datasets, publications, tools and media.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `linkage` | Linkage\|null |  |  | 2.0 | Metadata for various linkages with datasets and other gateway entities |
        | `linkage.associatedMedia` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Any media associated with the Gateway Organisation using a valid URI for the content. This is an opportunit… |
        | `linkage.dataUses` | CommaSeparatedValues\|null |  |  | 2.0 | ?? |
        | `linkage.datasetLinkage` | DatasetLinkage\|null |  |  | 2.0 | Dataset Linkage copied over from |
        | `linkage.datasetLinkage.isDerivedFrom` | array\|null |  |  | 2.0 | Indicate if derived datasets or predefined extracts are available and the type of derivation available. Not… |
        | `linkage.datasetLinkage.isDerivedFrom[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isDerivedFrom[].title` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isDerivedFrom[].url` | Url\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isMemberOf` | array\|null |  |  | 2.0 | Dataset is a member of XXX(?) |
        | `linkage.datasetLinkage.isMemberOf[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isMemberOf[].title` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isMemberOf[].url` | Url\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isPartOf` | array\|null |  |  | 2.0 | If the dataset is part of a group or family |
        | `linkage.datasetLinkage.isPartOf[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isPartOf[].title` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isPartOf[].url` | Url\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.linkedDatasets` | array\|null |  |  | 2.0 | Links to other datasets. |
        | `linkage.datasetLinkage.linkedDatasets[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.linkedDatasets[].title` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.linkedDatasets[].url` | Url\|null |  |  | 2.0 |  |
        | `linkage.investigations` | CommaSeparatedValues\|null |  |  | 2.0 | Please provide the keystone paper associated with the dataset. |
        | `linkage.isGeneratedUsing` | CommaSeparatedValues\|null |  |  | 2.0 | ?? |
        | `linkage.isReferenceIn` | CommaSeparatedValues\|null |  |  | 2.0 | The keystone paper associated with the dataset. Also include a list of known citations, if available and sh… |
        | `linkage.publicationAboutDataset` | array\|null |  |  | 2.0 | DOIs for publications which describe the dataset. |
        | `linkage.publicationUsingDataset` | array\|null |  |  | 2.0 | DOIs for publications which use the dataset for analysis. |
        | `linkage.syntheticDataWebLink` | CommaSeparatedValues\|null |  |  | 2.0 | Links to locations of information and or raw downloads of synthetic data associated with this dataset |
        | `linkage.tools` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | URL of any analysis tools or models that have been created for this dataset and are available for further use |

    ??? note "`observations` — 6 fields"

        Structured population counts, one entry per observed measure.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `observations` | array\|null |  |  | 2.0 | Multiple observations about the dataset may be provided and users are expected to provide at least one obse… |
        | `observations[].disambiguatingDescription` | AbstractText\|null |  |  | 2.0 | If SNOMED CT term does not provide sufficient detail, please provide a description that disambiguates the p… |
        | `observations[].measuredProperty` | MeasuredProperty | ✓ |  | 2.0 | Initially this will be defaulted to "COUNT" |
        | `observations[].measuredValue` | integer | ✓ |  | 2.0 | Please provide the population size associated with the population type the dataset i.e. 1000 people in a st… |
        | `observations[].observationDate` | string\|string | ✓ |  | 2.0 | Please provide the date that the observation was made. Some datasets may be continuously updated and the nu… |
        | `observations[].observedNode` | StatisticalPopulationConstrainedV2 | ✓ |  | 2.0 | Please select one of the following statistical populations for you observation |

    ??? note "`structuralMetadata` — 12 fields"

        Table and column level technical metadata.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `structuralMetadata` | array\|null |  |  | 2.0 | Descriptions of all tables and data elements that can be included in the dataset |
        | `structuralMetadata[].columns` | array | ✓ |  | 2.0 | A list of columns contained within a table in a dataset. |
        | `structuralMetadata[].columns[].dataType` | string | ✓ |  | 2.0 | The name of a column in a table. |
        | `structuralMetadata[].columns[].description` | string\|null |  |  | 2.0 | A description of a column in a table. |
        | `structuralMetadata[].columns[].name` | Name | ✓ |  | 2.0 | The name of a column in a table. |
        | `structuralMetadata[].columns[].sensitive` | boolean | ✓ |  | 2.0 | A True or False value, indicating if the field is sensitive or not |
        | `structuralMetadata[].columns[].values` | array\|null |  |  | 2.0 | values in a dataset |
        | `structuralMetadata[].columns[].values[].description` | string\|null |  |  | 2.0 | A description of a unique value in a column. |
        | `structuralMetadata[].columns[].values[].frequency` | integer\|null |  |  | 2.0 | The frequency of occurrance of a value in a column |
        | `structuralMetadata[].columns[].values[].name` | Name | ✓ |  | 2.0 | Unique value in a column . |
        | `structuralMetadata[].description` | string\|null |  |  | 2.0 | A description of a table in a dataset. |
        | `structuralMetadata[].name` | string\|null |  |  | 2.0 | The name of a table in a dataset. |

    ??? note "`tissuesSampleCollection` — 24 fields"

        MIABIS-aligned biosample collection metadata.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `tissuesSampleCollection` | array\|null |  |  | 2.0 | metedata for tissue samples |
        | `tissuesSampleCollection[].accessConditions` | CommaSeparatedValues\|null |  |  | 2.0 | Access conditions for the tissue sample collection |
        | `tissuesSampleCollection[].collectionType` | CommaSeparatedValues\|null |  |  | 2.0 | The type of the sample collection. Can be several values [MIABIS-2.0-16](https://github.com/BBMRI-ERIC/miab… |
        | `tissuesSampleCollection[].dataCategories` | CommaSeparatedValues\|null |  |  | 2.0 | The type of data that is associated with the samples in the study. Can be several values MIABIS-2.0-13 |
        | `tissuesSampleCollection[].disease` | CommaSeparatedValues\|null |  |  | 2.0 | Disease associated with the tissue sample collection |
        | `tissuesSampleCollection[].id` | CommaSeparatedValues\|null |  |  | 2.0 | ID of the tissue sample collection |
        | `tissuesSampleCollection[].materialType` | CommaSeparatedValues\|null |  |  | 2.0 | The biospecimen saved from a biological entity for propagation e.g. testing, diagnostics, treatment or rese… |
        | `tissuesSampleCollection[].sampleAgeRange` | CommaSeparatedValues\|null |  |  | 2.0 | Age range of the tissue sample collection |
        | `tissuesSampleCollection[].storageTemperature` | CommaSeparatedValues\|null |  |  | 2.0 | Storage temperature of the tissue sample collection |
        | `tissuesSampleCollection[].tissueSampleMetadata` | TissueSampleMetadata\|null |  |  | 2.0 | Metadata related to the tissue sample |
        | `tissuesSampleCollection[].tissueSampleMetadata.anatomicalSiteFreeText` | CommaSeparatedValues\|null |  |  | 2.0 | Free text describing the anatomical site |
        | `tissuesSampleCollection[].tissueSampleMetadata.anatomicalSiteOntologyCode` | CommaSeparatedValues\|null |  |  | 2.0 | Ontology code for the anatomical site, this code must match an ICD-0-3 format |
        | `tissuesSampleCollection[].tissueSampleMetadata.anatomicalSiteOntologyDescription` | CommaSeparatedValues\|null |  |  | 2.0 | Ontology description for the anatomical site |
        | `tissuesSampleCollection[].tissueSampleMetadata.creationDate` | string\|string\|null |  |  | 2.0 | Date when the tissue sample metadata was created |
        | `tissuesSampleCollection[].tissueSampleMetadata.id` | string\|null |  |  | 2.0 | ID of the tissue sample metadata |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleContentDiagnosis` | CommaSeparatedValues\|null |  |  | 2.0 | Diagnosis related to the sample content |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor` | SampleDonor\|null |  |  | 2.0 | Information about the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor.birthDate` | string\|string\|null |  |  | 2.0 | Date of birth of the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor.dataCategories` | CommaSeparatedValues\|null |  |  | 2.0 | Data categories related to the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor.id` | string\|null |  |  | 2.0 | ID of the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor.sex` | string\|null |  |  | 2.0 | Sex of the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleType` | CommaSeparatedValues\|null |  |  | 2.0 | Type of the tissue sample |
        | `tissuesSampleCollection[].tissueSampleMetadata.storageTemperature` | string\|null |  |  | 2.0 | Storage temperature of the tissue sample |
        | `tissuesSampleCollection[].tissueSampleMetadata.useRestrictions` | CommaSeparatedValues\|null |  |  | 2.0 | Restrictions on the use of the tissue sample |

    ??? note "`demographicFrequency` — 11 fields"

        Age, ethnicity and disease frequency bins.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `demographicFrequency` | DemographicFrequency\|null |  |  | 2.0 | An object containing demographic frequency data categorised by age, ethnicity, and disease attributes. |
        | `demographicFrequency.age` | array\|null |  |  | 2.0 | Array of age bins and their corresponding counts. |
        | `demographicFrequency.age[].bin` | AgeEnum | ✓ |  | 2.0 |  |
        | `demographicFrequency.age[].count` | integer | ✓ |  | 2.0 |  |
        | `demographicFrequency.disease` | array\|null |  |  | 2.0 | Array of diseases and their corresponding counts. |
        | `demographicFrequency.disease[].count` | integer | ✓ |  | 2.0 |  |
        | `demographicFrequency.disease[].diseaseCode` | string\|integer | ✓ |  | 2.0 |  |
        | `demographicFrequency.disease[].diseaseCodeVocabulary` | DiseaseCodeEnum | ✓ |  | 2.0 |  |
        | `demographicFrequency.ethnicity` | array\|null |  |  | 2.0 | Array of ethnicity bins and their corresponding counts. |
        | `demographicFrequency.ethnicity[].bin` | EthnicityEnum | ✓ |  | 2.0 |  |
        | `demographicFrequency.ethnicity[].count` | integer | ✓ |  | 2.0 |  |

    ??? note "`omics` — 3 fields"

        Assay and platform for omics datasets.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `omics` | Omics\|null |  |  | 2.0 | Omics |
        | `omics.assay` | Assay\|null |  | `NMR spectroscopy, Mass-spectrometry, Whole genome sequencing, Exome sequencing, Genotyping by array, Transcriptome profiling by high-throughput sequencing, Transcriptome profiling by array, Amplicon sequencing, Methylation binding domain sequencing, Methylation profiling by high-throughput sequencing, Genomic variant calling, Chromatin accessibility profiling by high-throughput sequencing, Histone modification profiling by high-throughput sequencing, Chromatin immunoprecipitation sequencing, Whole genome shotgun sequencing, Whole transcriptome sequencing, Targeted mutation analysis` | 2.0 | The specific 'omics assay that generated the dataset. |
        | `omics.platform` | Platform\|null |  | `Other, NMR Nightingale, Metabolon, Biocrates, Illumina, Oxford Nanopore, 454, Hi-C, HiFi` | 2.0 | The specific technology or infrastructure used to perform the assay. If the omics platform used to create y… |

=== "GWDM 2.1"

    ??? note "`required` — 9 fields"

        Identity and versioning. **Written by the Gateway API — see the warning below.**

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `required` 🔒 | Required | ✓ |  | 2.0 | Required metadata needed for the GWDM |
        | `required.gatewayId` 🔒 | string | ✓ |  | 2.0 | Associated identifier (number) that is the BigInt key in our SQL database for the dataset version associate… |
        | `required.gatewayPid` 🔒 | string | ✓ |  | 2.0 | A unique persistent identifier for the metadata version. This is a 128-bit unique identifiers, as 32 hexade… |
        | `required.issued` 🔒 | string | ✓ |  | 2.0 | Datetime stamp of when this metadata version was initially issued |
        | `required.modified` 🔒 | string | ✓ |  | 2.0 | Datetime stamp of when this metadata was last modified |
        | `required.revisions` 🔒 | array | ✓ |  | 2.0 | A list of persistent identifiers and version numbers for previous versions of metadata for this dataset |
        | `required.revisions[].url` | Url\|null | ✓ |  | 2.0 | Some url with a reference to the record of a previous version of this dataset |
        | `required.revisions[].version` | string | ✓ |  | 2.0 | Version number used for previous version of this dataset |
        | `required.version` | string | ✓ |  | 2.0 | Dataset metadata version |

    ??? note "`summary` — 18 fields"

        Title, description, keywords, publisher, population size. The block search relies on most.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `summary` | Summary | ✓ |  | 2.0 | Summary of metadata describing key pieces of information. |
        | `summary.abstract` | LongAbstractText | ✓ |  | 2.0 | Longer abstract detailing the dataset. |
        | `summary.contactPoint` | string\|null |  |  | 2.0 | email of a person who can be the main contact point of this dataset |
        | `summary.controlledKeywords` | CommaSeparatedValues\|null |  |  | 2.0 | Keywords that have been filtered and limited |
        | `summary.datasetSubType` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Placeholder for dataset sub-type |
        | `summary.datasetType` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | What type of dataset is this? |
        | `summary.description` | LongDescription\|null |  |  | 2.0 | Longer description of the dataset in detail |
        | `summary.doiName` | Doi\|null |  |  | 2.0 | DOI associated to this dataset |
        | `summary.funders` ⁂ | CommaSeparatedValues\|null |  |  | 2.1 | Comma-separated list of funders for this dataset. |
        | `summary.inPipeline` | Pipeline\|null |  | `Available, Not available` | 2.0 | Indicate whether this dataset is currently available for Researchers to request access. |
        | `summary.keywords` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Comma separated key words associated to this dataset. |
        | `summary.populationSize` | integer\|null |  |  | 2.0 | Summary population size of the cohort |
        | `summary.publisher` 🔒 | Organisation\|null |  |  | 2.0 | Link to details about the publisher of this dataset |
        | `summary.publisher.gatewayId` | string\|null |  |  | 2.0 | Identifier on the gateway |
        | `summary.publisher.name` | Name\|null |  |  | 2.0 | Name of the organisation |
        | `summary.publisher.rorId` | string\|null |  |  | 2.0 | The Research Organization Registry (ROR) for the organisation, if applicable |
        | `summary.shortTitle` | ShortTitle\|null |  |  | 2.0 | A shorter descriptive title of the dataset |
        | `summary.title` | TwoHundredFiftyFiveCharacters | ✓ |  | 2.0 | The main title of the dataset |

    ??? note "`coverage` — 6 fields"

        Geographic, temporal and demographic reach of the cohort.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `coverage` | Coverage\|null |  |  | 2.0 | This information includes attributes for geographical and temporal coverage, cohort details etc. to enable… |
        | `coverage.datasetCompleteness` | Url\|null |  |  | 2.0 | The URL where a Researcher can learn more about the completeness of the dataset. |
        | `coverage.followUp` | FollowupV2\|null |  | `0 - 6 Months, 6 - 12 Months, 1 - 10 Years, > 10 Years, Unknown, Continuous, Other, null` | 2.0 | If known, what is the typical time span that a patient appears in the dataset (follow up period) |
        | `coverage.pathway` | LongDescription\|null |  |  | 2.0 | Please indicate if the dataset is representative of the patient pathway and any limitations the dataset may… |
        | `coverage.spatial` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | The geographical area covered by the dataset. It is recommended that links are to entries in a well-maintai… |
        | `coverage.typicalAgeRange` | AgeRange\|null |  |  | 2.0 | Please indicate the age range in whole years of participants in the dataset. Please provide range in the fo… |

    ??? note "`provenance` — 12 fields"

        Where the data came from and how often it is refreshed.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `provenance` | Provenance\|null |  |  | 2.0 | Provenance information allows researchers to understand data within the context of its origins and can be a… |
        | `provenance.origin` | Origin\|null |  |  | 2.0 |  |
        | `provenance.origin.collectionSituation` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please indicate the setting(s) where data was collected. Multiple settings may be provided |
        | `provenance.origin.imageContrast` | Ternary\|null |  | `Yes, No, Not stated` | 2.0 | Indicate whether usage of imaging contrast is captured within the dataset. |
        | `provenance.origin.purpose` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please indicate the purpose(s) that the dataset was collected. |
        | `provenance.origin.source` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please indicate the source of the data extraction |
        | `provenance.temporal` | object | ✓ |  | 2.0 |  |
        | `provenance.temporal.accrualPeriodicity` | PeriodicityV2 | ✓ |  | 2.0 | Please indicate the frequency of distribution release. If a dataset is distributed regularly please choose… |
        | `provenance.temporal.distributionReleaseDate` | string\|string\|null |  |  | 2.0 | Date of the latest release of the dataset. If this is a regular release i.e. quarterly, or this is a static… |
        | `provenance.temporal.endDate` | string\|string\|null |  |  | 2.0 | The end of the time period that the dataset provides coverage for. If the dataset is “Continuous” and has n… |
        | `provenance.temporal.startDate` | string\|string\|null |  |  | 2.0 | The start of the time period that the dataset provides coverage for. If there are multiple cohorts in the d… |
        | `provenance.temporal.timeLag` | TimeLagV2 | ✓ |  | 2.0 | Please indicate the typical time-lag between an event and the data for that event appearing in the dataset |

    ??? note "`accessibility` — 22 fields"

        Access rights, formats, standards and usage conditions. Required.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `accessibility` | Accessibility | ✓ |  | 2.0 | Accessibility information allows researchers to understand access, usage, limitations, formats, standards a… |
        | `accessibility.access` | Access | ✓ |  | 2.0 | This section includes information about data access |
        | `accessibility.access.accessRequestCost` ⁂ | LongDescription\|null |  |  | 2.0 | Please provide link(s) to a webpage detailing the commercial model for processing data access requests for… |
        | `accessibility.access.accessRights` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please provide details for the data access rights |
        | `accessibility.access.accessService` | LongDescription\|null |  |  | 2.0 | Please provide a brief description of the data access services that are available including: environment th… |
        | `accessibility.access.accessServiceCategory` | CommaSeparatedValues\|null |  |  | 2.0 | Where access to data come from: TRE/SED, direct access, open acccess, varies based on project. |
        | `accessibility.access.dataController` | LongDescription\|null |  |  | 2.0 | Data Controller means a person/entity who (either alone or jointly or in common with other persons/entities… |
        | `accessibility.access.dataProcessor` | LongDescription\|null |  |  | 2.0 | A Data Processor, in relation to any Data Subject data, specifically personal data, means any person/entity… |
        | `accessibility.access.deliveryLeadTime` | DeliveryLeadTimeV2\|null |  | `Less than 1 week, 1-2 weeks, 2-4 weeks, 1-2 months, 2-6 months, More than 6 months, Variable, Not applicable, Other` | 2.0 | Please provide an indication of the typical processing times based on the types of requests typically recei… |
        | `accessibility.access.jurisdiction` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please use country code from ISO 3166-1 country codes and the associated ISO 3166-2 for regions, cities, st… |
        | `accessibility.formatAndStandards` | FormatAndStandards\|null |  |  | 2.0 | Section includes technical attributes for language vocabularies, sizes etc. and gives researchers facts abo… |
        | `accessibility.formatAndStandards.conformsTo` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | What the vocabulary conforms to. |
        | `accessibility.formatAndStandards.formats` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Format(s) the dataset can be made available in |
        | `accessibility.formatAndStandards.languages` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Language code(s) of the language of the dataset metadata and underlying data is made available. |
        | `accessibility.formatAndStandards.vocabularyEncodingSchemes` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Code value of the ontology vocabulary encoding |
        | `accessibility.usage` | Usage\|null |  |  | 2.0 | This section includes information about how the data can be used and how it is currently being used |
        | `accessibility.usage.dataUseLimitation` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please provide an indication of consent permissions for datasets and/or materials, and relates to the purpo… |
        | `accessibility.usage.dataUseRequirement` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please indicate fit here are any additional conditions set for use if any, multiple requirements may be pro… |
        | `accessibility.usage.resourceCreator` | Organisation\|null |  |  | 2.0 | Please provide the text that you would like included as part of any citation that credits this dataset. Thi… |
        | `accessibility.usage.resourceCreator.gatewayId` | string\|null |  |  | 2.0 | Identifier on the gateway |
        | `accessibility.usage.resourceCreator.name` ⁂ | Name\|null |  |  | 2.0 | Name of the organisation |
        | `accessibility.usage.resourceCreator.rorId` | string\|null |  |  | 2.0 | The Research Organization Registry (ROR) for the organisation, if applicable |

    ??? note "`linkage` — 27 fields"

        Relationships to other datasets, publications, tools and media.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `linkage` | Linkage\|null |  |  | 2.0 | Metadata for various linkages with datasets and other gateway entities |
        | `linkage.associatedMedia` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Any media associated with the Gateway Organisation using a valid URI for the content. This is an opportunit… |
        | `linkage.dataUses` | CommaSeparatedValues\|null |  |  | 2.0 | ?? |
        | `linkage.datasetLinkage` | DatasetLinkage\|null |  |  | 2.0 | Dataset Linkage copied over from |
        | `linkage.datasetLinkage.isDerivedFrom` | array\|null |  |  | 2.0 | Indicate if derived datasets or predefined extracts are available and the type of derivation available. Not… |
        | `linkage.datasetLinkage.isDerivedFrom[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isDerivedFrom[].title` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isDerivedFrom[].url` | Url\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isMemberOf` | array\|null |  |  | 2.0 | Dataset is a member of XXX(?) |
        | `linkage.datasetLinkage.isMemberOf[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isMemberOf[].title` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isMemberOf[].url` | Url\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isPartOf` | array\|null |  |  | 2.0 | If the dataset is part of a group or family |
        | `linkage.datasetLinkage.isPartOf[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isPartOf[].title` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isPartOf[].url` | Url\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.linkedDatasets` | array\|null |  |  | 2.0 | Links to other datasets. |
        | `linkage.datasetLinkage.linkedDatasets[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.linkedDatasets[].title` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.linkedDatasets[].url` | Url\|null |  |  | 2.0 |  |
        | `linkage.investigations` | CommaSeparatedValues\|null |  |  | 2.0 | Please provide the keystone paper associated with the dataset. |
        | `linkage.isGeneratedUsing` | CommaSeparatedValues\|null |  |  | 2.0 | ?? |
        | `linkage.isReferenceIn` | CommaSeparatedValues\|null |  |  | 2.0 | The keystone paper associated with the dataset. Also include a list of known citations, if available and sh… |
        | `linkage.publicationAboutDataset` | array\|null |  |  | 2.0 | DOIs for publications which describe the dataset. |
        | `linkage.publicationUsingDataset` | array\|null |  |  | 2.0 | DOIs for publications which use the dataset for analysis. |
        | `linkage.syntheticDataWebLink` | CommaSeparatedValues\|null |  |  | 2.0 | Links to locations of information and or raw downloads of synthetic data associated with this dataset |
        | `linkage.tools` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | URL of any analysis tools or models that have been created for this dataset and are available for further use |

    ??? note "`observations` — 6 fields"

        Structured population counts, one entry per observed measure.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `observations` | array\|null |  |  | 2.0 | Multiple observations about the dataset may be provided and users are expected to provide at least one obse… |
        | `observations[].disambiguatingDescription` | AbstractText\|null |  |  | 2.0 | If SNOMED CT term does not provide sufficient detail, please provide a description that disambiguates the p… |
        | `observations[].measuredProperty` | MeasuredProperty | ✓ |  | 2.0 | Initially this will be defaulted to "COUNT" |
        | `observations[].measuredValue` | integer | ✓ |  | 2.0 | Please provide the population size associated with the population type the dataset i.e. 1000 people in a st… |
        | `observations[].observationDate` | string\|string | ✓ |  | 2.0 | Please provide the date that the observation was made. Some datasets may be continuously updated and the nu… |
        | `observations[].observedNode` | StatisticalPopulationConstrainedV2 | ✓ |  | 2.0 | Please select one of the following statistical populations for you observation |

    ??? note "`structuralMetadata` — 12 fields"

        Table and column level technical metadata.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `structuralMetadata` | array\|null |  |  | 2.0 | Descriptions of all tables and data elements that can be included in the dataset |
        | `structuralMetadata[].columns` | array | ✓ |  | 2.0 | A list of columns contained within a table in a dataset. |
        | `structuralMetadata[].columns[].dataType` | string | ✓ |  | 2.0 | The name of a column in a table. |
        | `structuralMetadata[].columns[].description` | string\|null |  |  | 2.0 | A description of a column in a table. |
        | `structuralMetadata[].columns[].name` | Name | ✓ |  | 2.0 | The name of a column in a table. |
        | `structuralMetadata[].columns[].sensitive` | boolean | ✓ |  | 2.0 | A True or False value, indicating if the field is sensitive or not |
        | `structuralMetadata[].columns[].values` | array\|null |  |  | 2.0 | values in a dataset |
        | `structuralMetadata[].columns[].values[].description` | string\|null |  |  | 2.0 | A description of a unique value in a column. |
        | `structuralMetadata[].columns[].values[].frequency` | integer\|null |  |  | 2.0 | The frequency of occurrance of a value in a column |
        | `structuralMetadata[].columns[].values[].name` | Name | ✓ |  | 2.0 | Unique value in a column . |
        | `structuralMetadata[].description` | string\|null |  |  | 2.0 | A description of a table in a dataset. |
        | `structuralMetadata[].name` | string\|null |  |  | 2.0 | The name of a table in a dataset. |

    ??? note "`tissuesSampleCollection` — 24 fields"

        MIABIS-aligned biosample collection metadata.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `tissuesSampleCollection` | array\|null |  |  | 2.0 | metedata for tissue samples |
        | `tissuesSampleCollection[].accessConditions` | CommaSeparatedValues\|null |  |  | 2.0 | Access conditions for the tissue sample collection |
        | `tissuesSampleCollection[].collectionType` | CommaSeparatedValues\|null |  |  | 2.0 | The type of the sample collection. Can be several values [MIABIS-2.0-16](https://github.com/BBMRI-ERIC/miab… |
        | `tissuesSampleCollection[].dataCategories` | CommaSeparatedValues\|null |  |  | 2.0 | The type of data that is associated with the samples in the study. Can be several values MIABIS-2.0-13 |
        | `tissuesSampleCollection[].disease` | CommaSeparatedValues\|null |  |  | 2.0 | Disease associated with the tissue sample collection |
        | `tissuesSampleCollection[].id` | CommaSeparatedValues\|null |  |  | 2.0 | ID of the tissue sample collection |
        | `tissuesSampleCollection[].materialType` | CommaSeparatedValues\|null |  |  | 2.0 | The biospecimen saved from a biological entity for propagation e.g. testing, diagnostics, treatment or rese… |
        | `tissuesSampleCollection[].sampleAgeRange` | CommaSeparatedValues\|null |  |  | 2.0 | Age range of the tissue sample collection |
        | `tissuesSampleCollection[].storageTemperature` | CommaSeparatedValues\|null |  |  | 2.0 | Storage temperature of the tissue sample collection |
        | `tissuesSampleCollection[].tissueSampleMetadata` | TissueSampleMetadata\|null |  |  | 2.0 | Metadata related to the tissue sample |
        | `tissuesSampleCollection[].tissueSampleMetadata.anatomicalSiteFreeText` | CommaSeparatedValues\|null |  |  | 2.0 | Free text describing the anatomical site |
        | `tissuesSampleCollection[].tissueSampleMetadata.anatomicalSiteOntologyCode` | CommaSeparatedValues\|null |  |  | 2.0 | Ontology code for the anatomical site, this code must match an ICD-0-3 format |
        | `tissuesSampleCollection[].tissueSampleMetadata.anatomicalSiteOntologyDescription` | CommaSeparatedValues\|null |  |  | 2.0 | Ontology description for the anatomical site |
        | `tissuesSampleCollection[].tissueSampleMetadata.creationDate` | string\|string\|null |  |  | 2.0 | Date when the tissue sample metadata was created |
        | `tissuesSampleCollection[].tissueSampleMetadata.id` | string\|null |  |  | 2.0 | ID of the tissue sample metadata |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleContentDiagnosis` | CommaSeparatedValues\|null |  |  | 2.0 | Diagnosis related to the sample content |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor` | SampleDonor\|null |  |  | 2.0 | Information about the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor.birthDate` | string\|string\|null |  |  | 2.0 | Date of birth of the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor.dataCategories` | CommaSeparatedValues\|null |  |  | 2.0 | Data categories related to the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor.id` | string\|null |  |  | 2.0 | ID of the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor.sex` | string\|null |  |  | 2.0 | Sex of the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleType` | CommaSeparatedValues\|null |  |  | 2.0 | Type of the tissue sample |
        | `tissuesSampleCollection[].tissueSampleMetadata.storageTemperature` | string\|null |  |  | 2.0 | Storage temperature of the tissue sample |
        | `tissuesSampleCollection[].tissueSampleMetadata.useRestrictions` | CommaSeparatedValues\|null |  |  | 2.0 | Restrictions on the use of the tissue sample |

    ??? note "`demographicFrequency` — 11 fields"

        Age, ethnicity and disease frequency bins.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `demographicFrequency` | DemographicFrequency\|null |  |  | 2.0 | An object containing demographic frequency data categorised by age, ethnicity, and disease attributes. |
        | `demographicFrequency.age` | array\|null |  |  | 2.0 | Array of age bins and their corresponding counts. |
        | `demographicFrequency.age[].bin` | AgeEnum | ✓ |  | 2.0 |  |
        | `demographicFrequency.age[].count` | integer | ✓ |  | 2.0 |  |
        | `demographicFrequency.disease` | array\|null |  |  | 2.0 | Array of diseases and their corresponding counts. |
        | `demographicFrequency.disease[].count` | integer | ✓ |  | 2.0 |  |
        | `demographicFrequency.disease[].diseaseCode` | string\|integer | ✓ |  | 2.0 |  |
        | `demographicFrequency.disease[].diseaseCodeVocabulary` | DiseaseCodeEnum | ✓ |  | 2.0 |  |
        | `demographicFrequency.ethnicity` | array\|null |  |  | 2.0 | Array of ethnicity bins and their corresponding counts. |
        | `demographicFrequency.ethnicity[].bin` | EthnicityEnum | ✓ |  | 2.0 |  |
        | `demographicFrequency.ethnicity[].count` | integer | ✓ |  | 2.0 |  |

    ??? note "`omics` — 3 fields"

        Assay and platform for omics datasets.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `omics` | Omics\|null |  |  | 2.0 | Omics |
        | `omics.assay` | Assay\|null |  | `NMR spectroscopy, Mass-spectrometry, Whole genome sequencing, Exome sequencing, Genotyping by array, Transcriptome profiling by high-throughput sequencing, Transcriptome profiling by array, Amplicon sequencing, Methylation binding domain sequencing, Methylation profiling by high-throughput sequencing, Genomic variant calling, Chromatin accessibility profiling by high-throughput sequencing, Histone modification profiling by high-throughput sequencing, Chromatin immunoprecipitation sequencing, Whole genome shotgun sequencing, Whole transcriptome sequencing, Targeted mutation analysis` | 2.0 | The specific 'omics assay that generated the dataset. |
        | `omics.platform` | Platform\|null |  | `Other, NMR Nightingale, Metabolon, Biocrates, Illumina, Oxford Nanopore, 454, Hi-C, HiFi` | 2.0 | The specific technology or infrastructure used to perform the assay. If the omics platform used to create y… |

    ??? note "`icons` — 1 field"

        Calculated categorisation icons, added on export. GWDM 2.1+.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `icons` | array\|null |  |  | 2.1 | Calculated categorization icons added during export. |

    ??? note "`projectGrants` — 9 fields"

        Associated project grants. GWDM 2.1+, driven by CRUK.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `projectGrants` | array\|null |  |  | 2.1 |  |
        | `projectGrants[].grantNumber` | string | ✓ |  | 2.1 | List of CRUK and any other grant numbers. |
        | `projectGrants[].leadResearchInstitute` | OneHundredFiftyCharacters | ✓ |  | 2.1 |  |
        | `projectGrants[].leadResearcher` | OneHundredFiftyCharacters | ✓ |  | 2.1 |  |
        | `projectGrants[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.1 |  |
        | `projectGrants[].projectGrantEndDate` | string\|null | ✓ |  | 2.1 | Current end date of project grant. |
        | `projectGrants[].projectGrantName` | OneHundredFiftyCharacters | ✓ |  | 2.1 | The Project Grant Title should be unique to the CRUK datahub. (Add your institute or name if necessary to d… |
        | `projectGrants[].projectGrantScope` | string\|null |  |  | 2.1 | data and biospecimens expected to result from the grant. |
        | `projectGrants[].projectGrantStartDate` | string | ✓ |  | 2.1 | Starting date of projectGrant grant. |

    ??? note "`datasetFilters` — 6 fields"

        Categorisation tags for cancer type, data type and access. GWDM 2.1+.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `datasetFilters` | array\|null |  |  | 2.1 | Categorization tags regarding cancer type, data type, and access. |
        | `datasetFilters[].category` | string | ✓ |  | 2.1 |  |
        | `datasetFilters[].description` | string | ✓ |  | 2.1 |  |
        | `datasetFilters[].id` | string | ✓ |  | 2.1 |  |
        | `datasetFilters[].label` | string | ✓ |  | 2.1 |  |
        | `datasetFilters[].primaryGroup` | string | ✓ | `cancer-type, data-type, access-type` | 2.1 |  |

    ??? note "`erd` — 3 fields"

        Entity-relationship diagram of the dataset's tables. GWDM 2.1+.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `erd` | Image\|null |  |  | 2.1 | Visual representation of data table relationships. |
        | `erd.description` | Description\|null |  |  | 2.1 |  |
        | `erd.image` | string\|null |  |  | 2.1 | An image file. |

=== "GWDM 2.2"

    No GWDM 2.2 schema exists yet, so the rows below are **projected**:
    GWDM 2.1's fields plus the 3 paths HDRUK 4.1.0
    introduced. **GWDM 2.2 extends 2.1**, so it is a superset of everything in
    the 2.1 tab — including `projectGrants`, `datasetFilters`, `erd`, `icons`
    and `summary.funders`.

    Treat the three DUO rows as indicative on **shape** — whether `duoCodes`
    lands as a delimited string or a real array, and whether
    `patientRecontact` stays nested, is not settled until the model is
    written. See [The GWDM explained](gwdm.md#how-22-relates-to-21).

    !!! note "The current translation map lags this"
        `maps/GWDM/2.2/HDRUK/4.1.0/translation.jsonata` is scaffolding copied
        from the 2.0-targeted map, so it emits only 2.0's fields plus the DUO
        paths — not the 2.1 sections. That is an **unfinished map**, not the
        design. A field-by-field record of what it emits today is in
        [`fields-gwdm-2.2-UNVERIFIED.tsv`](../examples/fields-gwdm-2.2-UNVERIFIED.tsv).

    ??? note "`required` — 9 fields"

        Identity and versioning. **Written by the Gateway API — see the warning below.**

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `required` 🔒 | Required | ✓ |  | 2.0 | Required metadata needed for the GWDM |
        | `required.gatewayId` 🔒 | string | ✓ |  | 2.0 | Associated identifier (number) that is the BigInt key in our SQL database for the dataset version associate… |
        | `required.gatewayPid` 🔒 | string | ✓ |  | 2.0 | A unique persistent identifier for the metadata version. This is a 128-bit unique identifiers, as 32 hexade… |
        | `required.issued` 🔒 | string | ✓ |  | 2.0 | Datetime stamp of when this metadata version was initially issued |
        | `required.modified` 🔒 | string | ✓ |  | 2.0 | Datetime stamp of when this metadata was last modified |
        | `required.revisions` 🔒 | array | ✓ |  | 2.0 | A list of persistent identifiers and version numbers for previous versions of metadata for this dataset |
        | `required.revisions[].url` | Url\|null | ✓ |  | 2.0 | Some url with a reference to the record of a previous version of this dataset |
        | `required.revisions[].version` | string | ✓ |  | 2.0 | Version number used for previous version of this dataset |
        | `required.version` | string | ✓ |  | 2.0 | Dataset metadata version |

    ??? note "`summary` — 18 fields"

        Title, description, keywords, publisher, population size. The block search relies on most.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `summary` | Summary | ✓ |  | 2.0 | Summary of metadata describing key pieces of information. |
        | `summary.abstract` | LongAbstractText | ✓ |  | 2.0 | Longer abstract detailing the dataset. |
        | `summary.contactPoint` | string\|null |  |  | 2.0 | email of a person who can be the main contact point of this dataset |
        | `summary.controlledKeywords` | CommaSeparatedValues\|null |  |  | 2.0 | Keywords that have been filtered and limited |
        | `summary.datasetSubType` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Placeholder for dataset sub-type |
        | `summary.datasetType` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | What type of dataset is this? |
        | `summary.description` | LongDescription\|null |  |  | 2.0 | Longer description of the dataset in detail |
        | `summary.doiName` | Doi\|null |  |  | 2.0 | DOI associated to this dataset |
        | `summary.funders` ⁂ | CommaSeparatedValues\|null |  |  | 2.1 | Comma-separated list of funders for this dataset. |
        | `summary.inPipeline` | Pipeline\|null |  | `Available, Not available` | 2.0 | Indicate whether this dataset is currently available for Researchers to request access. |
        | `summary.keywords` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Comma separated key words associated to this dataset. |
        | `summary.populationSize` | integer\|null |  |  | 2.0 | Summary population size of the cohort |
        | `summary.publisher` 🔒 | Organisation\|null |  |  | 2.0 | Link to details about the publisher of this dataset |
        | `summary.publisher.gatewayId` | string\|null |  |  | 2.0 | Identifier on the gateway |
        | `summary.publisher.name` | Name\|null |  |  | 2.0 | Name of the organisation |
        | `summary.publisher.rorId` | string\|null |  |  | 2.0 | The Research Organization Registry (ROR) for the organisation, if applicable |
        | `summary.shortTitle` | ShortTitle\|null |  |  | 2.0 | A shorter descriptive title of the dataset |
        | `summary.title` | TwoHundredFiftyFiveCharacters | ✓ |  | 2.0 | The main title of the dataset |

    ??? note "`coverage` — 6 fields"

        Geographic, temporal and demographic reach of the cohort.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `coverage` | Coverage\|null |  |  | 2.0 | This information includes attributes for geographical and temporal coverage, cohort details etc. to enable… |
        | `coverage.datasetCompleteness` | Url\|null |  |  | 2.0 | The URL where a Researcher can learn more about the completeness of the dataset. |
        | `coverage.followUp` | FollowupV2\|null |  | `0 - 6 Months, 6 - 12 Months, 1 - 10 Years, > 10 Years, Unknown, Continuous, Other, null` | 2.0 | If known, what is the typical time span that a patient appears in the dataset (follow up period) |
        | `coverage.pathway` | LongDescription\|null |  |  | 2.0 | Please indicate if the dataset is representative of the patient pathway and any limitations the dataset may… |
        | `coverage.spatial` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | The geographical area covered by the dataset. It is recommended that links are to entries in a well-maintai… |
        | `coverage.typicalAgeRange` | AgeRange\|null |  |  | 2.0 | Please indicate the age range in whole years of participants in the dataset. Please provide range in the fo… |

    ??? note "`provenance` — 12 fields"

        Where the data came from and how often it is refreshed.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `provenance` | Provenance\|null |  |  | 2.0 | Provenance information allows researchers to understand data within the context of its origins and can be a… |
        | `provenance.origin` | Origin\|null |  |  | 2.0 |  |
        | `provenance.origin.collectionSituation` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please indicate the setting(s) where data was collected. Multiple settings may be provided |
        | `provenance.origin.imageContrast` | Ternary\|null |  | `Yes, No, Not stated` | 2.0 | Indicate whether usage of imaging contrast is captured within the dataset. |
        | `provenance.origin.purpose` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please indicate the purpose(s) that the dataset was collected. |
        | `provenance.origin.source` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please indicate the source of the data extraction |
        | `provenance.temporal` | object | ✓ |  | 2.0 |  |
        | `provenance.temporal.accrualPeriodicity` | PeriodicityV2 | ✓ |  | 2.0 | Please indicate the frequency of distribution release. If a dataset is distributed regularly please choose… |
        | `provenance.temporal.distributionReleaseDate` | string\|string\|null |  |  | 2.0 | Date of the latest release of the dataset. If this is a regular release i.e. quarterly, or this is a static… |
        | `provenance.temporal.endDate` | string\|string\|null |  |  | 2.0 | The end of the time period that the dataset provides coverage for. If the dataset is “Continuous” and has n… |
        | `provenance.temporal.startDate` | string\|string\|null |  |  | 2.0 | The start of the time period that the dataset provides coverage for. If there are multiple cohorts in the d… |
        | `provenance.temporal.timeLag` | TimeLagV2 | ✓ |  | 2.0 | Please indicate the typical time-lag between an event and the data for that event appearing in the dataset |

    ??? note "`accessibility` — 25 fields"

        Access rights, formats, standards and usage conditions. Required.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `accessibility` | Accessibility | ✓ |  | 2.0 | Accessibility information allows researchers to understand access, usage, limitations, formats, standards a… |
        | `accessibility.access` | Access | ✓ |  | 2.0 | This section includes information about data access |
        | `accessibility.access.accessRequestCost` ⁂ | LongDescription\|null |  |  | 2.0 | Please provide link(s) to a webpage detailing the commercial model for processing data access requests for… |
        | `accessibility.access.accessRights` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please provide details for the data access rights |
        | `accessibility.access.accessService` | LongDescription\|null |  |  | 2.0 | Please provide a brief description of the data access services that are available including: environment th… |
        | `accessibility.access.accessServiceCategory` | CommaSeparatedValues\|null |  |  | 2.0 | Where access to data come from: TRE/SED, direct access, open acccess, varies based on project. |
        | `accessibility.access.dataController` | LongDescription\|null |  |  | 2.0 | Data Controller means a person/entity who (either alone or jointly or in common with other persons/entities… |
        | `accessibility.access.dataProcessor` | LongDescription\|null |  |  | 2.0 | A Data Processor, in relation to any Data Subject data, specifically personal data, means any person/entity… |
        | `accessibility.access.deliveryLeadTime` | DeliveryLeadTimeV2\|null |  | `Less than 1 week, 1-2 weeks, 2-4 weeks, 1-2 months, 2-6 months, More than 6 months, Variable, Not applicable, Other` | 2.0 | Please provide an indication of the typical processing times based on the types of requests typically recei… |
        | `accessibility.access.jurisdiction` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please use country code from ISO 3166-1 country codes and the associated ISO 3166-2 for regions, cities, st… |
        | `accessibility.formatAndStandards` | FormatAndStandards\|null |  |  | 2.0 | Section includes technical attributes for language vocabularies, sizes etc. and gives researchers facts abo… |
        | `accessibility.formatAndStandards.conformsTo` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | What the vocabulary conforms to. |
        | `accessibility.formatAndStandards.formats` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Format(s) the dataset can be made available in |
        | `accessibility.formatAndStandards.languages` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Language code(s) of the language of the dataset metadata and underlying data is made available. |
        | `accessibility.formatAndStandards.vocabularyEncodingSchemes` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Code value of the ontology vocabulary encoding |
        | `accessibility.usage` | Usage\|null |  |  | 2.0 | This section includes information about how the data can be used and how it is currently being used |
        | `accessibility.usage.dataUseLimitation` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please provide an indication of consent permissions for datasets and/or materials, and relates to the purpo… |
        | `accessibility.usage.dataUsePermissions` | DataUsePermissions\|null |  |  | 2.2 | Permissions relating to how people and materials within this dataset may be used, beyond the general access… |
        | `accessibility.usage.dataUsePermissions.patientRecontact` | boolean\|null |  |  | 2.2 | Indicates whether the people from whom the dataset is generated can be recontacted as part of a follow-up o… |
        | `accessibility.usage.dataUseRequirement` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Please indicate fit here are any additional conditions set for use if any, multiple requirements may be pro… |
        | `accessibility.usage.duoCodes` ⁂ | CommaSeparatedValues\|null |  |  | 2.2 | Machine-readable codes from the GA4GH Data Use Ontology describing the permitted or restricted uses of this… |
        | `accessibility.usage.resourceCreator` | Organisation\|null |  |  | 2.0 | Please provide the text that you would like included as part of any citation that credits this dataset. Thi… |
        | `accessibility.usage.resourceCreator.gatewayId` | string\|null |  |  | 2.0 | Identifier on the gateway |
        | `accessibility.usage.resourceCreator.name` ⁂ | Name\|null |  |  | 2.0 | Name of the organisation |
        | `accessibility.usage.resourceCreator.rorId` | string\|null |  |  | 2.0 | The Research Organization Registry (ROR) for the organisation, if applicable |

    ??? note "`linkage` — 27 fields"

        Relationships to other datasets, publications, tools and media.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `linkage` | Linkage\|null |  |  | 2.0 | Metadata for various linkages with datasets and other gateway entities |
        | `linkage.associatedMedia` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | Any media associated with the Gateway Organisation using a valid URI for the content. This is an opportunit… |
        | `linkage.dataUses` | CommaSeparatedValues\|null |  |  | 2.0 | ?? |
        | `linkage.datasetLinkage` | DatasetLinkage\|null |  |  | 2.0 | Dataset Linkage copied over from |
        | `linkage.datasetLinkage.isDerivedFrom` | array\|null |  |  | 2.0 | Indicate if derived datasets or predefined extracts are available and the type of derivation available. Not… |
        | `linkage.datasetLinkage.isDerivedFrom[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isDerivedFrom[].title` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isDerivedFrom[].url` | Url\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isMemberOf` | array\|null |  |  | 2.0 | Dataset is a member of XXX(?) |
        | `linkage.datasetLinkage.isMemberOf[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isMemberOf[].title` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isMemberOf[].url` | Url\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isPartOf` | array\|null |  |  | 2.0 | If the dataset is part of a group or family |
        | `linkage.datasetLinkage.isPartOf[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isPartOf[].title` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.isPartOf[].url` | Url\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.linkedDatasets` | array\|null |  |  | 2.0 | Links to other datasets. |
        | `linkage.datasetLinkage.linkedDatasets[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.linkedDatasets[].title` | OneHundredFiftyCharacters\|null |  |  | 2.0 |  |
        | `linkage.datasetLinkage.linkedDatasets[].url` | Url\|null |  |  | 2.0 |  |
        | `linkage.investigations` | CommaSeparatedValues\|null |  |  | 2.0 | Please provide the keystone paper associated with the dataset. |
        | `linkage.isGeneratedUsing` | CommaSeparatedValues\|null |  |  | 2.0 | ?? |
        | `linkage.isReferenceIn` | CommaSeparatedValues\|null |  |  | 2.0 | The keystone paper associated with the dataset. Also include a list of known citations, if available and sh… |
        | `linkage.publicationAboutDataset` | array\|null |  |  | 2.0 | DOIs for publications which describe the dataset. |
        | `linkage.publicationUsingDataset` | array\|null |  |  | 2.0 | DOIs for publications which use the dataset for analysis. |
        | `linkage.syntheticDataWebLink` | CommaSeparatedValues\|null |  |  | 2.0 | Links to locations of information and or raw downloads of synthetic data associated with this dataset |
        | `linkage.tools` ⁂ | CommaSeparatedValues\|null |  |  | 2.0 | URL of any analysis tools or models that have been created for this dataset and are available for further use |

    ??? note "`observations` — 6 fields"

        Structured population counts, one entry per observed measure.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `observations` | array\|null |  |  | 2.0 | Multiple observations about the dataset may be provided and users are expected to provide at least one obse… |
        | `observations[].disambiguatingDescription` | AbstractText\|null |  |  | 2.0 | If SNOMED CT term does not provide sufficient detail, please provide a description that disambiguates the p… |
        | `observations[].measuredProperty` | MeasuredProperty | ✓ |  | 2.0 | Initially this will be defaulted to "COUNT" |
        | `observations[].measuredValue` | integer | ✓ |  | 2.0 | Please provide the population size associated with the population type the dataset i.e. 1000 people in a st… |
        | `observations[].observationDate` | string\|string | ✓ |  | 2.0 | Please provide the date that the observation was made. Some datasets may be continuously updated and the nu… |
        | `observations[].observedNode` | StatisticalPopulationConstrainedV2 | ✓ |  | 2.0 | Please select one of the following statistical populations for you observation |

    ??? note "`structuralMetadata` — 12 fields"

        Table and column level technical metadata.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `structuralMetadata` | array\|null |  |  | 2.0 | Descriptions of all tables and data elements that can be included in the dataset |
        | `structuralMetadata[].columns` | array | ✓ |  | 2.0 | A list of columns contained within a table in a dataset. |
        | `structuralMetadata[].columns[].dataType` | string | ✓ |  | 2.0 | The name of a column in a table. |
        | `structuralMetadata[].columns[].description` | string\|null |  |  | 2.0 | A description of a column in a table. |
        | `structuralMetadata[].columns[].name` | Name | ✓ |  | 2.0 | The name of a column in a table. |
        | `structuralMetadata[].columns[].sensitive` | boolean | ✓ |  | 2.0 | A True or False value, indicating if the field is sensitive or not |
        | `structuralMetadata[].columns[].values` | array\|null |  |  | 2.0 | values in a dataset |
        | `structuralMetadata[].columns[].values[].description` | string\|null |  |  | 2.0 | A description of a unique value in a column. |
        | `structuralMetadata[].columns[].values[].frequency` | integer\|null |  |  | 2.0 | The frequency of occurrance of a value in a column |
        | `structuralMetadata[].columns[].values[].name` | Name | ✓ |  | 2.0 | Unique value in a column . |
        | `structuralMetadata[].description` | string\|null |  |  | 2.0 | A description of a table in a dataset. |
        | `structuralMetadata[].name` | string\|null |  |  | 2.0 | The name of a table in a dataset. |

    ??? note "`tissuesSampleCollection` — 24 fields"

        MIABIS-aligned biosample collection metadata.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `tissuesSampleCollection` | array\|null |  |  | 2.0 | metedata for tissue samples |
        | `tissuesSampleCollection[].accessConditions` | CommaSeparatedValues\|null |  |  | 2.0 | Access conditions for the tissue sample collection |
        | `tissuesSampleCollection[].collectionType` | CommaSeparatedValues\|null |  |  | 2.0 | The type of the sample collection. Can be several values [MIABIS-2.0-16](https://github.com/BBMRI-ERIC/miab… |
        | `tissuesSampleCollection[].dataCategories` | CommaSeparatedValues\|null |  |  | 2.0 | The type of data that is associated with the samples in the study. Can be several values MIABIS-2.0-13 |
        | `tissuesSampleCollection[].disease` | CommaSeparatedValues\|null |  |  | 2.0 | Disease associated with the tissue sample collection |
        | `tissuesSampleCollection[].id` | CommaSeparatedValues\|null |  |  | 2.0 | ID of the tissue sample collection |
        | `tissuesSampleCollection[].materialType` | CommaSeparatedValues\|null |  |  | 2.0 | The biospecimen saved from a biological entity for propagation e.g. testing, diagnostics, treatment or rese… |
        | `tissuesSampleCollection[].sampleAgeRange` | CommaSeparatedValues\|null |  |  | 2.0 | Age range of the tissue sample collection |
        | `tissuesSampleCollection[].storageTemperature` | CommaSeparatedValues\|null |  |  | 2.0 | Storage temperature of the tissue sample collection |
        | `tissuesSampleCollection[].tissueSampleMetadata` | TissueSampleMetadata\|null |  |  | 2.0 | Metadata related to the tissue sample |
        | `tissuesSampleCollection[].tissueSampleMetadata.anatomicalSiteFreeText` | CommaSeparatedValues\|null |  |  | 2.0 | Free text describing the anatomical site |
        | `tissuesSampleCollection[].tissueSampleMetadata.anatomicalSiteOntologyCode` | CommaSeparatedValues\|null |  |  | 2.0 | Ontology code for the anatomical site, this code must match an ICD-0-3 format |
        | `tissuesSampleCollection[].tissueSampleMetadata.anatomicalSiteOntologyDescription` | CommaSeparatedValues\|null |  |  | 2.0 | Ontology description for the anatomical site |
        | `tissuesSampleCollection[].tissueSampleMetadata.creationDate` | string\|string\|null |  |  | 2.0 | Date when the tissue sample metadata was created |
        | `tissuesSampleCollection[].tissueSampleMetadata.id` | string\|null |  |  | 2.0 | ID of the tissue sample metadata |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleContentDiagnosis` | CommaSeparatedValues\|null |  |  | 2.0 | Diagnosis related to the sample content |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor` | SampleDonor\|null |  |  | 2.0 | Information about the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor.birthDate` | string\|string\|null |  |  | 2.0 | Date of birth of the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor.dataCategories` | CommaSeparatedValues\|null |  |  | 2.0 | Data categories related to the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor.id` | string\|null |  |  | 2.0 | ID of the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleDonor.sex` | string\|null |  |  | 2.0 | Sex of the sample donor |
        | `tissuesSampleCollection[].tissueSampleMetadata.sampleType` | CommaSeparatedValues\|null |  |  | 2.0 | Type of the tissue sample |
        | `tissuesSampleCollection[].tissueSampleMetadata.storageTemperature` | string\|null |  |  | 2.0 | Storage temperature of the tissue sample |
        | `tissuesSampleCollection[].tissueSampleMetadata.useRestrictions` | CommaSeparatedValues\|null |  |  | 2.0 | Restrictions on the use of the tissue sample |

    ??? note "`demographicFrequency` — 11 fields"

        Age, ethnicity and disease frequency bins.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `demographicFrequency` | DemographicFrequency\|null |  |  | 2.0 | An object containing demographic frequency data categorised by age, ethnicity, and disease attributes. |
        | `demographicFrequency.age` | array\|null |  |  | 2.0 | Array of age bins and their corresponding counts. |
        | `demographicFrequency.age[].bin` | AgeEnum | ✓ |  | 2.0 |  |
        | `demographicFrequency.age[].count` | integer | ✓ |  | 2.0 |  |
        | `demographicFrequency.disease` | array\|null |  |  | 2.0 | Array of diseases and their corresponding counts. |
        | `demographicFrequency.disease[].count` | integer | ✓ |  | 2.0 |  |
        | `demographicFrequency.disease[].diseaseCode` | string\|integer | ✓ |  | 2.0 |  |
        | `demographicFrequency.disease[].diseaseCodeVocabulary` | DiseaseCodeEnum | ✓ |  | 2.0 |  |
        | `demographicFrequency.ethnicity` | array\|null |  |  | 2.0 | Array of ethnicity bins and their corresponding counts. |
        | `demographicFrequency.ethnicity[].bin` | EthnicityEnum | ✓ |  | 2.0 |  |
        | `demographicFrequency.ethnicity[].count` | integer | ✓ |  | 2.0 |  |

    ??? note "`omics` — 3 fields"

        Assay and platform for omics datasets.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `omics` | Omics\|null |  |  | 2.0 | Omics |
        | `omics.assay` | Assay\|null |  | `NMR spectroscopy, Mass-spectrometry, Whole genome sequencing, Exome sequencing, Genotyping by array, Transcriptome profiling by high-throughput sequencing, Transcriptome profiling by array, Amplicon sequencing, Methylation binding domain sequencing, Methylation profiling by high-throughput sequencing, Genomic variant calling, Chromatin accessibility profiling by high-throughput sequencing, Histone modification profiling by high-throughput sequencing, Chromatin immunoprecipitation sequencing, Whole genome shotgun sequencing, Whole transcriptome sequencing, Targeted mutation analysis` | 2.0 | The specific 'omics assay that generated the dataset. |
        | `omics.platform` | Platform\|null |  | `Other, NMR Nightingale, Metabolon, Biocrates, Illumina, Oxford Nanopore, 454, Hi-C, HiFi` | 2.0 | The specific technology or infrastructure used to perform the assay. If the omics platform used to create y… |

    ??? note "`icons` — 1 field"

        Calculated categorisation icons, added on export. GWDM 2.1+.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `icons` | array\|null |  |  | 2.1 | Calculated categorization icons added during export. |

    ??? note "`projectGrants` — 9 fields"

        Associated project grants. GWDM 2.1+, driven by CRUK.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `projectGrants` | array\|null |  |  | 2.1 |  |
        | `projectGrants[].grantNumber` | string | ✓ |  | 2.1 | List of CRUK and any other grant numbers. |
        | `projectGrants[].leadResearchInstitute` | OneHundredFiftyCharacters | ✓ |  | 2.1 |  |
        | `projectGrants[].leadResearcher` | OneHundredFiftyCharacters | ✓ |  | 2.1 |  |
        | `projectGrants[].pid` | OneHundredFiftyCharacters\|null |  |  | 2.1 |  |
        | `projectGrants[].projectGrantEndDate` | string\|null | ✓ |  | 2.1 | Current end date of project grant. |
        | `projectGrants[].projectGrantName` | OneHundredFiftyCharacters | ✓ |  | 2.1 | The Project Grant Title should be unique to the CRUK datahub. (Add your institute or name if necessary to d… |
        | `projectGrants[].projectGrantScope` | string\|null |  |  | 2.1 | data and biospecimens expected to result from the grant. |
        | `projectGrants[].projectGrantStartDate` | string | ✓ |  | 2.1 | Starting date of projectGrant grant. |

    ??? note "`datasetFilters` — 6 fields"

        Categorisation tags for cancer type, data type and access. GWDM 2.1+.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `datasetFilters` | array\|null |  |  | 2.1 | Categorization tags regarding cancer type, data type, and access. |
        | `datasetFilters[].category` | string | ✓ |  | 2.1 |  |
        | `datasetFilters[].description` | string | ✓ |  | 2.1 |  |
        | `datasetFilters[].id` | string | ✓ |  | 2.1 |  |
        | `datasetFilters[].label` | string | ✓ |  | 2.1 |  |
        | `datasetFilters[].primaryGroup` | string | ✓ | `cancer-type, data-type, access-type` | 2.1 |  |

    ??? note "`erd` — 3 fields"

        Entity-relationship diagram of the dataset's tables. GWDM 2.1+.

        | Field | Type | Req | Values | Introduced | Description |
        |---|---|---|---|---|---|
        | `erd` | Image\|null |  |  | 2.1 | Visual representation of data table relationships. |
        | `erd.description` | Description\|null |  |  | 2.1 |  |
        | `erd.image` | string\|null |  |  | 2.1 | An image file. |

## Regenerating this page

```bash
# 1. refresh the field inventories from schemata
python3 docs/examples/field_inventory.py ../schemata-2

# 2. rebuild this page from them
python3 docs/examples/gwdm_reference.py
```

Both scripts are committed next to their output in `docs/examples/`. Step 1
needs a local checkout of [`HDRUK/schemata`](https://github.com/HDRUK/schemata);
step 2 needs nothing but the TSVs.

Once GWDM 2.2 lands in `schemata`, set its `VERSIONS` row in
`gwdm_reference.py` to the real `fields-gwdm-2.2.tsv` and clear its
`unverified` flag. The projection and both admonitions then disappear on
their own — see `FACTS.md` F28 for the full fill-in list.
