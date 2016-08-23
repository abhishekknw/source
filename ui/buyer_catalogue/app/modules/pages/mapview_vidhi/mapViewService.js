 'use strict';


 angular.module('catalogueApp')
 .factory('mapViewService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

    var url_base = 'v0/ui/website/';

    var mapViewService = {};


    mapViewService.getSpaces = function(proposal_id){
        // done
        var url = url_base + proposal_id + "/getSpaces/";
        return machadaloHttp.get(url);
    };

    // mapViewService.getSpace = function(id){
        // 	var url = url_base + "getSpace/" + id +"/";
        // 	return machadaloHttp.get(url);
    // }

    mapViewService.getChangedCenterSpaces = function(proposal_id, data){
        // done
        var url = url_base + proposal_id + '/getSpaces/';
        return machadaloHttp.post(url,data);
    };


    mapViewService.resetCenter = function(proposal_id, center_id){
        // done
        var url = url_base + proposal_id + "/getSpaces/?center=" + center_id ;
        return machadaloHttp.get(url);
    }

    mapViewService.getFilterSocieties = function(get_data){
        var url = url_base + 'getFilteredSocieties/' + get_data;
        return machadaloHttp.get(url); 
    }

    mapViewService.createFinalProposal = function(proposal_id, centers_data){
        var url = url_base + proposal_id + '/createFinalProposal/';
        return machadaloHttp.post(url, centers_data);
    }

    return mapViewService;
}]);