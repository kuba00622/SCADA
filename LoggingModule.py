import logging 

__version__ = '1.0.1'

class LogManager():

    """
    Initialize logging module. 
    Created to inform programmer about various error massages at diffrent
    importance level.
    Logs info from modules where log_manager is defined. To seperate log info between modules just simply change log_filepath argument in LogManager class
    
    log_manager is an object created in LoggingModule.py module (global approach) \n
    LogManager is a class (local approach)

    Arguments:
        log_filepath -- filepath with filename eg. 
                        If left blank log file will generate in logger source localisation (default 'log.log')
    
    Examples: 
        a:  Global approach (recommended) - control many loggers from main module.
                    Importing log_manager object straight from LogModule 
                     Should be defined in all modules which are in use.

            >>> from log import log_manager
            
            >>> log_manager.set_level("INFO")
            >>> logger = log_manager.get_logger(__name__, True, True)

        b:  Local approach - separetly importing class LogManager and creating log_manager object localy
            >>> from log import LogManager

            >>> log_manager = LogManager()
            >>> logger = log_manager.get_logger(__name__, logging_to_console=True, logging_to_file=False)

            >>> devices = ['dev1', 'dev2', 'dev3']
            >>> logger.debug(f'List of devices: {devices}')
            >>> logger.setLevel("INFO")

        c:  Local - shows how to log to seperate file yourfilepath
            >>> from log import LogManager

            >>> log_manager = LogManager(log_filepath=yourfilepath)
            
            >>> logger = log_manager.get_logger(__name__)

            >>> devices = ['dev1', 'dev2', 'dev3']
            >>> logger.info(f'List of devices: {devices}')


    """

    def __init__(self, log_filepath="log.log") -> None:
        
        self.logger_level = logging.DEBUG

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(self.logger_level)

        self.file_handler = logging.FileHandler(log_filepath) 
        self.file_handler.setLevel(self.logger_level)

        self.formatter = logging.Formatter(
            "%(asctime)s [%(name)s] [%(levelname)s]: %(message)s")
        self.console_handler.setFormatter(self.formatter)
        self.file_handler.setFormatter(self.formatter)

        self.loggers = {}

    def get_logger(self, module_name, logging_to_console=True, logging_to_file=False):
        """
        Returns log object

        Arguments:
            logging_to_console -- logging to console (default True) \n
            logging_to_file -- logging to file (default False) \n
        """

        log = logging.getLogger(module_name)
        log.setLevel(self.logger_level)
        
        if logging_to_console:
            log.addHandler(self.console_handler)

        if logging_to_file:
            log.addHandler(self.file_handler)
        
        # gathers loggers from modules where logger is defined (tuple)
        self.loggers[module_name] = log

        return log

    def set_level(self, level):
        """
        Set level of all loggers used in project (global)

        Arguments:
            level -- set log level: 'DEBUG', 'INFO', 'WARNING', 'CRITICAL'
        """
        if level == 'DEBUG':
            self.logger_level = logging.DEBUG
        elif level == 'INFO':
            self.logger_level = logging.INFO
        elif level == 'WARNING':
            self.logger_level = logging.WARNING
        elif level == 'CRITICAL':
            self.logger_level = logging.CRITICAL
        
        self.console_handler.setLevel(self.logger_level)
        self.file_handler.setLevel(self.logger_level)

        # set importance level of each logger 
        for log in self.loggers.values():
            log.setLevel(level)

# initialise log_manager object
log_manager = LogManager()
