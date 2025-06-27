from datosLsApp.serializer.documentSerializer import SerializerDocument


class RertunrRequestSerializer(SerializerDocument):

    @staticmethod
    def document_serializer(doc_data):
        # Llamar a la versión base para mantener toda la lógica existente
        base_data = SerializerDocument.document_serializer(doc_data)
        
        # Construir el bloque DocumentReferences
        ref_doc_entr = doc_data.get('RefDocEntr', None)
        if ref_doc_entr:
            document_references = [
                {
                    "RefDocEntr": ref_doc_entr,
                    "RefObjType": "rot_SalesInvoice"
                }
            ]
            base_data['DocumentReferences'] = document_references

        return base_data