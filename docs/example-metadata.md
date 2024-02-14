## HDRUK 2.1.2 Schema

### SAIL

??? example "Education Daily Attendance Dataset (EDAD)"

    ```json

    {
        "identifier": "https://web.www.healthdatagateway.org/7eb5d9ff-0d54-4438-9c60-423848aebb4c",
        "version": "11.0.0",
        "issued": "2023-08-17T00:00:00.000Z",
        "modified": "2023-08-17T00:00:00.000Z",
        "revisions": [],
        "summary": {
                "title": "Education Daily Attendance Dataset (EDAD)",
                "abstract": "This dataset provides information about daily educational attendance within Wales.",
                "publisher": {
                    "identifier": "https://web.www.healthdatagateway.org/5f3f98068af2ef61552e1d75",
                    "name": "SAIL",
                    "logo": null,
                    "description": null,
                    "contactPoint": null,
                    "memberOf": "ALLIANCE"
                },
                "contactPoint": "SAILDatabank@swansea.ac.uk",
                "keywords": "Education, SAIL,EDAD,core-res,Health & Wellbeing,Children & Young People,Inequality & Social Inclusion, Housing & Communities",
                "alternateIdentifiers": null,
                "doiName": null
        },
        "documentation": {
                "description": "This dataset provides detailed information about daily educational attendance within Wales.\n\nAttendance data in the EDUW schema was discontinued after 2019 and the Education Daily Attendance Dataset (EDAD) schema replaced it. This dataset contains more detailed information on attendance than was previously available in EDUW.\n\nThere is no ALF within this dataset, projects will need apply for education (EDUW) data to enable ALF linkage to other datasets",
                "associatedMedia": "https://saildatabank.com/about-us/",
                "isPartOf": null
        },
        "coverage": {
                "spatial": "United Kingdom,Wales",
                "typicalAgeRange": "0-20",
                "physicalSampleAvailability": null,
                "followup": "0 - 6 MONTHS",
                "pathway": "Education"
        },
        "provenance": {
                "origin": {
                    "purpose": "ADMINISTRATIVE",
                    "source": "OTHER",
                    "collectionSituation": "OTHER"
                },
                "temporal": {
                    "accrualPeriodicity": "MONTHLY",
                    "distributionReleaseDate": null,
                    "startDate": "2020-09-01",
                    "endDate": "2021-12-17",
                    "timeLag": "2-6 MONTHS"
                }
        },
        "accessibility": {
                "usage": {
                    "dataUseLimitation": "GENERAL RESEARCH USE",
                    "dataUseRequirements": "PROJECT SPECIFIC RESTRICTIONS,USER SPECIFIC RESTRICTION",
                    "resourceCreator": "Welsh Government",
                    "investigations": null,
                    "isReferencedBy": "Littlecott HJ, Moore GF, Moore L, Lyons RA, Murphy S. Association between breakfast consumption and educational outcomes in 9-11-year-old children. Public Health Nutr. 2016 Jun;19(9):1575-82. doi: 10.1017/S1368980015002669. Epub 2015 Sep 28. Erratum in: Public Health Nutr. 2016 Jun;19(9):1583. PMID: 26411331; PMCID: PMC4873891. "
                },
                "access": {
                    "accessRights": "https://saildatabank.com/data/apply-to-work-with-the-data/",
                    "accessService": "The SAIL Databank is powered by the UK Secure e-Research Platform (UKSeRP). Following approval through safeguard processes, access to project-specific data within the secure environment is permitted using two-factor authentication.",
                    "accessRequestCost": "Data provision is free from SAIL. Overall project costing depends on the number of people that require access to the SAIL Gateway, the activities that SAIL needs to complete (e.g. loading non-standard datasets), data refreshes, analytical work required, disclosure control process, and special case technological requirements.",
                    "deliveryLeadTime": null,
                    "jurisdiction": "GB",
                    "dataProcessor": "SAIL Databank",
                    "dataController": "Welsh Government"
                },
                "formatAndStandards": {
                    "vocabularyEncodingScheme": "LOCAL",
                    "conformsTo": "LOCAL",
                    "language": "en",
                    "format": "SQL database table"
                }
        },
        "enrichmentAndLinkage": {
                "qualifiedRelation": "Yes. To any SAIL dataset & reference data.",
                "derivation": null,
                "tools": "https://conceptlibrary.saildatabank.com/"
        },
        "observations": [
                {
                    "observedNode": "EVENTS",
                    "measuredValue": 3000000,
                    "observationDate": "2021-09-01",
                    "measuredProperty": "Count",
                    "disambiguatingDescription": "Approx 70-80% coverage of Welsh population through GP registrations."
                }
        ],
        "structuralMetadata": [
                {
                    "name": "EDAD",
                    "description": "Education Daily Activity Dataset table",
                    "elements": [
                            {
                                "name": "AVAIL_FROM_DT",
                                "description": "Date when the data made available i.e. date of loading",
                                "dataType": "DATE",
                                "sensitive": false
                            }
                    ]
                },
                {
                    "name": "EDAD",
                    "description": "Education Daily Activity Dataset table",
                    "elements": [
                            {
                                "name": "DATEATTENDANCE",
                                "description": "Date of session attendance",
                                "dataType": "DATE",
                                "sensitive": false
                            }
                    ]
                },
                {
                    "name": "EDAD",
                    "description": "Education Daily Activity Dataset table",
                    "elements": [
                            {
                                "name": "ESTAB_E",
                                "description": "Establishment Code - Encrypted",
                                "dataType": "BIGINT",
                                "sensitive": false
                            }
                    ]
                },
                {
                    "name": "EDAD",
                    "description": "Education Daily Activity Dataset table",
                    "elements": [
                            {
                                "name": "LEA",
                                "description": "Local Education Area",
                                "dataType": "INTEGER",
                                "sensitive": false
                            }
                    ]
                },
                {
                    "name": "EDAD",
                    "description": "Education Daily Activity Dataset table",
                    "elements": [
                            {
                                "name": "SCHOOLREF_E",
                                "description": "School Reference ID",
                                "dataType": "BIGINT",
                                "sensitive": false
                            }
                    ]
                },
                {
                    "name": "EDAD",
                    "description": "Education Daily Activity Dataset table",
                    "elements": [
                            {
                                "name": "SESSION",
                                "description": "-",
                                "dataType": "VARCHAR",
                                "sensitive": false
                            }
                    ]
                },
                {
                    "name": "EDAD",
                    "description": "Education Daily Activity Dataset table",
                    "elements": [
                            {
                                "name": "SESSIONTYPE",
                                "description": "To idenitify whether the session was in the morning or afternoon e.g. AM",
                                "dataType": "VARCHAR",
                                "sensitive": false
                            }
                    ]
                },
                {
                    "name": "EDAD",
                    "description": "Education Daily Activity Dataset table",
                    "elements": [
                            {
                                "name": "SYSTEM_ID_E",
                                "description": "Local pupil identifier. This is specific to the school and one ALF may have mulitple SYSTEM_ID",
                                "dataType": "BIGINT",
                                "sensitive": false
                            }
                    ]
                }
        ]
    }


    ```
