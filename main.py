from google.oauth2 import service_account
from googleapiclient.discovery import build

def validate_doc(file_id, service_account_file='service_account.json', output_file='output.txt'):
    """
    Validates a Google Doc for:
    - Duplicate tags (case-insensitive)
    - Invalid characters in Filter Option values: normal comma (,) or parentheses ()
    Returns: (is_valid: bool, issues: list[str])
    """
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    try:
        content = service.files().export_media(
            fileId=file_id, mimeType='text/plain').execute()
    except Exception as e:
        return False, [f"❌ Failed to download document: {e}"]

    with open(output_file, 'wb') as f:
        f.write(content)

    text = content.decode('utf-8')
    lines = text.splitlines()

    issues = []
    seen_tags = set()
    current_product = None
    in_filter_block = False

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line and not any(line.lower().startswith(prefix) for prefix in [
            "required information", "row", "allowed", "category",
            "tags", "variation type", "filter option"
        ]):
            current_product = line
            in_filter_block = False

        if "tags (comma" in line.lower():
            if i + 1 < len(lines):
                tag_line = lines[i + 1].strip()
                tags = [t.strip().lower() for t in tag_line.split(',') if t.strip()]
                for tag in tags:
                    if tag in seen_tags:
                        issues.append(f"❌ Duplicate tag '{tag}' found in '{current_product}' (line {i+2})")
                    else:
                        seen_tags.add(tag)
            i += 2
            continue

        if line.lower().startswith("filter option:"):
            in_filter_block = True
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if not next_line or any(next_line.lower().startswith(k) for k in [
                    "required information", "row", "allowed", "category",
                    "tags", "variation type", "filter option"]):
                    in_filter_block = False
                    break

                if ',' in next_line and '‚' not in next_line:
                    issues.append(f"❌ INVALID COMMA in Filter Option under '{current_product}': '{next_line}' (line {i+1})")
                if '(' in next_line or ')' in next_line:
                    issues.append(f"❌ INVALID PARENTHESIS in Filter Option under '{current_product}': '{next_line}' (line {i+1})")
                i += 1
            continue

        i += 1

    return len(issues) == 0, issues

# Example usage
if __name__ == "__main__":
    FILE_ID = 'your-google-doc-file-id'  # Replace with your own file ID
    is_valid, problems = validate_doc(FILE_ID)
    if is_valid:
        print("✅ All checks passed.")
    else:
        print("❌ Issues found:")
        for p in problems:
            print(p)
