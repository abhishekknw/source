import v0.ui.utils as ui_utils
from v0.ui.inventory.serializers import InventorySummarySerializer
from v0.ui.finances.models import PriceMappingDefault
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import status


def inventory_summary_insert(data, supplier_inventory_data):
    supplier_object = data['supplier_object']
    inventory_object = data['inventory_object']
    supplier_type_code = data['supplier_type_code']
    # supplier_type_code = 'CP'
    # society = SupplierTypeSociety.objects.get(pk=id)
    # item = InventorySummary.objects.get(supplier=society)
    tower_response = ui_utils.get_tower_count(supplier_object, supplier_type_code)
    if not tower_response.data['status']:
        return tower_response
    towercount = tower_response.data['data']

    poster_campaign = 0
    standee_campaign = 0
    stall_campaign = 0
    flier_campaign = 0
    total_campaign = 0

    with transaction.atomic():
        if data['poster_allowed_nb']:
            if data['nb_count']:
                supplier_object.poster_allowed_nb = True
                poster_campaign = int(data['nb_count'])
                data['poster_campaign'] = poster_campaign
            else:
                supplier_object.poster_allowed_nb = False
        else:
            supplier_object.poster_allowed_nb = False

        if data['lift_count'] and data['poster_allowed_lift']:
            if data['lift_count'] > 0:
                supplier_object.poster_allowed_lift = True
                poster_campaign = poster_campaign + int(data['lift_count'])
                data['poster_campaign'] = poster_campaign
            else:
                supplier_object.poster_allowed_lift = False
        else:
            supplier_object.poster_allowed_lift = False

        if data['standee_allowed']:
            if data['total_standee_count']:
                supplier_object.standee_allowed = True
                standee_campaign = int(data['total_standee_count'])
                data['standee_campaign'] = standee_campaign
            else:
                supplier_object.standee_allowed = False
        else:
            supplier_object.standee_allowed = False

        if data['stall_allowed'] or data['car_display_allowed']:
            if data['total_stall_count']:
                stall_campaign = int(data['total_stall_count'])
                data['stall_or_cd_campaign'] = stall_campaign

        if data['flier_allowed']:
            if data['flier_frequency']:
                supplier_object.flier_allowed = True
                flier_campaign = int(data['flier_frequency'])
                data['flier_campaign'] = flier_campaign
            else:
                supplier_object.flier_allowed = False
        else:
            supplier_object.flier_allowed = False

        # flier creation

        flag1 = True
        if 'id' in data:
            flag1 = False
            if data['flier_allowed']:
                if data['flier_frequency'] and inventory_object.flier_frequency <data['flier_frequency']:
                    if not inventory_object.flier_frequency:
                        ui_utils.save_flyer_locations(0, data['flier_frequency'], supplier_object,
                                                      supplier_type_code)
                    else:
                        ui_utils.save_flyer_locations(inventory_object.flier_frequency,
                                                      data['flier_frequency'], supplier_object,
                                                      supplier_type_code)
                serializer = InventorySummarySerializer(inventory_object, data=supplier_inventory_data)
        else:
            if flag1 and data['flier_frequency']:
                ui_utils.save_flyer_locations(0, data['flier_frequency'], supplier_object,
                                              supplier_type_code)
            serializer = InventorySummarySerializer(data=supplier_inventory_data)

        supplier_object.stall_allowed = True if data['stall_allowed'] else False
        supplier_object.car_display_allowed = True if data['car_display_allowed'] else False

        # society = SupplierTypeSociety.objects.get(pk=id)
        supplier_object.total_campaign = poster_campaign + standee_campaign + stall_campaign + flier_campaign
        supplier_object.save()

        # stall creation
        flag = True
        if 'id' in data:
            flag = False
            if data['stall_allowed']:
                if data['total_stall_count'] and inventory_object.total_stall_count < data['total_stall_count']:
                    if not inventory_object.total_stall_count:
                        ui_utils.save_stall_locations(0, data['total_stall_count'], supplier_object,
                                                      supplier_type_code)
                    else:
                        ui_utils.save_stall_locations(inventory_object.total_stall_count,
                                                      data['total_stall_count'], supplier_object,
                                                      supplier_type_code)
            serializer = InventorySummarySerializer(inventory_object, data=supplier_inventory_data)

        else:
            if flag and data['total_stall_count']:
                ui_utils.save_stall_locations(0, data['total_stall_count'], supplier_object,
                                              supplier_type_code)
                #
                # serializer = InventorySummarySerializer(data=supplier_inventory_data)
                # if serializer.is_valid():
                #     serializer.save(supplier=supplier_object)
                # else :
                #     return Response({'error': serializer.errors},status=400)

        adinventory_dict = ui_utils.adinventory_func()
        duration_type_dict = ui_utils.duration_type_func()
        price_list = []
        if data['poster_price_week_nb']:

            posPrice = int(data['poster_price_week_nb'])
            if data['poster_allowed_nb']:
                if data['nb_A3_allowed']:
                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['poster_a3'],
                                                   duration_type_dict['campaign_weekly']), id,
                        supplier_type_code)
                    ui_utils.save_price_data(price, posPrice)

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['poster_a3'],
                                                   duration_type_dict['unit_weekly']), id, supplier_type_code)
                    ui_utils.save_price_data(price, posPrice / towercount)

                if data['nb_A4_allowed']:
                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['poster_a4'],
                                                   duration_type_dict['campaign_weekly']), id,
                        supplier_type_code)
                    ui_utils.save_price_data(price, posPrice)

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['poster_a4'],
                                                   duration_type_dict['unit_weekly']), id, supplier_type_code)
                    ui_utils.save_price_data(price, posPrice / towercount)

        if data['poster_price_week_lift']:
            posPrice = int(data['poster_price_week_lift'])
            if data['poster_allowed_lift']:
                price = PriceMappingDefault.objects.get_price_mapping_object(
                    ui_utils.make_dict_manager(adinventory_dict['poster_lift_a3'],
                                               duration_type_dict['campaign_weekly']), id, supplier_type_code)
                ui_utils.save_price_data(price, posPrice)

                price = PriceMappingDefault.objects.get_price_mapping_object(
                    ui_utils.make_dict_manager(adinventory_dict['poster_lift_a3'],
                                               duration_type_dict['unit_weekly']), id, supplier_type_code)
                ui_utils.save_price_data(price, posPrice / towercount)

                price = PriceMappingDefault.objects.get_price_mapping_object(
                    ui_utils.make_dict_manager(adinventory_dict['poster_lift_a4'],
                                               duration_type_dict['campaign_weekly']), id, supplier_type_code)
                ui_utils.save_price_data(price, posPrice)

                price = PriceMappingDefault.objects.get_price_mapping_object(
                    ui_utils.make_dict_manager(adinventory_dict['poster_lift_a4'],
                                               duration_type_dict['unit_weekly']), id, supplier_type_code)
                ui_utils.save_price_data(price, posPrice / towercount)

        if data['standee_price_week']:
            stanPrice = int(data['standee_price_week'])
            if data['standee_allowed']:
                if data['standee_small']:
                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['standee_small'],
                                                   duration_type_dict['campaign_weekly']), id,
                        supplier_type_code)

                    ui_utils.save_price_data(price, stanPrice)

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['standee_small'],
                                                   duration_type_dict['unit_weekly']), id, supplier_type_code)
                    ui_utils.save_price_data(price, stanPrice / towercount)

                if data['standee_medium']:
                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['standee_medium'],
                                                   duration_type_dict['campaign_weekly']), id,
                        supplier_type_code)

                    ui_utils.save_price_data(price, stanPrice)

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['standee_medium'],
                                                   duration_type_dict['unit_weekly']), id, supplier_type_code)
                    ui_utils.save_price_data(price, stanPrice / towercount)

        if data['stall_allowed']:
            if data['stall_small']:
                if data['stall_price_day_small']:
                    stallPrice = int(data['stall_price_day_small'])

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['stall_small'],
                                                   duration_type_dict['unit_daily']), id, supplier_type_code)
                    ui_utils.save_price_data(price, stallPrice)

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['stall_canopy'],
                                                   duration_type_dict['unit_daily']), id, supplier_type_code)
                    ui_utils.save_price_data(price, stallPrice)

            if data['stall_large']:
                if data['stall_price_day_large']:
                    stallPrice = int(data['stall_price_day_large'])

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['stall_large'],
                                                   duration_type_dict['unit_daily']), id, supplier_type_code)
                    ui_utils.save_price_data(price, stallPrice)

        if data['car_display_allowed']:
            if data['cd_standard']:
                if data['cd_price_day_standard']:
                    cdPrice = int(data['cd_price_day_standard'])

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['car_display_standard'],
                                                   duration_type_dict['unit_daily']), id, supplier_type_code)
                    ui_utils.save_price_data(price, cdPrice)

            if data['cd_premium']:
                if data['cd_price_day_premium']:
                    cdPrice = int(data['cd_price_day_premium'])

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['car_display_premium'],
                                                   duration_type_dict['unit_daily']), id, supplier_type_code)
                    ui_utils.save_price_data(price, cdPrice)

        if data['flier_price_day']:
            flierPrice = int(data['flier_price_day'])
            if data['mailbox_allowed']:
                price = PriceMappingDefault.objects.get_price_mapping_object(
                    ui_utils.make_dict_manager(adinventory_dict['flier_mailbox'],
                                               duration_type_dict['unit_daily']), id, supplier_type_code)
                ui_utils.save_price_data(price, flierPrice)

            if data['d2d_allowed']:
                price = PriceMappingDefault.objects.get_price_mapping_object(
                    ui_utils.make_dict_manager(adinventory_dict['flier_door_to_door'],
                                               duration_type_dict['unit_daily']), id, supplier_type_code)
                ui_utils.save_price_data(price, flierPrice)

            if data['flier_lobby_allowed']:
                try:
                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['flier_lobby'],
                                                   duration_type_dict['unit_daily']), id, supplier_type_code)
                    ui_utils.save_price_data(price, flierPrice)

                except KeyError as e:
                    raise KeyError(e.message)
        if data['gateway_arch_allowed']:
            ui_utils.save_gateway_arch_location(supplier_object, supplier_type_code)

        serializer = InventorySummarySerializer(inventory_object, data=supplier_inventory_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


