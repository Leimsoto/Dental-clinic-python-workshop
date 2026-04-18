"""Client data container with simple attributes.

Using a dataclass makes creation and (de)serialization simple.
"""

from dataclasses import dataclass


@dataclass
class Client:
    id_number: str = ""
    name: str = ""
    phone: str = ""
    client_type: str = "Private"      # Private, EPS, Prepaid
    service_type: str = "Cleaning"    # Cleaning, Filling, Extraction, Diagnosis
    quantity: int = 1
    priority: str = "Normal"          # Normal, Urgent
    appointment_date: str = ""
    visit_fee: float = 0.0
    service_fee: float = 0.0
    total_fee: float = 0.0
