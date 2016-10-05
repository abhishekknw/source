from rest_framework.response import Response
from rest_framework import status


def do_each_model(myModel, supplier_model, content_type):
    """
    :param myModel: Model whose fields need to be populated
    :param supplier_model: supplier type model
    :param content_type:  the content Type object
    :return: success in case of success, failure otherwise
    """
    try:
        for row in myModel.objects.all():
            supplier_type = supplier_model.objects.get(supplier_id=row.supplier.supplier_id)
            row.content_type = content_type
            row.object_id = row.supplier.supplier_id
            row.content_object = supplier_type
            row.save()
        return Response({'status': True, 'data': 'success'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
