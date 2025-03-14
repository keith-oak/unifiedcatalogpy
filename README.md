# Introducing: UnifiedCatalogPy

A Python wrapper for Microsoft Purview Data Governance's Unified Catalog API.

## Overview 🔥

UnifiedCatalogPy simplifies the interaction with Microsoft Purview's Unified Catalog API. It provides a set of features that allow you to manage and interact with various data governance elements, including:

- Governance Domains (Discovery and Management)
  - Glossary Terms
  - Data Products
  - OKRs (Objectives and Key Results)
  - Critical Data Elements
- Health Management
  - Health Controls
  - Health Actions
  - ~~Data Quality~~ (no API support yet!)

> [!WARNING]
> This library is currently in development and the features listed above are yet to be implemented.

## Quick Start 🚀

Start by installing the library. You will also need to install the `azure-identity` library to authenticate with Microsoft Purview.

```bash
# Installation
pip install unifiedcatalogpy azure-identity
```

In your Python code, you can use the library as follows:

```python
# Import the dependencies
from unifiedcatalogpy import UnifiedCatalogClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

# ...Coming soon...
```

## Documentation 📖

These features are yet to be developed, but the following are planned:

#### Governance Domain

An organizational object that provides context for your data assets and make it easier scale data governance practices. [Learn more](https://learn.microsoft.com/en-us/purview/concept-governance-domain)

##### Create a Governance Domain

##### Retrieve Governance Domains

##### Update a Governance Domain

##### Delete a Governance Domain

#### Glossary Term

Active values that provide context but also apply policies that determine how your data should be managed, governed, and made discoverable for use. [Learn more](https://learn.microsoft.com/en-us/purview/concept-glossary-terms)

##### Create a Glossary Term

##### Retrieve a Glossary Term

##### Update a Glossary Term

##### Delete a Glossary Term

#### Data Product

A kit of data assets (tables, files, Power BI reports, etc.) that provides assets with a use case for ease of discovery and understanding. [Learn more](https://learn.microsoft.com/en-us/purview/concept-data-products)

##### Create a Data Product

##### Retrieve a Data Product

##### Update a Data Product

##### Delete a Data Product

##### Search Data Products

##### Search Data Product by ID

##### Search Data Product by Name

##### Search Data Product by Type

##### Search Data Product by Owner

##### Search Data Product by Term

#### OKRs

Objectives and key results link data products directly to your objectives to bridge the gap between your business and Unified Catalog. You use data to discover and track objectives in your business, and Unified Catalog should make it easy to see those connections and track your goals. [Learn more](https://learn.microsoft.com/en-us/purview/concept-okr)

##### Create an OKR

##### Retrieve an OKR

##### Update an OKR

##### Delete an OKR

##### Search OKRs

##### Search OKR by ID

##### Search OKR by Name

##### Search OKR by Owner

##### Search OKR by Term

##### Search OKR by Data Product

##### Search OKR by Governance Domain

#### Critical Data Element

Critical data elements are a logical grouping of important pieces of information across your data estate. [Learn more](https://learn.microsoft.com/en-us/purview/how-to-create-manage-critical-data)

##### Create a Critical Data Element

##### Retrieve a Critical Data Element

##### Update a Critical Data Element

##### Delete a Critical Data Element

##### Search Critical Data Elements

##### Search Critical Data Element by ID

##### Search Critical Data Element by Name

##### Search Critical Data Element by Owner

##### Search Critical Data Element by Term

##### Search Critical Data Element by Data Product

##### Search Critical Data Element by Governance Domain

##### Search Critical Data Element by OKR

### Health Management

Health management refers to the ongoing processes and practices involved in ensuring that an organization's data remains accurate, complete, consistent, secure, and accessible throughout its lifecycle.

#### Health Controls

Track your journey to complete data governance by monitoring health controls to track your progress. Health controls measure your current governance practices against standards that give your data estate a score. [Learn more](https://learn.microsoft.com/en-us/purview/how-to-health-controls)

##### Create a Health Control

##### Retrieve a Health Control

##### Update a Health Control

##### Delete a Health Control

#### Health Actions

Health actions are concrete steps you can take to improve data governance across your data estate. The actions are provided in a single list that can focus your data governance journey, and democratize ownership. Completing these actions will improve data quality and discoverability across your data estate. [Learn more](https://learn.microsoft.com/en-us/purview/data-estate-health-actions)

##### Create a Health Action

##### Retrieve a Health Action

##### Update a Health Action

##### Delete a Health Action

##### Search Health Actions

##### Search Health Action by ID

##### Search Health Action by Type

##### Search Health Action by Owner

##### Search Health Action by Date

## Additional Resources 🎉

- [Coming Soon: Microsoft Purview Unified Catalog API Documentation]()
