import os
import json
from pathlib import Path
from datetime import date, datetime # 导入 datetime 和 date
from mofa.utils.files.read import read_yaml
from packaging.version import Version, InvalidVersion

# Root directory: Replace with your local top-level path where OpenAPI specs are stored
ROOT_DIR = Path('/Users/chenzi/project/github/openapi-directory/APIs')

# Define output directory for processed APIs and errors
OUTPUT_DIR = Path('./apis')
ERROR_LOG_PATH = OUTPUT_DIR / 'errors.json'


def find_latest_spec(root: Path):
    """
    Finds the latest OpenAPI/Swagger spec (.yaml) for each service
    within the given root directory based on semantic versioning.
    Returns a dictionary mapping service names to (version, path).
    """
    latest_specs = {}
    for service_dir in root.iterdir():
        if not service_dir.is_dir():
            continue

        best_ver = None
        best_path = None

        # Iterate through version subdirectories
        for version_dir in service_dir.iterdir():
            if not version_dir.is_dir():
                continue
            try:
                ver = Version(version_dir.name)
            except InvalidVersion:
                # Skip if not a valid semantic version
                continue

            # Look for .yaml files in this version directory
            for fname in ('openapi.yaml', 'swagger.yaml'):
                candidate = version_dir / fname
                if candidate.exists():
                    if best_ver is None or ver > best_ver:
                        best_ver = ver
                        best_path = candidate

        if best_path:
            latest_specs[service_dir.name] = (str(best_ver), str(best_path))

    return latest_specs


def resolve_ref(ref_path, full_data):
    """
    Resolves a JSON reference path within the full data structure.
    Only internal references are handled for simplicity (those starting with '#/').
    """
    if not ref_path.startswith('#/'):
        return None  # External references or malformed refs are not resolved by this simple function

    path_parts = ref_path[2:].split('/')
    current = full_data
    for part in path_parts:
        # Handle cases where part might be a list index (e.g., #/array/0)
        try:
            if isinstance(current, list) and part.isdigit():
                current = current[int(part)]
            elif isinstance(current, dict):
                current = current[part]
            else:
                return None # current is not a dict or list for traversal
        except (KeyError, IndexError):
            return None  # Path segment not found
    return current


def _extract_api_info_openapi3(swagger_data, file_path=""):
    """
    Extracts API path, method, summary, description, parameters, and responses
    from an OpenAPI 3.0.0 data structure (dictionary).
    Includes building the full URL for each API based on the 'servers' object.
    """
    apis_info = []

    # Get base URL from 'servers' array (OpenAPI 3.0.0)
    # We'll use the URL from the first server object found.
    base_url = None
    servers = swagger_data.get('servers')
    if servers and isinstance(servers, list) and len(servers) > 0:
        base_url = servers[0].get('url')
        if base_url and base_url.endswith('/'):
            # Remove trailing slash if it's not just '/' to avoid double slashes later
            if base_url != '/':
                base_url = base_url.rstrip('/')

    if not base_url:
        # print(f"Warning for {file_path}: 'servers' or a valid 'url' not found in OpenAPI 3.0 data. Full URLs may not be accurate.")
        base_url = ""  # An empty base_url will result in relative paths only for now

    for path, path_data in swagger_data.get('paths', {}).items():
        # Construct the full URL for the API
        api_path = path
        # Ensure path starts with a slash if base_url is not empty and path itself doesn't start with one
        if base_url and not api_path.startswith('/'):
            api_path = '/' + api_path

        full_url = f"{base_url}{api_path}"

        # Clean up potential double slashes, but be careful with protocol part (e.g., http://)
        full_url = full_url.replace('://', '###TEMP###').replace('//', '/').replace('###TEMP###', '://')

        for method, method_data in path_data.items():
            # Filter for common HTTP methods (lowercase in OpenAPI paths)
            if method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head', 'trace']:
                api_info = {
                    'full_url': full_url,
                    'relative_path': path,
                    'method': method.upper(),
                    'summary': method_data.get('summary'),
                    'description': method_data.get('description'),
                    'parameters': [],
                    'responses': []
                }

                # Extract parameters for the current API operation
                for param_def in method_data.get('parameters', []):
                    if '$ref' in param_def:
                        ref_resolved = resolve_ref(param_def['$ref'], swagger_data)
                        if ref_resolved:
                            param_info = {
                                'name': ref_resolved.get('name'),
                                'in': ref_resolved.get('in'),
                                'description': ref_resolved.get('description'),
                                'required': ref_resolved.get('required', False),
                                'type': None  # Initialise, will be populated from schema
                            }
                            if 'schema' in ref_resolved:
                                param_info['schema'] = ref_resolved['schema']
                                if ref_resolved['schema'].get('type'):
                                    param_info['type'] = ref_resolved['schema']['type']
                                if 'enum' in ref_resolved['schema']:
                                    param_info['enum'] = ref_resolved['schema']['enum']
                        else:
                            param_info = {'name': 'UNKNOWN (Ref Not Found)', 'ref': param_def['$ref']}
                    else:
                        param_info = {
                            'name': param_def.get('name'),
                            'in': param_def.get('in'),
                            'description': param_def.get('description'),
                            'required': param_def.get('required', False),
                            'type': None
                        }
                        if 'schema' in param_def:
                            param_info['schema'] = param_def['schema']
                            if param_def['schema'].get('type'):
                                param_info['type'] = param_def['schema']['type']
                            if 'enum' in param_def['schema']:
                                param_info['enum'] = param_def['schema']['enum']

                    api_info['parameters'].append(param_info)

                # Extract responses for the current API operation
                for status_code, response_def in method_data.get('responses', {}).items():
                    if '$ref' in response_def:
                        ref_resolved = resolve_ref(response_def['$ref'], swagger_data)
                        if ref_resolved:
                            response_info = {
                                'status_code': status_code,
                                'description': ref_resolved.get('description'),
                                'content': ref_resolved.get('content')  # OpenAPI 3.0 uses 'content'
                            }
                        else:
                            response_info = {'status_code': status_code, 'description': 'UNKNOWN (Ref Not Found)',
                                             'ref': response_def['$ref']}
                    else:
                        response_info = {
                            'status_code': status_code,
                            'description': response_def.get('description'),
                            'content': response_def.get('content')
                        }
                    api_info['responses'].append(response_info)

                apis_info.append(api_info)
    return apis_info


def _extract_api_info_swagger2(swagger_data, file_path=""):
    """
    Extracts API path, method, summary, description, parameters, and responses
    from a Swagger 2.0 data structure (dictionary).
    Includes building the full URL for each API based on 'schemes', 'host', and 'basePath'.
    """
    apis_info = []

    # Get base URL components from Swagger 2.0
    scheme = swagger_data.get('schemes', ['https'])[0]  # Default to https
    host = swagger_data.get('host')
    base_path = swagger_data.get('basePath', '/')  # Default to '/'

    if not host:
        # print(f"Warning for {file_path}: 'host' not found in Swagger 2.0 data. Full URLs may not be accurate.")
        return []

    # Ensure base_path starts and ends with a single slash (unless it's just '/')
    if not base_path.startswith('/'):
        base_path = '/' + base_path
    if not base_path.endswith('/') and base_path != '/':
        base_path = base_path + '/'

    for path, path_data in swagger_data.get('paths', {}).items():
        cleaned_path = path
        if cleaned_path.startswith('/'):
            cleaned_path = cleaned_path[1:]

        full_url = f"{scheme}://{host}{base_path}{cleaned_path}"
        # Clean up double slashes if any, except for the protocol part
        full_url = full_url.replace('://', '###TEMP###').replace('//', '/').replace('###TEMP###', '://')

        for method, method_data in path_data.items():
            if method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                api_info = {
                    'full_url': full_url,
                    'relative_path': path,
                    'method': method.upper(),
                    'summary': method_data.get('summary'),
                    'description': method_data.get('description'),
                    'parameters': [],
                    'responses': []
                }

                # Extract parameters
                for param_def in method_data.get('parameters', []):
                    if '$ref' in param_def:
                        ref_resolved = resolve_ref(param_def['$ref'], swagger_data)
                        if ref_resolved:
                            param_info = {
                                'name': ref_resolved.get('name'),
                                'in': ref_resolved.get('in'),
                                'description': ref_resolved.get('description'),
                                'required': ref_resolved.get('required', False),
                                'type': ref_resolved.get('type')
                            }
                            if 'enum' in ref_resolved:
                                param_info['enum'] = ref_resolved['enum']
                            if 'schema' in ref_resolved:
                                param_info['schema'] = ref_resolved['schema']
                        else:
                            param_info = {'name': 'UNKNOWN (Ref Not Found)', 'ref': param_def['$ref']}
                    else:
                        param_info = {
                            'name': param_def.get('name'),
                            'in': param_def.get('in'),
                            'description': param_def.get('description'),
                            'required': param_def.get('required', False),
                            'type': param_def.get('type')
                        }
                        if 'enum' in param_def:
                            param_info['enum'] = param_def['enum']
                        if 'schema' in param_def:
                            param_info['schema'] = param_def['schema']
                    api_info['parameters'].append(param_info)

                # Extract responses
                for status_code, response_def in method_data.get('responses', {}).items():
                    if '$ref' in response_def:
                        ref_resolved = resolve_ref(response_def['$ref'], swagger_data)
                        if ref_resolved:
                            response_info = {
                                'status_code': status_code,
                                'description': ref_resolved.get('description'),
                                'schema': ref_resolved.get('schema')
                            }
                        else:
                            response_info = {'status_code': status_code, 'description': 'UNKNOWN (Ref Not Found)',
                                             'ref': response_def['$ref']}
                    else:
                        response_info = {
                            'status_code': status_code,
                            'description': response_def.get('description'),
                            'schema': response_def.get('schema')
                        }
                    api_info['responses'].append(response_info)

                apis_info.append(api_info)
    return apis_info


def extract_api_info(swagger_data, file_path=""):
    """
    Detects the OpenAPI/Swagger specification version and dispatches
    to the appropriate extraction function.
    """
    if 'openapi' in swagger_data and swagger_data['openapi'].startswith('3.'):
        print(f"Detected OpenAPI 3.0.x specification for {file_path.name}.")
        return _extract_api_info_openapi3(swagger_data, file_path)
    elif 'swagger' in swagger_data and swagger_data['swagger'] == '2.0':
        print(f"Detected Swagger 2.0 specification for {file_path.name}.")
        return _extract_api_info_swagger2(swagger_data, file_path)
    else:
        raise ValueError(f"Unknown or unsupported OpenAPI/Swagger specification version for {file_path.name}.")


def load_error_log():
    """Loads existing error log or returns an empty list."""
    if ERROR_LOG_PATH.exists():
        with open(ERROR_LOG_PATH, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # Return empty if file is malformed
    return []


def save_error_log(errors):
    """Saves the error log to errors.json."""
    with open(ERROR_LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(errors, f, indent=4, ensure_ascii=False)

# --- NEW HELPER FUNCTION ---
def json_serial_date_handler(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()  # Convert date/datetime objects to ISO 8601 strings
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

# --- MODIFIED MAIN BLOCK ---
if __name__ == '__main__':
    print(f"Searching for OpenAPI/Swagger specs in: {ROOT_DIR}\n")
    specs = find_latest_spec(ROOT_DIR)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load existing errors
    all_errors = load_error_log()
    processed_count = 0
    skipped_count = 0

    if not specs:
        print(f"No API specifications found in {ROOT_DIR}. Please check the path and directory structure.")
    else:
        print(f"Found {len(specs)} latest API specifications.")

        for service_name, (version, spec_path_str) in specs.items():
            target_api_path = Path(spec_path_str)

            print(f"\nProcessing {service_name} (version {version}) from: {target_api_path}")

            try:
                # Load the data from the YAML file
                data = read_yaml(target_api_path)

                if data:
                    # Extract the information
                    extracted_apis = extract_api_info(data, target_api_path)

                    if extracted_apis:
                        # Define output JSON filename based on service name
                        output_filename = OUTPUT_DIR / f"{service_name}.json"
                        with open(output_filename, 'w', encoding='utf-8') as f:
                            # --- IMPORTANT CHANGE HERE ---
                            json.dump(extracted_apis, f, indent=4, ensure_ascii=False, default=json_serial_date_handler)
                        print(f"Successfully extracted and saved API info for '{service_name}' to {output_filename}")
                        processed_count += 1
                    else:
                        error_reason = "No API operations found or extracted after parsing."
                        all_errors.append({
                            'file_path': str(target_api_path),
                            'service_name': service_name,
                            'error_reason': error_reason
                        })
                        print(f"Skipped '{service_name}': {error_reason}")
                        skipped_count += 1
                else:
                    error_reason = "Failed to load YAML data (file might be empty or malformed)."
                    all_errors.append({
                        'file_path': str(target_api_path),
                        'service_name': service_name,
                        'error_reason': error_reason
                    })
                    print(f"Skipped '{service_name}': {error_reason}")
                    skipped_count += 1
            except Exception as e:
                error_reason = f"An error occurred during processing: {e}"
                all_errors.append({
                    'file_path': str(target_api_path),
                    'service_name': service_name,
                    'error_reason': error_reason
                })
                print(f"Skipped '{service_name}': {error_reason}")
                skipped_count += 1

            print("\n" + "=" * 80 + "\n")  # Separator for better readability

    # Save the accumulated errors
    if all_errors:
        save_error_log(all_errors)
        print(f"\nCompleted processing. Total processed: {processed_count}, Skipped (with errors): {skipped_count}")
        print(f"Errors logged to: {ERROR_LOG_PATH}")
    else:
        print(f"\nCompleted processing. All {processed_count} APIs processed successfully. No errors found.")