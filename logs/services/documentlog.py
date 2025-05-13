from logs.repositories.doclogsrepo import DocumentsLogsRepository


class DocumentsLogs:
    @staticmethod
    def register_logs(**args) -> None:
        """
        Register logs in the database
        """
        create_log = DocumentsLogsRepository.create_log(args)

