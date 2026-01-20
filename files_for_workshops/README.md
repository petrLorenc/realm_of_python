# Files for Workshop

This directory contains sample JSON and CSV files for practicing data processing with Python's standard library and third-party libraries.

## Directory Structure

```
files_for_workshops/
├── JSON/          # JSON files with various structures
├── CSV/           # CSV files with different formats
└── README.md      # This file
```

## JSON Files

### Standard Library: `json` module

The `json` module is built into Python and provides methods to work with JSON data.

**Available Files:**
- `simple_data.json` - Basic JSON object with primitive types
- `nested_structure.json` - Deeply nested JSON with multiple levels
- `array_of_objects.json` - Array containing multiple objects
- `complex_data.json` - Complex structure with employees, departments, and revenue data
- `edge_cases.json` - Edge cases: null values, empty collections, unicode, special characters

**Basic Usage:**

```python
import json

# Reading JSON
with open('JSON/simple_data.json', 'r') as f:
    data = json.load(f)

# Writing JSON
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)

# String operations
json_string = json.dumps(data, indent=2)
data_from_string = json.loads(json_string)
```

### Recommended Third-Party Libraries

#### 1. **orjson** ⭐ Recommended
Fast, correct JSON library with better performance than the standard library.

```bash
pip install orjson
```

```python
import orjson

# Reading
data = orjson.loads(json_bytes)

# Writing (returns bytes)
json_bytes = orjson.dumps(data)
```

**Advantages:**
- 2-3x faster serialization than standard `json`
- Supports datetime objects natively
- Produces compact JSON by default
- Type safety

#### 2. **ujson** (Ultra JSON)
High-performance JSON encoder/decoder.

```bash
pip install ujson
```

```python
import ujson

data = ujson.loads(json_string)
json_string = ujson.dumps(data)
```

#### 3. **jsonschema**
Validate JSON data against schemas.

```bash
pip install jsonschema
```

```python
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"}
    }
}

validate(instance=data, schema=schema)
```

#### 4. **jq** (Python bindings)
Query and manipulate JSON like the command-line `jq` tool.

```bash
pip install jq
```

```python
import jq

result = jq.compile('.employees[] | select(.department == "Engineering")').input(data).all()
```

#### 5. **pydantic**
Data validation using Python type annotations.

```bash
pip install pydantic
```

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

user = User(**json_data)
```

---

## CSV Files

### Standard Library: `csv` module

The `csv` module handles CSV file reading and writing with various dialects.

**Available Files:**
- `simple_users.csv` - Basic user data with standard comma delimiter
- `products.csv` - Product inventory with quotes in fields
- `employees.csv` - Employee records with empty fields
- `weather_data.csv` - Time-series weather data
- `edge_cases.csv` - CSV edge cases: quotes, commas, newlines in fields
- `semicolon_delimited.csv` - CSV using semicolon delimiter (common in Europe)

**Basic Usage:**

```python
import csv

# Reading CSV
with open('CSV/simple_users.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'], row['age'])

# Writing CSV
with open('output.csv', 'w', newline='') as f:
    fieldnames = ['name', 'age', 'email']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'name': 'Alice', 'age': 30, 'email': 'alice@example.com'})

# Custom delimiter
with open('CSV/semicolon_delimited.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter=';')
    data = list(reader)
```

### Recommended Third-Party Libraries

#### 1. **pandas** ⭐ Recommended
The de facto standard for data analysis in Python.

```bash
pip install pandas
```

```python
import pandas as pd

# Reading CSV
df = pd.read_csv('CSV/products.csv')

# Data manipulation
filtered = df[df['price'] > 50]
grouped = df.groupby('category')['price'].mean()

# Writing CSV
df.to_csv('output.csv', index=False)

# Reading with custom delimiter
df = pd.read_csv('CSV/semicolon_delimited.csv', delimiter=';')
```

**Advantages:**
- Powerful data manipulation and analysis
- Handles missing data elegantly
- Statistical operations
- Easy data transformation and aggregation
- Integration with visualization libraries

#### 2. **polars**
Blazingly fast DataFrame library (Rust-based).

```bash
pip install polars
```

```python
import polars as pl

df = pl.read_csv('CSV/products.csv')
result = df.filter(pl.col('price') > 50).select(['product_name', 'price'])
```

**Advantages:**
- Much faster than pandas for large datasets
- Lower memory usage
- Better type handling
- SQL-like syntax

#### 3. **csvkit**
Suite of command-line tools for working with CSV.

```bash
pip install csvkit
```

```bash
# Command line
csvstat CSV/products.csv
csvgrep -c category -m Electronics CSV/products.csv
csvsql --query "SELECT * FROM simple_users WHERE age > 30" CSV/simple_users.csv
```

**Advantages:**
- Great for quick CSV exploration
- SQL queries on CSV files
- CSV format conversion

#### 4. **tabulate**
Pretty-print tabular data.

```bash
pip install tabulate
```

```python
from tabulate import tabulate
import csv

with open('CSV/simple_users.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)
    print(tabulate(data, headers='keys', tablefmt='grid'))
```

#### 5. **pyarrow**
Fast columnar data processing (used by pandas and polars).

```bash
pip install pyarrow
```

```python
import pyarrow.csv as pa_csv

table = pa_csv.read_csv('CSV/products.csv')
df = table.to_pandas()  # Convert to pandas if needed
```

---

## Practice Exercises

### JSON Exercises
1. Load `complex_data.json` and calculate the average salary of employees in Engineering
2. Parse `array_of_objects.json` and find all products that are in stock
3. Navigate `nested_structure.json` to extract the user's city and coordinates
4. Handle the edge cases in `edge_cases.json` (null values, empty collections, unicode)

### CSV Exercises
1. Read `employees.csv` and calculate the average salary by department
2. Parse `weather_data.csv` and find the days with precipitation > 5mm
3. Handle the edge cases in `edge_cases.csv` (quotes, commas in fields, newlines)
4. Read `semicolon_delimited.csv` with the correct delimiter
5. Combine `products.csv` with inventory tracking (create your own data)

### Combined Exercises
1. Convert CSV files to JSON format
2. Convert JSON files to CSV format (flatten nested structures)
3. Compare performance of standard library vs third-party libraries
4. Build a data pipeline: CSV → process → JSON output

---

## Performance Tips

### For JSON:
- Use `orjson` for production workloads with large JSON files
- Use `json.loads()` for strings, `json.load()` for files
- Consider streaming parsers for very large files (ijson library)

### For CSV:
- Use `pandas` for complex data analysis
- Use `polars` for large datasets requiring high performance
- Always specify `newline=''` when opening CSV files in write mode
- Use `DictReader`/`DictWriter` for more readable code

---

## Additional Resources

- [Python JSON documentation](https://docs.python.org/3/library/json.html)
- [Python CSV documentation](https://docs.python.org/3/library/csv.html)
- [Pandas documentation](https://pandas.pydata.org/docs/)
- [Polars documentation](https://pola-rs.github.io/polars/)
- [Real Python CSV tutorial](https://realpython.com/python-csv/)
- [Real Python JSON tutorial](https://realpython.com/python-json/)
