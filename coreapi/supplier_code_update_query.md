//This is done in local where supplier_code updated with last three letters of supplier_id wherever supplier_code was null.
 
>>update machadalotech.supplier_society set supplier_code=SUBSTR(supplier_id, LENGTH(supplier_id) - 2, 3)  where supplier_code is NULL;

