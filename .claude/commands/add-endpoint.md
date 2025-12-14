Help me add a new REST API endpoint to the FastAPI application.

Follow these steps:
1. Ask me for the endpoint details (path, HTTP method, purpose)
2. Create appropriate Pydantic request/response models in models/schemas.py
3. Implement the service method if needed in services/
4. Create the route function in api/routes/ with:
   - Proper dependency injection for database session
   - Request validation with Pydantic models
   - Error handling with appropriate HTTP status codes
   - Comprehensive docstring with examples
5. Register the router in main.py if it's a new router
6. Show me how to test it with curl or httpx

Make sure to follow the project's layered architecture pattern: API → Service → Repository → Database.
