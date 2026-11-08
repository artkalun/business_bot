# Business telegram bot
## What is `BUSINESS-CONNECTION-ID` in `.env.example`?

> Uniqe indentifer of the user who linked bot to an account.

You can get it with:

``` python
@dp.business_connection()
async def tmp(business_connection):
    print(business_connection.id)
```
