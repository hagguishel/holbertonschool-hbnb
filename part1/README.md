# HBnB - Technical Architecture & Sequence Diagrams

## Table of Contents
- [Introduction](#introduction)
- [High-Level Architecture](#high-level-architecture)
- [Business Logic Layer](#business-logic-layer)
- [API Interaction Flow](#api-interaction-flow)
  - [User Registration](#sequence-diagram-1-user-registration)
  - [Place Creation](#sequence-diagram-2-place-creation)
  - [Review Submission](#sequence-diagram-3-review-submission)
  - [Fetching Places](#sequence-diagram-4-fetching-places)
- [Conclusion](#conclusion)
- [Authors](#authors)
---

## Introduction

This document serves as a comprehensive technical blueprint for the **HBnB** project, a RESTful web application designed to manage short-term housing listings, users, reviews, and amenities. It consolidates architectural and behavioral diagrams into one structured reference, providing a foundational guide to drive implementation across all layers of the system.

The primary objectives of this document are:

- To define the system’s structure using package and class diagrams.
- To explain how the application components interact through sequence diagrams.
- To clarify design decisions and support scalability, maintainability, and extensibility.

---

## High-Level Architecture

### Diagram: High-Level Package Diagram

<div align="center">
    <img src="/part1/High-Level_Package_Diagram.png" width="500" height="800">
</div>

**Purpose**:  
This diagram presents the macro-level view of the application’s layered architecture, following a **facade pattern** to ensure decoupling between layers.

**Architecture Layers**:

- **Presentation Layer (API)**  
  Handles HTTP requests/responses, routes, serialization, and error management. Delegates processing to the business logic.

- **Business Logic Layer**  
  Contains the core logic, processes input, applies rules, and coordinates access to persistence.

- **Persistence Layer (ORM/Models)**  
  Manages interaction with the underlying database using data models and repositories.

- **Cross-Cutting Concerns**  
  Includes JWT Authentication, error handling, logging, and environment configurations.

**Design Rationale**:

- **Separation of Concerns**: Each layer has a well-defined responsibility.
- **Security**: JWT is integrated for stateless authentication.
- **Modularity**: Facilitates unit testing and feature scalability.

---

## Business Logic Layer

### Diagram: Class Diagram

<div align="center">
    <img src="/part1/Class_Diagram_for_Business_Logic_Layer.png" width="500" height="800">
</div>

**Purpose**:  
This diagram defines the core domain entities and their interrelationships, emphasizing data structure and logic encapsulation within the Business Layer.

**Core Classes and Responsibilities**:

- **User**
  - Attributes: `id`, `first_name`, `last_name` `email`, `password`, `is_admin`
  - Methods: `get_full_name()`, `set_password()`, `set_email()`, `update_profile_information()`,`delete()`

- **Place**
  - Attributes: `id`, `title`, `description`, `price`, `latitude`, `longitude`
  - Methods: `get_amenity_names()`, `add_amenity()`, `remove_amenity()`, `update_price()`, `delete()`

- **Review**
  - Attributes: `id`, `user_id`, `place_id`, `rating`, `comment`, `created_at`, `updated_at`
  - Methods: `set_rating()`, `set_comment()`, `delete()`

- **Amenity**
  - Attributes: `id`, `name`, `description`, `created_at`, `updated_at`
  - - Methods: `update_name()`, `update_description()`, `set_update_at()`, `delete()`
  - Relationships: Many-to-Many with `Place`

**Design Decisions**:

- **Encapsulation**: All data access is controlled via methods.
- **Associations**: Bidirectional links (e.g., Place ↔ Amenity) to enable intuitive navigation.
- **Validation**: Business logic layer is responsible for input validation beyond API filters.

---

## API Interaction Flow

### Sequence Diagram 1: User Registration

<div align="center">
    <img src="/part1/Sequence_Diagrams_User_Registration.png" width="500" height="800">
</div>

**Purpose**:  
Demonstrates the process of creating a new user account through the API.

**Interaction Steps**:

1. Client sends `POST /register` with required fields.
2. API controller validates input syntax.
3. Business logic checks for existing email.
4. Password is hashed securely.
5. User is persisted in the database.
6. A JWT token is generated and returned.

**Error Scenarios**:
- `400 Bad Request`: Missing or malformed input
- `401 Unauthorized`: JWT missing or invalid.
- `409 Conflict`: Email already registered.
- `500 Internal Server Error`: Database query failed or unhandled exception.
---

### Sequence Diagram 2: Place Creation

<div align="center">
    <img src="/part1/Sequence_Diagrams_Place_Creation.png" width="500" height="800">
</div>

**Purpose**:  
Explains the flow for adding a new listing by an authenticated user.

**Interaction Steps**:

1. Authenticated client sends `POST /places` with place data.
2. Token is validated by middleware.
3. API passes data to business logic.
4. Logic checks constraints (e.g., required fields, ownership).
5. Place is saved.
6. A success response is returned.

**Error Scenarios**:

- `400 Bad Request`: Malformed request or missing required fields.
- `401 Unauthorized`: JWT missing or invalid.
- `404 User Not Found`: User or resource not found.
- `422 Unprocessable Entity`: Input fails domain validation.
- `500 Internal Server Error`: Unexpected server-side failure

---

### Sequence Diagram 3: Review Submission

<div align="center">
    <img src="/part1/Sequence_Diagram_Review_Submission.png" width="500" height="800">
</div>

**Purpose**:  
Covers how users leave feedback on a listing.

**Interaction Steps**:

1. Authenticated user sends `POST /places/{id}/reviews`.
2. Token is validated.
3. API checks if the place exists.
4. Review content is validated.
5. Review is linked and saved.
6. Confirmation is sent back.

**Error Scenarios**:

- `404 Not Found`:  User or resource not found.
- `400 Bad Request`: Malformed request or missing required fields.
- `422 Unprocessable Entity`: Rating out of accepted range.
- `500 Internal Server Error`: Unexpected server-side failure
- `422 Unprocessable Entity`:Input is syntactically correct but fails domain validation.

---

### Sequence Diagram 4: Fetching Places

<div align="center">
    <img src="/part1/Sequence_Diagram_Rewiew_Fetching_a_List_of_Places.png" width="500" height="800">
</div>

**Purpose**:  
Describes how filtered listings are retrieved by city or criteria.

**Interaction Steps**:

1. Client sends `GET /places?city=X`.
2. API parses and validates query parameters.
3. Business logic constructs database query.
4. Matching places are fetched and serialized.
5. Response is returned to the client.

**Error Scenarios**:

- `400 Bad Request`: Malformed request or missing required fields.
- `500 Internal Server Error`: Unexpected server-side failure (e.g., database unavailable).

---

## Conclusion

This document is intended to act as a single source of truth throughout the development of the HBnB application. By clearly documenting architectural layers, class structures, and data interaction patterns, the team can ensure consistency, simplify onboarding for new contributors, and maintain code quality throughout all stages of development.

---

## Authors

👤 **Julien Pulon**  
*Développeur Full Stack Junior*  
- GitHub: [@julienpulon](https://github.com/JulienPul)  
- LinkedIn: [Julien Pulon](https://www.linkedin.com/in/julienpulon/)  

👤 **Haggui Razafimaitso**  
*Développeur Full Stack Junior*  
- GitHub: [@hagguishel](https://github.com/hagguishel)  
- LinkedIn: [Haggui Razafimaitso](https://www.linkedin.com/in/haggui-razafimaitso/)  

---

> Contributions: conception de l’architecture, modélisation des données, implémentation des API, rédaction de la documentation.
