from django.core.paginator import Paginator

def paginate(data,serializer,request,limit=10):
    paginator = Paginator(data, limit)

    page = request.GET.get('page',1)

    page_data = paginator.page(page)
    
    object_list = serializer(page_data,many=True).data
    
    return {
        "count": paginator.count,
        "pages": paginator.num_pages,
        "current_page":page,
        "has_next": page_data.has_next(),
        "has_previous": page_data.has_previous(),
        "list": object_list
    }

def paginateMongo(data,request,limit=10):
    paginator = Paginator(data, limit)

    page = request.GET.get('page',1)

    page_data = paginator.page(page)
    
    # object_list = serializer(page_data,many=True).data
    
    return {
        "count": paginator.count,
        "pages": paginator.num_pages,
        "current_page":page,
        "has_next": page_data.has_next(),
        "has_previous": page_data.has_previous(),
        "list": page_data
    }