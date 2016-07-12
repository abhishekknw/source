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

    // mapViewService.getSpace = function(id){
        // 	var url = url_base + "getSpace/" + id +"/";
        // 	return machadaloHttp.get(url);
    // }

    mapViewService.getChangedCenterSpaces = function(data){
        var url = url_base + 'getSpaces/';
        return machadaloHttp.post(url,data);
    };


    mapViewService.resetCenter = function(center_id){
        var url = url_base + "getSpaces/?center=" + center_id ;
        return machadaloHttp.get(url);
    }

    mapViewService.getFilterSocieties = function(get_data){
        var url = url_base + 'getFilteredSocieties/' + get_data;
        return machadaloHttp.get(url); 
    }

    mapViewService.createFinalProposal = function(centers_data){
        var url = url_base + 'createFinalProposal/';
        return machadaloHttp.post(url, centers_data);
    }

    return mapViewService;
}]);