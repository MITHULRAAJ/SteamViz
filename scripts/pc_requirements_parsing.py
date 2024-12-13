#pip install requests beautifulsoup4

import requests
import pandas as pd
import time

# Function to fetch data with retries
def fetch_app_details(appid, retries=3):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data[str(appid)]['success']:
                    return data[str(appid)]['data'].get('pc_requirements', {})
            else:
                print(f"Failed with status code {response.status_code}. Retrying...")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying in {2 ** attempt} seconds...")
            time.sleep(2 ** attempt)
    print(f"Failed to fetch details for AppID {appid}")
    return {}

# AppIDs to fetch
appids = [
    2778580, 570, 730, 578080, 1172470, 440, 1623730, 1063730, 2358720, 1938090,
    271590, 550, 1599340, 304930, 553850, 230410, 236390, 1245620, 105600, 291550,
    431960, 1086940, 4000, 359550, 1085660, 252490, 346110, 892970, 1091500, 945360,
    218620, 901583, 238960, 242760, 413150, 322330, 899770, 1203220, 340, 381210,
    1097150, 292030, 291480, 49520, 444090, 438100, 552990, 990080, 227300, 739630,
    272060, 620, 227940, 1517290, 1966720, 582010, 320, 1240440, 108600, 240, 1468810,
    10, 648800, 444200, 386360, 252950, 755790, 1174180, 220, 550650, 400, 250900,
    301520, 367520, 239140, 100, 814380, 417910, 433850, 251570, 1222670, 594650,
    219990, 261550, 8930, 304050, 532210, 377160, 477160, 107410, 221100, 289070,
    255710, 526870, 60, 72850, 204360, 1238810, 1811260, 96000, 632360
]

# Collect data
app_details = []
for appid in appids:
    pc_requirements = fetch_app_details(appid)

    # Debugging to check if data exists for the appid
    if not pc_requirements:
        print(f"No PC requirements found for AppID {appid}.")

    # Check for recommended, fallback to minimum if not available
    requirements = pc_requirements.get('recommended', pc_requirements.get('minimum', 'Not Available'))

    # Append to the list
    app_details.append({
        "appid": appid,
        "requirements": requirements
    })

# Convert to DataFrame and save
df = pd.DataFrame(app_details)

# Save to CSV file
output_path = 'steam_pc_requirements.csv'
df.to_csv(output_path, index=False)
print(f"Data saved to '{output_path}'")

import re
import requests
import pandas as pd
import time

# Function to fetch data with retries
def fetch_app_details(appid, retries=3):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data[str(appid)]['success']:
                    return data[str(appid)]['data'].get('pc_requirements', {})
            else:
                print(f"Failed with status code {response.status_code}. Retrying...")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying in {2 ** attempt} seconds...")
            time.sleep(2 ** attempt)
    return {}

# Function to parse requirements into individual fields
def parse_requirements(requirements):
    if not requirements:
        return {'os': None, 'cpu': None, 'gpu': None, 'ram': None, 'storage': None}

    os_match = re.search(r'<strong>OS\s*\*?:</strong>\s*([\w\s\-,®/().]+(?:\d+[/,\s]*)?[^<]*)<br>', requirements)
    cpu_match = re.search(r'<strong>Processor:</strong>\s*([\w\s\-,/.()+™@|ï»¿]+(?:\d+[.,]\d+\s*(GHz|GHz \(.*?\)|CPUs|cores|physical cores)?|or better|or equivalent performance)?[^<]*)<br>?', requirements)
    gpu_match = re.search(r'<strong>(Graphics|Video Card):</strong>\s*([\w\s\-,/.+™®@|&×;:()]+(?:\d+[.,]\d+\s*(GB|VRAM)?|Pixel Shader|OpenGL|DirectX)?[^<]*)<br>?', requirements)
    ram_match = re.search(r'<strong>Memory:</strong>\s*(\d+\s*GB\s*RAM)<br>', requirements)
    storage_match = re.search(r'<strong>(Storage|Hard Drive|Additional Notes):</strong>\s*([\w\s\-,/.+()]*?(\d+\s*(GB|MB))\s*(available\s*)?(HD\s*)?(space|at launch)?(?:[^<]*))(?:<br>|</li>)', requirements)

    storage = storage_match.group(3) if storage_match else None
    return {
        'os': os_match.group(1) if os_match else None,
        'cpu': cpu_match.group(1) if cpu_match else None,
        'gpu': gpu_match.group(2) if gpu_match else None,
        'ram': ram_match.group(1) if ram_match else None,
        'storage': storage
    }

# AppIDs to fetch
app_ids = [
    2778580, 570, 730, 578080, 1172470, 440, 1623730, 1063730, 2358720, 1938090,
    271590, 550, 1599340, 304930, 553850, 230410, 236390, 1245620, 105600, 291550,
    431960, 1086940, 4000, 359550, 1085660, 252490, 346110, 892970, 1091500, 945360,
    218620, 901583, 238960, 242760, 413150, 322330, 899770, 1203220, 340, 381210,
    1097150, 292030, 291480, 49520, 444090, 438100, 552990, 990080, 227300, 739630,
    272060, 620, 227940, 1517290, 1966720, 582010, 320, 1240440, 108600, 240, 1468810,
    10, 648800, 444200, 386360, 252950, 755790, 1174180, 220, 550650, 400, 250900,
    301520, 367520, 239140, 100, 814380, 417910, 433850, 251570, 1222670, 594650,
    219990, 261550, 8930, 304050, 532210, 377160, 477160, 107410, 221100, 289070,
    255710, 526870, 60, 72850, 204360, 1238810, 1811260, 96000, 632360
]

# Collect data
app_details = []
for appid in app_ids:
    pc_requirements = fetch_app_details(appid)
    requirements_text = pc_requirements.get('recommended', pc_requirements.get('minimum', 'Not Available'))
    parsed_data = parse_requirements(requirements_text)
    parsed_data['appid'] = appid
    app_details.append(parsed_data)

# Convert to DataFrame
df = pd.DataFrame(app_details)

# Reorder columns to make 'appid' the first column
columns = ['appid'] + [col for col in df.columns if col != 'appid']
df = df[columns]

# Save to CSV
output_path = 'parsed_steam_requirements.csv'
df.to_csv(output_path, index=False)
print(f"Data saved to '{output_path}'")

"""Working one"""

import re
import requests
import pandas as pd
import time

def fetch_app_details(appid, retries=3):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data[str(appid)]['success']:
                    return data[str(appid)]['data'].get('pc_requirements', {})
            else:
                print(f"Failed with status code {response.status_code}. Retrying...")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying in {2 ** attempt} seconds...")
            time.sleep(2 ** attempt)
    print(f"Failed to fetch details for AppID {appid}")
    return {}

# Function to parse requirements into individual fields
def parse_requirements(requirements):
    if not requirements:
        return {'os': None, 'cpu': None, 'gpu': None, 'ram': None, 'storage': None}

    os_match = re.search(r'<strong>OS\s*\*?:</strong>\s*([\w\s\-,®/().]+(?:\d+[/,\s]*)?[^<]*)<br>', requirements)
    cpu_match = re.search(r'<strong>Processor:</strong>\s*([\w\s\-,/.()+™@|ï»¿]+(?:\d+[.,]\d+\s*(GHz|GHz\s*\(.*?\)|CPUs|cores|physical cores|processor)?|or better|or equivalent performance)?[^<]*)<br>?', requirements)
    gpu_match = re.search(r'<strong>(Graphics|Video Card):</strong>\s*([\w\s\-,/.+™®@|&×;:()]+(?:\d+[.,]\d+\s*(GB|VRAM)?|Pixel Shader|OpenGL|DirectX)?[^<]*)<br>?', requirements)
    ram_match = re.search(r'<strong>Memory:</strong>\s*(\d+\s*(GB|MB)\s*RAM)<br>', requirements)
    storage_match = re.search(r'<strong>(Storage|Hard Drive|Additional Notes):</strong>\s*([\w\s\-,/.+()]*?(\d+\s*(GB|MB))\s*(available\s*)?(HD\s*)?(space|at launch)?(?:[^<]*))(?:<br>|</li>)', requirements)

    storage = storage_match.group(3) if storage_match else None

    return {
        'os': os_match.group(1) if os_match else None,
        'cpu': cpu_match.group(1) if cpu_match else None,
        'gpu': gpu_match.group(2) if gpu_match else None,
        'ram': ram_match.group(1) if ram_match else None,
        'storage': storage
    }

app_ids = [
    '1097150', '381210', '301520', '413150', '261550', '204360', '107410', '582010',
    '272060', '1240440', '1938090', '394360', '227300', '2358720', '49520', '377160',
    '431960', '359550', '291550', '945360', '570', '1172470', '1222670', '438100',
    '1174180', '60', '578080', '755790', '8930', '291480', '632360', '218620', '550',
    '739630', '1063730', '271590', '96000', '620', '444200', '72850', '1203220',
    '218230', '322330', '105600', '255710', '238960', '4000', '289070', '1238810',
    '444090', '367520', '108600', '386360', '251570', '346110', '240', '892970',
    '990080', '10', '433850', '553850', '1623730', '552990', '899770', '239140',
    '320', '730', '648800', '292030', '70', '1966720', '440', '242760', '1086940',
    '594650', '250900', '1517290', '400', '1811260', '1085660', '304930', '526870',
    '1089350', '252490', '236390', '252950', '230410', '417910', '532210', '1468810',
    '1599340', '477160', '1091500', '340', '550650', '901583', '221100', '814380',
    '304050', '1245620'
]

app_details = []
for appid in app_ids:
    pc_requirements = fetch_app_details(appid)

    if not pc_requirements:
        print(f"No PC requirements found for AppID {appid}.")

    # Check for recommended, fallback to minimum if not available
    requirements = pc_requirements.get('recommended', pc_requirements.get('minimum', 'Not Available'))

    parsed_data = parse_requirements(requirements)
    parsed_data['appid'] = appid
    app_details.append(parsed_data)

df = pd.DataFrame(app_details)

columns = ['appid'] + [col for col in df.columns if col != 'appid']
df = df[columns]

# Save to CSV
output_path = 'parsed_steam_pcrequirements.csv'
df.to_csv(output_path, index=False)
print(f"Data saved to '{output_path}'")

"""For Windows ranking"""

import pandas as pd
import re

# Define the priority order for OS ranks
os_rank_map = {
    "Windows XP": 1,
    "Windows VISTA": 2,
    "Windows 7": 3,
    "Windows 8": 4,
    "Windows 10": 5,
    "Windows 11": 6,
    "Windows Unknown": 7  # Assign the highest rank for unknown OS
}

# Function to simplify the OS value using regex
def simplify_os_with_regex(os_value):
    """
    Simplify the OS column to the lowest version mentioned using regex.
    - Matches 'xp', 'vista', '7', '8', '10', '11'.
    - Returns the lowest version found.
    """
    os_value = str(os_value).lower()  # Ensure case-insensitive matching
    # Define the order of priority (lowest to highest)
    os_keywords = ["xp", "vista", "7", "8", "10", "11"]
    matches = []

    # Check for each OS keyword in the string
    for keyword in os_keywords:
        if re.search(r'\b' + keyword + r'\b', os_value):  # Match the whole word
            matches.append(keyword)

    # If matches are found, return the lowest (first in priority order)
    if matches:
        lowest_version = matches[0]  # The order in os_keywords ensures the lowest version
        return f"Windows {lowest_version.upper()}"
    return "Windows Unknown"  # If no match is found

# Function to assign ranks based on the simplified OS
def assign_rank(simplified_os):
    """
    Assign a rank to the simplified OS value based on the predefined ranking.
    """
    return os_rank_map.get(simplified_os, os_rank_map["Windows Unknown"])

# Load the CSV file
file_path = 'FINAL_fulldata_steam.csv'  # Replace with your actual file path
df = pd.read_csv(file_path, encoding='ISO-8859-1')  # Use appropriate encoding for your file

# Simplify OS values
df['simplified_os'] = df['os'].apply(simplify_os_with_regex)

# Assign ranks based on the simplified OS
df['os_rank'] = df['simplified_os'].apply(assign_rank)

# Save the updated DataFrame to a new file
output_path = 'simplified_os_with_ranks.csv'  # Replace with your desired output path
df.to_csv(output_path, index=False)

print(f"File saved with simplified OS values and ranks at: {output_path}")

"""Preprocess os, ram, storage"""

import pandas as pd
import re

# Define the priority order for OS ranks
os_rank_map = {
    "Windows XP": 1,
    "Windows VISTA": 2,
    "Windows 7": 3,
    "Windows 8": 4,
    "Windows 10": 5,
    "Windows 11": 6,
    "Windows Unknown": 7  # Assign the highest rank for unknown OS
}

# Function to simplify the OS value using regex
def simplify_os_with_regex(os_value):
    """
    Simplify the OS column to the lowest version mentioned using regex.
    - Matches 'xp', 'vista', '7', '8', '10', '11'.
    - Returns the lowest version found.
    """
    os_value = str(os_value).lower()  # Ensure case-insensitive matching
    # Define the order of priority (lowest to highest)
    os_keywords = ["xp", "vista", "7", "8", "10", "11"]
    matches = []

    # Check for each OS keyword in the string
    for keyword in os_keywords:
        if re.search(r'\b' + keyword + r'\b', os_value):  # Match the whole word
            matches.append(keyword)

    # If matches are found, return the lowest (first in priority order)
    if matches:
        lowest_version = matches[0]  # The order in os_keywords ensures the lowest version
        return f"Windows {lowest_version.upper()}"
    return "Windows Unknown"  # If no match is found

# Function to assign ranks based on the simplified OS
def assign_rank(simplified_os):
    """
    Assign a rank to the simplified OS value based on the predefined ranking.
    """
    return os_rank_map.get(simplified_os, os_rank_map["Windows Unknown"])

# Function to convert RAM or storage to GB
def convert_to_gb(value):
    """
    Converts any value in MB to GB (dividing by 1000). Returns GB as a float.
    Assumes the input format is a string like "16 GB RAM" or "500 MB".
    """
    if pd.isna(value):
        return None  # Handle NaN values gracefully

    value = str(value).lower()  # Ensure case-insensitive matching
    match = re.search(r'(\d+)\s*(gb|mb)', value)
    if match:
        size = int(match.group(1))  # Extract the numeric value
        unit = match.group(2)  # Extract the unit (GB or MB)
        if unit == 'mb':
            return size / 1000  # Convert MB to GB
        return size  # Return GB as-is
    return None  # If no match, return None

# Load the CSV file
file_path = 'FINAL_fulldata_steam.csv'  # Replace with your actual file path
df = pd.read_csv(file_path, encoding='ISO-8859-1')  # Use appropriate encoding for your file

# Simplify OS values
df['simplified_os'] = df['os'].apply(simplify_os_with_regex)

# Assign ranks based on the simplified OS
df['os_rank'] = df['simplified_os'].apply(assign_rank)

# Convert RAM to GB
df['ram_gb'] = df['ram'].apply(convert_to_gb)

# Convert Storage to GB
df['storage_gb'] = df['storage'].apply(convert_to_gb)

# Save the updated DataFrame to a new file
output_path = 'simplified_os_with_ranks_ram_storage.csv'  # Replace with your desired output path
df.to_csv(output_path, index=False)

print(f"File saved with simplified OS values, ranks, and RAM/Storage in GB at: {output_path}")

"""For cpu"""

import pandas as pd
import re

# Load the Excel file
file_path = 'Cpualone.xlsx'  # Replace with the actual file path
df = pd.read_excel(file_path)

# Function to categorize CPU
def categorize_cpu(cpu_name):
    # Ensure the input is a string
    if not isinstance(cpu_name, str):
        return 'Other/Uncategorized'

    # Define patterns for categorization
    patterns = {
        r'i3[-\s]?(\d{4})': 'i3 {}K Series',
        r'i5[-\s]?(\d{4})': 'i5 {}K Series',
        r'i7[-\s]?(\d{4})': 'i7 {}K Series',
        r'i9[-\s]?(\d{4})': 'i9 {}K Series',
        r'ryzen\s?(\d)\s?(\d{3,4})': 'Ryzen {} {}K Series',
        r'fx[-\s]?(\d{4})': 'FX {}K Series',
        r'athlon\s?(\d{4})': 'Athlon {}K Series',
        r'a(\d[-\s]?\d{3,4})': 'AMD A{} Series',
        r'r[\s-]?series': 'AMD R Series',
        r'r[\s-]?(\d{4})': 'AMD R{} Series',
        r'core\s?2': 'Core 2 Series',
        r'pentium': 'Pentium Series',
        r'dual\s?core': 'Dual Core Series',
        r'quad\s?core': 'Quad Core Series'
    }

    categories = []  # To hold multiple matches

    # Check for patterns and collect all matches
    for pattern, category_format in patterns.items():
        matches = re.finditer(pattern, cpu_name, re.IGNORECASE)
        for match in matches:
            if 'ryzen' in pattern and match.lastindex >= 2:
                categories.append(category_format.format(match.group(1), match.group(2)))
            elif match.lastindex and match.group(1):  # Intel/AMD pattern with series
                categories.append(category_format.format(match.group(1)))
            else:
                categories.append(category_format)

    # Join all found categories
    return ', '.join(categories) if categories else 'Other/Uncategorized'

# Apply the categorization function
df['Category'] = df['cpu'].apply(categorize_cpu)

# Save the updated DataFrame to a new Excel file
output_path = 'Categorized_CPU_with_Both_Intel_AMD.xlsx'
df.to_excel(output_path, index=False)
print(f"Categorized data saved to '{output_path}'")

import pandas as pd

# Define the CPU list in order of ranking
cpu_order = [
    "Intel Core i5 or AMD equivalent", "Intel Core i3-4170 or AMD FX-8300 or higher",
    "Intel Dual Core or better with SSE2 support or equivalent AMD family", "2 Ghz",
    "Intel Core i5-9600K / AMD Ryzen 5 3600X", "Intel Core 2 Duo 2GHz+ or better",
    "Intel Dual-Core 2.4 GHz or AMD Dual-Core Athlon 2.5 GHz",
    "Intel Core i7 3770 or Core i3 8350 or Core i3 9350F / AMD Ryzen 5 1500X or Ryzen 5 3400G",
    "1.6Ghz", "AMD Ryzen 7 3700X or Intel i7-9700k", "AMD Ryzen 5 1600X or Intel Core i7-6700K",
    "Intel Core i5 2500K | AMD Ryzen 3 2200G", "Intel Core i5-9600 or AMD Ryzen 5 3600 or similar",
    "Intel Core i7-9700 / AMD Ryzen 5 5500", "2.3 GHz Quad Core processor",
    "Intel Core i7 4790 3.6 GHz/AMD FX-9590 4.7 GHz or equivalent",
    "2.0 GHz Intel i7 or equivalent", "AMD Ryzen 3 1200 @ 3.1 GHz, Intel Core i5-4590 @ 3.3 GHz, or better",
    "Intel core i3-4330", "Dual core from Intel or AMD at 2.8 GHz", "Ryzen 5 CPU or Equivalent",
    "Intel core i5 (4 cores), AMD Ryzen 5 or better", "Intel i5-4590 / AMD FX 8350 equivalent or greater",
    "Intel Core i7-4770K / AMD Ryzen 5 1500X", "800 mhz processor",
    "Intel Core i5-6600K / AMD Ryzen 5 1600", "Intel i5 2500(4 Core, 3.3HGz) or equivalent",
    "1.8 GHz Quad Core CPU", "Core i5 3470 / AMD Athlon 240GE",
    "Intel Core i5-4670K / AMD Ryzen 5 1500X", "2.3 GHz Intel Quad Core Processor",
    "Intel core 2 duo 2.4GHz", "Intel Core i5-10600 / AMD Ryzen 5 3600",
    "Intel Core i7-10700K @ 3.80Ghz / AMD Ryzen 5 3600X",
    "Intel Core i5 3470 @ 3.2GHz (4 CPUs) / AMD X8 FX-8350 @ 4GHz (8 CPUs)",
    "1.5 GHz equivalent or higher processor", "3.0 GHz P4, Dual Core 2.0 (or higher) or AMD64X2 (or higher)",
    "2 GHz", "Quad-core Intel or AMD CPU", "Intel i7 7th generation or equivalent",
    "Intel i5 6600K or higher / AMD Ryzen 5 1600 or higher", "1.7+ GHz or better",
    "Dual Core 3.0 Ghz", "Intel Core I7 2700K  |   AMD Ryzen 7 2700X",
    "Quad core 3.2GHz x64-compatible", "2.5 GHz Processor or better",
    "Fourth Generation Intel Core i5 2.5 Ghz or AMD FX8350 4.0 Ghz or greater",
    "AMD Ryzen 3 1300X/Intel Core i7 4790", "Intel Core i5-750, 2.67 GHz / AMD Phenom II X4 965, 3.4 GHz",
    "Intel Core i5", "Intel 2.77GHz Quad-core", "Intel Core i5 or AMD Phenom II X3, 2.8 GHz",
    "3.2 Ghz Quad Core CPU or faster", "Intel Core i5-2400/AMD FX-8320 or better",
    "Pentium 4 processor (3.0GHz, or better)", "i5 3GHz or Ryzen 5 3GHz",
    "Intel Core i7-8700 (3.2Ghz) or AMD Ryzen 5 3600 (3.6 Ghz)", "Intel Core i5-6600K / AMD Ryzen 5 1600",
    "Intel Core i7-9700K or AMD Ryzen 7 3700X", "i9-9900K 3.6 GHz 8 Core",
    "Intel Core i5-10400 2.9GHz,  AMD Ryzen 5 3600 3.6 GHz", "Intel Core i5 6500 or AMD Ryzen 3 1200",
    "Intel Core i5-4670K @3.4 GHz / AMD FX-8350 @4.0 GHz", "2.4 GHz Processor",
    "4 hardware CPU threads - Intel Core i5 750 or higher", "Intel Core i5-6600 3.3GHz or similar",
    "Intel Core i5-7400 / Ryzen 5 1600", "Intel Core i5-7400 CPU @ 3.00GHz",
    "Quad Core Processor", "Intel i7 8700K / AMD Ryzen 5 3600",
    "Intel i7 8700 / AMD Ryzen 5 2700", "2.4 GHz Quad Core 2.0 (or higher)",
    "AMD Ryzen 7 2700X, Intel Core i7 4790", "Intel Core i7 6700 or AMD Ryzen 7 2700X",
    "Processor Intel Core i5 2400 3.4 GHz or i5 7400 3.5 GHz / AMD Ryzen R5 1600X 3.6 GHz",
    "4 GHz", "Ryzen 5 5600X or i5-12400 or equivalent performance, 6 physical cores minimum",
    "Intel Core i5-4430 @ 3 GHz / AMD FX-8370 @ 3.4 GHz or better",
    "Intel Core i7-4790K / AMD Ryzen 5 2600 or better", "Intel Core i5 or Ryzen 5 3600 or better",
    "3.0+ GHz Quad core", "Intel Core i7 860, Intel Core i5 750, or AMD FX-4100 (SSE 4.2 support required)",
    "Intel core 2 duo 2.4GHz", "Intel Core i5 3470, (3.20 Ghz) or AMD FX-8350, (4.00 Ghz)",
    "2.50GHz", "Intel i5 or AMD Ryzen 5",
    "Intel Core2 Quad Q9300 (4 * 2500) or equivalent | AMD A10-5800K APU (4*3800)",
    "Core i7-12700 or Ryzen 7 7800X3D", "Pentium 4 2.4GHz or AMD 2800+ Processor",
    "Intel Core i3-4170 / AMD FX-8300",
    "Intel Core 2 Duo 1.8GHz, AMD Athlon X2 64 2.4GHz",
    "Intel Core i5-6600K or AMD R5 1600X", "Intel Core i5-2500K | AMD Ryzen 5 1400",
    "Intel Core i5-2XXX @ 2.0GHz / AMD Phenom II X4 @ 2.6GHz",
    "Intel Core I7-8700K or AMD Ryzen 5 3600X"
]

# Load the data
file_path = 'Categorized_CPU_with_Both_Intel_AMD.xlsx'  # Replace with your file path
df = pd.read_excel(file_path)

# Create a ranking dictionary
ranking = {cpu: rank for rank, cpu in enumerate(cpu_order, start=1)}

# Map the ranking to the 'cpu' column
df['Rank'] = df['cpu'].map(ranking)

# Save the updated DataFrame
output_file_path = 'Ranked_CPUs.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Rank column added and saved to {output_file_path}.")

import pandas as pd

def rank_processors(processor_list):
    ranked = []
    for entry in processor_list:
        intel, ryzen = None, None

        # Handle Intel and Ryzen extraction
        if "i" in entry:  # Intel processor exists
            intel = entry.split(",")[0].strip()
        if "Ryzen" in entry:  # Ryzen processor exists
            ryzen = entry.split(",")[1].strip() if "," in entry else None

        # Add entry as a tuple
        ranked.append((intel, ryzen, entry))

    # Sort by Intel first, then Ryzen
    ranked.sort(key=lambda x: (x[0] or "", x[1] or ""))
    return [entry[2] for entry in ranked]

def assign_ranks_to_excel(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Extract the CPU category column
    cpu_categories = df['Category'].tolist()

    # Rank the processors using the custom logic
    ranked_processors = rank_processors(cpu_categories)

    # Create a mapping of processor category to rank
    rank_mapping = {processor: rank + 1 for rank, processor in enumerate(ranked_processors)}

    # Assign ranks to the original DataFrame
    df['Rank'] = df['Category'].map(rank_mapping)

    # Save the ranked DataFrame to a new Excel file
    df.to_excel(output_file, index=False)
    print(f"File with ranks assigned saved to {output_file}")

# File paths
input_file_path = 'Categorized_CPU_with_Both_Intel_AMD.xlsx'
output_file_path = 'Categorized_CPU_with_Proper_Ranks.xlsx'

# Assign ranks and save
assign_ranks_to_excel(input_file_path, output_file_path)

"""For gpu"""

import pandas as pd
import re

# Load GPU data
file_path = 'gpualone.xlsx'  # Replace with your file path
df = pd.read_excel(file_path)

# Function to categorize GPUs and extract all relevant GPUs
def categorize_gpu_all(gpu_name):
    if pd.isna(gpu_name):
        return "Other/Uncategorized"

    gpu_name = gpu_name.lower()

    # Specific categorization for DirectX and Video Memory
    if "directx" in gpu_name:
        directx_versions = re.findall(r"directx\s?(version\s?\d+|\d+(\.\d+)?(c)?)", gpu_name)
        directx_categories = [f"DirectX {v[0].capitalize().replace('Directx', 'DirectX')}" for v in directx_versions]
        if directx_categories:
            return ", ".join(directx_categories)

    if "graphics card" in gpu_name or "video card" in gpu_name or "video memory" in gpu_name:
        return "Generic Graphics Card / Video Memory"

    # NVIDIA and AMD patterns
    nvidia_pattern = r"(gtx|rtx|geforce|quadro|tesla|nvidia)\s?(\d+)"
    amd_pattern = r"(radeon|rx|hd|firepro|vega|ati)\s?(\d+)"
    intel_pattern = r"(intel)\s?(hd\s?\d+|iris|arc\s?[a-z]?\d+)"

    nvidia_matches = re.findall(nvidia_pattern, gpu_name)
    amd_matches = re.findall(amd_pattern, gpu_name)
    intel_matches = re.findall(intel_pattern, gpu_name)

    # Construct categories from matches
    categories = []
    for match in nvidia_matches:
        if "geforce" in match[0] or "nvidia" in match[0]:
            categories.append(f"Nvidia GeForce {match[1]} Series")
        else:
            categories.append(f"Nvidia {match[0].upper()} {match[1]} Series")

    for match in amd_matches:
        categories.append(f"AMD {match[0].upper()} {match[1]} Series")

    for match in intel_matches:
        categories.append(f"Intel {match[1].capitalize()} Series")

    return ", ".join(categories) if categories else "Other/Uncategorized"

# Apply the function to extract all GPU specifications
df['GPU Category'] = df['gpu'].apply(categorize_gpu_all)

# Save the updated DataFrame to a new Excel file
output_path = 'Standardized_Multi_Categorized_GPU.xlsx'
df.to_excel(output_path, index=False)
print(f"GPU data categorized with multiple matches saved to {output_path}")

import pandas as pd

# Define GPU categories and ranks
gpu_rankings = {
    "Ultimate GPUs": 8,
    "Very High-End GPUs": 7,
    "High-End GPUs": 6,
    "Mid-Range GPUs": 5,
    "Lower Mid-Range GPUs": 4,
    "Entry-Level GPUs": 3,
    "Legacy GPUs": 2,
    "Generic/Unspecified GPUs": 1
}

# Map GPUs to their categories
gpu_categories = {
    "Ultimate GPUs": [7
        "Nvidia RTX 3060 Series, AMD RX 6600 Series",
    ],
    "Very High-End GPUs": [6
        "Nvidia RTX 2070 Series, AMD RX 5700 Series",
        "Nvidia RTX 2060 Series, AMD RX 5700 Series, Intel Arc a750 Series",
        "AMD VEGA 56 Series"
    ],
    "High-End GPUs": [5
        "Nvidia GTX 1080 Series, AMD RX 5700 Series, Intel Arc a770 Series",
        "Nvidia GTX 1070 Series, AMD RX 480 Series",
        "Nvidia GTX 1060 Series, Nvidia GTX 1650 Series, AMD RX 480 Series, AMD RX 570 Series",
        "Nvidia GTX 970 Series, AMD RX 570 Series",
        "Nvidia GTX 1070 Series, AMD RX 480 Series",
        "Nvidia GTX 1060 Series, Nvidia GTX 1650 Series, AMD RX 480 Series, AMD RX 570 Series",
        "Nvidia GTX 970 Series, Nvidia GTX 1060 Series",
    ],
    "Mid-Range GPUs": [4
        "Nvidia GTX 1660 Series, AMD RX 5600 Series",
        "Nvidia GTX 960 Series, AMD RX 560 Series, Intel Arc a380 Series"
    ],
    "Lower Mid-Range GPUs": [3
        "Nvidia GTX 660 Series, AMD HD 7870 Series",
        "Nvidia GTX 770 Series, AMD RX 570 Series",
        "Nvidia GTX 650 Series, AMD HD 7750 Series",
    ],
    "Entry-Level GPUs": [2
        "Nvidia GTX 580 Series, AMD RX 560 Series",
        "Nvidia GTX 560 Series, AMD HD 5850 Series",
        "Nvidia GTX 470 Series, AMD HD 6970 Series"
        "Nvidia GTX 560 Series, AMD HD 5850 Series",
        "Nvidia GTX 470 Series, AMD HD 6970 Series",
    ],
    "Legacy GPUs": [1
        "Nvidia GeForce 9800 Series, AMD HD 5670 Series",
        "Nvidia GeForce 8600 Series, AMD HD 2600 Series",
        "Nvidia GeForce 9800 Series, AMD HD 5670 Series",
        "Nvidia GeForce 8600 Series, AMD HD 2600 Series",
        "AMD HD 5450 Series",
    ],
    "Generic/Unspecified GPUs": [0
        "Generic Graphics Card / Video Memory",
        "Other/Uncategorized"
    ]
}

# Function to categorize GPUs based on the mapping
def categorize_gpu(gpu_name):
    for category, gpu_list in gpu_categories.items():
        if any(gpu in gpu_name for gpu in gpu_list):
            return category
    return "Generic/Unspecified GPUs"

# Read the Excel file
file_path = "/content/Standardized_Multi_Categorized_GPU.xlsx"  # Replace with your actual file path
df = pd.read_excel(file_path)

# Ensure the third column is named "GPU Name" and add "Category" and "Rank" columns
df.rename(columns={df.columns[2]: "GPU Name"}, inplace=True)
df["Category"] = df["GPU Name"].apply(categorize_gpu)
df["Rank"] = df["Category"].map(gpu_rankings)

# Save the result to a new Excel file
output_file_path = "categorized_ranked_gpus.xlsx"
df.to_excel(output_file_path, index=False)

print(f"GPU categorization and ranking completed. The updated data has been saved to {output_file_path}.")