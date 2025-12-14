Help me write comprehensive tests for a component.

Process:
1. Ask me what needs to be tested (endpoint, service, model, etc.)
2. Create appropriate test file in tests/ directory following the structure:
   - tests/test_api/ for endpoint tests
   - tests/test_services/ for service tests
   - tests/test_models/ for model tests
3. Write tests covering:
   - Happy path (successful operation)
   - Error cases (validation errors, not found, etc.)
   - Edge cases (boundary values, empty inputs)
   - Geospatial operations if applicable (distance calculations, spatial queries)
4. Use appropriate fixtures:
   - test_db for database operations
   - client for API endpoint tests
   - Mock external services (geocoding, etc.)
5. Follow AAA pattern: Arrange, Act, Assert
6. Use descriptive test names that explain what is being tested
7. Add parametrized tests for multiple input scenarios if applicable

Show me how to run the tests and check coverage:
```bash
pytest tests/[test_file].py -v
pytest --cov=pymypersonalmap --cov-report=term-missing
```
