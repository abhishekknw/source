# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def general_user_permission(apps, schema_editor):
    """

    Args:
        apps:
        schema_editor:

    Returns:

    """
    general_user_permission_model = apps.get_model(settings.APP_NAME, 'GeneralUserPermission')
    organisation_model = apps.get_model(settings.APP_NAME, 'Organisation')
    profile_model = apps.get_model(settings.APP_NAME, 'Profile')

    organisation = organisation_model.objects.get(name='MACHADALO')
    profile = profile_model.objects.get(organisation=organisation, name='machadalo admin')

    valid_permissions = [
        'can_view_organisation_list',
        'can_view_organisation_details',
        'can_view_account_list',
        'can_add_new_account',
        'can_create_new_proposal',
        'can_view_proposal_list',
        'can_add_invoice_details',
        'can_change_radius_on_mapview',
        'can_change_center_location_on_mapview',
        'can_view_filters_on_mapview_and_gridview',
        'can_apply_filters_on_mapview_and_gridview',
        'can_save_data_on_mapview_and_gridview',
        'can_add_extra_suppliers_on_gridview',
        'can_request_proposal_on_gridview',
        'can_upload_proposal_on_gridview',
        'can_change_supplier_status_to_finalize_on_gridview',
        'can_change_supplier_status_to_buffer_on_gridview',
        'can_change_supplier_status_to_remove_on_gridview',
        'can_change_proposal_state_to_accept_on_opsdashboard',
        'can_change_proposal_state_to_decline_on_opsdashboard',
        'can_change_proposal_state_to_onhold_on_opsdashboard',
        'can_add_negotiated_price_on_supplierBookingPage',
        'can_view_negotiated_price_on_supplierBookingPage',
        'can_view_booking_status_of_supplier_on_supplierBookingPage',
        'can_change_booking_status_of_supplier_on_supplierBookingPage',
        'can_view_phase_of_supplier_on_supplierBookingPage',
        'can_add_phase_of_supplier_on_supplierBookingPage',
        'can_view_mode_of_payment_of_supplier_on_supplierBookingPage',
        'can_add_mode_of_payment_of_supplier_on_supplierBookingPage',
        'can_view_payment_details_of_supplier_on_supplierBookingPage',
        'can_view_inventory_ids_of_supplier_on_supplierBookingPage',
        'can_update_data_on_supplierBookingPage',
        'can_assign_dates_of_campaign_of_all_activities_on_ManageAuditDetailsPage',
        'can_view_dates_of_activities_on_ManageAuditDetailsPage',
        'can_add_comments_for_activities_on_ManageAuditDetailsPage',
        'can_update_data_on_ManageAuditDetailsPage',
        'can_ReAssign_activity_dates_on_OpsExecutionPage',
        'can_view_supplier_details_on_OpsExecutionPage',
        'can_view_images_on_OpsExecutionPage',
        'can_upload_images_on_OpsExecutionPage',
        'can_view_summary_details_on_OpsExecutionPage',
        'can_download_images_on_OpsExecutionPage',
        'can_view_Management_on_NavBar',
        'can_view_HomePage_Button_on_Menu',
        'can_view_OpsDashBoard_Button_on_Menu',
        'can_view_CampaignList_Button_on_Menu'
    ]

    general_user_permission_model.objects.all().delete()

    for perm in valid_permissions:
        general_user_permission_model.objects.create(profile=profile, name=perm, codename=perm[:10])


def reverse(apps, schema_editor):
    """

    Args:
        apps:
        schema_editor:

    Returns:

    """

    general_user_permission_model = apps.get_model(settings.APP_NAME, 'GeneralUserPermission')
    general_user_permission_model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0077_data_migration_updating_accounts'),
    ]

    operations = [
        migrations.RunPython(general_user_permission, reverse_code=reverse)
    ]