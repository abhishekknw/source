from django.contrib import admin


# from v0.models import BusinessInfo, BusinessAccountContact, BusinessTypes, BusinessSubTypes, AccountInfo, InventoryLocation, ImageMapping,  Campaign 
# from v0.models import CampaignTypeMapping, CampaignSupplierTypes, SupplierTypeSociety

from v0.models import BusinessInfo, BusinessAccountContact, AccountInfo, BusinessTypes, BusinessSubTypes

# class ImageMappingAdmin(admin.ModelAdmin):
# 	list_display = ['supplier','location_id','location_type']
# 	search_fields = ['supplier__supplier_code','supplier__society_zip','supplier__society_name','location_type','location_id']

# 	class Meta:
# 		model = ImageMapping

# admin.site.register(ImageMapping,ImageMappingAdmin)


# class InventoryLocationAdmin(admin.ModelAdmin):
# 	list_display = ['location_id','location_type']
# 	search_fields = ['location_id','location_type']

# 	class Meta:
# 		model = InventoryLocation

# admin.site.register(InventoryLocation, InventoryLocationAdmin)


class BusinessInfoAdmin(admin.ModelAdmin):
	list_display = ['id','name', 'type_name', 'sub_type', 'email' ]
	search_fields = ['name','type_name','sub_type']	

	class Meta:
		model = BusinessInfo

admin.site.register(BusinessInfo, BusinessInfoAdmin)


class BusinessAccountContactAdmin(admin.ModelAdmin):
	list_display = ['id','name','designation','department','phone']
	search_fields = ['name','designation','spoc']

	class Meta:
		model = BusinessAccountContact

admin.site.register(BusinessAccountContact, BusinessAccountContactAdmin)


class BusinessTypesAdmin(admin.ModelAdmin):
	list_display = ['id','business_type']
	search_fields = ['id','business_type']

	class Meta:
		model = BusinessTypes

admin.site.register(BusinessTypes, BusinessTypesAdmin)


class BusinessSubTypesAdmin(admin.ModelAdmin):
	list_display = ['id','business_type','business_sub_type']
	search_fields = ['id','business_type__business_type','business_sub_type']

	class Meta:
		model = BusinessSubTypes

admin.site.register(BusinessSubTypes, BusinessSubTypesAdmin)


class AccountInfoAdmin(admin.ModelAdmin):
	list_display = ['id','name','phone','email']
	search_fields = ['name','phone','email']

	class Meta:
		model = AccountInfo

admin.site.register(AccountInfo, AccountInfoAdmin)


# # class AccountContactAdmin(admin.ModelAdmin):
# # 	list_display = ['name','designation','department','phone']
# # 	search_fields = ['name','designation']

# # 	class Meta:
# # 		model = AccountContact

# # admin.site.register(AccountContact, AccountContactAdmin)


# class CampaignAdmin(admin.ModelAdmin):
# 	list_display = ['account','start_date','end_date']
# 	search_fields = ['account__name','start_date','end_date']

# 	class Meta:
# 		model = Campaign

# admin.site.register(Campaign, CampaignAdmin)


# class CampaignTypeMappingAdmin(admin.ModelAdmin):
# 	list_display = ['campaign', 'type',  'sub_type']
# 	search_fields = ['campaign', 'type', 'sub_type']

# 	class Meta:
# 		model = CampaignTypeMapping

# admin.site.register(CampaignTypeMapping, CampaignTypeMappingAdmin)


# class CampaignSupplierTypesAdmin(admin.ModelAdmin):
# 	list_display = ['campaign','supplier_type','count']
# 	search_fields = ['supplier_type','count']

# 	class Meta:
# 		model = CampaignSupplierTypes

# admin.site.register(CampaignSupplierTypes, CampaignSupplierTypesAdmin)



# class SupplierTypeSocietyAdmin(admin.ModelAdmin):
# 	list_display = ['supplier_id', 'supplier_code', 'society_name',  'society_address1']
# 	search_fields = ['supplier_id', 'supplier_code', 'society_name',  'society_address1']

# 	class Meta:
# 		model = SupplierTypeSociety

# admin.site.register(SupplierTypeSociety, SupplierTypeSocietyAdmin)