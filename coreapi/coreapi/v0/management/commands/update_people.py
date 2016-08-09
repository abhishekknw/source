from django.core.management.base import BaseCommand, CommandError
import csv, sys
from v0.models import SupplierTypeSociety, SocietyLeads


class Command(BaseCommand):
	help = 'Saves the society leads from the file provided'

	# def add_arguments(self, parser):
	# 	parser.add_argument('file_path',type=str)

	def handle(self,*args, **options):
		# print "sys.argv[2] : ",sys.argv[2]
		try:
			file_path = sys.argv[2]
		except IndexError:
			# self.stdout.write(self.style.SUCCESS('No file path provided'))
			print "\n\n\nNo file path provided"
			return

		person_list = []

		file = open(file_path,'rb')
		try:
			reader = csv.reader(file)
			for num,row in enumerate(reader):
				if num == 0:
					continue
				else:
					person_dict = {}
					try:
						person_dict['name'] = row[1]
						person_dict['phone'] = row[2] if row[2] else '0'
						person_dict['email'] = row[3] if row[3] else '0'
						person_dict['society'] = row[4] 
					except IndexError:
						continue

					try:
						society = SupplierTypeSociety.objects.get(supplier_id=person_dict['society'])
					except SupplierTypeSociety.DoesNotExist:
						continue

					person = SocietyLeads(name=person_dict['name'], phone=person_dict['phone'],
						email=person_dict['email'], society=society)
					# person.save()
					# print "Person saved"
					person_list.append(person)

		finally:
			SocietyLeads.objects.bulk_create(person_list)
			self.stdout.write(self.style.SUCCESS('\nSuccessfully saved society Leads\n'))
			file.close()