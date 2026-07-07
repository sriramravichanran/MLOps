import traceback
import sys

class CustomException(Exception):
    """
    Custom Exception class
    This helps in getting detailed error messages->
    Error filename, linenumber , error message
    """

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys):
        """
        Returns detailed error message with:
        -File name
        -Line Number
        -Original Error Message
        """

        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        return(
            f"Error Occured in script: [{file_name}]"
            f"at line number: [{line_number}]"
            f"error message: [{error_message}]"
        )


    def __str__(self):

        return self.error_message