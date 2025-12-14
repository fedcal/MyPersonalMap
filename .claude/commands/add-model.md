Help me add a new SQLAlchemy model to the database schema.

Steps to follow:
1. Ask me for the model details (table name, columns, relationships)
2. Create the SQLAlchemy model class in models/ inheriting from Base
3. Add appropriate columns with:
   - Correct data types (use Geometry for spatial columns with SRID 4326)
   - Constraints (nullable, unique, default values)
   - Indexes (including spatial indexes for POINT/LINESTRING)
   - Foreign keys with proper ON DELETE behavior
4. Define relationships with other models
5. Add __repr__ method for debugging
6. Create Alembic migration:
   ```bash
   alembic revision --autogenerate -m "Add [model_name] table"
   ```
7. Review the generated migration file and make manual adjustments if needed
8. Apply the migration:
   ```bash
   alembic upgrade head
   ```
9. Create corresponding Pydantic schemas for API request/response

Remember to use SRID 4326 (WGS84) for all spatial columns and add spatial indexes for performance.
