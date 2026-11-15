# Business telegram bot

## Database structure

``` sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    sent_at TIMESTAMP NOT NULL,
    type TEXT NOT NULL CHECK (
        type IN ("text", "photo")
    ),
    content TEXT DEFAULT NULL,
    file_expired BOOLEAN DEFAULT NULL
)
```

- `id` - uniqe `message.message_id`
- `sent_at` - `message.date`
- `type` - message type, describes the purpose of the following columns
- `content` - text, caption, checklist content, etc.
- `file_expired` - boolean column, with 3 states
    1. `NULL` - if the message had no file 
    2. `FALSE` - if the file is avalible
    3. `TRUE` - if the file has been stored too long

## FAQ
### What is `BUSINESS-CONNECTION-ID` in `.env.example`?

> Uniqe indentifer of the user who linked bot to an account.

You can get it with:

``` python
@dp.business_connection()
async def tmp(business_connection):
    print(business_connection.id)
```

