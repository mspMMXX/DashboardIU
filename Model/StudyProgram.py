from Model.Modul import Modul


class StudyProgram:

    def __init__(self):
        self.course_of_study = "Softwareentwicklung"
        self.study_duration = 4
        self.modul_list = {}
        self.initialize_modul_list()

    def initialize_modul_list(self):
        """
        Initialisiert alle Module des Studiengangs Softwareentwicklung.
        """
        self.modul_list = {
            1: Modul(1, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            2: Modul(2, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            3: Modul(3, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            4: Modul(4, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            5: Modul(5, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            6: Modul(6, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            7: Modul(7, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            8: Modul(8, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            9: Modul(9, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            10: Modul(10, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            11: Modul(11, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            12: Modul(12, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            13: Modul(13, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            14: Modul(14, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            15: Modul(15, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            16: Modul(16, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            17: Modul(17, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            18: Modul(18, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            19: Modul(19, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            20: Modul(20, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            21: Modul(21, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            22: Modul(22, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            23: Modul(23, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            24: Modul(24, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            25: Modul(25, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            26: Modul(26, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            27: Modul(27, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            28: Modul(28, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            29: Modul(29, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            30: Modul(30, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            31: Modul(31, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            32: Modul(32, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            33: Modul(33, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            34: Modul(34, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            35: Modul(35, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png"),
            36: Modul(1, "DLBDSIDS01_D", "Einführung in Data Science", "Fachpräsentation",
                     "/Users/msp/Dropbox/07_IU/11_Objektorientierte_Programmierung_Python/02_Portfolio/01_Code/"
                     "Dashboard/Images/Data_Science.png")
        }
