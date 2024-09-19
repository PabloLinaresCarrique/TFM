import streamlit as st
import urllib.parse  

def perform_osint_search(name, job, country):
    """
    Function to perform OSINT (Open Source Intelligence) searches based on 
    provided name, job, and country. Generates URLs for different searches.
    """
    st.write("### OSINT Search Results")  # Header for the OSINT search results

    osint_results = []  # List to store the different OSINT search result links

    # Google search query with name, job, and country
    google_query = f"{name} + {job} {country}"
    google_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(google_query)}"
    osint_results.append(("Basic Google Search", google_url))  # Add Google search URL to the results

    # LinkedIn search query for name and job
    linkedin_query = f"{name} {job}"
    linkedin_url = f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote_plus(linkedin_query)}"
    osint_results.append(("LinkedIn Search", linkedin_url))  # Add LinkedIn search URL to the results

    # Adverse media search query with specific keywords related to financial crime
    adverse_media_query = (
        f"{name} {country} (fraud OR corruption OR money laundering OR financial crime OR sanctions OR "
        "bribery OR tax evasion OR embezzlement OR insider trading OR terrorist financing OR tax fraud OR "
        "illegal arms trafficking OR cybercrime OR identity theft OR extortion OR racketeering OR counterfeit goods OR "
        "drug trafficking OR human trafficking OR financial misconduct OR regulatory violations OR organized crime OR "
        "securities fraud OR environmental crime OR market manipulation OR antitrust violations OR smuggling OR "
        "illegal gambling OR forgery OR bankruptcy fraud OR intellectual property theft)"
    )
    adverse_media_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(adverse_media_query)}"
    osint_results.append(("Adverse Media Search", adverse_media_url))  # Add adverse media search URL to the results


    # Company registry search on OpenCorporates
    company_registry_url = f"https://opencorporates.com/search?q={urllib.parse.quote_plus(name)}"
    osint_results.append(("Company Registry Search", company_registry_url))  # Add company registry search URL

    # Sanctions search on OpenSanctions, filtering for regulatory scope (e.g., OFAC)
    sanctions_url = f"https://www.opensanctions.org/search/?scope=regulatory&q={urllib.parse.quote_plus(name)}"
    osint_results.append(("Sanctions Search (OFAC)", sanctions_url))  # Add sanctions search URL

    # Politically Exposed Persons (PEP) search on OpenSanctions
    pep_query = f"{name}"
    pep_url = f"https://www.opensanctions.org/search/?scope=peps&q={urllib.parse.quote_plus(pep_query)}"
    osint_results.append(("PEP Search (World-Check One)", pep_url))  # Add PEP search URL

    # Loop through the OSINT results and display them as clickable links in Streamlit
    for title, url in osint_results:
        st.markdown(f"[{title}]({url})")  # Display the title and make the URL clickable

    st.write("Note: Some of these searches may require additional authentication or subscriptions.") 

    return osint_results  # Return the list of OSINT results
