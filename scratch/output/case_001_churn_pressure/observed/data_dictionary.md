# Data Dictionary

Ontology: churn_pressure_world_observed

## Entities

### Customer

A customer using the product.

| Field | Description |
|---|---|
| id | Unique customer identifier. |
| usage_score | Observed customer product usage score. |
| churned | Whether the customer has churned. |

### SupportTicket

An observable support ticket created by a customer.

| Field | Description |
|---|---|
| id | Unique support ticket identifier. |
| customer_id | Customer this ticket belongs to. |
| created_tick | Simulation tick when the ticket was created. |
| severity | Ticket severity. |
| category | Ticket category. |

## Relationships

| Relationship | From | To | Description |
|---|---|---|---|
| support_ticket_belongs_to_customer | SupportTicket.customer_id | Customer.id | Each support ticket belongs to one customer. |
