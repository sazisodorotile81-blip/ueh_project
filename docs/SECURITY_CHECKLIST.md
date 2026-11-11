# Security checklist

- [x] Password hashing handled by Django.
- [x] Passwords excluded from API serializers.
- [x] Registration password strength validation.
- [x] JWT authentication on protected endpoints.
- [x] Role and object-level permission checks.
- [x] ORM usage rather than raw SQL string concatenation.
- [x] Serializer validation for user input.
- [x] CSRF middleware enabled in Django.
- [x] Clickjacking and content-type sniffing protections enabled.
- [x] React displays untrusted content as text; no `dangerouslySetInnerHTML`.
- [x] Secrets loaded from environment variables; `.env` excluded from Git.
- [ ] Production HTTPS configured.
- [ ] Production `DEBUG=False` and strong `SECRET_KEY` set.
- [ ] PostgreSQL backups and restricted database credentials configured.
- [ ] Rate limiting, audit logging and email verification added before production.
- [ ] Prefer secure HttpOnly cookie auth for production browser sessions.

Do not claim unchecked production controls are complete. Record evidence/screenshots for each item.
