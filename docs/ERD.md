# Entity Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ SERVICE_REQUEST : submits
    USER ||--o{ SERVICE_REQUEST : assigned_to
    USER ||--o{ OPPORTUNITY : posts
    USER ||--o{ APPLICATION : submits
    USER ||--o{ REQUEST_STATUS_HISTORY : changes
    SERVICE_REQUEST ||--o{ REQUEST_STATUS_HISTORY : records
    OPPORTUNITY ||--o{ APPLICATION : receives

    USER {
      int id PK
      string username
      string email
      string password_hash
      string role
      string business_name
    }
    SERVICE_REQUEST {
      int id PK
      int client_id FK
      int assigned_agent_id FK
      string category
      text description
      string urgency
      string status
      datetime created_at
    }
    REQUEST_STATUS_HISTORY {
      int id PK
      int service_request_id FK
      int changed_by_id FK
      string old_status
      string new_status
      datetime changed_at
    }
    OPPORTUNITY {
      int id PK
      int created_by_id FK
      string title
      string opportunity_type
      text description
      date closing_date
      boolean is_published
    }
    APPLICATION {
      int id PK
      int opportunity_id FK
      int applicant_id FK
      text motivation
      string status
      datetime submitted_at
    }
```

The business data model has five related tables: User, ServiceRequest, RequestStatusHistory, Opportunity and Application. RequestStatusHistory records who changed a request status and when, providing an audit trail.
