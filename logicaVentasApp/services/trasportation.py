class Trasnportation:

    @staticmethod

    def get_transportation_code(transportation_code):

        match transportation_code:
            case 1:
                return "Directa"
            case 2:
                return "Despacho"
            case 3:
                return "Retiro Panal"
            case 4:
                return "Retiro LC"
            case 5:
                return "Retiro PH"
            case _:
                return "No Aplica"