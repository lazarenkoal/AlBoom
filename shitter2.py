__author__ = 'aleksandrlazarenko'
import xmltodict
import program_data_manager

print(program_data_manager.upload_program_data())
program_data_manager.update_token('aaa')
program_data_manager.update_spent_money(10)
print(program_data_manager.upload_program_data())