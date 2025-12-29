import uuid

class BatchProduct:

    @staticmethod
    def generate_boundary():
        return str(uuid.uuid4())

    @staticmethod
    def generate_batch(listItems):
        boundary = BatchProduct.generate_boundary()
        changeset_boundary = "changeset_77162fcd-b8da-41ac-a9f8-9357efbbd"

        body_parts = []
        body_parts.append(f"--{boundary}")
        body_parts.append(f"Content-Type: multipart/mixed; boundary={changeset_boundary}")
        body_parts.append("")

        if listItems:
            for item in listItems:
                item_code = item


                if "SV" in item_code or 'PN' in item_code:
                        continue

                body_parts.append(f"--{changeset_boundary}")
                body_parts.append("Content-Type: application/http")
                body_parts.append("Content-Transfer-Encoding: binary")
                body_parts.append("")
                body_parts.append(f"PATCH /b1s/v1/Items('{item_code}') HTTP/1.1")
                body_parts.append("Content-Type: application/json")
                body_parts.append("")
                body_parts.append('{"U_LED_SYNC": 0}')
                body_parts.append("")

            body_parts.append(f"--{changeset_boundary}--")

        body_parts.append(f"--{boundary}--")

        body = "\n".join(body_parts)

        print(f"boy patch{body}")

        return body, boundary, changeset_boundary

