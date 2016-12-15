model_names = ['InventorySummary', 'ContactDetails', 'Events', 'FlyerInventory', 'ImageMapping', 'PosterInventory',
               'SocietyTower', 'PriceMappingDefault', 'SocietyInventoryBooking',
                                                      'StallInventory', 'WallInventory','FlatType'
               ]


# we have group_name and there respective codes. These codes are designed to respect the heirarchy of various kinds of
# users we have in our system
group_codes = {
    'master_users': '0',
    'ops_heads': '01',
    'bd_heads': '02',
    'external_bds': '03'
}

# model_name_to_user_mapping
model_name_user_mapping = {
    'AccountInfo': 'business__user__user_code',
    'ProposalInfo': 'account__business__user__user_code',
}