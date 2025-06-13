# 🧪 Google Docs Product Validator

This Python script connects to a Google Doc, parses its structure, and performs validation checks on **tags** and **filter option values**.

## ✅ What It Does

- ✔️ Detects **duplicate tags** across the document (case-insensitive)
- ❌ Flags any **filter option values** containing:
  - Parentheses: `(` or `)`
  - Normal commas: `,` (only allows `‚`)

## 📁 How It Works

1. Authenticates using a Google service account
2. Downloads the Google Doc as text
3. Parses lines to find:
   - `Tags (comma separated)` blocks
   - `Filter Option:` blocks
4. Returns clear issues found

## 📌 Example Issue Output

```text
❌ Duplicate tag 'craft foam' found in 'Arts & Crafts'
❌ INVALID COMMA in Filter Option under 'Paint Type': 'Acrylic, Water'
❌ INVALID PARENTHESIS in Filter Option under 'Material': 'Faux Mink ((('
```

## 🛠 Requirements

```bash
pip install google-api-python-client google-auth
```

## 🔐 Note

This repo contains no real client data and uses placeholder file IDs and dummy text.
