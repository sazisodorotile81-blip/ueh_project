# API Documentation
Interactive documentation is served at `/api/docs/`.

## Authentication
- `POST /api/auth/register/`: public MSME registration.
- `POST /api/auth/token/`: username/password -> access and refresh JWT.
- `POST /api/auth/token/refresh/`: refresh token -> access token.
- `GET /api/auth/me/`: current user profile.

Send authenticated requests with `Authorization: Bearer <access-token>`.

## Service requests
- `GET /api/requests/`
- `POST /api/requests/` with `{ "category":"FUNDING", "description":"...", "urgency":"HIGH" }`
- `GET /api/requests/{id}/`
- `PATCH /api/requests/{id}/` (agents/admins can update status; admins can assign agent)

## Opportunities and applications
- `GET /api/opportunities/` (optional filters: `?type=FUNDING` and/or `?search=title`)
- `POST /api/opportunities/` (admin only)
- `POST /api/opportunities/{id}/apply/` with `{ "motivation":"..." }` (client only)
- `GET /api/applications/`
- `PATCH /api/applications/{id}/` (admin review)

## Dashboard
- `GET /api/dashboard/`
