from main_controller import MainWindowViewController
import program_saver
__author__ = 'aleksandrlazarenko'


"""Main-main-main ultra-main!!!!!
"""
def main():
    # TODO: upload data from previous users visit (token, etc)
    userData = program_saver.upload_program_data()
    MainWindowViewController(userData)

main()