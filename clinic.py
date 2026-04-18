'''
Clinic management module for dental clinic clients.

Provides functions to calculate fees, manage client data, and perform searches.
'''

from client import Client
import json
import os
from dataclasses import asdict

# Price table for client types and services
PRICE_TABLE = {
    "Private": {
        "visit_fee":    80000,
        "Cleaning":     60000,
        "Filling":      80000,
        "Extraction":   100000,
        "Diagnosis":    50000,
    },
    "EPS": {
        "visit_fee":    5000,
        "Cleaning":     0,
        "Filling":      40000,
        "Extraction":   40000,
        "Diagnosis":    0,
    },
    "Prepaid": {
        "visit_fee":    30000,
        "Cleaning":     0,
        "Filling":      10000,
        "Extraction":   10000,
        "Diagnosis":    0,
    },
}

# Allowed types for client, service and priority
CLIENT_TYPES   = ["Private", "EPS", "Prepaid"]
SERVICE_TYPES  = ["Cleaning", "Filling", "Extraction", "Diagnosis"]
PRIORITIES     = ["Normal", "Urgent"]


def calculate_values(client: Client):
    # Compute price fields for a client based on PRICE_TABLE
    table = PRICE_TABLE[client.client_type]
    client.visit_fee     = table["visit_fee"]
    client.service_fee = table[client.service_type]
    client.total_fee    = client.visit_fee + client.service_fee * client.quantity


def total_clients(clients: list):
    # Return number of clients
    return len(clients)


def total_revenue(clients: list):
    # Sum total payments from all clients
    total = 0
    for c in clients:
        total += c.total_fee
    return total


def extraction_clients(clients: list):
    # Count clients with extraction service
    count = 0
    for c in clients:
        if c.service_type == "Extraction":
            count += 1
    return count


def sort_by_total_fee(clients: list):
    # Sort clients in-place by total fee, highest first
    clients.sort(key=lambda c: c.total_fee, reverse=True)


def binary_search_by_id(clients: list, id_number: str):
    # Binary search for client by ID (works on a sorted copy)
    sorted_list = sorted(clients, key=lambda c: c.id_number)
    left = 0
    right   = len(sorted_list) - 1

    while left <= right:
        mid = (left + right) // 2
        if sorted_list[mid].id_number == id_number:
            return sorted_list[mid]
        elif sorted_list[mid].id_number < id_number:
            left = mid + 1
        else:
            right = mid - 1
    return None


def save_clients(path: str, clients: list[Client]):
    # Save clients list to a JSON file (overwrite)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([asdict(c) for c in clients], f, ensure_ascii=False, indent=2)
    except Exception:
        # keep function simple for this learning exercise
        raise


def load_clients(path: str) -> list[Client]:
    # Load clients from JSON file, return list of Client
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        clients: list[Client] = []
        entries = data if isinstance(data, list) else data.get("clients", []) if isinstance(data, dict) else []
        for item in entries:
            # create Client from dict, missing keys use defaults
            c = Client(
                id_number=item.get("id_number", ""),
                name=item.get("name", ""),
                phone=item.get("phone", ""),
                client_type=item.get("client_type", "Private"),
                service_type=item.get("service_type", "Cleaning"),
                quantity=int(item.get("quantity", 1)),
                priority=item.get("priority", "Normal"),
                appointment_date=item.get("appointment_date", ""),
                visit_fee=float(item.get("visit_fee", 0)),
                service_fee=float(item.get("service_fee", 0)),
                total_fee=float(item.get("total_fee", 0)),
            )
            clients.append(c)
        return clients
    except Exception:
        # If file is corrupted or unreadable, return empty list
        return []
