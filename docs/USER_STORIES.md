# User stories and acceptance criteria

1. As an MSME client, I can register and log in so that I can access my business workspace.
   - Registration validates required fields and creates a CLIENT role.
   - Passwords are hashed; invalid credentials are rejected.
2. As a client, I can create a support request with category, description and urgency.
   - Description must contain at least 10 characters.
   - New requests start as OPEN and belong to the logged-in client.
3. As a client, I can track my requests.
   - I can only see my own requests.
   - I cannot assign agents or change status.
4. As an agent, I can view requests assigned to me and update progress.
   - Agents see only their assigned requests.
5. As an admin, I can assign agents and manage request statuses.
6. As an admin, I can create funding, tender and training opportunities.
7. As a client, I can browse opportunities and submit one application per opportunity.
8. As an admin, I can review applications and set a decision.
9. As an admin, I can see open, in-progress, resolved and application totals.
