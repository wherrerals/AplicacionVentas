from logs.repositories.doclogsrepo import DocumentsLogsRepository


class DocumentsLogs:
    @staticmethod
    def register_logs(**args) -> None:
        """
        Register logs in the database
        """
        print("Registering logs...")
        #imprimir los argumentos
        print("Arguments: ", args)
        create_log = DocumentsLogsRepository.create_log(args)

        print("Log created: ", create_log)