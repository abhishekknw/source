import v0.ui.utils as ui_utils
from v0.ui.inventory.serializers import InventorySummarySerializer
from v0.ui.finances.models import PriceMappingDefault
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import status
from v0.ui.utils import get_from_dict


def inventory_summary_insert(data, supplier_inventory_data):
    supplier_object = get_from_dict(data, 'supplier_object')
    inventory_object = get_from_dict(data, 'inventory_object')
    supplier_type_code = get_from_dict(data, 'supplier_type_code')
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
        if get_from_dict(data, 'poster_allowed_nb'):
            if get_from_dict(data, 'nb_count'):
                supplier_object.poster_allowed_nb = True
                poster_campaign = int(get_from_dict(data, 'nb_count'))
                data['poster_campaign'] = poster_campaign
            else:
                supplier_object.poster_allowed_nb = False
        else:
            supplier_object.poster_allowed_nb = False

        if get_from_dict(data, 'lift_count') and get_from_dict(data, 'poster_allowed_lift'):
            if get_from_dict(data, 'lift_count') > 0:
                supplier_object.poster_allowed_lift = True
                poster_campaign = poster_campaign + int(get_from_dict(data, 'lift_count'))
                data['poster_campaign'] = poster_campaign
            else:
                supplier_object.poster_allowed_lift = False
        else:
            supplier_object.poster_allowed_lift = False

        if get_from_dict(data, 'standee_allowed'):
            if get_from_dict(data, 'total_standee_count'):
                supplier_object.standee_allowed = True
                standee_campaign = int(get_from_dict(data, 'total_standee_count'))
                data['standee_campaign'] = standee_campaign
            else:
                supplier_object.standee_allowed = False
        else:
            supplier_object.standee_allowed = False

        if get_from_dict(data,'stall_allowed') or get_from_dict(data,'car_display_allowed'):
            if get_from_dict(data,'total_stall_count'):
                stall_campaign = int(get_from_dict(data,'total_stall_count'))
                data['stall_or_cd_campaign'] = stall_campaign

        if get_from_dict(data, 'flier_allowed'):
            if get_from_dict(data, 'flier_frequency'):
                supplier_object.flier_allowed = True
                flier_campaign = int(get_from_dict(data, 'flier_frequency'))
                data['flier_campaign'] = flier_campaign
            else:
                supplier_object.flier_allowed = False
        else:
            supplier_object.flier_allowed = False

        # flier creation

        flag1 = True
        if 'id' in data:
            flag1 = False
            if get_from_dict(data, 'flier_allowed'):
                if get_from_dict(data, 'flier_frequency') and inventory_object.flier_frequency < data['flier_frequency']:
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

        supplier_object.stall_allowed = True if get_from_dict(data, 'stall_allowed')else False
        supplier_object.car_display_allowed = True if get_from_dict(data, 'car_display_allowed')else False

        # society = SupplierTypeSociety.objects.get(pk=id)
        supplier_object.total_campaign = poster_campaign + standee_campaign + stall_campaign + flier_campaign
        supplier_object.save()

        # stall creation
        flag = True
        if 'id' in data:
            flag = False
            if get_from_dict(data, 'stall_allowed'):
                if get_from_dict(data, 'total_stall_count')and inventory_object.total_stall_count < data['total_stall_count']:
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
        if get_from_dict(data, 'poster_price_week_nb'):

            posPrice = int(get_from_dict(data, 'poster_price_week_nb'))
            if get_from_dict(data, 'poster_allowed_nb'):
                if get_from_dict(data, 'nb_A3_allowed'):
                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['poster_a3'],
                                                   duration_type_dict['campaign_weekly']), id,
                        supplier_type_code)
                    ui_utils.save_price_data(price, posPrice)

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['poster_a3'],
                                                   duration_type_dict['unit_weekly']), id, supplier_type_code)
                    ui_utils.save_price_data(price, posPrice / towercount)

                if get_from_dict(data, 'nb_A4_allowed'):
                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['poster_a4'],
                                                   duration_type_dict['campaign_weekly']), id,
                        supplier_type_code)
                    ui_utils.save_price_data(price, posPrice)

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['poster_a4'],
                                                   duration_type_dict['unit_weekly']), id, supplier_type_code)
                    ui_utils.save_price_data(price, posPrice / towercount)

        if get_from_dict(data, 'poster_price_week_lift'):
            posPrice = int(get_from_dict(data, 'poster_price_week_lift'))
            if get_from_dict(data, 'poster_allowed_lift'):
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

        if get_from_dict(data, 'standee_price_week'):
            stanPrice = int(get_from_dict(data, 'standee_price_week'))
            if get_from_dict(data, 'standee_allowed'):
                if get_from_dict(data, 'standee_small'):
                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['standee_small'],
                                                   duration_type_dict['campaign_weekly']), id,
                        supplier_type_code)

                    ui_utils.save_price_data(price, stanPrice)

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['standee_small'],
                                                   duration_type_dict['unit_weekly']), id, supplier_type_code)
                    ui_utils.save_price_data(price, stanPrice / towercount)

                if get_from_dict(data, 'standee_medium'):
                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['standee_medium'],
                                                   duration_type_dict['campaign_weekly']), id,
                        supplier_type_code)

                    ui_utils.save_price_data(price, stanPrice)

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['standee_medium'],
                                                   duration_type_dict['unit_weekly']), id, supplier_type_code)
                    ui_utils.save_price_data(price, stanPrice / towercount)

        if get_from_dict(data, 'stall_allowed'):
            if get_from_dict(data, 'stall_small'):
                if get_from_dict(data, 'stall_price_day_small'):
                    stallPrice = int(get_from_dict(data, 'stall_price_day_small'))

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['stall_small'],
                                                   duration_type_dict['unit_daily']), id, supplier_type_code)
                    ui_utils.save_price_data(price, stallPrice)

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['stall_canopy'],
                                                   duration_type_dict['unit_daily']), id, supplier_type_code)
                    ui_utils.save_price_data(price, stallPrice)

            if get_from_dict(data, 'stall_large'):
                if get_from_dict(data, 'stall_price_day_large'):
                    stallPrice = int(get_from_dict(data, 'stall_price_day_large'))

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['stall_large'],
                                                   duration_type_dict['unit_daily']), id, supplier_type_code)
                    ui_utils.save_price_data(price, stallPrice)

        if get_from_dict(data, 'car_display_allowed'):
            if get_from_dict(data, 'cd_standard'):
                if get_from_dict(data, 'cd_price_day_standard'):
                    cdPrice = int(get_from_dict(data, 'cd_price_day_standard'))

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['car_display_standard'],
                                                   duration_type_dict['unit_daily']), id, supplier_type_code)
                    ui_utils.save_price_data(price, cdPrice)

            if get_from_dict(data, 'cd_premium'):
                if get_from_dict(data, 'cd_price_day_premium'):
                    cdPrice = int(get_from_dict(data, 'cd_price_day_premium'))

                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['car_display_premium'],
                                                   duration_type_dict['unit_daily']), id, supplier_type_code)
                    ui_utils.save_price_data(price, cdPrice)

        if get_from_dict(data, 'flier_price_day'):
            flierPrice = int(get_from_dict(data, 'flier_price_day'))
            if get_from_dict(data, 'mailbox_allowed'):
                price = PriceMappingDefault.objects.get_price_mapping_object(
                    ui_utils.make_dict_manager(adinventory_dict['flier_mailbox'],
                                               duration_type_dict['unit_daily']), id, supplier_type_code)
                ui_utils.save_price_data(price, flierPrice)

            if get_from_dict(data, 'd2d_allowed'):
                price = PriceMappingDefault.objects.get_price_mapping_object(
                    ui_utils.make_dict_manager(adinventory_dict['flier_door_to_door'],
                                               duration_type_dict['unit_daily']), id, supplier_type_code)
                ui_utils.save_price_data(price, flierPrice)

            if get_from_dict(data, 'flier_lobby_allowed'):
                try:
                    price = PriceMappingDefault.objects.get_price_mapping_object(
                        ui_utils.make_dict_manager(adinventory_dict['flier_lobby'],
                                                   duration_type_dict['unit_daily']), id, supplier_type_code)
                    ui_utils.save_price_data(price, flierPrice)

                except KeyError as e:
                    raise KeyError(e.message)
        if get_from_dict(data, 'gateway_arch_allowed'):
            ui_utils.save_gateway_arch_location(supplier_object, supplier_type_code)

        serializer = InventorySummarySerializer(inventory_object, data=supplier_inventory_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


