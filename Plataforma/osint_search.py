import streamlit as st
import urllib.parse

def perform_osint_search(name, job, country):
    st.write("### OSINT Search Results")

    osint_results = []

    google_query = f"{name} + {job} {country}"
    google_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(google_query)}"
    osint_results.append(("Basic Google Search", google_url))

    linkedin_query = f"{name} {job}"
    linkedin_url = f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote_plus(linkedin_query)}"
    osint_results.append(("LinkedIn Search", linkedin_url))

    adverse_media_query = f"{name} {country} (fraud OR corruption OR money laundering OR financial crime OR sanctions)"
    adverse_media_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(adverse_media_query)}"
    osint_results.append(("Adverse Media Search", adverse_media_url))

    company_registry_url = f"https://opencorporates.com/search?q={urllib.parse.quote_plus(name)}"
    osint_results.append(("Company Registry Search", company_registry_url))

    sanctions_url = f"https://www.opensanctions.org/search/?scope=regulatory&q={urllib.parse.quote_plus(name)}"
    osint_results.append(("Sanctions Search (OFAC)", sanctions_url))

    pep_query = f"{name}"
    pep_url = f"https://www.opensanctions.org/search/?scope=peps&q={urllib.parse.quote_plus(pep_query)}"
    osint_results.append(("PEP Search (World-Check One)", pep_url))

    for title, url in osint_results:
        st.markdown(f"[{title}]({url})")

    st.write("Note: Some of these searches may require additional authentication or subscriptions.")

    return osint_results