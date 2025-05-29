from datosLsApp.repositories.comunarepository import ComunaRepository


class BusinessPartnerSerializer:

    @staticmethod
    def serializer_bp(data_bp, card_code):
        client_data = data_bp
        giro =  client_data.get("giroSN", "")

        # Serializa los datos principales del cliente
        serialized_data = {
            "CardCode": card_code,
            "CardName": f"{client_data.get('nombreSN', '')} {client_data.get('apellidoSN', '')}".strip(),
            "CardType": "cCustomer",
            "GroupCode": int(client_data.get("tipoSN", "")),
            "Phone1": client_data.get("telefonoSN", ""),
            "Phone2": client_data.get("telefonoSN", ""),
            "Notes": giro or "NO INDICADO", 
            "PayTermsGrpCode": -1,
            "FederalTaxID": client_data.get("rutSN", ""),
            "SalesPersonCode": -1,
            "Cellular": client_data.get("telefonoSN", ""),
            "EmailAddress": client_data.get("emailSN", ""),
            "CardForeignName": f"{client_data.get('nombreSN', '')} {client_data.get('apellidoSN', '')}".strip(),
            "DunningTerm": "ESTANDAR",
            "CompanyPrivate": "cPrivate",
            "AliasName": client_data.get("nombreSN", ""),
            "U_Tipo": "N",
            "U_FE_Export": "N",
            "BPAddresses": [],
            "ContactEmployees": []
        }
        
        # Serializa las direcciones
        direcciones = client_data.get("direcciones", [])
        tipos_direccion = {"13": None, "12": None}

        for address in direcciones:
            id_comuna = address.get('comuna')
            comunas = ComunaRepository().obtenerComunaPorId(id_comuna)    
            tipo_direccion = address.get("tipoDireccion", "")

            serialized_address = {
                "AddressName": f'{address.get("nombreDireccion", "")}',
                "Street": address.get("direccion", ""),
                "City": address.get("ciudad", ""),
                "County": f"{comunas.codigo} - {comunas.nombre}",
                "Country": "CL",  # Abreviación del país (e.g., Chile -> CL)
                "State": int(address.get("region", "")),
                "FederalTaxID": client_data.get("rutSN", "").split("-")[0],
                "TaxCode": "IVA",
                "AddressType": "bo_ShipTo" if tipo_direccion == "12" else "bo_BillTo"
            }

            serialized_data["BPAddresses"].append(serialized_address)
            tipos_direccion[tipo_direccion] = serialized_address

        # Genera la dirección faltante si solo hay una de las dos
        if tipos_direccion["12"] and not tipos_direccion["13"]:
            direccion_facturacion = tipos_direccion["12"].copy()
            direccion_facturacion["AddressType"] = "bo_BillTo"
            direccion_facturacion["AddressName"] = f'{direccion_facturacion["AddressName"]} - Facturación'
            serialized_data["BPAddresses"].append(direccion_facturacion)

        if tipos_direccion["13"] and not tipos_direccion["12"]:
            direccion_despacho = tipos_direccion["13"].copy()
            direccion_despacho["AddressType"] = "bo_ShipTo"
            direccion_despacho["AddressName"] = f'{direccion_despacho["AddressName"]} - Despacho'
            serialized_data["BPAddresses"].append(direccion_despacho)
        
        # Serializa los contactos
        contactos = client_data.get("contactos", [])
        
        if not contactos:  # Si no hay contactos, genera uno basado en el cliente principal
            name = client_data.get("nombreSN", "")
            if len(name) > 40:
                name = name[:40]
            name = name.split(" ")[0]  # Solo el primer nombre
            contacto_cliente_principal = {
                "Name": name,
                "Phone1": client_data.get("telefonoSN", ""),
                "MobilePhone": client_data.get("telefonoSN", ""),
                "E_Mail": client_data.get("emailSN", ""),
                "FirstName": name,
                "LastName": client_data.get("apellidoSN", "") or name,
            }
            serialized_data["ContactEmployees"].append(contacto_cliente_principal)
        else:
            for contact in contactos:
                name = contact.get("nombreContacto", "")
                if len(name) > 40:
                    name = name[:40]
                serialized_contact = {
                    "Name": name,
                    "Phone1": contact.get("telefonoContacto", ""),
                    "MobilePhone": contact.get("telefonoContacto", ""),
                    "E_Mail": contact.get("emailContacto", ""),
                    "FirstName": name,
                    "LastName": contact.get("apellidoContacto", "")
                }

                serialized_data["ContactEmployees"].append(serialized_contact)

        return serialized_data