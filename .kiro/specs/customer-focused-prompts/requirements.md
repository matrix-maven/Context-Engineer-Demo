# Requirements Document

## Introduction

The current AI-powered demo application responds to user queries with business consultation advice rather than acting as helpful industry-specific assistants. When users ask "show me running shoes for women," they receive generic business advice about selling shoes online instead of helpful product recommendations. When users ask healthcare questions, they get practice management advice instead of medical guidance. This feature will refactor the prompt templates and response format across all industry demos to make the AI act as customer-facing professionals (shopping assistants, medical practitioners, restaurant staff, financial advisors, educators, real estate agents) rather than business consultants.

## Requirements

### Requirement 1

**User Story:** As a user querying the demo application, I want responses that directly address my needs as a customer/client, so that the demo feels like interacting with real industry professionals rather than receiving business consultation advice.

#### Acceptance Criteria

1. WHEN a user asks "show me running shoes for women" THEN the system SHALL respond with product recommendations and shopping guidance
2. WHEN a user asks healthcare questions THEN the system SHALL act as a medical practitioner providing health guidance
3. WHEN a user asks restaurant questions THEN the system SHALL act as a concierge service helping with restaurant selection, reservations and dining
4. WHEN a user asks financial questions THEN the system SHALL act as a financial advisor providing personalized advice
5. WHEN a user asks education questions THEN the system SHALL act as an educator or academic advisor
6. WHEN a user asks real estate questions THEN the system SHALL act as a real estate agent helping with property needs
7. IF the query is industry-specific THEN the system SHALL respond as the appropriate professional role

### Requirement 2

**User Story:** As a user, I want the contextual responses to feel personalized and relevant to my profile across all industries, so that I can see the clear value of context-aware AI assistance.

#### Acceptance Criteria

1. WHEN using contextual responses THEN the system SHALL reference specific user preferences, history, and profile data
2. WHEN making recommendations THEN the system SHALL consider the user's budget, preferences, past behavior, and relevant context
3. WHEN displaying contextual responses THEN the system SHALL show clear personalization elements specific to each industry
4. WHEN comparing generic vs contextual THEN the difference SHALL be immediately apparent across all industry demos
5. IF context includes relevant history THEN recommendations SHALL reference appropriate past behavior for that industry

### Requirement 3

**User Story:** As a developer, I want the prompt templates to be customer-focused rather than business-focused across all industries, so that the AI generates appropriate professional service responses.

#### Acceptance Criteria

1. WHEN generating generic prompts THEN the system SHALL instruct the AI to act as the appropriate industry professional
2. WHEN generating contextual prompts THEN the system SHALL instruct the AI to use customer/client context for personalization
3. WHEN creating system messages THEN the system SHALL define the AI's role as the appropriate professional (shopping assistant, medical practitioner, concierge service, financial advisor, educator, real estate agent)
4. WHEN updating prompts THEN the system SHALL remove business consultation language across all industry templates
5. IF prompts reference industry context THEN they SHALL focus on professional service delivery within that industry

### Requirement 4

**User Story:** As a user, I want responses to be conversational and helpful, so that the interaction feels natural and engaging.

#### Acceptance Criteria

1. WHEN generating responses THEN the system SHALL use conversational, friendly language
2. WHEN providing recommendations THEN the system SHALL explain why items are suggested
3. WHEN displaying responses THEN the system SHALL use appropriate formatting and structure
4. WHEN addressing queries THEN the system SHALL be direct and solution-focused
5. IF multiple options exist THEN the system SHALL present them in an organized, helpful way

### Requirement 5

**User Story:** As a user, I want the demo to showcase realistic industry-specific interactions across all sectors, so that I can understand how context-aware AI would work in real professional service scenarios.

#### Acceptance Criteria

1. WHEN demonstrating any industry scenario THEN responses SHALL feel like real professional service interactions
2. WHEN showing recommendations THEN the system SHALL include realistic details appropriate to that industry (prices, features, medical advice, property details, etc.)
3. WHEN using customer/client context THEN the system SHALL reference relevant profile information naturally (loyalty status, medical history, dining preferences, financial goals, etc.)
4. WHEN comparing responses THEN the contextual version SHALL clearly demonstrate personalization value across all industries
5. IF the user asks industry-specific questions THEN the system SHALL provide detailed, professional information appropriate to that sector