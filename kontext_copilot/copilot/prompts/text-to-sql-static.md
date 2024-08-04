Given the schema of a SQL Server database you are working with, write SQL code to answer the specified question.
The schema and question are provided below.

## Schema:

```
CREATE TABLE "Customers" (
"CustomerId" INTEGER NOT NULL,
"FirstName" NVARCHAR(40) NOT NULL,
"LastName" NVARCHAR(20) NOT NULL,
PRIMARY KEY ("CustomerId"),
)

CREATE TABLE "Accounts" (
"AccountId" INTEGER NOT NULL,
"Balance" DECIMAL NOT NULL,
PRIMARY KEY ("AccountId"),
)

CREATE TABLE "CustomerAccounts" (
"CustomerId" INTEGER NOT NULL,
"AccountId" INTEGER NOT NULL,
PRIMARY KEY ("CustomerId", "AccountId"),
FOREIGN KEY("CustomerId") REFERENCES "Customers" ("CustomerId")
FOREIGN KEY("AccountId") REFERENCES "Accounts" ("AccountId")
)
```

## Question:

```
{{$input}}
```

Provide the SQL code as a JSON object with the key `sql`.
