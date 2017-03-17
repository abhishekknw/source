'use strict';

/**
 * @ngdoc function
 * @name societyCatalogApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the societyCatalogApp
 */

angular.module('societyCatalogApp').factory('societyDetailsService', ['$http', function ($http) {

	var base_url = "http://192.168.1.14:8080/machadaloweb/mastersuppliertypesociety/1";
	var societyDetailsService = {};

	societyDetailsService.getSocietyData = function() { 
		return $http({
      method: 'GET',
      url: base_url,
      headers: {'Accept': 'application/json',
      	        'Content-Type': 'application/json'    
                },
      data: ""
    })

   };
    

  return societyDetailsService;
}]);
    
