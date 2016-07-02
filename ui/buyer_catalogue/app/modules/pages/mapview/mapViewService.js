 'use strict';


 angular.module('catalogueApp')
 .factory('mapViewService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

  		var url_base = 'v0/ui/website/';

  		var mapViewService = {};


  		mapViewService.getSpaces = function(){
  			var url = url_base + "getSpaces/";
  			return machadaloHttp.get(url);
  		};

  		mapViewService.getSpace = function(id){
  			var url = url_base + "getSpace/" + id +"/";
  			return machadaloHttp.get(url);
  		}


      mapViewService.getAllSocieties = function(){
        var url = url_base + "getSpaces/";
        return machadaloHttp.post(url);
      }
  		return mapViewService;
}]);