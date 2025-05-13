from logs.models.documentslogs import DocumentLogDB


class DocumentsLogsRepository:

    @staticmethod
    def create_log(datalog):
        """
        Create a log in the database
        """

        try:
            DocumentLogDB.objects.create(
                docNum=datalog['docNum'],
                docEntry=datalog['docEntry'],
                tipoDoc=datalog['tipoDoc'],
                url=datalog['url'],
                json=datalog['json'],
                response=datalog['response'],
                estate=datalog['estate']
            )

            return True
        except Exception as e:

            return False