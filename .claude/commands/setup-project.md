Guide me through the complete project setup from scratch.

I'll walk you through:

1. **Environment Setup**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate   # Windows

   # Install dependencies
   pip install -r pymypersonalmap/requirements.txt
   ```

2. **Database Setup**
   ```bash
   # Create MySQL database
   mysql -u root -p
   CREATE DATABASE mypersonalmap;
   CREATE USER 'mypersonalmap_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON mypersonalmap.* TO 'mypersonalmap_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

3. **Configuration**
   ```bash
   # Copy environment template
   cp .env.example .env

   # Generate SECRET_KEY
   python -c "import secrets; print(secrets.token_urlsafe(32))"

   # Edit .env with your values:
   # - DATABASE_URL
   # - SECRET_KEY (use generated key above)
   # - Other settings as needed
   ```

4. **Database Migrations**
   ```bash
   # Initialize Alembic (if not done)
   alembic init alembic

   # Create initial migration
   alembic revision --autogenerate -m "Initial schema"

   # Apply migrations
   alembic upgrade head
   ```

5. **Verify Setup**
   ```bash
   # Run the application
   cd pymypersonalmap
   python main.py

   # In another terminal, test
   curl http://localhost:8000/health

   # Open browser
   # Swagger UI: http://localhost:8000/docs
   ```

6. **Run Tests**
   ```bash
   # Create test database
   mysql -u root -p
   CREATE DATABASE mypersonalmap_test;
   EXIT;

   # Run tests
   pytest
   ```

At each step, I'll check for errors and help you resolve them.
