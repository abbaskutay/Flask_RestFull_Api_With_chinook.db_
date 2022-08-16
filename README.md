# NTT-Data Case

NTT-Data Case

## Installation

With Docker:

```sh
$ docker compose up
```

## Handler Structure

- `/api/invoices                           | http://127.0.0.1:5000/api/invoices`
- `/api/invoices/invoice_id                | http://127.0.0.1:5000/api/invoices/<int:invoice_id>`
- `/api/invoices/add                       | http://127.0.0.1:5000/api/invoices/add`
- `/api/invoices/put/invoice_id            | http://127.0.0.1:5000/api/invoices/put/<int:invoice_id>`
- `/api/invoices/delete/invoice_id         | http://127.0.0.1:5000/api/invoices/delete/<int:invoice_id>`

# Converter Example Request

**URL** : `/api/invoices`

**Method** : `GET`

**Request example**

```json
{
  "weburl": "http://127.0.0.1:5000/api/invoices"
}
```

## Success Response

**Code** : `200 or 201`

**Content example**

```json
{
    "InvoiceId": 1,
    "CustomerId": 2,
    "InvoiceDate": "Thu, 01 Jan 2009 00:00:00 -0000",
    "BillingAddress": "Theodor-Heuss-Straße 34",
    "BillingCity": "Stuttgart",
    "BillingState": null,
    "BillingCountry": "Germany",
    "BillingPostalCode": "70174",
    "Total": 1.98
}
```


# Converter Example Request

**URL** : `api/invoices/int:invoice_id`

**Method** : `GET`

**Request example**

```json
{
  "weburl": "http://127.0.0.1:5000/api/invoices/<int:invoice_id>"
}
```

## Success Response

**Code** : `200 or 201`

**Content example**

```json
{
    "InvoiceId": 2,
    "CustomerId": 4,
    "InvoiceDate": "Fri, 02 Jan 2009 00:00:00 -0000",
    "BillingAddress": "Ullevålsveien 14",
    "BillingCity": "Oslo",
    "BillingState": null,
    "BillingCountry": "Norway",
    "BillingPostalCode": "0171",
    "Total": 3.96
}
```

# Converter Example Request

**URL** : `api/invoices/add`

**Method** : `POST`

**Request example**

**Arguments**
```json
{
    "InvoiceId": "Must be filled",
    "CustomerId": "Must be filled",
    "InvoiceDate": "Must not be filled" -> "it attaches today's date"
    "BillingAddress": "Optional",
    "BillingCity": "Optional",
    "BillingState": "Optional",
    "BillingCountry": "Optional",
    "BillingPostalCode": "Optional",
    "Total": "Must be filled"
}
```


```json
{
  "weburl": "http://127.0.0.1:5000/api/invoices/add"
}
```

## Success Response

**Code** : `200 or 201`

**Content example**

```json
{
    "InvoiceId": 3,
    "CustomerId": 8,
    "InvoiceDate": "Sat, 03 Jan 2009 00:00:00 -0000",
    "BillingAddress": null,
    "BillingCity": "Brussels",
    "BillingState": null,
    "BillingCountry": "Belgium",
    "BillingPostalCode": "1000",
    "Total": 5.94
}
```

# Converter Example Request

**URL** : `api/invoices/put/invoice_id`

**Method** : `PUT`

**Request example**

**Arguments**
```json
{
    "InvoiceId": "Must be filled",
    "CustomerId": "Must be filled",
    "InvoiceDate": "Must not be filled" -> "it attaches today's date"
    "BillingAddress": "Optional",
    "BillingCity": "Optional",
    "BillingState": "Optional",
    "BillingCountry": "Optional",
    "BillingPostalCode": "Optional",
    "Total": "Must be filled"
}
```


```json
{
  "weburl": "http://127.0.0.1:5000/api/invoices/put/<int:invoice_id>"
}
```

## Success Response

**Code** : `200 or 201`

**Content example**

```json
{
    "InvoiceId": 3,
    "CustomerId": 8,
    "InvoiceDate": "Sat, 03 Jan 2009 00:00:00 -0000",
    "BillingAddress": null,
    "BillingCity": "Brussels",
    "BillingState": null,
    "BillingCountry": "Belgium",
    "BillingPostalCode": "1000",
    "Total": 5.94
}
```
# Converter Example Request

**URL** : `api/invoices/delete/invoice_id`

**Method** : `DELETE`

**Request example**


```json
{
  "weburl": "http://127.0.0.1:5000/api/invoices/delete/<int:invoice_id>"
}
```

## Success Response

**Code** : `200 or 201`

**Content example**

```json
{
    "InvoiceId": 3,
    "CustomerId": 8,
    "InvoiceDate": "Sat, 03 Jan 2009 00:00:00 -0000",
    "BillingAddress": null,
    "BillingCity": "Brussels",
    "BillingState": null,
    "BillingCountry": "Belgium",
    "BillingPostalCode": "1000",
    "Total": 5.94
}
```

