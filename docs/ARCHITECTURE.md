# Architecture
- React + Vite single-page frontend.
- Django REST Framework API.
- Django ORM with SQLite locally and PostgreSQL for shared deployment.
- JWT authentication and role-based API permissions.

```mermaid
flowchart LR
  Browser[React Frontend] -->|HTTPS JSON + JWT| API[Django REST API]
  API --> Auth[Authentication and Permissions]
  API --> ORM[Django ORM]
  ORM --> DB[(PostgreSQL / SQLite)]
  Admin[UEH Admin] --> Browser
  Client[MSME Client] --> Browser
  Agent[Support Agent] --> Browser
```

## Main flows
1. Client registers and signs in; backend stores a salted password hash.
2. Client submits a support request; API validates fields and stores it with status OPEN.
3. Agent views assigned requests and updates status.
4. Admin publishes opportunities and reviews client applications.
5. Dashboard endpoint aggregates request and application counts.
