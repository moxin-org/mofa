# ConceptNet API Integration

This Python script demonstrates how to query the ConceptNet API to retrieve semantic relationships for a given concept. ConceptNet is a semantic network that links words and phrases with labeled relationships, useful for natural language understanding and knowledge discovery.

## Features
- Query ConceptNet for relationships related to a specific concept.
- Process and display the first 5 semantic relationships.
- Error handling for API request failures.

## Usage
1. Ensure you have the `requests` library installed:
   ```bash
   pip install requests
   ```
2. Run the script with the desired concept (e.g., 'test'):
   ```python
   python conceptnet_query.py
   ```

## Code Explanation
### Inputs
- `start`: The concept to query (e.g., `/c/en/test`).
- `rel`: The relationship type to filter by (e.g., `/r/RelatedTo`).

### Outputs
- Prints the first 5 relationships in the format:
  ```
  [Start Concept] -> [Relationship] -> [End Concept]
  ```

### Example Output
```
test -> RelatedTo -> exam
test -> RelatedTo -> quiz
test -> RelatedTo -> assessment
test -> RelatedTo -> trial
test -> RelatedTo -> experiment
```

## Error Handling
- If the API request fails, the script prints the status code for debugging.

## Dependencies
- Python 3.x
- `requests` library

## Notes
- Modify the `params` dictionary to query different concepts or relationships.
- The script limits results to the first 5 relationships for brevity. Adjust the slice (`[:5]`) as needed.