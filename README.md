![Banner](/assets/media/banner.png)

# Introducing: UnifiedCatalogPy

An unofficial Python wrapper for Microsoft Purview Data Governance's Unified Catalog API. Not affiliated or officially supported by Microsoft. Built as a personal project by observing Microsoft Purview browser network calls and reverse engineering the API.

## Overview 🔥

UnifiedCatalogPy simplifies the interaction with Microsoft Purview's Unified Catalog API. It provides a set of features that allow you to manage and interact with various data governance elements, including operations for creating, retrieving, updating, and deleting business concepts.

**Interact with:**

- Governance Domains
- Glossary Terms
- Data Products
- OKRs (Objectives and Key Results)
- Critical Data Elements
- Requests
- Health Management
  - Health Controls
  - Health Actions
  - ~~Data Quality~~ (no API support yet!)

> [!WARNING]
> This library is currently in development and the features listed above are yet to be implemented. It is not affiliated with Microsoft.

## Quick Start 🚀

### 1. Installation

Start by installing the library. You will also need to install the `azure-identity` library to authenticate with Microsoft Purview.

```bash
# Install the library
pip install unifiedcatalogpy azure-identity
```

### 2. Authentication

Microsoft Purview requires an authorized identity to perform tasks. You can choose between authenticating as a user (via [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli)) or using a Service Principal.

> [!NOTE]
> In most cases you should be using a Service Principal to query Microsoft Purview (RBAC permissions can be scoped independently of a user). Remember that ownership of an artifact defaults to its creator unless you specify a user/group at creation.

If you are using the Azure CLI, be sure to log in using `az login` before running your Python notebook. Alternatively, follow the instructions to set up a Service Principal in the [Setup Instructions](#setup-instructions).

Configure your environment variables (per [Setup Instructions](#setup-instructions)):

```
AZURE_CLIENT_ID=
AZURE_TENANT_ID=
AZURE_CLIENT_SECRET=
```

### 3. Using the Client

In your Python notebook, you can use the library as follows:

```python
# Import the library
from unifiedcatalogpy import UnifiedCatalogClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

# Create the Unified Catalog Client
client = UnifiedCatalogClient(
    account_id="<your-purview-account-id>",
    credential=credential
)

# Interact with the client
domains = client.get_governance_domains()
```

Detailed usage examples for each feature are provided in the sections below.

## Documentation 📖

These features are yet to be developed, but the following are planned:

### Governance Domain

An organizational object that provides context for your data assets and make it easier scale data governance practices. [Learn more](https://learn.microsoft.com/en-us/purview/concept-governance-domain)

#### Create a Governance Domain

```python
# Create a new governance domain
new_domain = client.create_governance_domain(
    name="My First Domain",
    description="<div>This is an example of a <b>rich text</b> description.</div>",
    type="FunctionalUnit",
    owners=[{ "id": "<owner-principal-id>" }],
    status="Draft",
)

# Show the new governance domain
print(new_domain)
```

#### Retrieve all Governance Domains

```python
# Get all governance domains
domains = client.get_governance_domains()
```

#### Retrieve a Governance Domain by ID

```python
# Get a governance domain by ID
domain = client.get_governance_domain_by_id("<your-governance-domain-id>")

# Show the governance domain
print(domain)
```

#### Update a Governance Domain

```python
# Update a governance domain by ID
updated_domain = client.update_governance_domain(
    governance_domain_id="<your-governance-domain-id>",
    name="Updated Domain Name",
    description="<div>This is an updated domain description.</div>",
    type="FunctionalUnit",
    owners=[{ "id": "<owner-principal-id>" }],
    status="Draft",
)

# Show the updated governance domain
print(updated_domain)
```

#### Delete a Governance Domain

```python
# Delete a governance domain by ID
deleted = client.delete_governance_domain("<your-governance-domain-id>")

if deleted:
    print("Governance domain deleted successfully.")
else:
    print("Failed to delete governance domain.")
```

---

### Glossary Terms

Active values that provide context but also apply policies that determine how your data should be managed, governed, and made discoverable for use. [Learn more](https://learn.microsoft.com/en-us/purview/concept-glossary-terms)

#### Create a Glossary Term

```python
# Create new glossary term
term = client.create_term(
    name="My First Term",
    description="<div>This is a <b>rich description</b> of my first term.</div>",
    status="Draft",
    governance_domain_id="<your-governance-domain-id>",
    acronyms=["ACRONYM_1", "ACRONYM_2"],
    resources=[
        {
            "name": "Read more details",
            "url": "https://example.com",
        }
    ],
    owners=[{"id": "<owner-principal-id>"}],
)

# Show the new glossary term
print(term)
```

#### Retrieve all Glossary Terms in a Governance Domain

```python
# Get all terms in the governance domain
terms = client.get_terms("<your-governance-domain-id>")

# Enumerate the terms
for term in terms:
    print(term)
```

#### Retrieve a Glossary Term by ID

```python
# Get a specific term by ID
term = client.get_term_by_id("<your-term-id>")

# Show the term
print(term)
```

#### Update a Glossary Term

```python
# Update a term
updated_term = client.update_term(
    term_id="<your-term-id>",
    name="Updated Term Name",
    description="<div>This is an updated term description.</div>",
    governance_domain_id="<your-governance-domain-id>",
    owners=[{"id": "<owner-principal-id>"}],
    acronyms=["ACRONYM_1_UPDATED", "ACRONYM_2_UPDATED"],
    resources=[
        {
            "name": "Read more about this term",
            "url": "https://example.com/more",
        }
    ],
    status="Draft",
)

# Show the updated term
print(updated_term)
```

#### Delete a Glossary Term

```python
# Delete a term
deleted = client.delete_term("<your-term-id>")

if deleted:
    print("Governance domain deleted successfully.")
else:
    print("Failed to delete governance domain.")
```

#### Create a Term Relationship (Synonyms / Related Terms)

##### Link Term to a Synonym

```python
# Link a synonym to a term
relationship = client.create_term_relationship(
    term_id="<your-term-id>",
    relationship_type="Synonym",
    entity_id="<your-target-term-id>",
    description="This is a synonym relationship.",
)

# Show the relationship
print(relationship)
```

##### Link Term to a Related Term

```python
# Link a related term to a term
relationship = client.create_term_relationship(
    term_id="<your-term-id>",
    relationship_type="Related",
    entity_id="<your-related-term-id>",
    description="This is a related term relationship.",
)

# Show the relationship
print(relationship)
```

#### Delete a Term Relationship (Synonyms / Related Terms)

##### Delete a Synonym relationship

```python
# Delete a term relationship
deleted = client.delete_term_relationship(
    term_id="<your-term-id>",
    entity_id="<your-target-term-id>",
    relationship_type="Synonym",
    entity_type="Term",
)

if deleted:
    print("Synonym relationship deleted successfully.")
else:
    print("Failed to delete the synonym relationship.")
```

##### Delete a Related Term relationship

```python
# Delete a term relationship
deleted = client.delete_term_relationship(
    term_id="<your-term-id>",
    entity_id="<your-target-term-id>",
    relationship_type="Related",
    entity_type="Term",
)

if deleted:
    print("Related relationship deleted successfully.")
else:
    print("Failed to delete the related relationship.")
```

---

### Data Products

A kit of data assets (tables, files, Power BI reports, etc.) that provides assets with a use case for ease of discovery and understanding. [Learn more](https://learn.microsoft.com/en-us/purview/concept-data-products)

#### Create a Data Product

```python
# Create a new Data Product
data_product = client.create_data_product(
    governance_domain_id=governance_domain,
    name="My First Data Product",
    description="<div>This is a <b>new</b> data product created for demonstration purposes.</div>",
    type="Operational",
    owners=[{"id": "<owner-principal-id>"}],
    status="Draft",
    audience=[],
    business_use="<div>Use Case 1, 2, 3</div>",
    documentation=[],
    updateFrequency="Weekly",
    endorsed=False,
    terms_of_use=[],
)

# Show Data Product
print(data_product)
```

#### Retrieve all Data Products in a Governance Domain

```python
# Get all data products in the governance domain
data_products = client.get_data_products("<your-governance-domain-id>")

# Enumerate the data products
for data_product in data_products:
    print(data_product)
```

#### Retrieve a Data Product by ID

```python
# Get data product by ID
data_product = client.get_data_product_by_id("<your-data-product-id>")

# Show data product
print(data_product)
```

#### Update a Data Product

```python
# Update a data product
updated_data_product = client.update_data_product(
    data_product_id="<your-data-product-id>",
    governance_domain_id="<your-governance-domain-id>",
    name="My Updated Data Product",
    description="<div>This is an <b>updated</b> data product description.</div>",
    owners=[
        {
            "id": "<owner-principal-id>",
            "description": "Data Product Owner",
        }
    ],
    status="Draft",
    audience=[],
    business_use="<div>Use Case 1, 2, 3</div>",
    documentation=[],
    endorsed=False,
    terms_of_use=[],
    type="Operational",
    updateFrequency="Monthly",
)

# Show the updated data product
print(updated_data_product)
```

#### Delete a Data Product

```python
# Delete data product
deleted = client.delete_data_product("<your-data-product-id>")

if deleted:
    print("Data Product deleted successfully.")
else:
    print("Failed to delete Data Product.")
```

#### Link Glossary Term to a Data Product

#### Link Asset to a Data Product

#### Link OKR to a Data Product

#### Link Critical Data Element to a Data Product

---

### Objectives and Key Results (OKRs)

Objectives and key results link data products directly to your objectives to bridge the gap between your business and Unified Catalog. You use data to discover and track objectives in your business, and Unified Catalog should make it easy to see those connections and track your goals. [Learn more](https://learn.microsoft.com/en-us/purview/concept-okr)

#### Create an Objective

```python
# Create an objective
objective = client.create_objective(
    definition="Revamp customer service to improve satisfaction and retention rates.",
    governance_domain_id="<your-governance-domain-id>",
    status="Draft",
    owners=[
        {
            "id": "<owner-principal-id>",
            "description": "Objective Owner",
        }
    ],
    target_date="2025-12-30T14:00:00.000Z",
)

# Show objective
print(objective)
```

#### Retrieve all Objectives in a Governance Domain

#### Retrieve an OKR by ID

#### Update an OKR

#### Delete an OKR

---

### Critical Data Elements

Critical data elements are a logical grouping of important pieces of information across your data estate. [Learn more](https://learn.microsoft.com/en-us/purview/how-to-create-manage-critical-data)

#### Create a Critical Data Element

#### Retrieve all Critical Data Element in a Governance Domain

#### Retrieve a Critical Data Element by ID

#### Update a Critical Data Element

#### Delete a Critical Data Element

---

### Requests

If you discover a data product in the catalog that you would like to access, you can request access directly through Microsoft Purview. The request triggers a workflow requesting that the owners of the data resource grant you access to the data product. [Learn more](https://learn.microsoft.com/en-us/purview/unified-catalog-access-policies)

#### Create a Request

#### Retrieve all Requests in a Governance Domain

#### Retrieve a Request by ID

#### Update a Request

#### Delete a Request

---

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

## Setup Instructions 🛠

1. ️Navigate to the Azure portal to [create a new Service Principal](https://learn.microsoft.com/en-us/purview/tutorial-using-rest-apis) for your application.
2. Copy the Application (client) ID, Directory (tenant) ID, and Client Secret (value) into your Python environment variables.

````

AZURE_CLIENT_ID=
AZURE_TENANT_ID=
AZURE_CLIENT_SECRET=

```

3. Navigate to Properties tab of your Microsoft Purview Azure resource to locate your Purview account ID. It can be found in the Atlas endpoint URL.
   `https://<your-purview-account-id>-api.purview-service.microsoft.com/catalog`

Copy the `<your-purview-account-id>` value into your Python environment variables.

```

PURVIEW_ACCOUNT_ID=

```

4. Navigate to the Microsoft Purview portal _> Settings > Solution Settings > Unified Catalog > Roles and Permissions > Data Governance Administrators_ to add the Service Principal as a Data Governance Administrator.

## Additional Resources 🎉

- [Coming Soon: Microsoft Purview Unified Catalog API Documentation]()
```
````
