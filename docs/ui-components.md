# UI Components System Documentation

## Overview

The Context Engineering Demo features a comprehensive UI components system built on Streamlit, providing reusable, modular components for consistent user experience across all industry demonstrations.

## Architecture

### Core Classes

#### UIComponents
The main class providing standardized UI elements for the application.

#### LayoutManager
Utility class for responsive design and layout management.

#### Data Models
- **ResponseData**: Container for response display data
- **MetricsData**: Container for metrics display data

## UIComponents API Reference

### Page Structure Components

#### `render_page_header(title, subtitle)`
Renders the main page header with title and subtitle.

**Parameters:**
- `title` (str): Main page title (default: "🧠 Context Engineering Demo")
- `subtitle` (str): Subtitle/description text

**Example:**
```python
UIComponents.render_page_header(
    title="🧠 Context Engineering Demo",
    subtitle="**See how AI responses transform when context is applied**"
)
```

#### `render_ai_status_indicator(ai_enabled, provider_name)`
Renders AI status indicator showing current mode.

**Parameters:**
- `ai_enabled` (bool): Whether AI is currently enabled
- `provider_name` (str): Name of the AI provider (default: "AI")

**Example:**
```python
UIComponents.render_ai_status_indicator(ai_enabled=True, provider_name="OpenAI")
```

#### `render_metrics_dashboard(metrics)`
Renders the top-level metrics dashboard with 4 key metrics.

**Parameters:**
- `metrics` (MetricsData): Container with metric values

**Example:**
```python
metrics = UIComponents.create_metrics_data(ai_enabled=True)
UIComponents.render_metrics_dashboard(metrics)
```

#### `render_footer(ai_enabled)`
Renders application footer with mode information.

**Parameters:**
- `ai_enabled` (bool): Whether AI mode is currently enabled

### Query Interface Components

#### `render_query_input(industry_name, placeholder, key)`
Renders query input field with industry-specific styling.

**Parameters:**
- `industry_name` (str): Name of the industry for labeling
- `placeholder` (str): Placeholder text for the input
- `key` (Optional[str]): Unique key for the input

**Returns:**
- `Optional[str]`: User query string or None

**Example:**
```python
query = UIComponents.render_query_input(
    industry_name="Restaurant Reservations",
    placeholder="Enter your restaurant request...",
    key="restaurant_query"
)
```

#### `render_sample_queries(queries, industry_name, input_key, max_columns)`
Renders sample queries as clickable buttons.

**Parameters:**
- `queries` (List[str]): List of sample query strings
- `industry_name` (str): Name of the industry
- `input_key` (str): Key for the input field to update
- `max_columns` (int): Maximum number of columns for button layout (default: 3)

**Example:**
```python
UIComponents.render_sample_queries(
    queries=["Book a table", "Find restaurants", "Check availability"],
    industry_name="Restaurant Reservations",
    input_key="restaurant_query"
)
```

#### `render_demo_placeholder(industry_name)`
Renders placeholder message when no query is entered.

**Parameters:**
- `industry_name` (str): Name of the current industry

### Response Display Components

#### `render_comparison_columns(response_data)`
Renders side-by-side comparison of generic vs contextual responses.

**Parameters:**
- `response_data` (ResponseData): Container with both responses and context

**Example:**
```python
response_data = UIComponents.create_response_data(
    generic_response="Generic response...",
    contextual_response="Contextual response...",
    context_data=context,
    query=query,
    industry="Healthcare"
)
UIComponents.render_comparison_columns(response_data)
```

#### `render_context_expander(context_data, title)`
Renders expandable context display section.

**Parameters:**
- `context_data` (Dict[str, Any]): Dictionary containing context information
- `title` (str): Title for the expander section (default: "📊 Available Context")

**Returns:**
- `bool`: True if expander is expanded, False otherwise

**Example:**
```python
UIComponents.render_context_expander(
    context_data={"user": "John", "preferences": ["Italian", "Mexican"]},
    title="📊 User Context"
)
```

### Feedback & Status Components

#### `render_loading_indicator(message, show_spinner)`
Renders loading indicator for AI processing.

**Parameters:**
- `message` (str): Loading message to display (default: "🤖 AI is thinking...")
- `show_spinner` (bool): Whether to show spinner animation (default: True)

**Example:**
```python
with UIComponents.render_loading_indicator("🤖 AI is thinking..."):
    # AI processing code here
    response = generate_ai_response(query)
```

#### `render_error_display(error_message, error_type, show_details, details)`
Renders error message with optional details.

**Parameters:**
- `error_message` (str): Main error message to display
- `error_type` (str): Type of error (default: "Error")
- `show_details` (bool): Whether to show detailed error information (default: False)
- `details` (Optional[str]): Detailed error information

**Example:**
```python
UIComponents.render_error_display(
    error_message="Failed to generate AI response",
    error_type="Error",
    show_details=True,
    details=str(exception)
)
```

#### `render_success_message(message, details)`
Renders success message with optional details.

**Parameters:**
- `message` (str): Success message to display
- `details` (Optional[str]): Optional additional details

**Example:**
```python
UIComponents.render_success_message(
    "Response generated successfully!",
    details=f"Used {tokens} tokens in {time:.2f}s"
)
```

#### `render_info_message(message, icon)`
Renders informational message.

**Parameters:**
- `message` (str): Information message to display
- `icon` (str): Icon to display with the message (default: "ℹ️")

### Utility Components

#### `render_industry_selector(industries, key)`
Renders industry selection sidebar.

**Parameters:**
- `industries` (List[str]): List of available industries
- `key` (str): Unique key for the selectbox (default: "industry_selector")

**Returns:**
- `str`: Selected industry name

#### `render_debug_sidebar(debug_info)`
Renders debug information in sidebar.

**Parameters:**
- `debug_info` (Dict[str, Any]): Dictionary containing debug information

## LayoutManager API Reference

### Column Layouts

#### `create_two_column_layout(left_ratio)`
Creates a two-column layout with specified ratio.

**Parameters:**
- `left_ratio` (float): Ratio for left column (0.0 to 1.0, default: 0.5)

**Returns:**
- `Tuple[Any, Any]`: Tuple of (left_column, right_column)

**Example:**
```python
left_col, right_col = LayoutManager.create_two_column_layout(left_ratio=0.6)
with left_col:
    st.write("Left content")
with right_col:
    st.write("Right content")
```

#### `create_three_column_layout(ratios)`
Creates a three-column layout with specified ratios.

**Parameters:**
- `ratios` (Optional[List[float]]): List of ratios for columns (default: [1, 1, 1])

**Returns:**
- `Tuple[Any, Any, Any]`: Tuple of (left_column, center_column, right_column)

**Example:**
```python
col1, col2, col3 = LayoutManager.create_three_column_layout([1, 2, 1])
```

### Container Management

#### `create_centered_container(width)`
Creates a centered container with specified width.

**Parameters:**
- `width` (str): CSS width value for the container (default: "80%")

**Returns:**
- Streamlit container

**Example:**
```python
with LayoutManager.create_centered_container():
    st.write("Centered content")
```

### Spacing and Sections

#### `add_vertical_space(lines)`
Adds vertical spacing between elements.

**Parameters:**
- `lines` (int): Number of empty lines to add (default: 1)

**Example:**
```python
LayoutManager.add_vertical_space(lines=2)
```

#### `create_sidebar_section(title, content_func)`
Creates a sidebar section with title and content.

**Parameters:**
- `title` (str): Section title
- `content_func`: Function to render section content

**Example:**
```python
def render_debug_info():
    st.write("Debug information here")

LayoutManager.create_sidebar_section("Debug Info", render_debug_info)
```

## Data Models

### ResponseData

Container for response display data.

**Fields:**
- `generic_response` (str): Generic AI response
- `contextual_response` (str): Context-aware AI response
- `context_data` (Dict[str, Any]): Context information used
- `query` (str): Original user query
- `industry` (str): Industry name
- `timestamp` (Optional[datetime]): Response timestamp

**Example:**
```python
response_data = ResponseData(
    generic_response="Generic advice...",
    contextual_response="Personalized advice...",
    context_data={"user": "John", "age": 35},
    query="I need financial advice",
    industry="Financial Services",
    timestamp=datetime.now()
)
```

### MetricsData

Container for metrics display data.

**Fields:**
- `industries_count` (int): Number of available industries (default: 6)
- `context_points` (str): Context data points available (default: "50+")
- `response_quality` (str): Quality improvement indicator (default: "10x")
- `user_satisfaction` (str): User satisfaction metric (default: "95%")
- `ai_enabled` (bool): AI enablement status (default: False)

**Example:**
```python
metrics = MetricsData(
    industries_count=6,
    context_points="50+",
    response_quality="10x",
    user_satisfaction="95%",
    ai_enabled=True
)
```

## Convenience Functions

### `render_demo_header(industry_name, icon)`
Quick function to render demo header.

**Parameters:**
- `industry_name` (str): Name of the industry
- `icon` (str): Industry icon (default: "🏢")

### `render_query_section(industry_name, placeholder, sample_queries)`
Complete query input section with sample queries.

**Parameters:**
- `industry_name` (str): Name of the industry
- `placeholder` (str): Input placeholder text
- `sample_queries` (List[str]): List of sample queries

**Returns:**
- `Optional[str]`: User query string

### `render_response_comparison(generic_response, contextual_response, context_data, query, industry)`
Complete response comparison display.

**Parameters:**
- `generic_response` (str): Generic AI response
- `contextual_response` (str): Contextual AI response
- `context_data` (Dict[str, Any]): Context information
- `query` (str): Original user query
- `industry` (str): Industry name

## Usage Patterns

### Complete Demo Page

```python
from ui.components import UIComponents, render_demo_header, render_query_section, render_response_comparison

# Page setup
UIComponents.render_page_header()
UIComponents.render_ai_status_indicator(ai_enabled=True, provider_name="OpenAI")

# Metrics
metrics = UIComponents.create_metrics_data(ai_enabled=True)
UIComponents.render_metrics_dashboard(metrics)

# Demo header
render_demo_header("Restaurant Reservations", "🍽️")

# Query interface
sample_queries = ["Book a table", "Find restaurants", "Check availability"]
query = render_query_section("Restaurant Reservations", "Enter request...", sample_queries)

# Response comparison
if query:
    with UIComponents.render_loading_indicator():
        generic_response = generate_generic_response(query)
        contextual_response = generate_contextual_response(query, context)
    
    render_response_comparison(generic_response, contextual_response, context, query, "Restaurant Reservations")

# Footer
UIComponents.render_footer(ai_enabled=True)
```

### Error Handling Pattern

```python
try:
    response = ai_provider.generate_response(request)
    UIComponents.render_success_message(
        "Response generated successfully!",
        details=f"Tokens: {response.tokens_used}, Time: {response.response_time:.2f}s"
    )
except Exception as e:
    UIComponents.render_error_display(
        error_message="Failed to generate AI response",
        error_type="Error",
        show_details=True,
        details=str(e)
    )
```

### Layout Management Pattern

```python
from ui.components import LayoutManager

# Two-column layout
left_col, right_col = LayoutManager.create_two_column_layout(left_ratio=0.7)

with left_col:
    # Main content
    render_query_section(...)

with right_col:
    # Sidebar content
    UIComponents.render_context_expander(context_data)

# Add spacing
LayoutManager.add_vertical_space(lines=2)

# Centered container for footer
with LayoutManager.create_centered_container():
    UIComponents.render_footer(ai_enabled=True)
```

## Design Principles

### Consistency
- All components follow the same visual and interaction patterns
- Consistent spacing, colors, and typography
- Standardized error handling and feedback

### Modularity
- Components are self-contained and reusable
- Clear separation of concerns between layout and content
- Easy to extend and customize

### Responsiveness
- Components adapt to different screen sizes
- Mobile-friendly layouts and interactions
- Flexible column systems

### Accessibility
- Semantic HTML structure through Streamlit
- Clear visual hierarchy and contrast
- Keyboard navigation support

## Integration with Demo Framework

The UI components integrate seamlessly with the demo framework:

```python
from demos.base_demo import BaseDemo
from ui.components import UIComponents

class CustomDemo(BaseDemo):
    def render_demo_ui(self):
        # Use UI components for consistent interface
        UIComponents.render_page_header(f"🏢 {self.industry_name}")
        
        # Industry-specific query interface
        query = UIComponents.render_query_input(
            industry_name=self.industry_name,
            placeholder=self.get_query_placeholder()
        )
        
        # Sample queries
        UIComponents.render_sample_queries(
            queries=self.get_sample_queries(),
            industry_name=self.industry_name,
            input_key=f"{self.industry_name}_query"
        )
        
        return query
```

## Best Practices

### Component Usage
1. Always use the provided data models (ResponseData, MetricsData) for consistency
2. Leverage convenience functions for common patterns
3. Use LayoutManager for responsive designs
4. Handle errors gracefully with the error display components

### Performance
1. Use session state keys consistently to avoid unnecessary re-renders
2. Cache expensive operations outside of UI components
3. Use loading indicators for long-running operations

### Customization
1. Extend components through inheritance rather than modification
2. Use the provided styling hooks for theme integration
3. Follow the established naming conventions for new components

## Future Enhancements

### Planned Features
- Theme customization system
- Advanced layout templates
- Interactive data visualization components
- Enhanced mobile responsiveness
- Accessibility improvements

### Extension Points
- Custom component registration system
- Plugin architecture for industry-specific components
- Advanced styling and theming options
- Integration with external UI libraries