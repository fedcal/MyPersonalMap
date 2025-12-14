Help me document an API endpoint or update the API documentation.

Process:
1. Ask me which endpoint needs documentation
2. Review the endpoint implementation
3. Write comprehensive documentation including:
   - Clear description of what the endpoint does
   - HTTP method and path
   - Authentication requirements
   - Request body schema with all parameters:
     - Type
     - Required/optional
     - Constraints
     - Description
   - Response schema
   - Possible error codes with descriptions
   - Complete request/response examples in JSON
4. Add the docstring to the route function following Google style
5. Update doc/api-documentation.md if it's a new endpoint
6. Ensure the Swagger UI (/docs) will display correctly

The documentation should be clear enough that a frontend developer can integrate the API without asking questions.
