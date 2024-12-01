# The sys library in Python provides functions and variables used to manipulate different parts of the Python runtime environment. It allows operating on the interpreter as it provides access to the variables and functions that interact strongly with the interpreter.
import sys
import logging

# def error_message_details(error, error_details:sys):
#     _,_,exc_tb = error_details.exc_info()
#     file_name = exc_tb.tb_frame.f_code.co_filename
#     error_message = f"Error occured in python script a name {file_name} line number {exc_tb.tb_lineno} and error message {str(error)}"

#     return error_message


# class CustomException(Exception):
#     def __init__(self, error_message, error_details:sys):
#         super().__init__(error_message)
#         self.error_message=error_message_details(error_message, error_message_details)  

#     def __str__(self):
#         return self.error_message


# if __name__=='__main__':
#     try:
#         a = 1/0
#     except Exception as e:
#         logging.info('Divide by zero')
#         raise CustomException(e, sys)


import sys

def error_message_details(error, error_details: sys):
    _, _, exc_tb = error_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f"Error occurred in script: {file_name}, line: {line_number}, error: {str(error)}"
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_details)

    def __str__(self):
        return self.error_message

