import v0.models as models


def create_city_area_subarea():
        """

        Returns: a dict containing necessary objects for creating a subarea

        """
        state =  models.State.objects.create(state_name='UP', state_code='UP')
        city =  models.City.objects.create(city_name='LKO', city_code='LKO', state_code=state)
        city_area = models.CityArea.objects.create(label='Aminabad', area_code='A', city_code=city)
        city_subarea = models.CitySubArea.objects.create(subarea_name='Vihar', subarea_code='V',  area_code=city_area)

        context = {
            'state': state,
            'city': city,
            'area': city_area,
            'subarea': city_subarea
        }
        return context

