# Implementation Plan

- [x] 1. Update core prompt service infrastructure

  - Modify PromptTemplate class to include professional role and customer focus fields
  - Add response style and personalization metadata to template structure
  - Update template validation to ensure customer-focused language
  - _Requirements: 3.1, 3.3, 4.1_

- [x] 2. Rewrite system message templates for all industries

  - [x] 2.1 Update e-commerce system message to define shopping assistant role

    - Replace business consultant language with personal shopping assistant role
    - Focus on helping customers find products and make purchasing decisions
    - _Requirements: 1.1, 3.3_

  - [x] 2.2 Update healthcare system message to define medical practitioner role

    - Replace practice management language with healthcare professional role
    - Focus on providing medical guidance and health information
    - Include appropriate medical disclaimers
    - _Requirements: 1.2, 3.3_

  - [x] 2.3 Update restaurant system message to define concierge service role

    - Replace restaurant business language with concierge service role
    - Focus on restaurant selection, reservations, and dining recommendations
    - _Requirements: 1.3, 3.3_

  - [x] 2.4 Update financial system message to define financial advisor role

    - Replace financial business language with personal financial advisor role
    - Focus on providing personalized financial guidance and advice
    - Include appropriate financial disclaimers
    - _Requirements: 1.4, 3.3_

  - [x] 2.5 Update education system message to define educator/advisor role

    - Replace educational business language with educator/academic advisor role
    - Focus on providing learning guidance and academic advice
    - _Requirements: 1.5, 3.3_

  - [x] 2.6 Update real estate system message to define real estate agent role
    - Replace real estate business language with real estate agent role
    - Focus on helping with property needs and real estate decisions
    - _Requirements: 1.6, 3.3_

- [x] 3. Rewrite generic prompt templates for customer-facing responses

  - [x] 3.1 Transform e-commerce generic template to shopping assistant format

    - Remove business consultation language about selling products online
    - Add customer service language for helping customers find products
    - Include product recommendation and shopping guidance instructions
    - _Requirements: 1.1, 3.1, 4.1_

  - [x] 3.2 Transform healthcare generic template to medical practitioner format

    - Remove practice management language about healthcare operations
    - Add medical professional language for providing health guidance
    - Include patient care and medical information instructions
    - _Requirements: 1.2, 3.1, 4.1_

  - [x] 3.3 Transform restaurant generic template to concierge service format

    - Remove restaurant business language about operations and management
    - Add concierge service language for restaurant selection and reservations
    - Include dining recommendation and reservation assistance instructions
    - _Requirements: 1.3, 3.1, 4.1_

  - [x] 3.4 Transform financial generic template to financial advisor format

    - Remove financial business language about operations and compliance
    - Add personal financial advisor language for providing financial guidance
    - Include investment advice and financial planning instructions
    - _Requirements: 1.4, 3.1, 4.1_

  - [x] 3.5 Transform education generic template to educator/advisor format

    - Remove educational business language about administration and operations
    - Add educator/advisor language for providing learning guidance
    - Include academic advice and educational resource instructions
    - _Requirements: 1.5, 3.1, 4.1_

  - [x] 3.6 Transform real estate generic template to real estate agent format
    - Remove real estate business language about operations and management
    - Add real estate agent language for helping with property needs
    - Include property recommendation and real estate guidance instructions
    - _Requirements: 1.6, 3.1, 4.1_

- [ ] 4. Enhance contextual prompt templates for personalized responses

  - [x] 4.1 Update e-commerce contextual template for personalized shopping assistance

    - Add instructions to reference customer purchase history and preferences
    - Include loyalty status, budget considerations, and favorite brands
    - Structure template to provide personalized product recommendations
    - _Requirements: 2.1, 2.2, 2.3, 3.2_

  - [x] 4.2 Update healthcare contextual template for personalized medical guidance

    - Add instructions to reference patient medical history and conditions
    - Include age, lifestyle factors, and health goals
    - Structure template to provide personalized health recommendations
    - _Requirements: 2.1, 2.2, 2.3, 3.2_

  - [x] 4.3 Update restaurant contextual template for personalized dining recommendations

    - Add instructions to reference dining preferences and dietary restrictions
    - Include location, occasion type, and previous restaurant visits
    - Structure template to provide personalized restaurant recommendations
    - _Requirements: 2.1, 2.2, 2.3, 3.2_

  - [x] 4.4 Update financial contextual template for personalized financial advice

    - Add instructions to reference financial goals and risk tolerance
    - Include current financial situation and investment history
    - Structure template to provide personalized financial recommendations
    - _Requirements: 2.1, 2.2, 2.3, 3.2_

  - [x] 4.5 Update education contextual template for personalized learning guidance

    - Add instructions to reference learning style and academic background
    - Include career goals, interests, and previous achievements
    - Structure template to provide personalized educational recommendations
    - _Requirements: 2.1, 2.2, 2.3, 3.2_

  - [x] 4.6 Update real estate contextual template for personalized property guidance
    - Add instructions to reference property preferences and budget
    - Include location requirements, lifestyle needs, and property history
    - Structure template to provide personalized property recommendations
    - _Requirements: 2.1, 2.2, 2.3, 3.2_

- [x] 5. Update demo fallback responses to match new professional roles

  - [x] 5.1 Update e-commerce demo fallback responses to shopping assistant style

    - Rewrite hardcoded responses to act as personal shopping assistant
    - Include product recommendations and shopping guidance
    - Remove business consultation language from fallback responses
    - _Requirements: 1.1, 4.2, 5.1_

  - [x] 5.2 Update healthcare demo fallback responses to medical practitioner style

    - Rewrite hardcoded responses to act as healthcare professional
    - Include medical guidance and health information
    - Remove practice management language from fallback responses
    - _Requirements: 1.2, 4.2, 5.1_

  - [x] 5.3 Update restaurant demo fallback responses to concierge service style

    - Rewrite hardcoded responses to act as concierge service
    - Include restaurant recommendations and reservation assistance
    - Remove restaurant business language from fallback responses
    - _Requirements: 1.3, 4.2, 5.1_

  - [x] 5.4 Update financial demo fallback responses to financial advisor style

    - Rewrite hardcoded responses to act as personal financial advisor
    - Include financial advice and investment guidance
    - Remove financial business language from fallback responses
    - _Requirements: 1.4, 4.2, 5.1_

  - [x] 5.5 Update education demo fallback responses to educator/advisor style

    - Rewrite hardcoded responses to act as educator/academic advisor
    - Include learning guidance and academic advice
    - Remove educational business language from fallback responses
    - _Requirements: 1.5, 4.2, 5.1_

  - [x] 5.6 Update real estate demo fallback responses to real estate agent style
    - Rewrite hardcoded responses to act as real estate agent
    - Include property recommendations and real estate guidance
    - Remove real estate business language from fallback responses
    - _Requirements: 1.6, 4.2, 5.1_

- [x] 6. Add response formatting and structure improvements

  - Implement consistent response formatting across all industries
  - Add conversational language patterns and friendly tone
  - Include clear call-to-action elements in responses
  - Structure responses with organized sections and bullet points
  - _Requirements: 4.1, 4.3, 4.4, 4.5_

- [ ] 7. Create comprehensive test cases for new prompt behavior

  - [ ] 7.1 Write unit tests for updated prompt templates

    - Test that generic templates generate customer-focused responses
    - Test that contextual templates properly use personalization data
    - Verify that system messages define appropriate professional roles
    - _Requirements: 3.4, 3.5_

  - [ ] 7.2 Create integration tests for end-to-end response quality
    - Test complete user query flows for each industry
    - Verify responses feel like professional service interactions
    - Compare old vs. new response styles for quality improvement
    - _Requirements: 5.1, 5.2, 5.4_

- [x] 8. Update documentation and examples

  - Update prompt service documentation to reflect new customer-focused approach
  - Add examples of professional responses for each industry
  - Document the transformation from business consultation to customer service
  - Create guidelines for maintaining professional role consistency
  - _Requirements: 3.4, 4.1_

- [ ] 9. Validate response quality across all industries
  - Test sample queries from each industry to ensure appropriate professional responses
  - Verify contextual responses properly personalize using customer data
  - Confirm that responses are helpful, conversational, and solution-focused
  - Validate that professional boundaries and disclaimers are appropriate
  - _Requirements: 1.7, 2.4, 4.1, 5.5_
