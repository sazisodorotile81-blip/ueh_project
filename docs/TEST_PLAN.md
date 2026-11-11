# Test plan

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Register with valid details | Account created with CLIENT role |
| T02 | Register with weak password | Validation error |
| T03 | Login with incorrect password | 401 response |
| T04 | Client submits valid support request | 201; status OPEN |
| T05 | Client submits short description | 400 validation error |
| T06 | Client requests another client's request | 404 / inaccessible |
| T07 | Client attempts to change status | 400 validation error |
| T08 | Agent views own assigned requests | Only assigned requests returned |
| T09 | Client creates opportunity | 403 forbidden |
| T10 | Admin posts opportunity | 201 created |
| T11 | Client applies twice to same opportunity | Duplicate rejected |
| T12 | Admin reviews application | Status updated and review timestamp set |
| T13 | Unauthenticated request to protected endpoint | 401 unauthorized |
| T14 | Dashboard statistics | Counts match database records |

Run automated backend tests:
`python manage.py test`
