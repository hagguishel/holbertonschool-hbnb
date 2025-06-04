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

![High-Level Architecture Diagram](./part1/High-Level_Package_Diagram.png)

### Diagram: High-Level Package Diagram

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
![High-Level Architecture Diagram](./part1/Class_Diagram_for_Business_Logic_Layer.png)

**Purpose**:  
This diagram defines the core domain entities and their interrelationships, emphasizing data structure and logic encapsulation within the Business Layer.

**Core Classes and Responsibilities**:

- **User**
  - Attributes: `id`, `email`, `hashed_password`, `is_admin`
  - Methods: `register()`, `authenticate()`, `update_profile()`

- **Place**
  - Attributes: `id`, `name`, `city`, `owner_id`, `amenities`, `reviews`
  - Methods: `create()`, `update()`, `delete()`

- **Review**
  - Attributes: `id`, `user_id`, `place_id`, `rating`, `comment`, `timestamp`
  - Methods: `validate_rating()`, `to_dict()`

- **Amenity**
  - Attributes: `id`, `name`, `description`
  - Relationships: Many-to-Many with `Place`

**Design Decisions**:

- **Encapsulation**: All data access is controlled via methods.
- **Associations**: Bidirectional links (e.g., Place ↔ Amenity) to enable intuitive navigation.
- **Validation**: Business logic layer is responsible for input validation beyond API filters.

---

## API Interaction Flow

### Sequence Diagram 1: User Registration

![High-Level Architecture Diagram](./part1/Sequence_Diagrams_User_Registration.png)

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

- `400 Bad Request`: Missing or malformed input.
- `409 Conflict`: Email already registered.

---

### Sequence Diagram 2: Place Creation

![High-Level Architecture Diagram](./part1/Sequence_Diagrams_Place_Creation.png)

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

- `401 Unauthorized`: JWT missing or invalid.
- `422 Unprocessable Entity`: Input fails domain validation.

---

### Sequence Diagram 3: Review Submission

![High-Level Architecture Diagram](./part1/Sequence_Diagram_Review_Submission.png)

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

- `404 Not Found`: Place ID invalid.
- `400 Bad Request`: Rating out of accepted range.

---

### Sequence Diagram 4: Fetching Places

![High-Level Architecture Diagram](./part1/Sequence_Diagram_Rewiew_Fetching_a_List_of_Places.png)

**Purpose**:  
Describes how filtered listings are retrieved by city or criteria.

**Interaction Steps**:

1. Client sends `GET /places?city=X`.
2. API parses and validates query parameters.
3. Business logic constructs database query.
4. Matching places are fetched and serialized.
5. Response is returned to the client.

**Error Scenarios**:

- `422 Unprocessable Entity`: Invalid query parameters.
- `500 Internal Server Error`: Database access failure.

---

## Conclusion

This document is intended to act as a single source of truth throughout the development of the HBnB application. By clearly documenting architectural layers, class structures, and data interaction patterns, the team can ensure consistency, simplify onboarding for new contributors, and maintain code quality throughout all stages of development.

---

## Authors

👤 **Julien Pulon**  
*Développeur Web & Web Mobile*  
- GitHub: [@julienpulon](https://github.com/julienpulon)  
- LinkedIn: [Julien Pulon](https://www.linkedin.com/in/julienpulon/)  

👤 **Haggui Razafimaitso**  
*Développeur Full Stack Junior*  
- GitHub: [@haggui-rz](https://github.com/haggui-rz)  
- LinkedIn: [Haggui Razafimaitso](https://www.linkedin.com/in/haggui-razafimaitso/)  

---

> Contributions: conception de l’architecture, modélisation des données, implémentation des API, rédaction de la documentation.
