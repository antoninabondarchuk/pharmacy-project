import codecs
import urllib.request
from datetime import datetime

from drugs.drug_model import Drug
from drugs.models import InternationalName, MarketingStatus, PharmacotherapeuticGroup, ATC, DrugType, \
    PrematureTermination, INN
from firms.models import Country, Applicant, Manufacturer
from pharmacy.celery import app
from csv import reader

WORKING_CSV = "reestr.csv"
TAK = "Так"


def get_value_or_none(value):
    return value or None


@app.task
def update_drugs(file_url):
    urllib.request.urlretrieve(file_url, WORKING_CSV)


@app.task
def update_db():
    with codecs.open(WORKING_CSV, encoding="windows-1251") as csv_file:
        csv_reader = reader(csv_file, delimiter=";")
        titles = next(csv_reader)
        for row in csv_reader:
            drug_dict = dict(zip(titles, row))
            new_drug, _ = Drug.objects.get_or_create(source_id=drug_dict['ID'])
            new_drug.trade_name = drug_dict['Торгівельне найменування']
            new_drug.drug_form = drug_dict['Форма випуску']
            international_name, _ = InternationalName.objects.get_or_create(
                name=drug_dict['Міжнародне непатентоване найменування'])
            new_drug.international_name = international_name
            new_drug.save()
            drug_marketing_status, _ = MarketingStatus.objects.get_or_create(
                name=get_value_or_none(drug_dict['Умови відпуску']))
            new_drug.marketing_status = drug_marketing_status
            new_drug.save()
            new_drug.formula = drug_dict['Склад (діючі)']
            drug_pharmacotherapeutic_group, _ = PharmacotherapeuticGroup.objects.get_or_create(
                name=drug_dict['Фармакотерапевтична група'])
            new_drug.pharmacotherapeutic_group = drug_pharmacotherapeutic_group
            new_drug.save()
            if drug_dict['Код АТС 1']:
                atc_1, _ = ATC.objects.get_or_create(name=drug_dict['Код АТС 1'], type=1)
                new_drug.atcs.add(atc_1)
                new_drug.save()
                if drug_dict['Код АТС 2']:
                    atc_2, _ = ATC.objects.get_or_create(name=drug_dict['Код АТС 2'], type=2)
                    new_drug.atcs.add(atc_2)
                    new_drug.save()
                    if drug_dict['Код АТС 3']:
                        atc_3, _ = ATC.objects.get_or_create(name=drug_dict['Код АТС 3'], type=3)
                        new_drug.atcs.add(atc_3)
                        new_drug.save()
            applicant_country, _ = Country.objects.get_or_create(name=drug_dict['Заявник: країна'])
            applicant, _ = Applicant.objects.get_or_create(
                name=drug_dict['Заявник: назва українською'], country=applicant_country,
                address=drug_dict['Заявник: адреса'])
            new_drug.drug_applicant = applicant
            new_drug.save()
            for start_manufacturer_index in range(14, 29, 3):
                if row[start_manufacturer_index]:
                    manufacturer_country, _ = Country.objects.get_or_create(name=row[start_manufacturer_index + 1])
                    manufacturer, _ = Manufacturer.objects.get_or_create(
                        name=row[start_manufacturer_index],
                        country=manufacturer_country, address=row[start_manufacturer_index + 2])
                    new_drug.manufacturers.add(manufacturer)
                    new_drug.save()
            new_drug.registration_number = drug_dict['Номер Реєстраційного посвідчення']
            new_drug.registration_date = datetime.strptime(drug_dict['Дата початку дії'], '%d.%m.%Y')
            new_drug.expiration_date = drug_dict['Дата закінчення']
            d_type, _ = DrugType.objects.get_or_create(name=drug_dict['Тип ЛЗ'])
            new_drug.drug_type = d_type
            new_drug.has_bio_origin = drug_dict['ЛЗ біологічного походження'] == TAK
            new_drug.has_phyto_origin = drug_dict['ЛЗ рослинного походження'] == TAK
            new_drug.is_orphan = drug_dict['ЛЗ-сирота'] == TAK
            new_drug.is_homeopatic = drug_dict['Гомеопатичний ЛЗ'] == TAK
            inn, _ = INN.objects.get_or_create(name=drug_dict['Тип МНН'])
            new_drug.INN = inn
            if drug_dict['Дострокове припинення'] == TAK:
                drug_premature_termination, _ = PrematureTermination.objects.get_or_create(
                    date=datetime.strptime(drug_dict['Дострокове припинення: останній день дії'], '%d.%m.%Y'),
                    reason=drug_dict['Дострокове припинення: причина'])
                new_drug.premature_termination = drug_premature_termination
            new_drug.instruction_url = drug_dict['URL інструкції']
            new_drug.save()
