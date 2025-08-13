from concurrent.futures import ThreadPoolExecutor
from documentSerializer import SerializerDocument
import pytest

from domain.services.calculador import CalculadoraTotales

@pytest.fixture
def document_data():

    return {'DocNum': '', 'DocEntry': '', 'DocDate': '2025-06-09', 'DocTotal': '1110688', 'NumAtCard': '', 'DocDueDate': '2025-06-09', 'Comments': '', 'TaxDate': '2025-06-09', 'ContactPersonCode': '13599', 'Address': '62205', 'Address2': '62206', 'CardCode': '28604599C', 'PaymentGroupCode': -1, 'SalesPersonCode': 33, 'TransportationCode': '1', 'U_LED_TIPDOC': 'BOLE', 'U_LED_FORENV': 1, 'DocumentLines': [{'LineNum': '0', 'DocEntry_line': '218174', 'ItemCode': 'N10101019', 'Quantity': 44, 'line_price': '$ 215.600', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '1', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '1', 'DocEntry_line': '218174', 'ItemCode': 'C10300165', 'Quantity': 351, 'line_price': '$ 130.900', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '1', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '2', 'DocEntry_line': '218174', 'ItemCode': 'C33300013', 'Quantity': 350, 'line_price': '$ 46.550', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 5, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '1', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '3', 'DocEntry_line': '218174', 'ItemCode': 'C10300189', 'Quantity': 2, 'line_price': '$ 99.800', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '2', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '4', 'DocEntry_line': '218174', 'ItemCode': 'C17900218', 'Quantity': 8, 'line_price': '$ 79.200', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '1', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '5', 'DocEntry_line': '218174', 'ItemCode': 'C10300163', 'Quantity': 35, 'line_price': '$ 11.543', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 3, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '1', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '6', 'DocEntry_line': '218174', 'ItemCode': 'C17900244', 'Quantity': 35, 'line_price': '$ 35.900', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '1', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '7', 'DocEntry_line': '218174', 'ItemCode': 'C19100009', 'Quantity': 4, 'line_price': '$ 43.600', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '4', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '8', 'DocEntry_line': '218174', 'ItemCode': 'C19100031', 'Quantity': 4, 'line_price': '$ 103.600', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '4', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '9', 'DocEntry_line': '218174', 'ItemCode': 'C19100010', 'Quantity': 359, 'line_price': '$ 250.895', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 5, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '1', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '10', 'DocEntry_line': '218174', 'ItemCode': 'C19100011', 'Quantity': 35, 'line_price': '$ 16.900', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '1', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '11', 'DocEntry_line': '218174', 'ItemCode': 'C33300035', 'Quantity': 5, 'line_price': '$ 19.500', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '5', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '12', 'DocEntry_line': '218174', 'ItemCode': 'SV00035', 'Quantity': 2, 'line_price': '$ 9.520', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '2', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '13', 'DocEntry_line': '218174', 'ItemCode': 'C19100020', 'Quantity': 35, 'line_price': '$ 7.900', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '1', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '14', 'DocEntry_line': '218174', 'ItemCode': 'C32500020', 'Quantity': 5, 'line_price': '$ 19.500', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '5', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '15', 'DocEntry_line': '218174', 'ItemCode': 'C10300172', 'Quantity': 2, 'line_price': '$ 17.800', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '2', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}, {'LineNum': '17', 'DocEntry_line': '218174', 'ItemCode': 'C10300203', 'Quantity': 2, 'line_price': '$ 1.980', 'ShipDate': '2025-06-09', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'LC', 'CostingCode': 'LC', 'ShippingMethod': '2', 'COGSCostingCode': 'LC', 'CostingCode2': 'AV', 'COGSCostingCode2': 'AV', 'CantidadInicialSAP': '44'}]}

@pytest.fixture
def document_data_2():
    
    return {'DocDate': '2025-06-10', 'DocDueDate': '2025-06-20', 'TaxDate': '2025-06-10', 'DocTotal': '141160.0', 'CardCode': '77768603C', 'NumAtCard': '', 'Comments': '', 'PaymentGroupCode': -1, 'SalesPersonCode': 78, 'TransportationCode': '1', 'U_LED_TIPVTA': 'TIEN', 'U_LED_TIPDOC': 'BOLE', 'U_LED_FORENV': '1', 'DocumentLines': [{'ItemCode': 'B25400087K2', 'Quantity': 4, 'UnitPrice': 26210.084, 'ShipDate': '2025-06-20', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'PH', 'CostingCode': 'PH', 'ShippingMethod': '1', 'COGSCostingCode': 'PH', 'CostingCode2': 'AV', 'TreeType': 'iSalesTree'}, {'ItemCode': 'N10101274', 'Quantity': 4, 'UnitPrice': 1428.5714, 'ShipDate': '2025-06-20', 'FreeText': '', 'DiscountPercent': 0, 'WarehouseCode': 'PH', 'CostingCode': 'PH', 'ShippingMethod': '1', 'COGSCostingCode': 'PH', 'CostingCode2': 'AV', 'TreeType': 'iNotATree'}], 'TaxExtension': {'StreetS': 'union obrera 592 4 rancagua', 'CityS': 'rancagua', 'CountyS': '6 - SIN COMUNA', 'StateS': 6, 'CountryS': 'CL', 'StreetB': 'union obrera 592 4 rancagua', 'CityB': 'rancagua', 'CountyB': '6 - SIN COMUNA', 'StateB': 6, 'CountryB': 'CL'}}


""" def test_serializer_document(document_data):

    serializer = SerializerDocument.document_serializer(document_data)
    assert serializer.is_valid(), f"Serializer inválido. Errores: {serializer.errors}"

    serializer = SerializerDocument.document_serializer(document_data)
    assert serializer.is_valid(), f"Serializer inválido. Errores: {serializer.errors}"

    serializer = SerializerDocument.document_serializer(document_data)
    assert serializer.is_valid(), f"Serializer inválido. Errores: {serializer.errors}"

    serializer = SerializerDocument.document_serializer(document_data)
    assert serializer.is_valid(), f"Serializer inválido. Errores: {serializer.errors}"

    serializer = SerializerDocument.document_serializer(document_data)
    assert serializer.is_valid(), f"Serializer inválido. Errores: {serializer.errors}"

    serializer = SerializerDocument.document_serializer(document_data)
    assert serializer.is_valid(), f"Serializer inválido. Errores: {serializer.errors}"
 """

""" def run_serialization(document_data, index):
    serializer = SerializerDocument.document_serializer(document_data)
    assert serializer.is_valid(), f"[Thread {index}] Serializer inválido. Errores: {serializer.errors}"


def test_concurrent_serializer_document(document_data):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(run_serialization, document_data, i) for i in range(40)]
        for future in futures:
            future.result()  # lanzará excepción si alguna falla """


def test_serializer_document(document_data_2):

    calculate = CalculadoraTotales.calculate_docTotal(document_data_2)
    assert calculate.is_valid(), f"Serializer inválido. Errores: {calculate.errors}"

# python -m pytest datosLsApp/serializer/test_serializers.py