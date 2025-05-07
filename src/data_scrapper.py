import requests
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm
from urllib.parse import urljoin

def scrape_sklearn_api_reference(base_url="https://scikit-learn.org/stable/api/index.html"):
    """
    Scrapes the Scikit-Learn API reference page and extracts the structured 
    list of sections and subsections along with their links.

    Parameters:
        base_url (str): The URL of the Scikit-Learn API reference page.

    Returns:
        dict: A dictionary containing structured API references.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        print("Error: Could not fetch the webpage! Check the URL and try again.")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    sidebar = soup.find("nav") or soup.find("div", class_="toctree-wrapper compound")

    if sidebar is None:
        print("Error: Could not find the sidebar! Check the page structure.")
        return None

    print("Sidebar found. Extracting data...")

    api_reference = {}

    for item in soup.find_all("li", class_="toctree-l1"):
        section_link = item.find("a", class_="reference internal")
        if section_link:
            section_name = section_link.text.strip()
            section_href = urljoin(base_url, section_link["href"])
            api_reference[section_name] = {"link": section_href, "subsections": {}}

            details = item.find("ul")
            if details:
                for sub_item in details.find_all("li", class_="toctree-l2"):
                    sub_link = sub_item.find("a", class_="reference internal")
                    if sub_link:
                        sub_name = sub_link.text.strip()
                        sub_href = urljoin(base_url, sub_link["href"])
                        api_reference[section_name]["subsections"][sub_name] = sub_href

    # Save to a JSON file
    with open("scikit-learn-api-reference.json", "w") as f:
        json.dump(api_reference, f, indent=4)

    print("Data saved to 'scikit-learn-api-reference.json'.")
    return api_reference

def extract_class_signature(url):
    # Fetch the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the class definition
    class_section = soup.find("dt", class_="sig sig-object py")
    
    if not class_section:
        return "Class definition not found."

    # Extract class name
    class_name = class_section.find("span", class_="sig-name").text.strip()
    
    # Extract class path (e.g., sklearn.cluster)
    class_path = class_section.find("span", class_="sig-prename")
    class_path = class_path.text.strip() if class_path else ""

    # Extract parameters
    params = []
    for param in class_section.find_all("em", class_="sig-param"):
        param_text = param.text.strip().replace("\n", "")
        params.append(param_text)

    # Format the output
    class_signature = f"class {class_path}{class_name}({', '.join(params)})"
    return class_signature

def extract_example_code(url):
    # Fetch the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the example section
    example_section = soup.find("div", class_="doctest highlight-default notranslate")
    
    if not example_section:
        return "Example code not found."

    # Extract the code text
    code_lines = example_section.find("pre").text

    # Remove '>>>' and '...' from the extracted code
    cleaned_code = "\n".join(
        line[4:] if line.startswith((">>> ", "... ")) else line 
        for line in code_lines.split("\n")
    )

    return cleaned_code.strip()

# Example usage
if __name__ == "__main__":
    api_reference = scrape_sklearn_api_reference()
    # iterate in json and save the data
    for section_name, section_data in tqdm(api_reference.items()):
        for subsection_name, subsection_link in section_data["subsections"].items():
            # Extract class signature and example
            class_signature = extract_class_signature(subsection_link)
            example_code = extract_example_code(subsection_link)
            # add class and example to the json
            section_data["subsections"][subsection_name] = {
                "link": subsection_link,
                "class_signature": class_signature, 
                "example_code": example_code
            }
        
    # Save the updated data to a JSON file
    with open("data/scikit-learn-api-reference.json", "w") as f:
        json.dump(api_reference, f, indent=4)