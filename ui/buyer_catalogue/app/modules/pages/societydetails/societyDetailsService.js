'use strict';

/**
 * @ngdoc function
 * @name machadaloPages.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the machadaloPages
 */

angular.module('machadaloPages')
.factory('societyDetailsService', ['$http', function ($http) {

  //var url_base = 'http://machadalocore.ap-southeast-1.elasticbeanstalk.com/';
  var url_base = 'http://192.168.1.10:8108/v0/ui/';
  //var url_base1 = "v0/ui/";
	var societyDetailsService = {};

	societyDetailsService.getSocietyData = function(id) {
		return $http({
      method: 'GET',
      url: url_base + "society/" + "HIMPOW",
      headers: {'Accept': 'application/json',
      	        'Content-Type': 'application/json'
                },
      data: ""
    })

   };
  return societyDetailsService;
}]);
