import sys
import traceback

class CustomException(Exception):
    
    def __init__(self, error_message, error_detail: sys):
        # Call the parent Exception class constructor with the initial message
        super().__init__(error_message)
        
        # Immediately process the error details to create the detailed message
        self.error_message = self.get_detailed_error_message(error_message, error_detail)
        
    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys):
        """
        Generates a detailed error string, safely handling the traceback extraction.
        """
        # --- FIX: ADDED SAFETY CHECK ---
        # Check if the object passed as error_detail has the exc_info method (i.e., is the sys module)
        if hasattr(error_detail, 'exc_info'):
            # The structure of the error detail tuple is (type, value, traceback object)
            _, _, exc_tb = error_detail.exc_info()
            
            # The traceback object (exc_tb) holds information about where the error occurred
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            
            return f"Error occur in script: [{file_name}], line: [{line_number}], error message: [{error_message}]"
        else:
            # Fallback message if a non-sys object (like 'NotFound') was passed
            # This prevents the AttributeError
            return f"Error message: [{error_message}]. Detailed traceback information unavailable."
    
    def __str__(self):
        """
        Defines the string representation of the exception object.
        """
        return self.error_message