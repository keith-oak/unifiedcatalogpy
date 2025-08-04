![Banner](https://raw.githubusercontent.com/olafwrieden/unifiedcatalogpy/main/assets/media/banner.png)

# Introducing: UnifiedCatalogPy

An unofficial Python wrapper for Microsoft Purview Data Governance's Unified Catalog API. Not affiliated or officially supported by Microsoft. Built as a personal project by tediously observing the internet browser's XHR network traffic and reverse engineering the API - ☕️ [buy me a coffee](https://buymeacoffee.com/olafwrieden).

## Overview 🔥

UnifiedCatalogPy simplifies the interaction with Microsoft Purview's Unified Catalog API. It provides a set of features that allow you to manage and interact with various data governance elements, including operations for creating, retrieving, updating, and deleting business concepts.

**Interact with:**

- Governance Domains
- Glossary Terms
- Data Products
- Objectives and Key Results (OKRs)
- Critical Data Elements (CDEs)
- Custom Attributes (🚧 coming soon)
- Requests (🚧 coming soon)
- Health Management (🚧 coming soon)
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

#### Using Azure CLI

If you are using the Azure CLI, be sure to log in using `az login` before running your Python notebook. Your credentials will be automatically picked up by the `DefaultAzureCredential` class. Your user must have the **Data Governance Administrator** role in Microsoft Purview to perform operations.

#### Using a Service Principal

1. ️Navigate to the Azure portal to [create a new Service Principal](https://learn.microsoft.com/en-us/purview/tutorial-using-rest-apis) for your application and generate a client secret.
2. Copy the Application (client) ID, Directory (tenant) ID, and Client Secret (value) into your Python environment variables.

   ```
   AZURE_CLIENT_ID=
   AZURE_TENANT_ID=
   AZURE_CLIENT_SECRET=
   ```

3. Navigate to the _Properties_ tab of your Microsoft Purview Azure resource to locate your Purview account ID. It can be found in the _Atlas endpoint URL_.

   **Example:** `https://<your-purview-account-id>-api.purview-service.microsoft.com/catalog`

   Copy the `<your-purview-account-id>` - you will need it in a moment to create the client.

4. Navigate to the Microsoft Purview portal _> Settings > Solution Settings > Unified Catalog > Roles and Permissions > Data Governance Administrators_ and add the Service Principal as a **Data Governance Administrator**.

5. Your Service Principal is now authorized to interact with Microsoft Purview Data Governance Unified Catalog API. Let's test it out! 🚀

### 3. Using the Client

In your Python notebook, you can use the library as follows:

```python
# Import the library
from unifiedcatalogpy.client import UnifiedCatalogClient
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

**💡 Good to know:** Detailed usage examples for supported functionality is provided in the documentation section below. _Let's automate!_

## Documentation 📖

Here is what's possible with the `UnifiedCatalogPy` client.

> [!NOTE]
> This library is not locked to a specific version of the Microsoft Purview API as an official API for the Unified Catalog is not yet available. This means functionality may change unexpectedly. [See limitations](#limitations-)

### Governance Domain

An organizational object that provides context for your data assets and make it easier scale data governance practices. [Learn more](https://learn.microsoft.com/en-us/purview/concept-governance-domain)

#### Create a Governance Domain

```python
# Create a new governance domain
new_domain = client.create_governance_domain(
    name="My First Domain",
    description="<div>This is an example of a <b>rich text</b> description.</div>",
    type="FunctionalUnit",
    owners=[{ "id": "<entra-object-id>" }],
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

_Note: Pagination over governance domains is not yet supported._

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
    owners=[{ "id": "<entra-object-id>" }],
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
    owners=[{"id": "<entra-object-id>"}],
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

_Note: Pagination over glossary terms is not yet supported._

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
    owners=[{"id": "<entra-object-id>"}],
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
    owners=[{"id": "<entra-object-id>"}],
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

_Note: Pagination over data products is not yet supported._

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
            "id": "<entra-object-id>",
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

#### Link a Glossary Term to a Data Product

```python
# Link a term to a data product
relationship = client.link_term_to_data_product(
    data_product_id="<your-data-product-id>",
    term_id="<your-term-id>",
    description="This term defines key concepts used in this data product",
    relationship_type="Related"  # or "Synonym"
)

# Show the created relationship
print(relationship)
```

#### Unlink a Glossary Term from a Data Product

```python
# Unlink a term from a data product
success = client.unlink_term_from_data_product(
    data_product_id="<your-data-product-id>",
    term_id="<your-term-id>",
    relationship_type="Related"  # Must match the relationship type used when linking
)

if success:
    print("Term unlinked successfully.")
else:
    print("Failed to unlink term.")
```

#### Link an Asset to a Data Product

_Note: Asset linking requires the asset management API which is not yet implemented in this library._

#### Unlink an Asset from a Data Product

_Note: Asset unlinking requires the asset management API which is not yet implemented in this library._

#### Link an Objective to a Data Product

```python
# Link an objective to a data product
relationship = client.link_objective_to_data_product(
    data_product_id="<your-data-product-id>",
    objective_id="<your-objective-id>",
    description="This data product supports achieving this business objective",
    relationship_type="Related"
)

# Show the created relationship
print(relationship)
```

#### Unlink an Objective from a Data Product

```python
# Unlink an objective from a data product
success = client.unlink_objective_from_data_product(
    data_product_id="<your-data-product-id>",
    objective_id="<your-objective-id>",
    relationship_type="Related"
)

if success:
    print("Objective unlinked successfully.")
else:
    print("Failed to unlink objective.")
```

#### Link a Critical Data Element to a Data Product

```python
# Link a critical data element to a data product
relationship = client.link_critical_data_element_to_data_product(
    data_product_id="<your-data-product-id>",
    cde_id="<your-cde-id>",
    description="This CDE is a key component of this data product",
    relationship_type="Related"
)

# Show the created relationship
print(relationship)
```

#### Unlink a Critical Data Element from a Data Product

```python
# Unlink a critical data element from a data product
success = client.unlink_critical_data_element_from_data_product(
    data_product_id="<your-data-product-id>",
    cde_id="<your-cde-id>",
    relationship_type="Related"
)

if success:
    print("Critical data element unlinked successfully.")
else:
    print("Failed to unlink critical data element.")
```

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
            "id": "<entra-object-id>",
            "description": "Objective Owner",
        }
    ],
    target_date="2025-12-30T14:00:00.000Z",
)

# Show the objective
print(objective)
```

#### Retrieve all Objectives in a Governance Domain

```python
# Get all objectives in the governance domain
objectives = client.get_objectives("<your-governance-domain-id>")

# Show objectives
print(objectives)
```

_Note: Pagination over objectives is not yet supported._

#### Retrieve an Objective by ID

```python
# Get objective by its ID
objective = client.get_objective_by_id("<your-objective-id>")

# Show the objective
print(objective)
```

#### Update an Objective

```python
# Update an objective
updated_objective = client.update_objective(
    objective_id="<your-objective-id>",
    status="Draft",
    governance_domain_id="<your-governance-domain-id>",
    owners=[
        {
            "id": "<entra-object-id>",
            "description": "Objective Owner",
        }
    ],
    definition="Improve customer service to improve satisfaction and retention rates.",
    target_date="2025-06-15T14:00:00.000Z",
)

# Show updated objective
print(updated_objective)
```

#### Delete an Objective

```python
# Delete an objective
deleted = client.delete_objective("<your-objective-id>")

if deleted:
    print("Objective deleted successfully.")
else:
    print("Failed to delete Objective.")
```

#### Create a Key Result for an Objective

```python
# Create a key result
key_result = client.create_key_result(
    progress=60,
    goal=80,
    max=100,
    status="AtRisk",
    definition="Increase customer satisfaction score by 20%.",
    objective_id="<your-objective-id>",
    governance_domain_id="<your-governance-domain-id>",
)

# Show the key result
print(key_result)
```

#### Retrieve all Key Results of an Objective

```python
# Get all key results of an objective
key_results = client.get_key_results("<your-objective-id>")

# Show the key results
print(key_results)
```

#### Retrieve a Key Result by ID

```python
# Get a key result by ID
key_result = client.get_key_result_by_id(
    key_result_id="<your-key-result-id>",
    objective_id="<your-objective-id>",
)

# Show key result
print(key_result)
```

#### Update a Key Result of an Objective

```python
# Update a key result
updated_key_result = client.update_key_result(
    key_result_id="<your-key-result-id>",
    progress=70,
    goal=80,
    max=100,
    status="OnTrack",
    definition="Increase customer satisfaction score by 20%.",
    objective_id="<your-objective-id>",
    governance_domain_id="<your-governance-domain-id>",
)

# Show the updated key result
print(updated_key_result)
```

#### Delete a Key Result of an Objective

```python
# Delete a key result
deleted = client.delete_key_result(
    key_result_id="<your-key-result-id>",
    objective_id="<your-objective-id>",
)

if deleted:
    print("Key Result deleted successfully.")
else:
    print("Failed to delete Key Result.")
```

#### Link a Data Product to an Objective

#### Unlink a Data Product from an Objective

---

### Critical Data Elements (preview)

Critical data elements are a logical grouping of important pieces of information across your data estate. [Learn more](https://learn.microsoft.com/en-us/purview/how-to-create-manage-critical-data)

#### Create a Critical Data Element

```python
# Create a critical data element
cde = client.create_critical_data_element(
    name="Customer Identifier (CID)",
    status="Draft",
    governance_domain_id="<your-governance-domain-id>",
    description="<div>Describes a numeric <b>customer identifier</b> throughout the data estate.</div>",
    data_type="Number",
    owners=[{ "id": "<entra-object-id>" }],
)

# Show critical data element
print(cde)
```

#### Retrieve all Critical Data Elements in a Governance Domain

```python
# Get all critical data elements in the governance domain
cdes = client.get_critical_data_elements("<your-governance-domain-id>")

# Enumerate the critical data elements
for cde in cdes:
    print(cde)
```

_Note: Pagination over critical data elements is not yet supported._

#### Retrieve a Critical Data Element by ID

```python
# Get critical data element by its ID
cde = client.get_critical_data_element_by_id("<your-critical-data-element-id>")

# Show critical data element
print(cde)
```

#### Update a Critical Data Element

```python
# Update a critical data element
updated_cde = client.update_critical_data_element(
    cde_id="<your-critical-data-element-id>",
    name="Customer Identifier (CID)",
    description="<div>An <b>updated description</b> of a customer identifier.</div>",
    status="Draft",
    governance_domain_id="<your-governance-domain-id>",
    data_type="String",
    owners=[{ "id": "<entra-object-id>" }],
)

# Show updated critical data element
print(updated_cde)
```

#### Delete a Critical Data Element

```python
# Delete a critical data element
deleted = client.delete_critical_data_element("<your-critical-data-element-id>")

if deleted:
    print("Critical Data Element deleted successfully.")
else:
    print("Failed to delete Critical Data Element.")
```

#### Add a Column to a Critical Data Element

```python
# Add a column to a critical data element
result = client.add_column_to_critical_data_element(
    cde_id="<your-critical-data-element-id>",
    column_qualified_name="mssql://server.database.com/db/schema/table#column",
    column_display_name="Customer ID Column"
)

# Show the result
print(result)
```

#### Remove a Column from a Critical Data Element

```python
# Remove a column from a critical data element
success = client.remove_column_from_critical_data_element(
    cde_id="<your-critical-data-element-id>",
    column_qualified_name="mssql://server.database.com/db/schema/table#column"
)

if success:
    print("Column removed successfully.")
else:
    print("Failed to remove column.")
```

#### Link a Glossary Term to a Critical Data Element

```python
# Link a term to a critical data element
relationship = client.link_term_to_critical_data_element(
    cde_id="<your-critical-data-element-id>",
    term_id="<your-term-id>",
    description="This term provides business context for this CDE",
    relationship_type="Related"
)

# Show the created relationship
print(relationship)
```

#### Unlink a Glossary Term from a Critical Data Element

```python
# Unlink a term from a critical data element
success = client.unlink_term_from_critical_data_element(
    cde_id="<your-critical-data-element-id>",
    term_id="<your-term-id>",
    relationship_type="Related"
)

if success:
    print("Term unlinked successfully.")
else:
    print("Failed to unlink term.")
```

---

### Custom Attributes (preview)

Custom attributes are admin-defined, attributes that can be applied to add additional metadata to business concepts in the Unified Catalog.

> [!WARNING]
> You cannot interact with Custom Attributes through this library yet.

---

### Requests

If you discover a data product in the catalog that you would like to access, you can request access directly through Microsoft Purview. The request triggers a workflow requesting that the owners of the data resource grant you access to the data product. [Learn more](https://learn.microsoft.com/en-us/purview/unified-catalog-access-policies)

> [!WARNING]
> You cannot interact with Requests through this library yet. This is work in progress. A pull request to add this functionality is welcome.

#### Create a Request

#### Retrieve all Requests in a Governance Domain

#### Retrieve a Request by ID

#### Update a Request

#### Delete a Request

---

### Health Management

Health management refers to the ongoing processes and practices involved in ensuring that an organization's data remains accurate, complete, consistent, secure, and accessible throughout its lifecycle.

#### Health Controls (preview)

Track your journey to complete data governance by monitoring health controls to track your progress. Health controls measure your current governance practices against standards that give your data estate a score. [Learn more](https://learn.microsoft.com/en-us/purview/how-to-health-controls)

> [!WARNING]
> You cannot interact with Health Controls through this library yet. This is work in progress. A pull request to add this functionality is welcome.

##### Create a Health Control

##### Retrieve a Health Control

##### Update a Health Control

##### Delete a Health Control

#### Health Actions (preview)

Health actions are concrete steps you can take to improve data governance across your data estate. The actions are provided in a single list that can focus your data governance journey, and democratize ownership. Completing these actions will improve data quality and discoverability across your data estate. [Learn more](https://learn.microsoft.com/en-us/purview/data-estate-health-actions)

> [!WARNING]
> You cannot interact with Health Actions through this library yet. This is work in progress. A pull request to add this functionality is welcome.

##### Create a Health Action

##### Retrieve a Health Action

##### Update a Health Action

##### Delete a Health Action

#### Data Quality

Data quality is the measurement of the quality of data in an organization, based on data quality rules that are configured and defined in Unified Catalog. [Learn more](https://learn.microsoft.com/en-us/purview/data-quality-overview)

> [!WARNING]
> You cannot interact with Data Quality through this library yet. There is a lot of complexity in the API, data quality sub-features, and interpretation of the results. A pull request to add this functionality is welcome.

## Advanced Features 🚀

### Pagination Support

All list operations support pagination for handling large datasets efficiently:

```python
from unifiedcatalogpy.models import PaginationOptions

# Get paginated governance domains
pagination = PaginationOptions(page_size=50)
result = client.get_governance_domains_paginated(pagination)

print(f"Retrieved {result.count} domains out of {result.total_count}")
print(f"Has more pages: {result.has_more}")

# Get next page
if result.has_more:
    next_pagination = PaginationOptions(
        page_size=50, 
        continuation_token=result.continuation_token
    )
    next_result = client.get_governance_domains_paginated(next_pagination)
```

### Automatic Iteration

Use iterator methods to automatically handle pagination:

```python
# Iterate through all terms automatically
for term in client.get_all_terms(governance_domain_id):
    print(f"Processing term: {term['name']}")

# Also available for:
# - get_all_governance_domains()
# - get_all_data_products(governance_domain_id)
# - get_all_objectives(governance_domain_id)
# - get_all_critical_data_elements(governance_domain_id)
# - get_all_key_results(objective_id)
```

### Typed Response Models

Get type-safe response objects with automatic date parsing:

```python
# Get typed governance domain
domain = client.get_governance_domain_by_id_typed(domain_id)
print(f"Domain: {domain.name}")
print(f"Status: {domain.status}")  # EntityStatus enum
print(f"Created: {domain.created_at}")  # datetime object

# Get typed term
term = client.get_term_by_id_typed(term_id)
print(f"Term: {term.name}")
print(f"Acronyms: {', '.join(term.acronyms)}")

# Get all domains as typed objects
domains = client.get_governance_domains_typed()
for domain in domains:
    print(f"{domain.name} ({domain.type})")
```

### Configuration Management

Multiple ways to configure the client:

```python
# From configuration file (YAML or JSON)
client = UnifiedCatalogClient.from_config_file("config.yaml")

# From environment variables
client = UnifiedCatalogClient.from_env()

# From connection string
client = UnifiedCatalogClient.from_connection_string(
    "AccountId=xxx;TenantId=yyy;ClientId=zzz;ClientSecret=secret"
)

# Auto-discovery (tries file, then env, then defaults)
client = UnifiedCatalogClient.from_default_config()
```

### Retry Logic and Circuit Breaker

Built-in reliability features with configurable retry logic:

```python
from unifiedcatalogpy.config import UnifiedCatalogConfig

config = UnifiedCatalogConfig(
    account_id="your-account-id",
    enable_retry=True,
    max_retry_attempts=5,
    retry_base_delay=2.0,
    retry_max_delay=120.0,
    enable_circuit_breaker=True,
    request_timeout=60  # seconds
)

client = UnifiedCatalogClient.from_config(config)
```

### Generic Relationship Management

Create relationships between any supported entity types:

```python
# Create relationship between any entities
relationship = client.create_relationship(
    entity_type="Term",  # or "DataProduct", "CriticalDataElement"
    entity_id="<source-entity-id>",
    relationship_type="Related",  # or "Synonym"
    target_entity_id="<target-entity-id>",
    description="Relationship description"
)

# Delete relationship
success = client.delete_relationship(
    entity_type="Term",
    entity_id="<source-entity-id>",
    target_entity_id="<target-entity-id>",
    relationship_type="Related"
)
```

### Context Manager Support

Properly manage resources with context manager:

```python
with UnifiedCatalogClient.from_env() as client:
    # Client session is automatically cleaned up
    domains = client.get_governance_domains()
    # ... do work ...
# Session closed automatically
```

## Limitations 🚧

- This library is not affiliated with Microsoft.
- The library is not locked to a specific version of the Microsoft Purview API as an official Microsoft Purview Data Governance API for the Unified Catalog is not yet available. This means functionality may change unexpectedly. Do not rely on this library in production for this reason.
- The library is maintained on a best-effort basis. It is not a full-time project and PRs are welcome.
- Managing business concept policies and data quality is not yet supported.
- The library includes a comprehensive test suite in the `tests/` directory covering configuration, models, and retry logic.
- Typed return schemas are available through the response models module for type-safe development.
