# Galaxy Backend

This is the `galaxy_backend` project, an API service built using FastAPI and Tortoise ORM. The service provides endpoints to save and retrieve coin amounts associated with user IDs. Below is a detailed description of the `main.py` code to help you understand its functionality.

## Overview

The application uses FastAPI to create an HTTP server and Tortoise ORM for database interactions. The service has two main endpoints:

- `/save/{user_id}/{coins}`: Save or update the number of coins for a user.
- `/get/{user_id}`: Retrieve the number of coins for a user.

## Detailed Explanation

### Dependencies

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.6+.
- **Tortoise ORM**: An easy-to-use async ORM (Object Relational Mapper) inspired by Django.
- **asynccontextmanager**: A context manager for asynchronous operations.

### Code Breakdown

1. **Initialization**:
    ```python
    app = FastAPI(title="galaxy_backend")
    ```
    Creates a FastAPI application instance with the title "galaxy_backend".

2. **Database Model**:
    ```python
    class Coin(Model):
        id = fields.IntField(primary_key=True)
        user_id = fields.IntField(db_index=True)
        amount = fields.IntField()
    ```
    Defines a `Coin` model with three fields: `id`, `user_id`, and `amount`. The `user_id` field is indexed for faster lookups.

3. **Lifespan Context Manager**:
    ```python
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        db_url = app.state.db_url if hasattr(app.state, 'db_url') else 'sqlite://data.db'
        await Tortoise.init(
            db_url=db_url,
            modules={'models': ['main']}
        )
        await Tortoise.generate_schemas()
        yield
        await Tortoise.close_connections()

    app.router.lifespan_context = lifespan
    ```
    Sets up the database connection using Tortoise ORM. It initializes the connection at the start of the app and closes it when the app shuts down.

4. **Endpoints**:

    - **Save Coins**:
        ```python
        @app.get("/save/{user_id}/{coins}")
        async def save_coins(user_id: int, coins: int):
            coin, created = await Coin.get_or_create(user_id=user_id, defaults={"amount": coins})
            if not created:
                coin.amount += coins
                await coin.save()
            return {"message": "Coins saved successfully", "user_id": user_id, "coin": coin.amount}
        ```
        This endpoint saves the coin amount for a user. If the user already exists, it updates the coin amount by adding the new coins to the existing amount. If the user doesn't exist, it creates a new record.

    - **Get Coins**:
        ```python
        @app.get("/get/{user_id}")
        async def get_coins(user_id: int):
            coin = await Coin.get_or_none(user_id=user_id)
            if coin is None:
                raise HTTPException(status_code=404, detail="User not found")
            return {"user_id": user_id, "coin": coin.amount}
        ```
        This endpoint retrieves the coin amount for a specific user. If the user is not found, it raises a 404 HTTP exception.

## How to Run

1. **Install Dependencies**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt 
    ```

2. **Run the Application**:
    ```bash
    uvicorn main:app --reload
    ```
    This command will start the FastAPI server with automatic reload enabled.

3. **Run test**
    ```bash
    pytest
    ```
    This command run script tests.
