# Cost Optimization for Azure Serverless Architecture

## Problem Statement

The goal of this project is to optimize the costs associated with storing billing records in **Azure Cosmos DB** within a serverless architecture. The system is **read-heavy**, but records older than **3 months** are rarely accessed, leading to increasing costs as the database grows. The challenge is to move these old records to a more cost-effective storage solution, while ensuring the data is still accessible with minimal latency, without requiring downtime, data loss, or changes to existing API contracts.

### Key Requirements:
- **Reduce storage costs** by offloading older records to a cheaper storage solution.
- Ensure **data accessibility** with response times within seconds for archived records.
- The solution must be **simple**, **scalable**, and **maintainable**.
- **No downtime** or **data loss** during the transition.
- **API contracts** must remain unchanged.

---

## Solution Overview

To solve this challenge, I propose a solution that archives old billing records (older than 3 months) from **Azure Cosmos DB** to **Azure Blob Storage**. By leveraging the **Cool** or **Archive** tiers of Blob Storage, we can significantly reduce storage costs. At the same time, **Azure Functions** will automate the archiving process, and metadata stored in Cosmos DB will allow for seamless access to archived records.

### Solution Approach:
- **Archiving**: Older records are moved from Cosmos DB to Blob Storage automatically.
- **Data Access**: Records are retrieved from Cosmos DB if they are recent; otherwise, they are fetched from Blob Storage using metadata.
- **Cost Optimization**: Cosmos DB operates in **serverless mode** to reduce cost, while Blob Storage uses **Cool** or **Archive** tiers for older records.
- **Automation**: Azure Functions periodically move data older than 3 months to Blob Storage, ensuring no manual intervention.

---

## Pre-requisites

Before deploying this solution, you need access to the following Azure services:

- **Azure Cosmos DB**: Existing Cosmos DB instance with billing records.
- **Azure Blob Storage**: An account to store archived data.
- **Azure Functions**: Used for automating the archiving process.
- **Azure CLI**: For creating and managing resources.

---
## To deploy resources listed above follow the terraform folder/files

# Cost Optimization Breakdown for Azure Cosmos DB and Azure Services

## Azure Cosmos DB

### Serverless Mode
- **Reduce costs** by using **serverless mode**, where you only pay for the requests made, not for the provisioned throughput.

### Lower RU/s
- If you are using **provisioned throughput**, **lower the RU/s** to cut down on the cost for read/write operations.

## Azure Blob Storage

### Store Old Records in Cool or Archive Tiers
- Store old records in the **Cool** or **Archive** tiers, which are much more cost-effective for **infrequently accessed data**.

### Set Up Lifecycle Management Policies
- **Automatically manage record aging and deletion** with Lifecycle Management Policies in Azure Blob Storage.

## Azure Functions

### Automate Record Archiving
- **Automate the process** of archiving records older than **3 months**, ensuring the system runs without manual intervention.

## Deployment Instructions

### 1. Create Azure Cosmos DB
- Set up **Cosmos DB** if not already existing.
- Ensure your **database** and **container** are ready for storing billing records.

### 2. Create Azure Blob Storage Account
- Set up an **Azure Blob Storage account**.
- Create a **container** for storing archived records.

### 3. Deploy Azure Functions
- Create a new **Azure Function App**.
- Deploy the provided **Python code** for archiving and data retrieval.
- Set the function to trigger periodically (e.g., every night) to move old records to Blob Storage.

### 4. Set Up Lifecycle Management in Blob Storage
- Define a **Lifecycle Management policy** to:
  - Move records to the **Cool** or **Archive tier** after **90 days**.
  - Delete records after a further specified period, if necessary.

## Results and Benefits

### Cost Reduction
- The solution drastically **reduces Cosmos DB storage costs** by offloading old records to the **Cool** or **Archive tiers** of Blob Storage, which is significantly cheaper.

### Performance
- Archived records are still **accessible within seconds**, ensuring that users can access older records without significant delays.

### Simplicity
- The solution is easy to implement with **minimal configuration** required in Azure services. It is also **scalable**, handling large amounts of data over time.

### No Downtime
- The transition to Blob Storage happens **automatically**, ensuring no downtime or service interruption.

## Conclusion
By offloading older billing records to **Blob Storage**, this solution optimizes costs while maintaining **quick access** to archived data. The use of **serverless Cosmos DB** and **automated archiving** via Azure Functions ensures that the system is both **efficient** and **cost-effective**, while also being easy to maintain and scale.


## Architecture Diagram

```plaintext
+-------------------------------+                  +----------------------------+
|       Client Application       |  <----------->  |    Azure Blob Storage      |
|   (Read/Write API Contracts)   |                 |  (Archiving and Cool Tier) |
+-------------------------------+                  +----------------------------+
                 |                                             |
                 v                                             v
+-------------------------------+                    +--------------------------+
|       Azure Cosmos DB         |                    |  Azure Blob Lifecycle    |
|    (Stores Active Records)    |                    |  Management Policies     |
|                               |                    +--------------------------+
|    +----------------------+   |                                |
|    |  Azure Functions     |----->                              |
|    | (Archiving Logic)    |                                    |
|    +----------------------+                                    |
+-------------------------------+                                |
                                                                 |
                                             +-----------------------+
                                             | Blob Metadata Storage |
                                             +-----------------------+


