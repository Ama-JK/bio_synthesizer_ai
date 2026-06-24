import requests

def get_chemical_info(plant_chemical):
    # Convert the name to lowercase for PubChem API compatibility
    chemical_name = plant_chemical.strip().lower()
    print(f"🔍 Searching PubChem for '{chemical_name}'...")

    # PubChem API URL to fetch CID (Chemical ID), IUPAC Name, and Molecular Formula in JSON format
    search_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_name}/property/IUPACName,MolecularFormula/JSON"
    
    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            data = response.json()
            print(data)
            properties = data["PropertyTable"]["Properties"][0]
            
            # Extracting specific chemical properties from the API response
            cid = properties.get("CID")
            iupac = properties.get("IUPACName")
            formula = properties.get("MolecularFormula")
            
            print("\n✅ Real-time data successfully fetched from PubChem!")
            print(f"🧪 Chemical ID (CID): {cid}")
            print(f"🧪 Molecular Formula: {formula}")
            print(f"🧪 IUPAC Name: {iupac}")
            
            return properties
        else:
            print(f"❌ Chemical not found. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ An error occurred: {e}")
        return None

# Testing the function with 'Curcumin' (the primary phytochemical in Turmeric)
get_chemical_info("curcumin")