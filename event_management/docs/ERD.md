## Database Design

Summary of Relationships
-HostProfile to CustomUser: One-to-One (each profile is linked to one user).
-HostProfile to Event: One-to-Many (each event has one host).
-Event to CustomUser: Many-to-Many (users can attend multiple events, and events can have multiple users)

The following diagram illustrates the relationships between the core models (User, HostProfile, and Event) :


![ERD Diagram](event_management/docs/ERD.png)
